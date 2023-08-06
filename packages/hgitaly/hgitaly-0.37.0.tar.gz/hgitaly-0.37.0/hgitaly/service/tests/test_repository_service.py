# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import attr

from contextlib import contextmanager
from io import BytesIO
import grpc
import os
from pathlib import Path
import shutil
import tarfile

import pytest
from mercurial_testhelpers import (
    as_bytes,
)


from hgext3rd.heptapod.branch import read_gitlab_typed_refs
from hgext3rd.heptapod.keep_around import (
    create_keep_around,
    iter_keep_arounds,
)

from hgitaly.repository import (
    GITLAB_PROJECT_FULL_PATH_FILENAME,
)
from hgitaly.testing import TEST_DATA_DIR
from hgitaly.testing.bundle import list_bundle_contents

from hgitaly.stub.shared_pb2 import Repository
from hgitaly import stream

from hgitaly.stub.repository_pb2 import (
    BackupCustomHooksRequest,
    CreateBundleRequest,
    CreateRepositoryFromBundleRequest,
    CreateRepositoryRequest,
    CreateBundleFromRefListRequest,
    FetchBundleRequest,
    FindMergeBaseRequest,
    FullPathRequest,
    GetArchiveRequest,
    GetCustomHooksRequest,
    HasLocalBranchesRequest,
    RemoveAllRequest,
    RemoveRepositoryRequest,
    RepositoryExistsRequest,
    RestoreCustomHooksRequest,
    SearchFilesByNameRequest,
    SetFullPathRequest,
    SetCustomHooksRequest,
    WriteRefRequest,
)
from hgitaly.stub.repository_pb2_grpc import RepositoryServiceStub
from mercurial import (
    error,
    node as node_mod,
    phases,
)
from .fixture import ServiceFixture

parametrize = pytest.mark.parametrize


