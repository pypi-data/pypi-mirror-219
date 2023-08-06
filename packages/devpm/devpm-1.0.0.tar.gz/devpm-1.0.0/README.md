# devpm
Development package manager

## Usage

* devpm install - Install packages by devpackage.json in current directory which support config:
  - vscodeDependencies for vscode extensions
  - vscodeUserSettings for edit vscode user settings file
  - pythonDependencies for python modules
  - bashDependencies for custom bash script
  - gitHooks for add git hooks like `pre-commit`, `commit-msg`

## Develop

```bash
$ python src/devpm/__main__.py install
```
