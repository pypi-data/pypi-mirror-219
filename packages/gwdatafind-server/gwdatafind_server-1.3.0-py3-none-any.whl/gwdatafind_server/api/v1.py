# -*- coding: utf-8 -*-
# Copyright (2019) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""GWDataFind API v1

This API provides the same endpoints as the 'original'
LDR DataFind server API.
"""

import json
import operator
import re
from collections import defaultdict
from functools import reduce, wraps
from math import inf as INF
from urllib.parse import urlparse, unquote

from flask import (Blueprint, current_app, request)

from ligo.segments import (segmentlist, segment)

from .. import authentication
from .utils import (
    as_json,
    error_as_json,
    _file_url,
    _gsiftp_url,
    _osdf_url,
)

blueprint = Blueprint(
    "api/v1",
    __name__,
    url_prefix="/services/data/v1",
)


# -- errors

class BadObservatory(KeyError):
    pass


class BadFiletype(KeyError):
    pass


def error_filetype(filetype, code=404):
    """Return an error response for a missing filetype

    This is 404 to match the original LDR datafind server implementation
    """
    return (
        error_as_json(f"Filetype '{filetype}' not found", code),
        code,
    )


def error_observatory(observatory, code=400):
    """Return an error response for a missing observatory

    This is 400 to match the original LDR datafind server implementation, see
    https://git.ligo.org/computing/ligo-data-replicator/-/blob/9ff125b/datafind-server/DataFindServer/LDRDataFindServer.py#L684-L688
    """
    return (
        error_as_json(f"Observatory ID '{observatory}' not recognised", code),
        code,
    )


def handle_errors_as_json(func):
    """Handle known errors and return error responses
    """
    @as_json
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadFiletype as exc:
            return error_filetype(exc.args[0])
        except BadObservatory as exc:
            return error_observatory(exc.args[0])
    return wrapped


# -- cache interactions

def get_filetype_cache(ext):
    """Get the current cache for the given filetype (extension)
    """
    cache = current_app.get_cache_data()
    try:
        return cache[ext]
    except KeyError:
        raise BadFiletype(ext)


def get_observatory_cache(ext, obs):
    """Get the current cache for the given observatory
    """
    cache = get_filetype_cache(ext)
    try:
        return cache[obs]
    except KeyError:
        raise BadObservatory(obs)


def get_dataset_cache(ext, obs, dataset):
    """Get the current cache for the given dataset (frametype)
    """
    return get_observatory_cache(ext, obs).get(dataset, {})


# -- API endpoints

@blueprint.route('/')
@authentication.validate
def show_my_urls():
    ret = '<h3>gwdatafind_server URLs</h3>\n'
    for rule in current_app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = f"[{arg}]"

        methods = ','.join(rule.methods)
        line = unquote(f"{rule.endpoint:50s} {methods:20s} {rule}")
        ret += f'<p>{line}</p>\n'

    return ret


@blueprint.route('/<ext>.json')
@handle_errors_as_json
@authentication.validate
def find_observatories(ext):
    """List all observatories
    """
    cache = get_filetype_cache(ext)
    return list(cache.keys())


@blueprint.route('<ext>/<site>.json')
@handle_errors_as_json
@authentication.validate
def find_types(ext, site):
    """List all data tags 'frametypes'
    """
    cache = get_filetype_cache(ext)
    if site == 'all':
        sites = list(cache.keys())
    else:
        sites = [site]
    try:
        return [
            tag
            for site in sites
            for tag in cache[site]
        ]
    except KeyError as exc:
        return error_observatory(exc.args[0])


@blueprint.route('<ext>/<site>/<tag>/segments.json')
@authentication.validate
@handle_errors_as_json
def find_all_times(ext, site, tag):
    """List segments known for a given tag
    """
    cache = get_dataset_cache(ext, site, tag)
    span = segmentlist([segment(0., INF)])
    return reduce(
        operator.or_,
        (segs & span for segs in cache.values()),
        segmentlist(),
    )


@blueprint.route('<ext>/<site>/<tag>/segments/<int:start>,<int:end>.json')
@handle_errors_as_json
@authentication.validate
def find_times(ext, site, tag, start, end):
    """List segments known for a given tag
    """
    cache = get_dataset_cache(ext, site, tag)
    span = segmentlist([segment(float(start), float(end))])
    return reduce(
        operator.or_,
        (segs & span for segs in cache.values()),
        segmentlist(),
    )


@blueprint.route('<ext>/<site>/<tag>/<filename>.json')
@handle_errors_as_json
@authentication.validate
def find_url(ext, site, tag, filename):
    """Return URL(s) for a given filename
    """
    # parse GPS information from filename
    _, _, start, dur = filename.split('-')
    dur = float(dur[:-len(ext)].rstrip('.'))
    start = float(start)
    end = start + dur
    # find urls
    return list(_find_urls(
        ext,
        site,
        tag,
        start,
        end,
    ))


@blueprint.route('<ext>/<site>/<tag>/<start>,<end>')  # for --ping
@blueprint.route('<ext>/<site>/<tag>/<start>,<end>.json')
@blueprint.route('<ext>/<site>/<tag>/<start>,<end>/<urltype>.json')
@handle_errors_as_json
@authentication.validate
def find_urls(ext, site, tag, start, end, urltype=None):
    """Find all URLs in a given GPS time interval
    """
    return list(_find_urls(
        ext,
        site,
        tag,
        start,
        end,
        urltype=urltype,
        **request.args,
    ))


@blueprint.route('<ext>/<site>/<tag>/latest.json')
@blueprint.route('<ext>/<site>/<tag>/latest/<urltype>.json')
@handle_errors_as_json
@authentication.validate
def find_latest_url(ext, site, tag, urltype=None):
    """Find the latest URL(s) for a given tag
    """
    return list(_find_urls(
        ext,
        site,
        tag,
        0,
        INF,
        urltype=urltype,
        latest=True,
    ))


# -- URL matcher --------------------------------------------------------------

URL_TRANSFORM = {
    "file": _file_url,
    "gsiftp": _gsiftp_url,
    "osdf": _osdf_url,
}


def _get_latest_segment(seglist, duration):
    """Get segment for latest file of the given duration in a segment list
    """
    end = seglist[-1][1]
    return segment(end-duration, end)


def _find_urls(
    ext,
    site,
    tag,
    start,
    end,
    urltype=None,
    match=None,
    latest=False,
):
    """Find all URLs for the given GPS interval.
    """
    cache = get_dataset_cache(ext, site, tag)

    # parse file paths
    search = segment(float(start), float(end))
    lfns = defaultdict(list)
    maxgps = -1e9  # something absurdly old
    for (path, cdur), seglist in cache.items():
        # if running a 'latest' URL search, restrict the search to
        # the most recent available segment for this frametype
        if latest and seglist:  # 'if seglist' to prevent IndexError
            # get latest segment for this path
            latest = _get_latest_segment(seglist, cdur)
            if latest[1] <= maxgps:  # if this is not an improvement, move on
                continue
            # only keep the segment of the last file
            maxgps = latest[1]
            seglist = [latest]
            # empty matches to keep only this one
            lfns = defaultdict(list)

        # loop over segments and construct file URLs
        for seg in seglist:
            if not seg.intersects(search):
                continue
            gps = seg[0]
            while gps < seg[1]:
                if segment(gps, gps+cdur).intersects(search):
                    lfn = f'{site}-{tag}-{gps}-{cdur}.{ext}'
                    lfns[lfn].append(f'{path}/{lfn}')
                gps += cdur

    # convert paths to URLs for various schemes
    urltypes = set(URL_TRANSFORM.keys())
    if urltype:
        urltypes &= {urltype}
    allurls = {}
    for lfn in lfns:
        allurls[lfn] = []
        for path in lfns[lfn]:
            # build URL for each urltype (ignoring None)
            allurls[lfn].extend(filter(
                None,
                (URL_TRANSFORM[_urlt](path) for _urlt in sorted(urltypes))
            ))

    # filter URLs for each LFN and return
    urls = []
    for lfn in allurls:
        urls.extend(_filter_urls(allurls[lfn], urltype=urltype, regex=match))

    return urls


# -- URL filtering ------------------------------------------------------------

def _filter_urls(urls, urltype=None, regex=None):
    """Filter a list of URLs that all represent the same LFN.
    """
    if urltype:
        # apply urltype filter
        urls = (u for u in urls if urlparse(u).scheme == urltype)

        # apply filter preferences
        urls = _filter_preference(urls)

    # apply regex
    if regex:
        regex = re.compile(regex)
        urls = filter(regex.search, urls)

    return urls


def _filter_preference(urls):
    """Preferencially downselect a list of URLs representing a single LFN.

    If ``filter_preference`` is empty, this will just return the input list
    unfiltered.
    """
    # parse filter preference as a dict of regex keys
    # each with a list of regexs as value
    filter_preference = {
        re.compile(key): list(map(re.compile, value)) for (key, value) in
        json.loads(current_app.config.get(
            'filter_preference',
            '{}',
        ).replace('\'', '"')).items()
    }

    matches = defaultdict(list)
    unmatched = []  # list of all URLs that didn't match any pattern
    for url in urls:
        matched = False
        for pattern in filter_preference:
            if pattern.match(url):
                matches[pattern].append(url)
                matched = True
        if not matched:
            unmatched.append(url)

    keep = []

    for pattern, murls in matches.items():
        if len(murls) == 1:  # one match, just keep
            keep.extend(murls)
            continue
        # multiple matches, so we pick the one that matches highest in
        # the filter_preference list set by the server admin
        keep.extend(_rank_select_urls(murls, filter_preference[pattern]))

    # return ranked, selected list of URLs, plus everything else that
    # didn't match a preference pattern
    return keep + unmatched


def _rank_select_urls(urls, patterns):
    """Filter multiple matches of a given pattern using admin preference

    Parameters
    ----------
    urls : `list` of `str`
        the list of URLs that all represent the same LFN, and all matched
        a given master pattern (usually just a URL type scheme)

    patterns : `list` of `re.Pattern`
        the ordered list of regular expressions against which to
        preferentially match URLs

    Returns
    -------
    matches : `list` of `str`
        a list containing a single URL that first matched one of the patterns,
        or the full input list of nothing matched
    """
    for pattern in patterns:
        for url in urls:
            if pattern.search(url):
                return [url]
    return urls  # we should never get to here