@attr.s
class RepositoryFixture(ServiceFixture):

    stub_cls = RepositoryServiceStub
    auto_cleanup = attr.ib(default=True)
    """cannot be overridden by class attribute"""

    def exists(self):
        return self.stub.RepositoryExists(
            RepositoryExistsRequest(repository=self.grpc_repo)).exists

    def has_local_branches(self):
        return self.stub.HasLocalBranches(
            HasLocalBranchesRequest(repository=self.grpc_repo)).value

    def write_ref(self, ref, target):
        self.stub.WriteRef(WriteRefRequest(
            repository=self.grpc_repo,
            ref=ref,
            revision=target,
        ))

    @contextmanager
    def get_archive_tarfile(self, commit_id, path=b''):
        with BytesIO() as fobj:
            for chunk_index, chunk_response in enumerate(
                    self.stub.GetArchive(GetArchiveRequest(
                        repository=self.grpc_repo,
                        format=GetArchiveRequest.Format.Value('TAR'),
                        commit_id=commit_id,
                        path=path,
                        prefix='archive-dir',
                    ))):
                fobj.write(chunk_response.data)

            fobj.seek(0)
            with tarfile.open(fileobj=fobj) as tarf:
                yield tarf, chunk_index + 1

    def find_merge_base(self, revisions):
        return self.stub.FindMergeBase(FindMergeBaseRequest(
            repository=self.grpc_repo,
            revisions=revisions,
        )).base.encode('ascii')  # needed for comparison with `changectx.hex()`

    def create_repository(self, rel_path, storage_name='default'):
        self.grpc_repo = Repository(relative_path=rel_path,
                                    storage_name=storage_name)
        self.stub.CreateRepository(CreateRepositoryRequest(
            repository=self.grpc_repo))
        self.repo_wrapper = self.make_repo_wrapper(rel_path,
                                                   storage_name=storage_name)

    def search_files_by_name(self, ref=b'branch/default', **kwargs):
        return [path
                for resp in self.stub.SearchFilesByName(
                        SearchFilesByNameRequest(
                            repository=self.grpc_repo,
                            ref=ref,
                            **kwargs,
                        ))
                for path in resp.files]

    def restore_custom_hooks(self, tarball_path,
                             grpc_repo=None,
                             nb_chunks=2,
                             **kw):
        if grpc_repo is None:
            grpc_repo = self.grpc_repo

        return self.stub.RestoreCustomHooks(
            RestoreCustomHooksRequest(repository=grpc_repo, data=chunk)
            for chunk in stream.slice_binary_file(tarball_path, nb_chunks)
        )

    def set_custom_hooks(self, tarball_path,
                         grpc_repo=None,
                         nb_chunks=2,
                         **kw):
        if grpc_repo is None:
            grpc_repo = self.grpc_repo

        return self.stub.SetCustomHooks(
            SetCustomHooksRequest(repository=grpc_repo, data=chunk)
            for chunk in stream.slice_binary_file(tarball_path, nb_chunks)
        )

    def backup_custom_hooks(self, save_path):
        with open(save_path, 'wb') as fobj:
            for chunk in self.stub.BackupCustomHooks(BackupCustomHooksRequest(
                    repository=self.grpc_repo)):
                fobj.write(chunk.data)

    def get_custom_hooks(self, save_path):
        with open(save_path, 'wb') as fobj:
            for chunk in self.stub.GetCustomHooks(GetCustomHooksRequest(
                    repository=self.grpc_repo)):
                fobj.write(chunk.data)

    def remove_repository(self, grpc_repo=None):
        if grpc_repo is None:
            grpc_repo = self.grpc_repo

        return self.stub.RemoveRepository(RemoveRepositoryRequest(
            repository=grpc_repo))

    def set_full_path(self, path, grpc_repo=None):
        if grpc_repo is None:
            grpc_repo = self.grpc_repo

        return self.stub.SetFullPath(SetFullPathRequest(repository=grpc_repo,
                                                        path=path))

    def full_path(self, grpc_repo=None):
        if grpc_repo is None:
            grpc_repo = self.grpc_repo

        return self.stub.FullPath(FullPathRequest(repository=grpc_repo)).path

    def create_bundle(self, save_path):
        with open(save_path, 'wb') as fobj:
            for chunk in self.stub.CreateBundle(CreateBundleRequest(
                    repository=self.grpc_repo)):
                fobj.write(chunk.data)

    def fetch_bundle(self, bundle_path, grpc_repo, nb_chunks=2, **kw):
        return self.stub.FetchBundle(
            FetchBundleRequest(repository=grpc_repo, data=chunk)
            for chunk in stream.slice_binary_file(bundle_path, nb_chunks)
        )

    def create_repository_from_bundle(self, bundle_path, grpc_repo,
                                      nb_chunks=2):
        """Call CreateRepositoryFromBundle.

        Makes several chunks by default to test that aggregation works.
        """
        return self.stub.CreateRepositoryFromBundle(
            CreateRepositoryFromBundleRequest(repository=grpc_repo, data=chunk)
            for chunk in stream.slice_binary_file(bundle_path, nb_chunks)
        )

    def create_bundle_from_ref_list(self, bundle_path, ref_patterns,
                                    nb_chunks=2,
                                    without_repository=False):
        """Call CreateBundleFromRefList.

        Makes several chunks by default to test that aggregation works.
        """
        def get_request_iter(patterns):
            first_req = True
            for chunk in stream.split_batches(patterns, nb_chunks):
                req_args = dict(patterns=chunk)
                if first_req and not without_repository:
                    first_req = False
                    req_args['repository'] = self.grpc_repo
                yield CreateBundleFromRefListRequest(**req_args)

        with open(bundle_path, 'wb') as fobj:
            for chunk in self.stub.CreateBundleFromRefList(
                    get_request_iter(ref_patterns)):
                fobj.write(chunk.data)

    def remove_all(self, storage_name):
        return self.stub.RemoveAll(RemoveAllRequest(storage_name=storage_name))

    def assert_compare_repos(self, target_repo_path):
        """Compare the fixture repo with another one.
        """
        wrapper = self.repo_wrapper
        orig = wrapper.repo.unfiltered()
        target = self.make_repo_wrapper(target_repo_path).repo.unfiltered()
        for rev_str in ('draft()', 'public()', 'obsolete()'):
            assert (
                [r for r in orig.revs(rev_str)]
                ==
                [r for r in target.revs(rev_str)])

        # assert empty incoming/outgoing changes between orig and target repo
        no_changes = 1  # code returned when no changes to transmit
        # XXX: extra args bundle, force should not be required once
        # upstream Mercurial use opts.get() instead of [] access
        incoming = wrapper.command('incoming', target.root,
                                   bundle=None, force=None)
        outgoing = wrapper.command('outgoing', target.root,
                                   bundle=None, force=None)
        assert incoming == no_changes
        assert outgoing == no_changes

        # assert branches
        orig_br = [br[0] for br in orig.branchmap().iterbranches()]
        target_br = [br[0] for br in target.branchmap().iterbranches()]
        assert orig_br == target_br

        # assert tags
        assert orig.tags() == target.tags()


@pytest.fixture
def fixture_with_repo(grpc_channel, server_repos_root):
    with RepositoryFixture(grpc_channel, server_repos_root) as fixture:
        yield fixture


