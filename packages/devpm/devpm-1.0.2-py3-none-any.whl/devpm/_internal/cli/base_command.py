# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

# Base command

class Command:
  def __init__(self, name, summary):
    self.name = name
    self.summary = summary


  def run(self, args = None):
    pass


  def main(self, args = None):
    self.run(args)
