# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

from argparse import ArgumentParser


def version():
  import pkg_resources
  return pkg_resources.get_distribution('devpm').version


def main(args = None):
  ver = version()
  print('devpm go2 ' + ver)


if __name__ == '__main__':
  main()