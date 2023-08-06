# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

# Visual studio code cli and user settings editor

import json
import os
import sys
import subprocess
from contextlib import contextmanager

class Code:
  def __init__(self):
    self.bin = None
    self.shell = False
    self.settings_root = None
    self.user_settings_path = None

  def init(self):
    host_os = sys.platform
    home = os.path.expanduser("~")
    # https://code.visualstudio.com/docs/getstarted/settings#_settings-file-locations
    if host_os == 'win32':
      self.settings_root = os.getenv('APPDATA')
    elif host_os == 'darwin':
      self.settings_root = os.path.join(home, 'Library', 'Application Support')
    else:
      self.settings_root = os.path.join(home, '.config')
    self.user_settings_path = os.path.join(self.settings_root, 'Code', 'User', 'settings.json')
    self.shell = host_os == 'win32'
    if os.environ.get('NODE_OPTIONS'):
      os.environ.pop('NODE_OPTIONS')
    try:
      subprocess.check_call(['code', '--version'], shell=self.shell)
      self.bin = 'code'
    except:
      # default path
      default_path = None
      if host_os == 'darwin':
        default_path = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
      elif host_os == 'win32':
        default_path = os.path.join(home, 'AppData', 'Local', 'Programs', 'Microsoft VS Code', 'bin', 'code')
      if not default_path or not os.path.exists(default_path):
        return False
      self.bin = default_path
      subprocess.check_call([self.bin, '--version'], shell=self.shell)
    return True

  def install_vsix(self, path, ver):
    args = [self.bin, '--install-extension']
    if ver == 'latest':
      args.append('--force')
    elif ver:
      args.append(path + '@' + ver)
    else:
      args.append(path)
    subprocess.call(args, shell=self.shell)

  def check_install_vsix(self, ext, ver):
    args = [self.bin, '--list-extensions', '--show-versions']
    installed_ver = None
    if ver == '':
      ver = None
    try:
      output = subprocess.check_output(args, shell=self.shell).decode('utf-8')
      for line in output.splitlines():
        index = line.find('@')
        if index > 0:
          if str(line[:index]).lower() == ext:
            installed_ver = str(line[index+1:])
    except:
      pass
    finally:
      if not installed_ver or (ver and installed_ver != ver):
        self.install_vsix(ext, ver)
      else:
        print('Version %s installed.' % installed_ver)

  @contextmanager
  def open_user_settings(self):
    f = open(self.user_settings_path, 'r')
    s = f.read()
    f.close()
    settings = json.loads(s)
    yield settings
    s2 = json.dumps(settings, indent=4)
    if s != s2:
      f = open(self.user_settings_path, 'w')
      f.write(s2)
      f.close()