@pytest.fixture
def fixture_without_repo(grpc_channel, server_repos_root):
    with RepositoryFixture(grpc_channel, server_repos_root,
                           with_repo=False) as fixture:
        yield fixture


def test_repository_exists(fixture_with_repo):
    fixture = fixture_with_repo
    assert fixture.exists()

    # directory exists but is not a Mercurial repo
    shutil.rmtree(fixture.repo_wrapper.path / '.hg')
    assert not fixture.exists()

    # directory does not exist
    fixture.grpc_repo.relative_path = 'does/not/exist'
    assert not fixture.exists()

    # storage does not exist
    fixture.grpc_repo.storage_name = 'dream'
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.exists()
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    # missing repo argument
    fixture.grpc_repo = None
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.exists()
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_has_local_branches(fixture_with_repo):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper

    assert not fixture.has_local_branches()
    wrapper.write_commit('foo')
    assert fixture.has_local_branches()

    wrapper.command('commit', message=b"closing the only head!",
                    close_branch=True)

    assert not fixture.has_local_branches()

    # missing repo argument
    fixture.grpc_repo = None
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.has_local_branches()
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_write_ref(fixture_with_repo):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper
    repo = wrapper.repo

    for ref, revision in ((b'refs/heads/something', b'dead01234cafe'),
                          (b'HEAD', b'topic/default/wont-last'),
                          (b'refs/keep-around/not-a-sha', b'not-a-sha'),
                          (b'refs/keep-around/feca01eade', b'cafe01dead'),
                          ):
        with pytest.raises(grpc.RpcError) as exc_info:
            fixture.write_ref(ref, revision)
        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    sha = wrapper.commit_file('foo').hex()

    to_write = {b'refs/merge-requests/12/head': sha,
                b'refs/pipelines/98192': b'refs/heads/branch/default',
                b'refs/environments/13/deployments/9826': b'branch/default',
                }
    for ref_path, target in to_write.items():
        fixture.write_ref(ref_path, target)
    assert read_gitlab_typed_refs(repo, 'special-refs') == {
        ref_path[5:]: sha for ref_path in to_write.keys()
    }

    # Keep-arounds. let's have a pre-existing one for good measure
    existing_ka = b'c8c3ae298f5549a0eb0c28225dcc4f6937b959a8'
    create_keep_around(repo, existing_ka)
    fixture.write_ref(b'refs/keep-around/' + sha, sha)
    assert set(iter_keep_arounds(repo)) == {sha, existing_ka}


def test_write_special_refs_exceptions(fixture_with_repo):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper
    wrapper.commit_file('foo')

    (wrapper.path / '.hg' / 'store' / 'gitlab.special-refs').write_text(
        'invalid')
    fixture.write_ref(b'refs/merge-requests/12/head', b'76ac23fe' * 5)


def test_get_archive(fixture_with_repo, tmpdir):
    # repo_stub = RepositoryServiceStub(grpc_channel)
    # wrapper, grpc_repo = make_empty_repo(server_repos_root)
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper

    ctx = wrapper.write_commit('foo', content="Foo")
    (wrapper.path / 'sub').mkdir()
    ctx2 = wrapper.write_commit('sub/bar', content="Bar")

    node_str = ctx.hex().decode()
    with fixture.get_archive_tarfile(node_str) as (tarf, _nb):
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo'}

        extract_dir = tmpdir.join('extract')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node_str in metadata_lines
        assert extract_dir.join('archive-dir', 'foo').read() == "Foo"

    node2_str = ctx2.hex().decode()
    with fixture.get_archive_tarfile(node2_str) as (tarf, _nb):
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo',
                                        'archive-dir/sub/bar'}

        extract_dir = tmpdir.join('extract-2')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node2_str in metadata_lines
        assert extract_dir.join('archive-dir', 'sub', 'bar').read() == "Bar"

    with fixture.get_archive_tarfile(node2_str, path=b'sub') as (tarf, _nb):
        assert tarf.getnames() == ['archive-dir/sub/bar']

        extract_dir = tmpdir.join('extract-sub')
        tarf.extractall(path=extract_dir)
        assert extract_dir.join('archive-dir', 'sub', 'bar').read() == "Bar"

    with pytest.raises(grpc.RpcError) as exc_info:
        # entering the context is needed to actually perform the RPC call
        fixture.get_archive_tarfile(node2_str, path=b'/etc/passwd').__enter__()
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_get_archive_multiple_chunks(fixture_with_repo, tmpdir):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper

    # we can't just override the environment variable: it's read at module
    # import time.
    large_content = "Foo" * 200000
    ctx = wrapper.write_commit('foo', content=large_content)
    node_str = ctx.hex().decode()
    with fixture.get_archive_tarfile(node_str) as (tarf, count):
        assert count > 1
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo'}

        extract_dir = tmpdir.join('extract')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node_str in metadata_lines
        assert extract_dir.join('archive-dir', 'foo').read() == large_content

    del large_content


