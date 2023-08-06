# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

# Common bash cli

import sys
import subprocess

class Bash:
  def __init__(self):
    self.is_win32 = sys.platform == 'win32'
    if self.is_win32:
      self.bin = r'C:\Program Files\Git\bin\bash.exe'
    else:
      self.bin = 'bash'

  def bash_path(self, path):
    drive, p = path.split(':')
    return '/%s%s' % (drive.lower(), p.replace('\\', '/'))

  def win32_bin_path(self, path):
    index = path.find('/', 1)
    drive = path[1:index].upper()
    p = path[index:].replace('/', '\\')
    return drive + ':' + p + '.exe'

  def which(self, bin):
    args = [self.bin, '-c', 'which ' + bin]
    try:
      output = subprocess.check_output(args, shell=False).decode('utf-8')
      return self.win32_bin_path(output.strip()) if self.is_win32 else output.strip()
    except:
      pass
    return None
  
  def check_install(self, bin, script):
    path = self.which(bin)
    if path:
      return path
    try:
      args = [self.bin, '-c', script]
      subprocess.check_call(args)
    except:
      return None
    return self.which(bin)
