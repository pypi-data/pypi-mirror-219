# -*- coding: utf-8 -*-
# Copyright (2019) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""The GWDataFind server app
"""

import os
import time
from importlib import import_module

from configobj import ConfigObj
import logging

from flask import Flask

from .api import (
    base as base_api,
    DEFAULT_API,
)
from .cache import CacheManager, GridmapManager

# add custom debug variable
os.environ.setdefault(
    "FLASK_DEBUG",
    os.getenv("GWDATAFIND_SERVER_DEBUG", "0"),
)


class GWDataFindApp(Flask):
    def __init__(self, import_name, configpath, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)

        config = ConfigObj(configpath)
        try:
            self.config.update(config["GWDataFindServer"])  # new key
        except KeyError:
            self.config.update(config["LDRDataFindServer"])  # old key

        # log to file
        if self.config.get("logfile"):
            lfh = logging.FileHandler(
                self.config["logfile"],
                mode='w',
            )
            lfh.setFormatter(self.logger.handlers[-1].formatter)
            self.logger.addHandler(lfh)

        # create thread to read cache file and start
        CacheMan = self._init_cache_manager(self.config)
        CacheMan.daemon = True
        CacheMan.start()

        # create thread to read grid map file and start
        GridMapMan = self._init_gridmap_manager(self.config)
        GridMapMan.daemon = True
        GridMapMan.start()

        # register all API endpoints
        self._register_blueprints()

    def _init_cache_manager(self, conf):
        cachefile = conf['framecachefile']
        patterns = {
            key.rsplit('_', 1)[0]: conf[key] for
            key in conf.keys() if key.endswith('_pattern')
        }
        sleeptime = float(conf.get('framecachetimeout', 60))
        self.cache_manager = CacheManager(self, cachefile, sleeptime=sleeptime,
                                          **patterns)
        return self.cache_manager

    def _init_gridmap_manager(self, conf):
        gridmapfile = conf['gridmapcachefile']
        sleeptime = float(conf.get('gridmapcachetimeout', 600))
        self.gridmap_manager = GridmapManager(self, gridmapfile,
                                              sleeptime=sleeptime)
        return self.gridmap_manager

    def get_cache_data(self, *keys):
        self.logger.debug('retrieving cache')
        while not self.cache_manager.ready:
            # cache file is not ready
            self.logger.debug("waiting for frame cache...")
            time.sleep(.5)
        with self.cache_manager.lock:
            return self._get_cache_data(keys)

    def _register_blueprints(self):
        # register the base API endpoint
        self.register_blueprint(base_api.blueprint)

        # register all supported APIs
        supported_apis = self.config.get(
            "supported_apis",
            [DEFAULT_API],
        )
        if isinstance(supported_apis, str):  # config parsed as a string
            supported_apis = [api.strip() for api in supported_apis.split(",")]
        for api in supported_apis:
            api_mod = import_module(f"..api.{api}", package=__name__)
            self.register_blueprint(api_mod.blueprint)

        # store the formatted list to be used by the /api/version endpoint
        self.config["supported_apis"] = supported_apis

    def _get_cache_data(self, keys):
        cache = self.cache_manager.cache
        keys = list(keys)
        while keys:
            key = keys.pop(0)
            cache = cache.get(key, {})
        return cache

    def get_gridmap_data(self):
        self.logger.debug('retrieving gridmap')
        while not self.gridmap_manager.ready:
            # cache file is not ready
            self.logger.debug("waiting for gridmap...")
            time.sleep(.5)
        with self.gridmap_manager.lock:
            return self.gridmap_manager.cache

    def shutdown(self):
        with self.cache_manager.lock:
            self.cache_manager.shutdown = True
        with self.gridmap_manager.lock:
            self.gridmap_manager.shutdown = True
        self.cache_manager.join()
        self.gridmap_manager.join()
