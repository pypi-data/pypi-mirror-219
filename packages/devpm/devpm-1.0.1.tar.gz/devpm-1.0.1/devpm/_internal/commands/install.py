# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

# devpm install

from devpm._internal.cli.base_command import Command
from devpm._internal.utils.context import Context
import os
import sys
import json


class InstallCommand(Command):
    def run(self, args=None):
        cwd = os.getcwd()
        config_file = os.path.join(cwd, 'devpackage.json')
        if not os.path.exists(config_file):
            sys.stdout.write('devpackage.json no found.')
            sys.exit(1)
        sys.stdout.write('Install from %s\n' % config_file)
        config = {}
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        context = Context()
        context.init()

        vscode_dependencies = config['vscodeDependencies']
        python_dependencies = config['pythonDependencies']
        bash_dependencies = config['bashDependencies']
        vscode_user_settings = config['vscodeUserSettings']
        git_hooks = config['gitHooks']

        # vscode extensions
        for dep in vscode_dependencies:
            context.log.h1('Checking vscode extension [%s]' % dep)
            context.code.check_install_vsix(dep, vscode_dependencies[dep])
        for dep in python_dependencies:
            context.log.h1('Checking python module [%s]' % dep)
            context.pip.check_install(dep, python_dependencies[dep])
        # vscode user settings
        if len(vscode_user_settings) > 0:
            with context.code.open_user_settings() as settings:
                for key in vscode_user_settings:
                    context.log.h1('Checking vscode user settings [%s]' % key)
                    needs_update = True
                    old_value = None
                    if key in settings:
                        old_value = settings[key]
                        if 'path' in key.lower():
                            # if old path not exists, force to update
                            needs_update = not os.path.exists(old_value)
                    if needs_update:
                        value = context.evaluate(vscode_user_settings[key])
                        if value and old_value != value:
                            settings[key] = value
                            print('Update from [%s] to [%s].' % (old_value, value))
                            continue
                    print(old_value)
        # bash scripts
        for key in bash_dependencies:
            deps = bash_dependencies[key]
            if sys.platform in deps:
                dep = deps[sys.platform]
                context.log.h1('Checking executable [%s]' % key)
                installed_path = context.bash.check_install(key, dep)
                if not installed_path:
                    context.log.abort('Failed to install %s, try by yourself: `%s`' % (key, dep))
                sys.stdout.write(installed_path + '\n')
        # git hooks
        if len(git_hooks) > 0:
            project_root = os.getcwd()
            git_path = context.git.git_path(project_root)
            if not git_path:
                context.log.warn('.git not found.')
            for hook_name in git_hooks:
                context.log.h1('Checking git hooks [%s]' % hook_name)
                context.git.append_hook(project_root, git_path, hook_name, git_hooks[hook_name], True)

        context.log.info('Done. You may need to restart console windows.')
