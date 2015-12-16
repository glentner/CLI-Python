#!/bin/bash
# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# build.sh


make || exit 1
make test || exit 1
