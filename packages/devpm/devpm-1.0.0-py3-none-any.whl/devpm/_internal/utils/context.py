# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

# System context manager

import subprocess
from devpm._internal.utils.git import Git
from devpm._internal.utils.bash import Bash
from devpm._internal.utils.log import Log
from devpm._internal.utils.code import Code
from devpm._internal.utils.pip import Pip


class Context:
  def __init__(self):
    self.log = Log()
    self.code = Code()
    self.pip = Pip()
    self.bash = Bash()
    self.git = Git()
  
  def init(self):
    self.log.h1('Checking executable [code]')
    if not self.code.init():
      self.log.abort('VSCode required. see https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line')

    self.log.h1('Checking executable [pip]')
    if not self.pip.init():
      self.log.abort('python3 required. see https://www.python.org/downloads/')

    self.log.h1('Checking executable [git]')
    if not self.git.init():
      self.log.abort('git required. see https://git-scm.com/downloads')

  def check_install_exe(self, exe, url):
    installed_ver = None
    args = [exe, '-h']
    try:
      p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output, error = p.communicate()
      if p.returncode != 1:
        if len(output) == 0:
          output = error.decode('utf-8')
        else:
          output = output.decode('utf-8')
        if len(output) > 0:
          lines = output.splitlines()
          installed_ver = lines[0]
    except:
      pass
    return installed_ver

  def evaluate(self, exp, cwd):
    if not exp or exp[0] != '$':
      return exp
    index = exp.find(':', 1)
    if index > 0:
      func = exp[1:index]
      args = exp[index+1:]
    else:
      func = exp[1:]
      args = None
    if func == 'pip.which':
      return self.pip.which(args)
    elif func == 'bash.which':
      return self.bash.which(args)
    elif func == 'git.install_pre_commit':
      return self.git.install_pre_commit(args, cwd)
    return None
