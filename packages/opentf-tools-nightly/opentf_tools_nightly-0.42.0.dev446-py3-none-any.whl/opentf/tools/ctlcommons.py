# Copyright 2022 Henix, henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""opentf-ctl commons"""

from typing import Iterable, List, Optional

import csv
import logging
import re
import sys


########################################################################
# debug


def _error(*msg) -> None:
    logging.error(*msg)


def _warning(*msg) -> None:
    logging.warning(*msg)


def _debug(*msg) -> None:
    logging.debug(*msg)


def _info(*msg) -> None:
    logging.info(*msg)


########################################################################
# sys.argv processing


COMMON_OPTIONS = [
    '--token=',
    '--user=',
    '--orchestrator=',
    '--context=',
    '--insecure-skip-tls-verify=',
    '--insecure_skip_tls_verify=',
    '--opentfconfig=',
]


def _ensure_options(args: List[str], extras=(), flags=()) -> None:
    """Check options.

    Exit with error code 2 if there are unknown options in args.

    # Required parameters

    - args: a list of strings

    # Optional parameters

    - extra: a collection of string collections
    - flags: a collection of string collections

    Items in `extra` are expecting a parameter, in the form `extra=x` or
    `extra x` (for example: `--user=foo` or `--user foo`).

    Items in `extra` may end with `=`, but this is not mandatory, it
    will be implicitly added if not there.
    """
    max_index = len(args) - 1
    processed: List[Optional[str]] = list(args)
    options = list(COMMON_OPTIONS)
    for option in extras:
        for alias in option:
            options.append(f'{alias.rstrip("=")}=')
    for option in flags:
        for alias in option:
            options.append(alias)
    for index, item in enumerate(args):
        if processed[index] is None:
            continue
        for option in options:
            if option[-1] == '=':
                if item.replace('_', '-').startswith(option):
                    processed[index] = None
                if item == option[:-1]:
                    if index < max_index:
                        processed[index] = None
                        processed[index + 1] = None
                    else:
                        _error(f'Missing parameter for option {item}.')
                        sys.exit(2)
            if item.replace('_', '-') == option:
                processed[index] = None

    unknown = [arg for arg in processed if arg is not None]
    if unknown:
        _error(f'Unknown option: {" ".join(unknown)}.')
        sys.exit(2)


def _is_command(command: str, args: List[str]) -> bool:
    """Check if args matches command.

    `_` are placeholders.

    # Examples

    ```text
    _is_command('get job _', ['', 'get', 'job', 'foo'])  -> True
    _is_command('get   job  _', ['', 'get', 'job', 'foo'])  -> True
    _is_command('GET JOB _', ['', 'get', 'job', 'foo'])  -> False
    ```

    # Required parameters

    - command: a string
    - args: a list of strings

    # Returned value

    A boolean.
    """
    pattern = command.split()
    pattern_length = len(pattern)
    maybe_missing = pattern_length == len(args) and pattern[-1] == '_'
    if pattern_length >= len(args) and not maybe_missing:
        return False
    for pos, item in enumerate(pattern, start=1):
        if maybe_missing and pos == pattern_length:
            _error(
                f'Missing required parameter.  Use "{" ".join(pattern[:-1])} --help" for details.'
            )
            sys.exit(1)
        if item not in ('_', args[pos]):
            return False
    return True


def _get_arg(prefix: str) -> Optional[str]:
    """Get value from sys.argv.

    `prefix` is a command line option prefix, such as `--foo=`.  It
    should not contain '_' symbols.

    The first found corresponding command line option is returned.

    The comparaison replaces '_' with '-' in the command line options.

    # Examples

    ```text
    _get_arg('--foo_bar=') -> baz if sys.argv contains `--foo-bar=baz`
                                or `--foo_bar=baz` or `--foo-bar baz`
    _get_arg('--foo=')     -> yada if sys.argv contains `--foo yada`
                                None otherwise
    _get_arg('-o=')        -> yada if sys.argv contains `-o yada` or
                                `-o=yada`, None otherwise
    ```

    # Required parameters

    - prefix: a string

    # Returned value

    None if `prefix` is not found in `sys.argv`, the corresponding entry
    with the prefix stripped if found.
    """
    max_index = len(sys.argv) - 1
    for index, item in enumerate(sys.argv[1:], start=1):
        if prefix[-1] == '=':
            if item.replace('_', '-').startswith(prefix):
                return item[len(prefix) :]
            if item == prefix[:-1] and index < max_index:
                return sys.argv[index + 1]
    return None


# csv processing


def _get_columns(wide: Iterable[str], default: Iterable[str]) -> Iterable[str]:
    """Return requested columns.

    Returns custom-columns if specified on command line.
    If not, if wide is specified on command line, it wins.
    Else default is returned.

    Raises ValueError if command line parameters are invalid.
    """
    output = _get_arg('--output=')
    if output is None:
        output = _get_arg('-o=')
    if output == 'wide':
        return wide

    if output and output.startswith('custom-columns='):
        ccs = output[15:].split(',')
        if not all(':' in cc for cc in ccs):
            raise ValueError(
                'Invalid custom-columns specification.  Expecting a comma-separated'
                ' list of entries of form TITLE:path'
            )
        return ccs
    if _get_arg('custom-columns='):
        raise ValueError('Missing "-o" parameter (found lone "custom-columns=")')
    return default


def _emit_csv(
    data: Iterable[Iterable[str]], columns: Iterable[str], file=sys.stdout
) -> None:
    """Generate csv.

    `data` is an iterable.  `columns` is a columns specification
    ('title:path').

    `file` is optional, and is `sys.stdout` by default.
    """
    writer = csv.writer(file)
    writer.writerow(path.split(':')[0] for path in columns)
    for row in data:
        writer.writerow(row)


# misc. helpers


def _ensure_uuid(parameter: str) -> None:
    """Ensure parameter is a valid UUID.

    Abort with error code 2 if `parameter` is not a valid UUID.
    """
    if not re.match(
        r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$',
        parameter,
    ):
        _error(
            'Parameter %s is not a valid UUID.  UUIDs should only contains '
            'digits, dashes ("-"), and lower case letters ranging from "a" to "f".',
            parameter,
        )
        sys.exit(2)


def _make_params_from_selectors() -> dict:
    """
    Get selectors from command line and return parameters dictionary
    which could then be passed in a request.
    Currently supports two types of parameters:
    labelSelector and fieldSelector.
    """
    params = {}
    if label_selector := _get_arg('--selector=') or _get_arg('-l='):
        params['labelSelector'] = label_selector
    if field_selector := _get_arg('--field-selector='):
        params['fieldSelector'] = field_selector
    return params
