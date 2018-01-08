#! /usr/bin/env python

from app.collect import Main
import os


_dir = os.path.dirname(__file__)
filename = os.path.join(_dir, 'config.xml')


# we are going to parse xml and get stats for the servers
Main().parse_collect_data(filename)
