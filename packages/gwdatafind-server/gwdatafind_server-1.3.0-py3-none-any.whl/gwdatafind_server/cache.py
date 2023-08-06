# -*- coding: utf-8 -*-
# Copyright (2019) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""Utilities for the GWDataFind Server
"""

import re
import threading
import time
from collections import defaultdict
from os.path import getmtime


from ligo.segments import (segment, segmentlist)

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


class FileManager(threading.Thread):
    """Common methods for caching files in memory
    """
    def sleep(self):
        """Wait until next iteration
        """
        self.logger.debug(f"sleeping for {self.sleeptime} seconds")
        start = time.time()
        while time.time() - start < self.sleeptime:
            time.sleep(.5)
            if self.shutdown:
                self.state = 'SHUTDOWN'
                return

    def run(self):
        """Continuously read and update the cache
        """
        last = 0
        while True:
            if self.shutdown:
                return

            try:
                mod = getmtime(self.path)
            except OSError as exc:
                self.logger.error(
                    "unable to determine modification time of "
                    f"{self.path}: {exc}",
                )
                mod = 0

            if last < mod:  # file changed since last iteration
                try:
                    self.parse()
                except (TypeError, ValueError) as exc:
                    self.logger.error(f"error parsing {self.path}: {exc}")
                else:
                    last = time.time()
            else:
                self.logger.debug('cache file unchanged since last iteration')
            self.sleep()


class CacheManager(FileManager):
    """Thread to continuously update the diskcache in memory
    """
    def __init__(self, parent, path, sleeptime=60,
                 site_exclude=None, site_include=None,
                 frametype_exclude=None, frametype_include=None):
        super().__init__(name=type(self).__name__)
        self.path = path

        # create logger
        self.logger = parent.logger

        # create lock and flags
        self.lock = threading.Lock()
        self.shutdown = False
        self.ready = False

        # create cache
        self.cache = defaultdict(dict)

        # time between iterations
        self.sleeptime = sleeptime

        # record exclusion filters
        self.patterns = {key: self._parse_pattern(value) for key, value in [
             ('site_exclude', site_exclude),
             ('site_include', site_include),
             ('frametype_exclude', frametype_exclude),
             ('frametype_include', frametype_include),
        ]}

    @staticmethod
    def _parse_pattern(pattern):
        if pattern is None:
            pattern = []
        if not isinstance(pattern, list):
            pattern = [pattern]
        return [re.compile(reg) for reg in pattern]

    def _update(self, cache):
        self.logger.debug('updating frame cache')
        with self.lock:
            self.cache = cache
        self.logger.debug(f'updated frame cache with {len(cache)} entries')
        # print what we got
        for a, suba in cache.items():  # filetype
            for b, subb in suba.items():  # observatory
                for c, subc in subb.items():  # dataset
                    self.logger.debug(
                        f"  {a}/{b}/{c}: {len(subc)} entries",
                    )

    def exclude(self, site, tag):
        """Return `True` if this site and tag combination should be excluded
        """
        for var, key in ((site, 'site'), (tag, 'frametype')):
            pat = f"{key}_exclude"
            for regex in self.patterns[pat]:
                if regex.search(var):  # positive match
                    return pat
            pat = f"{key}_include"
            for regex in self.patterns[pat]:
                if not regex.search(var):  # negative match
                    return pat

    def parse(self):
        """Read the frame cache from the path
        """
        self.logger.info(f'parsing frame cache from {self.path}')
        exclusions = {key: 0 for key in self.patterns}
        nlines = 0
        cache = {}

        with open(self.path, 'rb') as fobj:
            for line in fobj:
                if line.startswith(b"#"):
                    continue
                # parse line
                site, tag, path, dur, ext, segments = self._parse_line(line)
                # determine exclusion
                exclude = self.exclude(site, tag)
                if exclude:  # record why excluded
                    exclusions[exclude] += 1
                    continue
                # store this line in the cache
                subcache = cache
                for key in (
                    ext,
                    site,
                    tag,
                ):
                    subcache = subcache.setdefault(key, {})
                subcache[(path, int(dur))] = segments
                nlines += 1

        self.logger.info(f'parsed {nlines} lines from frame cache file')
        for key, count in exclusions.items():
            self.logger.debug(f'excluded {count} lines with {key}')

        # store new cache
        self._update(cache)
        self.ready = True  # can now be used

    @staticmethod
    def _parse_line(line):
        """Parse one line from the frame cache file
        """
        try:
            if isinstance(line, bytes):
                line = line.decode('utf-8')

            # parse line
            header, modt, count, times = line.strip().split(' ', 3)
            hdr_list = header.split(',')
            # old style datafind files assume gwf
            if len(hdr_list) == 5:
                hdr_list.append('gwf')
            path, site, tag, _, dur, ext = tuple(hdr_list)

            # format times
            times = list(map(int, times[1:-1].strip().split(' ')))
            segments = segmentlist(map(
                segment, (times[i:i+2] for i in range(0, len(times), 2))))
        except Exception as ex:
            ermsg = 'Error parsing line "{0}"\n {1} - {2}'.\
                format(line, ex.__class__.name, str(ex))
            raise AssertionError(ermsg)
        return site, tag, path, dur, ext, segments


class GridmapManager(FileManager):
    """Thread to continuously update the grid-mapfile in memory
    """
    def __init__(self, parent, path, sleeptime=600):
        super().__init__(name=type(self).__name__)
        self.path = path

        # create logger
        self.logger = parent.logger

        # create lock and flags
        self.lock = threading.Lock()
        self.shutdown = False
        self.ready = False

        # create cache
        self.cache = []

        # time between iterations
        self.sleeptime = sleeptime

    def _update(self, cache):
        self.logger.debug('updating grid map cache with lock...')
        with self.lock:
            self.cache = cache
        self.logger.debug(f'updated grid map cache with {len(cache)} entries')
        # self.logger.debug(str(cache))
        self.logger.debug('lock released')

    def parse(self):
        """Read the grid-map file from the path
        """
        self.logger.info(f'parsing grid map file from {self.path}')
        nlines = 0
        cache = []

        with open(self.path, 'r') as fobj:
            for line in fobj:
                subject = self._parse_line(line)
                cache.append(subject)
                nlines += 1

        self.logger.info(f'parsed {nlines} lines from grid map file')

        # store new cache
        self._update(cache)
        self.ready = True  # can now be used

    @staticmethod
    def _parse_line(line):
        """Parse one line from the grid map file
        """
        parts = line.strip().split('"')
        if len(parts) in {2, 3}:
            return parts[1]
        if len(parts) == 1:
            return parts[0]
        raise RuntimeError(f"error parsing grid map file line: '{line}'")
