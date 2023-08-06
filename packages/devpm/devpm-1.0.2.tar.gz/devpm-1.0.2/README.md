# devpm
Development package manager

## Usage

* devpm install - Install packages by devpackage.json in current directory which support config:
  - vscodeDependencies for vscode extensions
  - vscodeUserSettings for edit vscode user settings file
  - pythonDependencies for python modules
  - bashDependencies for custom bash script
  - gitHooks for add git hooks like `pre-commit`, `commit-msg`

## devpackage.json

### vscodeDependencies
Packages installed by visutal studio code.
Key for vscode extension id, value for `version` (1).
Version definition: 
* "" (empty)          - install when not exists
* "latest"            - uninstall and install latest
* "1.0.0" (specified) - install when version mismatched

### pythonDependencies
Packages installed by pip.
Key for pip name, value for `version`, ses (1).

### bashDependencies
Packages installed by custom bash script.
Key for excutable name after installed, value is an object describes script in platforms.
The platform is from python `sys.platform`, include 'darwin', 'win32' and 'linux'.

### vscodeUserSettings
Write to visual studio code user settings <https://code.visualstudio.com/docs/getstarted/settings#_settings-file-locations>.
Key and value format same to the user settings.
In addition, the value support `devpm expression`:
* `$bash.which:[bin]` - returns the bin path in system by `which [bin]`
* `$pip.which:[bin]` - returns the bin path in pip by `pip show [bin]`

### gitHooks
Write to git hooks for root project and it's git submodules. Support commit-msg, pre-commit.
#### commit-msg
`type` (string) now is always `regexp`, for custom regexp match.
`pattern` (string) for the regexp pattern.
`tips` (array) used to show tips when the `commit-msg` mismatched, each item for one line.

#### pre-commit
`type` (string) now is always `pre-commit`, use the`pre-commit` plugin <https://pre-commit.com/>.
`repos` (array) content is same to '.pre-commit-config.yaml' but in json format.

### Example

```json
{
  "$schema": "https://raw.githubusercontent.com/wequick/devpm/main/devpackage.schema.json",
  "vscodeDependencies": {
    "ms-vscode.cpptools-extension-pack": "",
    "wequick.cpp-creator": "",
    "wequick.coverage-gutters": "",
    "mine.cpplint": ""
  },
  "vscodeUserSettings": {
    "cpplint.cpplintPath": "$pip.which:cpplint",
    "cmake.cmakePath": "$bash.which:cmake"
  },
  "pythonDependencies": {
    "gcovr": "4.2",
    "cpplint": "1.6.1",
    "pre-commit": "3.3.3"
  },
  "bashDependencies": {
    "OpenCppCoverage": {
      "win32": "https://github.com/OpenCppCoverage/OpenCppCoverage/releases/download/release-0.9.9.0/OpenCppCoverageSetup-x64-0.9.9.0.exe"
    },
    "cppcheck": {
      "win32": "https://github.com/danmar/cppcheck/releases/download/2.11/cppcheck-2.11-x64-Setup.msi",
      "linux": "apt-get install cppcheck",
      "darwin": "brew install cppcheck"
    }
  },
  "gitHooks": {
    "commit-msg": {
      "type": "regexp",
      "pattern": "^[feat|fix|refactor|chore|test|style|docs]",
      "tips": [
        "Invalid commit message style, please format as following:",
        "  fix: some msg",
        "  ^^^^              Type: feat|fix|refactor|chore|test|style|docs",
        "       ^^^^^^^^     Summary in present tense",
        "Type:",
        "  feat     : new feature for the user, not a new feature for build script",
        "  fix      : bug fix for the user, not a fix to a build script",
        "  docs     : changes to the documentation",
        "  style    : formatting, missing semi colons, etc; no production code change",
        "  refactor : refactoring production code, eg. renaming a variable",
        "  test     : adding missing tests, refactoring tests; no production code change",
        "  chore    : updating grunt tasks etc; no production code change",
        "",
        "See <https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716> for more details.",
        ""
      ]
    },
    "pre-commit": {
      "type": "pre-commit",
      "repos": [
        {
          "repo": "https://github.com/pocc/pre-commit-hooks",
          "rev": "v1.3.5",
          "hooks": [
            { "id": "cpplint" },
            { "id": "cppcheck" }
          ]
        }
      ]
    }
  }
}
```

## Develop

```bash
$ python src/devpm/__main__.py install
```
