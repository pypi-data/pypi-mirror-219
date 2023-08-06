# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

# Common log

class Log:
  def __init__(self):
    pass

  def abort(self, msg):
    print('')
    print(' [!] Error: %s' % (msg))
    print('')
    exit(1)

  def warn(self, msg):
    print('')
    print(' [!] Warn: %s' % (msg))
    print('')

  def info(self, msg):
    print('')
    print(' [!] %s' % (msg))
    print('')

  def h1(self, msg):
    print('')
    print('==== %s ====' % (msg))