def test_find_merge_base(fixture_with_repo, tmpdir):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper
    # repo structure:
    #
    #   o 2 add animal (branch/stable)
    #   |
    #   | 1 add bar
    #   |/
    #   |
    #   o 0 add foo    o 3 tut
    #
    ctx0 = wrapper.write_commit('foo')
    sha0 = ctx0.hex()
    sha1 = wrapper.write_commit('bar').hex()
    sha2 = wrapper.write_commit('animal', branch='stable', parent=ctx0).hex()
    # commting new root, to test no gca case
    sha3 = wrapper.commit_file('tut', branch='other',
                               parent=node_mod.nullid).hex()

    # Actual test
    assert fixture.find_merge_base([sha1, sha2]) == sha0
    assert fixture.find_merge_base([b'branch/stable', sha1]) == sha0

    # when no merge base (gca) found
    assert fixture.find_merge_base([sha0, sha3]) == b''

    # test with invalid_argument, as it requires minimum 2 revisions
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.find_merge_base([sha0])
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert (
        exc_info.value.details()
        ==
        'at least 2 revisions are required'
    )

    sha_not_exists = b'deadnode' * 5
    assert fixture.find_merge_base([sha0, sha_not_exists]) == b''

    # cases with obsolescence
    wrapper.update(sha2)
    wrapper.amend_file('animal', message='amended animal').hex()

    assert fixture.find_merge_base([sha1, sha2]) == sha0

    wrapper.update(sha0)
    wrapper.amend_file('foo', message='amended foo')
    assert fixture.find_merge_base([sha1, sha2]) == sha0

    # cases with more than 2 changesets
    # (in a previous version, only the 2 first arguments would have been
    # considered, giving wrong results but no error)
    assert fixture.find_merge_base([sha1, sha1, sha2]) == sha0
    assert fixture.find_merge_base([sha1, sha2, sha3]) == b''


def test_create_repository(fixture_without_repo):
    fixture = fixture_without_repo
    rel_path = 'sample_repo'

    # try to instantiate wrapper before repo creation
    with pytest.raises(error.RepoError) as exc_info:
        fixture.make_repo_wrapper(rel_path)
    assert b''.join(exc_info.value.args).endswith(b'sample_repo not found')

    fixture.create_repository(rel_path)
    # instantiating wrapper to check successful repo creation
    assert fixture.repo_wrapper.repo.path.endswith(b'sample_repo/.hg')

    # As of Gitaly 14.6, attempt to create existing repo is an error.
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.create_repository(rel_path)
    assert exc_info.value.code() == grpc.StatusCode.ALREADY_EXISTS
    assert 'exists already' in exc_info.value.details()

    # when storage doesn't exist
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.create_repository(rel_path, storage_name='cargoship')
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert 'no such storage' in exc_info.value.details()

    # test with a broken symlink (which points to itself)
    # This used to be a way to test failure in `hg init`, now should be
    # refused as already existing path (see Gitaly Comparison tests)
    brepo_name = "myrepo_a_broken_symlink"
    path = fixture.repo_path(brepo_name)
    path.symlink_to(path)
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.create_repository(brepo_name)
    assert exc_info.value.code() == grpc.StatusCode.ALREADY_EXISTS
    assert 'exists already' in exc_info.value.details()

    # using a broken symlink for the whole storage directory
    # to pass the check for existing repo and still fail in `hg init`
    rel_path = 'creation_error'
    storage_path = fixture.storage_path()
    try:
        shutil.rmtree(storage_path)
        storage_path.symlink_to(storage_path)
        with pytest.raises(grpc.RpcError) as exc_info:
            fixture.create_repository(rel_path)
        assert exc_info.value.code() == grpc.StatusCode.INTERNAL
    finally:
        storage_path.unlink()
        storage_path.mkdir(exist_ok=True)


