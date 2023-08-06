# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import pytest
import time

from hgext3rd.heptapod.special_ref import (
    special_refs,
)
from hgitaly.stub.shared_pb2 import (
    PaginationParameter,
)
from hgitaly.stub.ref_pb2 import (
    FindBranchRequest,
    FindTagRequest,
    FindLocalBranchesRequest,
    ListRefsRequest,
    DeleteRefsRequest,
    RefExistsRequest,
)
from hgitaly.stub.ref_pb2_grpc import RefServiceStub

from . import skip_comparison_tests
from .comparison import (
    normalize_commit_message,
)
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip

parametrize = pytest.mark.parametrize


def test_compare_find_branch(gitaly_comparison):
    fixture = gitaly_comparison
    git_repo = fixture.git_repo

    fixture.hg_repo_wrapper.write_commit('foo', message="Some foo")
    gl_branch = b'branch/default'

    # mirror worked
    assert git_repo.branch_titles() == {gl_branch: b"Some foo"}

    def normalize_response(rpc_helper, resp, **kw):
        normalize_commit_message(resp.branch.target_commit)

    rpc_helper = fixture.rpc_helper(
        stub_cls=RefServiceStub,
        method_name='FindBranch',
        request_cls=FindBranchRequest,
        response_sha_attrs=['branch.target_commit.id'],
        normalizer=normalize_response,
    )

    rpc_helper.assert_compare(name=gl_branch)

    # invalid case
    rpc_helper.assert_compare_errors(name=gl_branch, repository=None,
                                     same_details=False)


@parametrize('hg_server', ('hgitaly', 'rhgitaly'))
def test_compare_ref_exists(gitaly_rhgitaly_comparison, hg_server):
    fixture = gitaly_rhgitaly_comparison
    wrapper = fixture.hg_repo_wrapper

    rpc_helper = fixture.rpc_helper(
        hg_server=hg_server,
        stub_cls=RefServiceStub,
        method_name='RefExists',
        request_cls=RefExistsRequest,
        )

    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    # empty repo, when state files don't exist yet
    assert_compare(ref=b'refs/heads/branch/default')
    assert_compare(ref=b'refs/keep-around/' + b'1234' * 10)

    ctx0 = wrapper.commit_file('foo')
    wrapper.command('tag', b'start-tag', rev=ctx0.hex())
    ctx1 = wrapper.commit_file('foo', topic='sampletop')
    fixture.invalidate()

    mr_ref_path, _ = fixture.write_special_ref(b'merge-requests/2/train',
                                               ctx1.hex())
    hg_ka_ref_path, git_ka_ref_path = fixture.create_keep_around(ctx1.hex())

    assert_compare(ref=b'refs/heads/branch/default')
    assert_compare(ref=b'refs/heads/topic/default/sampletop')
    assert_compare(ref=b'refs/heads/not-found')
    assert_compare(ref=b'refs/tags/start-tag')
    assert_compare(ref=b'refs/tags/unknown-tag')
    assert_compare(ref=b'refs/merge-requests/2/train')
    assert_compare(ref=b'refs/merge-requests/3/head')  # result is False
    assert_compare(ref=b'refs/')
    assert_compare(ref=b'refs/tags')
    assert_compare(ref=b'refs/tags/')
    # assert_compare() not being able to convert the keep-around ref path from
    # Mercurial to Git on the fly, we need to go lower level
    hg_resp = rpc_helper.rpc('hg', ref=hg_ka_ref_path)
    git_resp = rpc_helper.rpc('git', ref=git_ka_ref_path)
    assert hg_resp == git_resp

    assert_compare(ref=b'refs/keep-around/not-even-a-hash')

    assert_compare_errors(ref=b'refs')
    assert_compare_errors(ref=b'HEAD')
    assert_compare_errors(ref=b'notrefs/something')


