#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import datetime


class Plugin(object):
    def __init__(self, **kwargs):
        self.result = []

    def save(self, to, result, **kwargs):
        """docstring for save"""
        info = kwargs
        now = datetime.datetime.utcnow()
        record = dict(result, time = now, **info)
        self.result.append(record)
        to.insert(record)


class PluginManager:
    def __init__(self, path=None, plugin_init_args={}):
        if path:
            self.plugin_dir = path
        else:
            self.plugin_dir = os.path.dirname(__file__) + '/../plugins/'
        self.plugins = {}
        self._load_plugins()
        self._register_plugins(**plugin_init_args)

    def _load_plugins(self):
        sys.path.append(self.plugin_dir)
        plugin_files = [fn for fn in os.listdir(self.plugin_dir) if fn.startswith('plugin_') and fn.endswith('.py')]
        plugin_modules = [m.split('.')[0] for m in plugin_files]
        for module in plugin_modules:
            m = __import__(module)

    def _register_plugins(self, **kwargs):
        for plugin in Plugin.__subclasses__():
            obj = plugin(**kwargs)
            if hasattr(obj, 'keywords'):
                self.plugins[obj] = obj.keywords
            else:
                self.plugins[obj] = []

    def call_method(self, method, keywords=[], **args):
        for plugin in self.plugins:
            if not keywords or (set(keywords) & set(self.plugins[plugin])):
                try:
                    getattr(plugin, method)(**args)
                except:
                    raise