def test_search_files_by_name(fixture_with_repo):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper

    ctx0 = wrapper.write_commit('afoo', message="Some foo")
    sub = (wrapper.path / 'sub')
    sub.mkdir()
    (sub / 'bar').write_text('bar content')
    (sub / 'ba2').write_text('ba2 content')
    # TODO OS indep for paths (actually TODO make wrapper.commit easier to
    # use, e.g., check how to make it accept patterns)
    wrapper.commit(rel_paths=['sub/bar', 'sub/ba2'],
                   message="zebar", add_remove=True)

    wrapper.write_commit('animals', message="A branch without subdir",
                         branch='other', parent=ctx0)

    search = fixture.search_files_by_name
    assert search(filter='/bar', query='.') == [b'sub/bar']
    assert search(filter='^sub/', query='.') == [b'sub/ba2', b'sub/bar']
    # matching in subdirectory only
    assert search(filter='a', query='sub') == [b'sub/ba2', b'sub/bar']
    assert search(filter='b?r$', query='sub') == [b'sub/bar']

    # without filter
    assert search(query='.') == [b'afoo', b'sub/ba2', b'sub/bar']
    assert search(query='sub') == [b'sub/ba2', b'sub/bar']

    # offset and limit
    assert search(query='.', limit=2) == [b'afoo', b'sub/ba2']
    assert search(query='.', limit=1, offset=1) == [b'sub/ba2']

    # from a different ref
    assert search(filter='bar', query='.', ref=b'branch/other') == []
    assert search(filter='.*', query='.', ref=b'branch/other') == [b'afoo',
                                                                   b'animals']

    # query is mandatory
    with pytest.raises(grpc.RpcError) as exc_info:
        search(filter='/ba')
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    # problems with regexp
    with pytest.raises(grpc.RpcError) as exc_info:
        search(filter='\\', query='.')
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    with pytest.raises(grpc.RpcError) as exc_info:
        search(filter='a' * 1001, query='.')
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    # unknown ref gives back an empty list of files, not an error
    assert search(ref=b'unknown', query='.') == []


@parametrize('rpc_name', ['restore', 'set'])
def test_set_custom_hooks(fixture_with_repo, tmpdir, rpc_name):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper

    if rpc_name == 'restore':
        meth = fixture.restore_custom_hooks
    else:
        meth = fixture.set_custom_hooks

    # this is a valid tar file with the minimal `hgrc` used in these tests
    # the underlying restoration function from py-heptapod is itself tested,
    # and Heptapod backup tests will further exercise this.
    # We only need a minimal set of assertions here.
    tarball_path = TEST_DATA_DIR / 'backup_additional_no_git.tar'
    hgrc_path = wrapper.path / '.hg/hgrc'

    os.unlink(hgrc_path)
    meth(tarball_path)
    assert hgrc_path.read_text()

    # TODO test unknown storage and repo

    # invalid tarball (seems to be what Gitaly returns, to be confirmed
    # by a comparison test)
    invalid_tarball_path = tmpdir / 'invalid.tgz'
    invalid_tarball_path.write("something else")
    with pytest.raises(grpc.RpcError) as exc_info:
        meth(invalid_tarball_path)
    assert exc_info.value.code() == grpc.StatusCode.INTERNAL


@parametrize('rpc_name', ['backup', 'get'])
def test_backup_custom_hooks(fixture_with_repo, tmpdir, rpc_name):
    fixture = fixture_with_repo
    if rpc_name == 'backup':
        meth = fixture.backup_custom_hooks
    else:
        meth = fixture.get_custom_hooks

    tarball_path = tmpdir / 'hg_aditional.tgz'
    meth(tarball_path)
    assert tarball_path.exists()


def test_remove_repository(fixture_with_repo):
    fixture = fixture_with_repo
    wrapper, grpc_repo = fixture.repo_wrapper, fixture.grpc_repo

    fixture.remove_repository()
    assert not wrapper.path.exists()

    # no other leftovers alongside the removed repo
    assert os.listdir(fixture.storage_path()) == ['+hgitaly']

    # no leftover in the temporary directory either
    tmp_dir = wrapper.path.parent / '+hgitaly/tmp'
    assert not os.listdir(tmp_dir)

    # unknown storage and repo
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.remove_repository(grpc_repo=Repository(storage_name='unknown'))
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.remove_repository(
            grpc_repo=Repository(storage_name=grpc_repo.storage_name,
                                 relative_path='no/such/path'))
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

    # missing repo argument
    fixture.grpc_repo = None
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.remove_repository(grpc_repo=None)
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_set_full_path(fixture_with_repo):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper
    grpc_repo = fixture.grpc_repo

    def assert_full_path(expected):
        assert (wrapper.path / '.hg'
                / GITLAB_PROJECT_FULL_PATH_FILENAME.decode('ascii')
                ).read_text(encoding='utf-8') == expected
        assert fixture.full_path() == expected

    def call_then_assert(full_path):
        fixture.set_full_path(full_path)
        assert_full_path(full_path)

    def call_then_assert_error(full_path, error_code, grpc_repo=grpc_repo):
        with pytest.raises(grpc.RpcError) as exc_info:
            fixture.set_full_path(full_path, grpc_repo=grpc_repo)
        assert exc_info.value.code() == error_code

    call_then_assert('group/proj')
    call_then_assert('accent-lovers/projé')
    call_then_assert('group/subgroup/proj')

    call_then_assert_error('', grpc.StatusCode.INVALID_ARGUMENT)
    call_then_assert_error('some/path', grpc.StatusCode.NOT_FOUND,
                           grpc_repo=Repository(
                               storage_name=grpc_repo.storage_name,
                               relative_path='no/such/repo'))
    call_then_assert_error('some/path', grpc.StatusCode.INVALID_ARGUMENT,
                           grpc_repo=Repository(
                               relative_path=grpc_repo.relative_path,
                               storage_name='unknown'))


