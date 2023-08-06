# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

# Python pip manager

import os
import sys
import subprocess


class Pip:
  def __init__(self):
    self.bin = None
    self.shell = sys.platform == 'win32'
  
  def init(self):
    try:
      output = subprocess.check_output(['pip', '--version']).decode('utf-8')
      if 'python 2' in output:
        return False
      print(output.strip())
      self.bin = 'pip'
      return True
    except:
      return False

  def install(self, lib, ver):
    args = [self.bin, 'install']
    if ver:
      args.append('-v')
      args.append('%s==%s' % (lib, ver))
    else:
      args.append(lib)
    subprocess.call(args, shell=self.shell)

  def show(self, lib):
    info = {}
    args = [self.bin, 'show', lib]
    try:
      output = subprocess.check_output(args).decode('utf-8')
      for line in output.splitlines():
        token = ': '
        index = line.find(token)
        if index > 0:
          info[line[:index]] = line[index+len(token):]
    except:
      pass
    return info

  def check_install(self, lib, ver):
    installed_ver = None
    info = self.show(lib)
    if 'Version' in info:
      installed_ver = info['Version']
    if not installed_ver or (ver and installed_ver != ver):
      self.install(lib, ver)
    else:
      print('Version %s installed.' % installed_ver)

  def which(self, lib):
    info = self.show(lib)
    bin_name = lib if sys.platform != 'win32' else lib + '.exe'
    if 'Location' in info:
      bin_path = info['Location']
      bin = os.path.join(bin_path, bin_name)
      if os.path.exists(bin):
        return bin
      bin_path = os.path.abspath(os.path.join(bin_path, '..', '..', 'Scripts'))
      bin = os.path.join(bin_path, bin_name)
      if os.path.exists(bin):
        return bin
    return None
