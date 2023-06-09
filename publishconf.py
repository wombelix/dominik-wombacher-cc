#!/usr/bin/env python

# SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
#
# SPDX-License-Identifier: CC0-1.0

# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://dominik.wombacher.cc'
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True