def test_full_path_errors(fixture_with_repo):
    fixture = fixture_with_repo
    grpc_repo = fixture.grpc_repo

    def call_then_assert_error(error_code, grpc_repo=None):
        with pytest.raises(grpc.RpcError) as exc_info:
            fixture.full_path(grpc_repo=grpc_repo)
        assert exc_info.value.code() == error_code

    # existing repo, but full path not set
    call_then_assert_error(grpc.StatusCode.INTERNAL)

    call_then_assert_error(grpc.StatusCode.NOT_FOUND,
                           grpc_repo=Repository(
                               storage_name=grpc_repo.storage_name,
                               relative_path='no/such/repo'))
    call_then_assert_error(grpc.StatusCode.INVALID_ARGUMENT,
                           grpc_repo=Repository(
                               relative_path=grpc_repo.relative_path,
                               storage_name='unknown'))


def test_fetch_bundle(fixture_with_repo, tmpdir):
    fixture = fixture_with_repo
    wrapper = fixture.repo_wrapper

    target_repo_path, target_repo_msg = fixture.additional_repo('target_repo')

    # first call will create the repo
    sha1 = wrapper.commit_file('foo').hex()
    bundle_path = tmpdir / '1.bundle'
    wrapper.command('bundle', as_bytes(bundle_path), all=True)
    fixture.fetch_bundle(bundle_path, target_repo_msg)
    fixture.assert_compare_repos(target_repo_path)

    # subsequent call adds a changeset
    wrapper.commit_file('inc')
    # this seems to be either a minor bug in Mercurial 6.4 or in
    # mercurial-testhelpers: the `tip` pseudo tag is not immediately updated
    # leading to the `assert_compare_repos` failing.
    wrapper.reload()
    bundle2_path = tmpdir / '2.bundle'
    wrapper.command('bundle', as_bytes(bundle2_path), rev=[b'.'], base=[sha1])
    fixture.fetch_bundle(bundle2_path, target_repo_msg, nb_chunks=1)
    fixture.assert_compare_repos(target_repo_path)


def test_create_bundle_and_create_repository_from_bundle(fixture_with_repo,
                                                         tmpdir):
    fixture = fixture_with_repo
    grpc_repo = fixture.grpc_repo
    wrapper = fixture.repo_wrapper
    # repo structure:
    #
    #   @ 3 zoo (phase: draft) (amended)
    #   |
    #   | o 1 bar (phase: public) (tag: v1.2.3)
    #   |/
    #   o 0 foo (phase: public)
    #
    ctx0 = wrapper.commit_file('foo')
    sha0 = ctx0.hex()
    sha1 = wrapper.commit_file('bar').hex()
    wrapper.commit_file('zoo', parent=ctx0)
    wrapper.amend_file('zoo')
    wrapper.set_phase('public', [sha0, sha1])
    wrapper.update(sha1)
    wrapper.command('tag', b'v1.2.3', rev=sha1)

    bundle_path = tmpdir / 'my.bundle'
    target_repo_path, target_repo_msg = fixture.additional_repo('target_repo')

    # Bundling and creating new repo from bundle
    fixture.create_bundle(bundle_path)
    fixture.create_repository_from_bundle(bundle_path, target_repo_msg)

    # compare the created repository content with original one
    fixture.assert_compare_repos(target_repo_path)

    # error case of repository creation when target repo already exists
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.create_repository_from_bundle(bundle_path,
                                              target_repo_msg)
    assert exc_info.value.code() == grpc.StatusCode.ALREADY_EXISTS
    details = exc_info.value.details()
    assert 'exists already' in details

    # when storage name doesn't exists
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.create_repository_from_bundle(
            bundle_path,
            Repository(relative_path='new_target_repo',
                       storage_name='hippoship')
        )
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert 'no such storage' in exc_info.value.details()

    # test errors while creating repo itself
    # Because the main code refuses existing paths, we make a parent dir that
    # is a broken symlink (which points to itself). This way the repo path
    # does not exist *and* its creation fails.
    br_dir = Path("my_broken_symlink")
    br_path = fixture.repo_path(br_dir)
    br_path.symlink_to(br_path)
    trepo_msg = Repository(relative_path=str(br_dir / 'repo'),
                           storage_name=grpc_repo.storage_name)
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.create_repository_from_bundle(bundle_path, trepo_msg)
    assert exc_info.value.code() == grpc.StatusCode.INTERNAL
    assert 'Too many levels of symbolic links' in exc_info.value.details()

    # in case of error after repo creation, the repo must be removed
    trepo_msg = Repository(relative_path='bundle-fail',
                           storage_name=grpc_repo.storage_name)
    broken_bundle_path = tmpdir / 'broken-bundle'
    broken_bundle_path.write("Obviously garbage")
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.create_repository_from_bundle(broken_bundle_path, trepo_msg)
    assert exc_info.value.code() == grpc.StatusCode.INTERNAL
    assert "bundle" in exc_info.value.details()
    assert not fixture.repo_path('bundle-fail').exists()