def test_compare_find_local_branches(gitaly_comparison):
    fixture = gitaly_comparison
    wrapper = fixture.hg_repo_wrapper

    # make three branches with the 3 possible orderings differ
    now = time.time()
    commit_ages = {0: 30, 1: 40, 2: 20}
    for i in range(3):
        wrapper.commit_file('foo', branch='br%02d' % i, return_ctx=False,
                            utc_timestamp=now - commit_ages[i])
    # mirror worked
    assert set(fixture.git_repo.branch_titles().keys()) == {
        b'branch/br%02d' % i for i in range(3)}

    def normalize_response(rpc_helper, resp, **kw):
        for chunk in resp:
            for branch in chunk.local_branches:
                normalize_commit_message(branch.target_commit)

    rpc_helper = fixture.rpc_helper(
        stub_cls=RefServiceStub,
        method_name='FindLocalBranches',
        request_cls=FindLocalBranchesRequest,
        streaming=True,
        response_sha_attrs=['local_branches[].target_commit.id',
                            'local_branches[].target_commit.parent_ids[]',
                            ],
        normalizer=normalize_response,
    )

    def assert_compare(limit=0, page_token='', pagination=True, **kw):
        if pagination:
            pagination_params = PaginationParameter(limit=limit,
                                                    page_token=page_token)
        else:
            pagination_params = None

        rpc_helper.assert_compare(pagination_params=pagination_params, **kw)

    for limit in (0, 3, 8, -1):
        assert_compare(limit=limit)

    # case without any pagination parameters
    assert_compare(123, pagination=False)

    assert_compare(10, page_token='refs/heads/branch/br01')

    # sort options
    for sort_by in FindLocalBranchesRequest.SortBy.values():
        assert_compare(10, sort_by=sort_by)


def test_find_tag(gitaly_comparison):
    fixture = gitaly_comparison
    hg_wrapper = fixture.hg_repo_wrapper

    hg_wrapper.commit_file('foo')
    hg_wrapper.command('tag', b'v3.3', rev=b'.')
    hg_wrapper.command('gitlab-mirror')

    # mirror worked
    assert fixture.git_repo.tags() == {b'v3.3'}

    def normalize_response(rpc_helper, resp, **kw):
        normalize_commit_message(resp.tag.target_commit)
        # no tag ids in Mercurial until we can assign a tagging changeset
        # (requires a long-term core change)
        resp.tag.id = ''

    rpc_helper = fixture.rpc_helper(
        stub_cls=RefServiceStub,
        method_name='FindTag',
        response_sha_attrs=['tag.target_commit.id'],
        request_cls=FindTagRequest,
        normalizer=normalize_response,
    )
    rpc_helper.assert_compare(tag_name=b'v3.3')
    rpc_helper.assert_compare_errors(tag_name=b'nosuchtag')

    rpc_helper.feature_flags.append(('find-tag-structured-error', True))
    rpc_helper.assert_compare_errors(tag_name=b'nosuchtag')


def test_delete_refs(gitaly_comparison):
    fixture = gitaly_comparison
    git_repo = fixture.git_repo
    hg_wrapper = fixture.hg_repo_wrapper

    base_hg_ctx = hg_wrapper.commit_file('foo')
    hg_sha = base_hg_ctx.hex()
    mr_ref_name = b'merge-requests/2/train'
    mr_ref_path, git_sha = fixture.write_special_ref(mr_ref_name, hg_sha)

    rpc_helper = fixture.rpc_helper(stub_cls=RefServiceStub,
                                    method_name='DeleteRefs',
                                    request_cls=DeleteRefsRequest)

    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    assert_compare_errors(refs=[b'xy'], except_with_prefix=[b'refs/heads'])
    assert_compare(refs=[mr_ref_path])

    # unknown refs dont create errors
    fixture.write_special_ref(mr_ref_name, hg_sha)
    unknown = b'refs/environments/imaginary'
    assert_compare(refs=[unknown])

    # also mixing unknown with known is ok
    assert_compare(refs=[unknown, mr_ref_path])

    assert git_repo.all_refs() == {b'refs/heads/branch/default': git_sha}
    hg_wrapper.reload()
    assert special_refs(hg_wrapper.repo) == {}

    # using except_with_prefix
    env_ref_name = b'environments/2877'
    env_ref_path, _ = fixture.write_special_ref(env_ref_name, hg_sha)

    # on the Mercurial side, we'll consider the special ref only,
    # but on the Git side, the `refs/heads` prefix has to be ignored.
    # This is similar to what the current actual caller,
    # `Projects::AfterImportService`, does.
    for except_prefixes in (
            [b'refs/environments/', b'refs/heads/'],
            [b'refs/environments', b'refs/heads/'],
            [b'refs/envir', b'refs/heads/'],
            ):
        fixture.write_special_ref(mr_ref_name, hg_sha)
        fixture.write_special_ref(env_ref_name, hg_sha)

        assert_compare(except_with_prefix=except_prefixes)
        assert git_repo.all_refs() == {b'refs/heads/branch/default': git_sha,
                                       env_ref_path: git_sha}
        hg_wrapper.reload()
        assert special_refs(hg_wrapper.repo) == {env_ref_name: hg_sha}


