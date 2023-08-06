# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [0-based versioning](https://0ver.org/).

## [Unreleased]

## v0.1.10 (2023-07-16)

### Added

- Add Changelog page to project URL
- Add `-o` or `--overwrite` output filename arg
- Check for existing output filename when writing output for `xstxt`

### Changed

- Remove deprecated FAQ for `xstxt` from doc
- Remove support for Python 3.7
- Remove unused `line-profiler` dep
- Run coverage test in parallel by default
- Switch to `pipenv` to manage deps
- Update `tox` to use `pipenv` and use `tox.ini` as config
- Update changelog for consistent header style

### Fixed

- Fix cannot start xstxt due to uninitialized variable
- Fix coverage report due to typo error
- Fix missing `monitor` field in `xstxt.toml` file
- Fix inconsistent output sphinx output folder
- Remove warnings on deprecated `script_runner` calls

## v0.1.9 (2023-05-28)

### Added

- Add watching mode, `-m` or `--monitor` for `xstxt` to regenerate the content
  from html files

### Changed

- Update project classifiers and dependencies
- Run test randomly by default
- Update PyPi's classifiers

### Fixed

- Fix session not closed during test
- Resolve raising generic exception
- Use `pip install -e` to install local development copy

## v0.1.8 (2023-04-16)

### Added

- Add multiprocessor support for `pytest`

### Changed

- Deprecate and remove `is_relative_url` and `relative_to_absolute_url`
  function in favour of lxml's `make_links_absolute` function
- Reduce number of browser session to prevent locking
- Refactor async tests
- Remove explicit config for async in tests

### Fixed

- Set `index.html` as default filename for index page if missing
- Rename `-w` to `-wf` option to prevent duplicate with `--width`
- Update translations

## v0.1.7 (2023-02-26)

### Added

- Add `-oi` or `--output-individual-file` to create a txt file for its
  corresponding html file

### Changed

- Revise default environment for tox to run
- Remove escaped paragraph separator argument during argument parsing
- Remove the duplicate `_unescape` function
- Show longer chapter title in debugging log

### Fixed

- Fix incorrect wrapping which was set to default `70`

## v0.1.6 (2023-01-29)

### Added

- Support `-la` or `--language` option for metadata when exporting text file

### Changed

- Use `-V` or `--version` flag instead of `-v` for show program version
- Support long options for all command option flags
- Use same logging output convention for error and exception message
- Format help message indentation to improve readability

## v0.1.5 (2022-12-30)

### Added

- Show progress when processing multiple HTML files when debugging (`-d`) was
  disabled
- Add `-fw` option to convert selected halfwidth characters to its fullwidth
  equivalent
- Add `-ps` option to set paragraph separator, default to two newlines (`\n\n`)
- Add `flake8-simplify` plugin in linting with Flake8

### Changed

- Support and test against Python 3.11
- Show debug logging for arguments and parsed arguments
- Set default width `-w` for wrapping to `0` (disabled)
- Set default indentation characters `-ic` to `""` (disabled)
- Width `-w` and indentation characters `-ic` option should work independently
- Update regex rule in `xstxt.toml` file to replace repeated empty line
- Update missing type hints
- Refactor to use global config instead of individual config item
- Refactor handling of piping for default URL argument for `xsget`
- Set Pylint check to the minimum support Python version (3.7)
- Split logging of downloading and saving HTML into two separate lines
- Bump support for latest Python versions in `pyenv`

### Fixed

- Fix layout for `width` argument help message
- Fix extra help menu string when generating doc through Sphinx
- Add missing package in contribution doc
- Resolve W0621 issue raised by Pylint

## v0.1.4 (2022-10-14)

### Added

- Add `-b` option to crawl site by actual browser
- Add `-bs` option to set the number of session/page to open by browser
- Add `-bd` option to set the delay to wait for a page to load in browser

### Changed

- Use simpler asyncio syntax that support Python 3.7
- Sync asyncio debugging with `-d` option
- Switch to pre-commit as default linter tool from tox
- Resolve mypy and pylint warnings

## v0.1.3 (2022-08-09)

### Added

- Add `-w` option to wrap text at specify length
- Add `-ic` option to set indent characters for a paragraph only if `-w` option
  is more than zero

### Changed

- Upgrade the TOML config file if there are changes in the config template file
  for both xsget and xstxt app

### Fixed

- Fix not showing exact regex debug log
- Show individual config item in debug log

## v0.1.2 (2022-07-29)

### Changed

- Switch to pre-commit to manage code linting
- Update FAQ for xstxt usage
- Add more html replacement regex rules to xstxt.toml

### Fixed

- Fix invalid base_url in config
- Enable debug by default in config

## v0.1.1 (2022-07-09)

### Changed

- Fix missing description in PyPi page
- Test version using dynamic value

## v0.1.0 (2022-07-08)

### Added

- Initial public release