def test_create_bundle_from_ref_list(fixture_with_repo, tmpdir):
    fixture = fixture_with_repo
    wrapper, grpc_repo = fixture.repo_wrapper, fixture.grpc_repo

    # repo structure:
    #
    #   @ 4 zoo (branch:toys) (phase: public) (amended)
    #   |
    #   | o 2 added tag (branch: animal) (phase: draft)
    #   | |
    #   | o 1 bar (tag: v1.2.3)
    #   |/
    #   o 0 foo (branch: default)
    #
    ctx0 = wrapper.commit_file('foo')
    sha0 = ctx0.hex()
    sha1 = wrapper.commit_file('bar', branch='animal').hex()
    wrapper.command('tag', b'v1.2.3')
    obs_sha = wrapper.commit_file('zoo', parent=ctx0, branch='toys').hex()
    sha4 = wrapper.amend_file('zoo').hex()
    wrapper.set_phase('public', [sha0, sha4])

    def target_repo_msg(bundle_name):
        return Repository(relative_path='%s_repo' % (bundle_name),
                          storage_name=grpc_repo.storage_name)

    def target_repo(bundle_name):
        return fixture.make_repo_wrapper(
            '%s_repo' % bundle_name
        ).repo.unfiltered()

    def assert_compare_created_repository_from_bundle(
            bundle_name, exp_branches, exp_tags, exp_cids):
        repo = target_repo(bundle_name)

        # assert branches
        branch_prefix = b'refs/heads/branch/'
        branches = set(
            [branch_prefix + br[0] for br in repo.branchmap().iterbranches()])
        assert branches == set(exp_branches)

        # assert tags
        tag_prefix = b'refs/tags/'
        hg_tags = set(map(lambda t: tag_prefix + t, repo.tags().keys()))
        hg_tags.remove(b'refs/tags/tip')
        assert hg_tags == set(exp_tags)

        # assert included revs
        allrevs = repo.revs('all()')
        revs = set(map(lambda x: repo[x].hex(), allrevs))
        assert revs == set(exp_cids)

    repo = wrapper.repo.unfiltered()
    all_cids = [repo[0].hex(), repo[1].hex(), repo[2].hex(), repo[4].hex()]
    all_cids_unfiltered = all_cids + [obs_sha]

    # test with all refs
    allrefs_bundle = 'all_refs_bundle'
    allrefs_bundle_path = tmpdir / allrefs_bundle
    branch_list = [b'refs/heads/branch/animal', b'refs/heads/branch/toys',
                   b'refs/heads/branch/default']
    tag_list = [b'refs/tags/v1.2.3']

    fixture.create_bundle_from_ref_list(allrefs_bundle_path,
                                        branch_list + tag_list)
    fixture.create_repository_from_bundle(allrefs_bundle_path,
                                          target_repo_msg(allrefs_bundle))

    # test successful repo creation from bundle
    assert_compare_created_repository_from_bundle(
        allrefs_bundle,
        exp_branches=branch_list,
        exp_tags=tag_list,
        exp_cids=all_cids,
    )

    # test with the `ALL` pseudo ref
    full_bundle = 'full_bundle'
    full_bundle_path = tmpdir / full_bundle
    fixture.create_bundle_from_ref_list(full_bundle_path,
                                        [b'ALL'])
    fixture.create_repository_from_bundle(full_bundle_path,
                                          target_repo_msg(full_bundle))
    assert_compare_created_repository_from_bundle(
        full_bundle,
        exp_branches=branch_list,
        exp_tags=tag_list,
        exp_cids=all_cids_unfiltered,
    )

    # test with some full ref paths
    someref_bundle = 'some_refs_bundle'
    someref_path = tmpdir / someref_bundle
    ref_list = [b'refs/heads/branch/default', b'refs/heads/branch/toys']

    fixture.create_bundle_from_ref_list(someref_path, ref_list)
    fixture.create_repository_from_bundle(someref_path,
                                          target_repo_msg(someref_bundle))

    # test successful repo creation from bundle
    assert_compare_created_repository_from_bundle(
        someref_bundle,
        exp_branches=ref_list,
        exp_tags=[],
        exp_cids=[sha0, sha4],
    )

    # test error case: when repository is absent in request obj
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        fixture.create_bundle_from_ref_list(
            tmpdir / 'temp_bname', [b'refs/heads/branch/default'],
            without_repository=True)
    assert exc_info_hg.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert exc_info_hg.value.details() == 'empty Repository'

    # test incrementality with negative revspecs

    # first bundle won't have the obsolete changeset, since it is not
    # an ancestor of `refs/heads/branch/toys`.
    inc_bundle_1, inc_bundle2 = 'bundle_inc.1', 'bundle_inc.2'
    inc_path_1, inc_path_2 = tmpdir / inc_bundle_1, tmpdir / inc_bundle2
    fixture.create_bundle_from_ref_list(inc_path_1, [b'branch/toys', sha1])
    fixture.create_bundle_from_ref_list(inc_path_2,
                                        [b'branch/animal', b'^' + sha1])

    # loading the two bundles is equivalent to loading the full backup
    # without the obsolete changeset
    target_grpc_repo = target_repo_msg('incremental')
    fixture.create_repository_from_bundle(inc_path_1, target_grpc_repo)
    fixture.fetch_bundle(inc_path_2, target_grpc_repo)
    assert_compare_created_repository_from_bundle(
        'incremental',
        exp_branches=branch_list,
        exp_tags=tag_list,
        exp_cids=all_cids,
    )

    # Same by including obsolete changesets, thanks to the ALL pseudo-ref
    # Also adding a phase change, so that we can test if it gets bundled.
    wrapper.set_phase('public', [sha1])
    wrapper.update('toys')
    obs_sha2 = wrapper.commit_file('zoo', message='obs2').hex()
    sha5 = wrapper.amend_file('zoo').hex()
    inc_bundle_3 = 'bundle_inc.3'
    inc_path_3 = tmpdir / inc_bundle_3
    exclude_previous = [b'^' + sha for sha in all_cids]
    fixture.create_bundle_from_ref_list(inc_path_3,
                                        [b'ALL'] + exclude_previous)
    inc_cids = set(list_bundle_contents(inc_path_3)['nodes'])

    # caveat: obs_sha is present in incremental bundle, because it is
    # not an ancestor of previously backed up changesets.
    assert inc_cids == {obs_sha2, sha5, obs_sha}

    fixture.fetch_bundle(inc_path_3, target_grpc_repo)
    all_cids_unfiltered.extend((obs_sha2, sha5))
    assert_compare_created_repository_from_bundle(
        'incremental',
        exp_branches=branch_list,
        exp_tags=tag_list,
        exp_cids=all_cids_unfiltered,
    )
    unbundled_repo = target_repo('incremental')

    # confirmation that phase change of previously backed up changeset
    # is not in the incremental bundle
    # TODO do better and assert phases.public
    assert unbundled_repo[sha1].phase() == phases.draft


def test_remove_all(fixture_with_repo):
    fixture = fixture_with_repo
    storage_path = fixture.storage_path('default')
    (storage_path / 'foo').write_bytes(b'something')
    (storage_path / 'bar').symlink_to('foo')
    (storage_path / 'broken').symlink_to('missing')
    fixture.remove_all(storage_name='default')

    assert list(storage_path.iterdir()) == []

    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.remove_all(storage_name='unknown')
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    storage_path.rmdir()  # create error condition by removing the root dir
    with pytest.raises(grpc.RpcError) as exc_info:
        fixture.remove_all(storage_name='default')
    exc = exc_info.value
    assert exc.code() == grpc.StatusCode.INTERNAL
    assert "No such file or directory: '%s'" % storage_path in exc.details()
