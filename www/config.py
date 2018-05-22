#!/user/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration."""

__author__ = 'Zachary Zhang'


import config_default


class Table(dict):
	# simple dict but support access as x.y style.

	def __init__(self, names=(), values=(), **kw):
		super(Table, self).__init__(**kw)
		for k, v in zip(names, values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

	@classmethod
	def from_dict(cls, src_dict):
		t = Table()
		for k, v in t.items():
			t[k] = from_dict(v) if isinsctance(v, dict) else v
		return t


def merge(defaults, override):
	d = {}
	for k, v in defaults.items():
		if k in override:
			if isinsctance(v, dict):
				d[k] = merge(v, override[k])
			else:
				d[k] = override[k]
		else:
			d[k] = v
	return d


configs = config_default.configs

try:
	import config_override
	configs = merge(configs, config_override.configs)
except ImportError:
	pass

configs = Table.from_dict(configs)