def test_list_refs(gitaly_comparison):
    fixture = gitaly_comparison
    hg_wrapper = fixture.hg_repo_wrapper

    def normalize_refs(rpc_helper, resps, vcs=None):
        if vcs != 'hg':
            return

        prefix = b'refs/keep-around/'

        for resp in resps:
            all_pseudo_ref_idx = None
            for i, ref_msg in enumerate(resp.references):
                if ref_msg.name == b'ALL' and rpc_helper.norm_all_pseudo_ref:
                    all_pseudo_ref_idx = i
                if ref_msg.name.startswith(prefix):
                    ref_msg.name = prefix + rpc_helper.hg2git(
                        ref_msg.name[len(prefix):])
            if all_pseudo_ref_idx is not None:
                del resp.references[all_pseudo_ref_idx]

    rpc_helper = fixture.rpc_helper(
        stub_cls=RefServiceStub,
        method_name='ListRefs',
        request_cls=ListRefsRequest,
        request_defaults=dict(patterns=[b"refs/"], head=True),
        streaming=True,
        response_sha_attrs=['references[].target'],
        normalizer=normalize_refs,
    )
    rpc_helper.norm_all_pseudo_ref = True
    # empty repo, in particular no default GitLab branch (HEAD)
    rpc_helper.assert_compare()

    # make three changesets on which the 3 possible orderings differ
    # (in Mercurial committer and author dates are the same)
    now = time.time()
    commit_ages = {0: 30, 1: 40, 2: 20}
    hg_sha = hg_wrapper.commit_file('bar').hex()

    # branches
    for i in range(3):
        hg_wrapper.commit_file('foo', branch='br%02d' % i, return_ctx=False,
                               utc_timestamp=now - commit_ages[i])
    rpc_helper.assert_compare()
    for head in False, True:
        rpc_helper.assert_compare(patterns=[b'refs/heads/'], head=head)

    # with tags
    hg_wrapper.command('tag', b'v3.1', rev=b'br01')
    hg_wrapper.command('gitlab-mirror')
    fixture.invalidate()
    rpc_helper.assert_compare()
    for head in False, True:
        rpc_helper.assert_compare(patterns=[b'refs/heads/'], head=head)
        rpc_helper.assert_compare(patterns=[b'refs/tags/'], head=head)

    # now with special refs
    fixture.write_special_ref(b'pipeline/13', hg_sha)
    rpc_helper.assert_compare()
    for head in False, True:
        rpc_helper.assert_compare(patterns=[b'refs/heads/'], head=head)
        rpc_helper.assert_compare(patterns=[b'refs/tags/'], head=head)

    # with a keep around
    fixture.create_keep_around(hg_sha)
    rpc_helper.assert_compare()
    for head in False, True:
        rpc_helper.assert_compare(patterns=[b'refs/heads/'], head=head)
        rpc_helper.assert_compare(patterns=[b'refs/tags/'], head=head)

    # more general patterns
    rpc_helper.norm_all_pseudo_ref = False
    for head in False, True:
        # notice how HEAD is ignored by pattern matching
        rpc_helper.assert_compare(patterns=[b'refs/heads/branch/br*'],
                                  head=head)

        # 'branch/something' should not match `br*` and special case of
        # HEAD not being part of response if nothing matches
        rpc_helper.assert_compare(patterns=[b'refs/heads/br*'], head=head)

    # logical conjunction of several patterns
    rpc_helper.assert_compare(patterns=[b'refs/heads/branch/br*',
                                        b'refs/heads/branch/d*'],
                              head=head)

    # no error that we can think of would be specific of this gRPC method
