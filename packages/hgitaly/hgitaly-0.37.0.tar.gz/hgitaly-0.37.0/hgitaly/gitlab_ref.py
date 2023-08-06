# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Handling of GitLab refs.

This module is primarily geared towards "special" refs, such as
`refs/merge_requests/1/head`, but should really adopt all general
utilities about refs, i.e, anything about a full ref path, such as
`refs/some/thing` and not yet refined to a given type, such as branches
or tags.
"""
from fnmatch import fnmatch

from hgext3rd.heptapod import ensure_gitlab_special_refs
from hgext3rd.heptapod import ensure_gitlab_keep_arounds
from hgext3rd.heptapod.special_ref import (
    GITLAB_TYPED_REFS_MISSING,
    parse_special_ref,
    special_refs,
)
from hgext3rd.heptapod.keep_around import iter_keep_arounds


def gitlab_special_ref_target(repo, ref_path):
    """Return the changeset for a special ref.

    :returns: a :class:`changectx` instance, for the unfiltered version of
       ``repo``. The changeset itself may be obsolete.
    """
    name = parse_special_ref(ref_path)
    if name is None:
        return None

    all_special_refs = special_refs(repo)
    if all_special_refs is GITLAB_TYPED_REFS_MISSING:
        # transitional while we still have an inner Git repo
        # would still be the best we can do near the end of HGitaly2 milestone
        all_special_refs = ensure_special_refs(repo)

    sha = all_special_refs.get(name)
    if sha is None:
        return None

    # TODO catch RepoLookupError (case of inconsistency)
    return repo.unfiltered()[sha]


def path_match(path_segments, pattern_segments):
    # special case for prefix_matching
    if pattern_segments[-1] == b'':
        # direct equality could have issues comparing lists to tuples
        return all(
            path_segment == pat_segment
            for path_segment, pat_segment in zip(path_segments,
                                                 pattern_segments[:-1]))

    return (len(pattern_segments) == len(path_segments)
            and all(
                fnmatch(path_segment, pat_segment)
                for path_segment, pat_segment in zip(path_segments,
                                                     pattern_segments)
                ))


def path_match_any(path, patterns):
    """Tell if path matches at least one of the given glob-like patterns.

    The matching is done as in `git-for-each-ref`, that is either as in
    `fnmatch(3)` (C stdlib function, matches segment by segment of the path)
    or as a direct prefix if pattern ends
    with a slash.

    Because Python's :func:`fnmatch` does not match per slash-separated
    segment, but on the whole string, considering the slash to be an ordinary
    character, we implement the segmentation, and hence need patterns to
    come pre-split at slashes.

    :param patterns: iterable of patterns, each pattern being an iterable
      of segment level patterns, e.g., ``[b'refs', b'heads', b'branch', b'*']``
    """
    path_segments = path.split(b'/')
    return any(path_match(path_segments, pat) for pat in patterns)


def iter_gitlab_special_refs_as_refs(repo, deref=True, patterns=None):
    """Iterate on special refs, yielding full ref paths and target hashes.

    :param patterns: as in :func:`path_match_any` (presplit)
    """
    all_special_refs = special_refs(repo)
    if all_special_refs is GITLAB_TYPED_REFS_MISSING:
        # transitional while we still have an inner Git repo
        # would still be the best we can do near the end of HGitaly2 milestone
        all_special_refs = ensure_special_refs(repo)

    for sref, sha in all_special_refs.items():
        ref_path = b'refs/' + sref
        if patterns and not path_match_any(ref_path, patterns):
            continue
        yield ref_path, (repo[sha] if deref else sha.decode('ascii'))


def ensure_special_refs(repo):
    return ensure_gitlab_special_refs(repo.ui, repo)


def has_keep_around(repo, sha):
    """Tell if there is a keep around for the given changeset hash.

    :param bytes sha: the changeset hash.
    """
    for ka in iter_keep_arounds(repo):
        if ka is GITLAB_TYPED_REFS_MISSING:
            ensure_gitlab_keep_arounds(repo.ui, repo)
            return has_keep_around(repo, sha)
        if ka == sha:
            return True
    return False


def keep_around_ref_path(sha):
    # TODO should move to py-heptapod
    return b'refs/keep-around/' + sha


def iter_keep_arounds_as_refs(repo, deref=True, patterns=None):
    for sha in iter_keep_arounds(repo):
        if sha is GITLAB_TYPED_REFS_MISSING:
            ensure_gitlab_keep_arounds(repo.ui, repo)
            yield from iter_keep_arounds_as_refs(repo, deref=deref)
            return
        ref_path = keep_around_ref_path(sha)
        if patterns and not path_match_any(ref_path, patterns):
            continue

        yield (ref_path, (repo[sha] if deref else sha.decode('ascii')))


def sort_key_ref_changeset_date_asc(ref_chgset):
    """Sorting key function meant for ref items.

    :param ref_chgset: a pair made of ref name and changeset (changectx)
    """
    return ref_chgset[1].date()[0]


def sort_key_ref_changeset_date_desc(ref_chgset):
    """Sorting key function meant for ref items.

    :param ref_chgset: a pair made of ref name and changeset (changectx)
    """
    return -ref_chgset[1].date()[0]
