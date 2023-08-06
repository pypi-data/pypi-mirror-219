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

"""opentf-ctl config module"""

from typing import Any, Dict, List, NoReturn, Optional, Tuple

import os
import sys

from importlib.metadata import version

import yaml

from opentf.tools.ctlcommons import _is_command, _get_arg, _error, _ensure_options


########################################################################

# pylint: disable=broad-except

CONFIG = {}
HEADERS = {}


########################################################################
# Help messages

CONFIG_HELP = '''Modify opentfconfig files using subcommands like "opentf-ctl config use-context my-context"

 The following rules are used to find the configuration file to use:

 1.  If the --opentfconfig flag is set, then that file is loaded.
 2.  If $OPENTF_CONFIG environment variable is set, then it is used as a file path and that file is loaded.
 3.  Otherwise, ${HOME}/.opentf/config is used.

Available Commands:
  generate             Generate a configuration file from user inputs
  use-context          Set the current-context in an opentfconfig file
  set-context          Set a context entry in opentfconfig
  set-orchestrator     Set an orchestrator entry in opentfconfig
  set-credentials      Set a user entry in opentfconfig
  delete-context       Delete a context entry from the opentfconfig
  delete-orchestrator  Delete an orchestrator entry from the opentfconfig
  delete-credentials   Delete a user entry from the opentfconfig
  view                 Display current configuration

Usage:
  opentf-ctl config <command> [options]

Use "opentf-ctl config <command> --help" for more information about a given command.
Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_GENERATE_HELP = '''Generate a configuration file from user inputs and streams it in stdout

Options:
  --name='': Nickname that will be used for context and orchestrator registration (default: default)
  --orchestrator-server='': Address of the opentf orchestrator
  --orchestrator-receptionist-port='': Port of the receptionist service (integer)  (default: 7774)
  --orchestrator-observer-port='': Port of the observer service (integer) (default: 7775)
  --orchestrator-eventbus-port='': Port of the eventbus service (integer) (default: 38368)
  --orchestrator-killswitch-port='': Port of the killswitch service (integer) (default: 7776)
  --orchestrator-agentchannel-port='': Port of the agentchannel service (integer) (default: 24368)
  --orchestrator-qualitygate-port='': Port of the qualitygate service (integer) (default: 12312)
  --insecure-skip-tls-verify=false|true: Skip TLS verification (default: false)
  --token=": User's token to sign communications with orchestrator

Usage:
  opentf-ctl config generate [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_USE_CONTEXT_HELP = '''Select the current context to use

Examples:
  # Use the context for the prod orchestrator
  opentf-ctl config use-context prod

Usage:
  opentf-ctl config use-context CONTEXT_NAME

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_SET_CONTEXT_HELP = '''Sets a context entry in opentfconfig

 Specifying a name that already exists will merge new fields on top of existing values for those fields.

Examples:
  # Set the user field on the foo context entry without touching other values
  opentf-ctl config set-context foo --user=admin

Options:
      --current=false: Modify the current context

Usage:
  opentf-ctl config set-context [NAME | --current] [--orchestrator=orchestrator_nickname] [--user=user_nickname] [--namespace=namespace] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_SET_ORCHESTRATOR_HELP = '''Sets an orchestrator entry in opentfconfig

 Specifying a name that already exists will merge new fields on top of existing values.

Examples:
  # Set only the server field of the e2e orchestrator entry without touching other values.
  opentf-ctl config set-orchestrator e2e --server=https://1.2.3.4

  # Set the port and prefix of the e2e's eventbus service without touching other values.
  opentf-ctl config set-orchestrator e2e --eventbus-port=8888 --eventbus-prefix=e2eeventbus

Options:
  --insecure-skip-tls-verify=false|true: Skip TLS verification
  --server='': Address of the opentf orchestrator
  --SERVICE-force-base-url=false|true: Override link URLs
  --SERVICE-port='': Port of the service (integer)
  --SERVICE-prefix='': Prefix for the service (string)

  where SERVICE is one of 'receptionist', 'observer', 'eventbus', 'killswitch', 'agentchannel', or 'qualitygate'.

Usage:
  opentf-ctl config set-orchestrator NAME [--insecure-skip-tls-verify=true] [--server=server] [--SERVICE-port=port] [--SERVICE-prefix=prefix] [--SERVICE-force-base-url=boolean] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_SET_CREDENTIALS_HELP = '''Sets a user entry in opentfconfig

 Specifying a name that already exists will merge new fields on top of existing values.

  Bearer token flags:
    --token=bearer_token

Examples:
  # Set token auth for the "admin" entry
  opentf-ctl config config set-credentials cluster-admin --token=token

Options:
      --token='': Bearer token
      --step-depth=<n>: Default step depth for workflow operations
      --job-depth=<n>: Default job depth for workflow operations
      --max-command-length=<n>: Default length limit of running commands

Usage:
  kubectl config set-credentials NAME [--token=bearer_token] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_DELETE_CONTEXT_HELP = '''Delete the specified context from the opentfconfig

Examples:
  # Delete the context for the demo orchestrator
  opentf-ctl config delete-context demo

Usage:
  opentf-ctl config delete-context NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_DELETE_ORCHESTRATOR_HELP = '''Delete the specified orchestrator from the opentfconfig

Usage:
  opentf-ctl config delete-orchestrator NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_DELETE_CREDENTIALS_HELP = '''Delete the specified user from the opentfconfig

Examples:
  # Delete the admin user
  opentf-ctl config delete-credentials admin

Usage:
  opentf-ctl config delete-credentials NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

CONFIG_VIEW_HELP = '''Display current configuration

The displayed configuration will be in order of priority the one pointed by
  - the --opentfconfig= argument value
  - the environment variable OPENTF_CONFIG
  - the current user configuration located at ~/.opentf/config

Usage:
  opentf-ctl config view [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################


def _fatal_cannot_modify_configuration_file(filename: str, err) -> NoReturn:
    _error('Could not modify configuration file %s: %s.', filename, err)
    sys.exit(2)


def read_configuration() -> None:
    """Read configuration file.

    Configuration file is by default ~/.opentf/config, but this can be
    overridden by specifying the OPENTF_CONFIG environment variable or
    by using the `--opentfconfig=' command line parameter.

    Configuration file is a kubeconfig-like file, in YAML:

    ```yaml
    apiVersion: opentestfactory.org/v1alpha1
    kind: CtlConfig
    current-context: default
    contexts:
    - context:
        orchestrator: default
        user: default
      name: default
    orchestrators:
    - name: default
      orchestrator:
        insecure-skip-tls-verify: true
        server: http://localhost
        services:
          observer:
            port: 1234
            prefix: yada
            force-base-url: true
    users:
    - name: default
      user:
        token: ey...
        job-depth: n
        step-depth: n
        max-command-length: n
    ```

    Optional command-line options:

    --token=''
    --user=''
    --orchestrator=''
    --context=''
    --insecure-skip-tls-verify=false|true
    --opentfconfig=''
    """

    def _get(kind: str, name: str) -> Optional[Dict[str, Any]]:
        for item in config[f'{kind}s']:
            if item['name'] == name:
                return item[kind]
        return None

    def _safe_get(kind: str, name: str) -> Dict[str, Any]:
        what = _get(kind, name)
        if what is None:
            _error('%s %s is not available in configuration.', kind.title(), repr(name))
            _error('(Using the %s configuration file.)', repr(_))
            sys.exit(2)
        return what

    def _safe_get_arg(option: str) -> Optional[str]:
        what = _get_arg(option)
        if what == '':
            _error('The %s option specifies an empty value.', option)
            sys.exit(2)
        return what

    _, config = _read_opentfconfig()

    context_name = _safe_get_arg('--context=') or config.get('current-context')
    if not context_name:
        _error(
            'Empty or undefined current context.  Please specify a current context in your configuration file or use the --context= command line option.'
        )
        sys.exit(2)
    context = _safe_get('context', context_name)

    orchestrator_name = _safe_get_arg('--orchestrator=') or context.get('orchestrator')
    if not orchestrator_name:
        _error(
            'No orchestrator defined in the context.  Please specify an orchestrator in your configuration file or use the --orchestrator= command line option.'
        )
        sys.exit(2)
    orchestrator = _safe_get('orchestrator', orchestrator_name)

    user_name = _safe_get_arg('--user=') or context.get('user')
    if not user_name:
        _error(
            'No user defined in the context.  Please specify a user in your configuration file or use the --user= command line option.'
        )
        sys.exit(2)
    user = _safe_get('user', user_name)

    try:
        CONFIG['token'] = (
            _get_arg('--token=') or os.environ.get('OPENTF_TOKEN') or user['token']
        )
        CONFIG['job-depth'] = user.get('job-depth')
        CONFIG['step-depth'] = user.get('step-depth')
        CONFIG['max-command-length'] = user.get('max-command-length')
        CONFIG['orchestrator'] = orchestrator
        CONFIG['orchestrator']['insecure-skip-tls-verify'] = CONFIG['orchestrator'].get(
            'insecure-skip-tls-verify', False
        ) or (_get_arg('--insecure-skip-tls-verify=') == 'true')
        CONFIG['namespace'] = context.get('namespace')
        HEADERS['Authorization'] = 'Bearer ' + CONFIG['token']
    except Exception as err:
        _error('Could not read configuration: %s.', err)
        sys.exit(2)


########################################################################
# Helpers


def _get_port(service: str, default: int) -> int:
    port = (
        _get_arg(f'--orchestrator-{service}-port=')
        or input(f'Please specify the {service} port ({default}): ').strip()
        or default
    )
    try:
        return int(port)
    except ValueError as err:
        _error('Not a valid port value: %s', err)
        sys.exit(2)


def _get_prefix(service: str, default: str) -> str:
    prefix = (
        _get_arg(f'--orchestrator-{service}-prefix=')
        or input(f'Please specify the {service} prefix ({default}): ').strip()
        or default
    )
    return prefix


########################################################################
# Commands


## config commands


def config_cmd() -> None:
    """Interact with opentf-config.

    Possible sub commands are
        generate             Generate configuration file from user inputs
        set-context          Set a context entry in the opentf-config
        set-orchestrator     Set an orchestrator entry in the opentf-config
        set-credentials      Set a user entry in the opentf-config
        delete-context       Unset a context entry in the opentf-config
        delete-orchestrator  Unset an orchestrator entry in the opentf-config
        delete-credentials   Unset a user entry in the opentf-config
        view                 Display current opentf-config
    """
    if _is_command('config generate', sys.argv):
        generate_config()
    elif _is_command('config use-context _', sys.argv):
        use_context(sys.argv[3])
    elif _is_command('config set-context _', sys.argv):
        set_context(sys.argv[3])
    elif _is_command('config set-orchestrator _', sys.argv):
        set_orchestrator(sys.argv[3])
    elif _is_command('config set-credentials _', sys.argv):
        set_credentials(sys.argv[3])
    elif _is_command('config delete-context _', sys.argv):
        delete_context(sys.argv[3])
    elif _is_command('config delete-orchestrator _', sys.argv):
        delete_orchestrator(sys.argv[3])
    elif _is_command('config delete-credentials _', sys.argv):
        delete_credentials(sys.argv[3])
    elif _is_command('config view', sys.argv):
        _ensure_options(sys.argv[3:])
        view_config()
    elif len(sys.argv) == 2:
        print_config_help(sys.argv)
    else:
        _error(
            'Unknown subcommand.  Use "opentf-ctl config --help" to list known subcommands.'
        )
        sys.exit(1)


def _write_opentfconfig(conf_filename: str, config: Dict[str, Any]) -> None:
    with open(conf_filename, 'w', encoding='utf-8') as conffile:
        yaml.safe_dump(config, conffile)


def _read_opentfconfig() -> Tuple[str, Dict[str, Any]]:
    conf_filename = (
        _get_arg('--opentfconfig=')
        or os.environ.get('OPENTF_CONFIG')
        or os.path.expanduser('~/.opentf/config')
    )
    try:
        with open(conf_filename, 'r', encoding='utf-8') as conffile:
            config = yaml.safe_load(conffile)
    except Exception as err:
        _error('Could not read configuration file %s: %s.', conf_filename, err)
        _error(
            'You may generate a configuration file using the "opentf-ctl config generate" subcommand.  Use "opentf-ctl config generate --help" for usage.'
        )
        sys.exit(2)
    return conf_filename, config


def _ensure_name_exists(name: str, label: str, config, src) -> None:
    names = [item['name'] for item in config[f'{label}s']]
    if name not in names:
        _error(
            '%s %s does not exist in configuration file %s.',
            label.title(),
            repr(name),
            repr(src),
        )
        _error('Available %ss: %s.', label, ','.join(names))
        sys.exit(2)


# Contexts


def use_context(name: str) -> None:
    """Change current context."""
    conf_filename, config = _read_opentfconfig()
    try:
        _ensure_name_exists(name, 'context', config, conf_filename)
        config['current-context'] = name
        _write_opentfconfig(conf_filename, config)
    except Exception as err:
        _fatal_cannot_modify_configuration_file(conf_filename, err)


def set_context(name: str) -> None:
    """Create or update context."""
    conf_filename, config = _read_opentfconfig()
    try:
        if name == '--current':
            if 'current-context' not in config:
                _error(
                    'No current context defined in configuration file %s.',
                    conf_filename,
                )
                _error(
                    'You can use the "opentf-ctl config use-context" subcommand to define a default context.'
                )
                sys.exit(2)
            name = config['current-context']
        contexts = {item['name']: item for item in config['contexts']}
        if name not in contexts:
            entry = {'context': {}, 'name': name}
            contexts[name] = entry
            config['contexts'].append(entry)
            msg = f'Context "{name}" created in {conf_filename}.'
        else:
            msg = f'Context "{name}" modified in {conf_filename}.'
        if orchestrator := _get_arg('--orchestrator='):
            _ensure_name_exists(orchestrator, 'orchestrator', config, conf_filename)
            contexts[name]['context']['orchestrator'] = orchestrator
        if user := _get_arg('--user='):
            _ensure_name_exists(user, 'user', config, conf_filename)
            contexts[name]['context']['user'] = user
        if namespace := _get_arg('--namespace='):
            contexts[name]['context']['namespace'] = namespace
        _write_opentfconfig(conf_filename, config)
        print(msg)
    except Exception as err:
        _fatal_cannot_modify_configuration_file(conf_filename, err)


def delete_context(name: str) -> None:
    """Delete context."""
    conf_filename, config = _read_opentfconfig()
    try:
        _ensure_name_exists(name, 'context', config, conf_filename)
        config['contexts'] = [
            item for item in config['contexts'] if item['name'] != name
        ]
        _write_opentfconfig(conf_filename, config)
        print(f'Deleted context "{name}" from {conf_filename}.')
    except Exception as err:
        _fatal_cannot_modify_configuration_file(conf_filename, err)


# Credentials


def set_credentials(name: str) -> None:
    """Create or update user entry."""
    conf_filename, config = _read_opentfconfig()
    try:
        users = {item['name']: item for item in config['users']}
        if name not in users:
            entry = {'user': {}, 'name': name}
            users[name] = entry
            config['users'].append(entry)
        if token := _get_arg('--token='):
            users[name]['user']['token'] = token
        if step_depth := _get_arg('--step-depth='):
            try:
                step_depth = int(step_depth)
                users[name]['user']['step-depth'] = int(step_depth)
            except ValueError:
                _fatal_cannot_modify_configuration_file(
                    conf_filename, 'step depth must be an integer'
                )
        if job_depth := _get_arg('--job-depth='):
            try:
                job_depth = int(job_depth)
                users[name]['user']['job-depth'] = int(job_depth)
            except ValueError:
                _fatal_cannot_modify_configuration_file(
                    conf_filename, 'job depth must be an integer'
                )
        if max_command_length := _get_arg('--max-command-length='):
            try:
                max_command_length = int(max_command_length)
                users[name]['user']['max-command-length'] = int(max_command_length)
            except ValueError:
                _fatal_cannot_modify_configuration_file(
                    conf_filename, 'max command length must be an integer'
                )
        _write_opentfconfig(conf_filename, config)
        print(f'User "{name}" set in {conf_filename}.')
    except Exception as err:
        _fatal_cannot_modify_configuration_file(conf_filename, err)


def delete_credentials(name: str) -> None:
    """Delete user."""
    conf_filename, config = _read_opentfconfig()
    try:
        _ensure_name_exists(name, 'user', config, conf_filename)
        config['users'] = [item for item in config['users'] if item['name'] != name]
        _write_opentfconfig(conf_filename, config)
        print(f'Deleted user "{name}" from {conf_filename}.')
    except Exception as err:
        _fatal_cannot_modify_configuration_file(conf_filename, err)


# Orchestrators


def set_orchestrator(name: str) -> None:
    """Create or update orchestrator.

    Create or update orchestrator definition using the following
    command-line parameters:

    - --insecure-skip-tls-verify=
    - --server=

    And for each possible service:

    - --{sercice}-port=
    - --{service}-prefix=
    - --{service}-force-base-url=

    # Required parameter

    - name: a string
    """
    conf_filename, config = _read_opentfconfig()
    try:
        orchestrators = {item['name']: item for item in config['orchestrators']}
        if name not in orchestrators:
            entry = {'orchestrator': {}, 'name': name}
            orchestrators[name] = entry
            config['orchestrators'].append(entry)
            msg = f'Orchestrator "{name}" created in {conf_filename}.'
        else:
            msg = f'Orchestrator "{name}" modified in {conf_filename}.'

        orchestrator = orchestrators[name]['orchestrator']
        if verify := _get_arg('--insecure-skip-tls-verify='):
            orchestrator['insecure-skip-tls-verify'] = verify.lower() == 'true'
        if server := _get_arg('--server='):
            orchestrator['server'] = server

        ports = {}
        prefixes = {}
        forcebaseurls = {}
        for svc in [
            'receptionist',
            'observer',
            'killswitch',
            'eventbus',
            'agentchannel',
            'qualitygate',
        ]:
            if port := _get_arg(f'--{svc}-port='):
                try:
                    port = int(port)
                except ValueError:
                    _error('%s port must be an integer: %s.', svc.title(), repr(port))
                    sys.exit(2)
                ports[svc] = port
            if prefix := _get_arg(f'--{svc}-prefix='):
                prefixes[svc] = prefix
            if baseurl := _get_arg(f'--{svc}-force-base-url='):
                if baseurl.lower() not in ('true', 'false'):
                    _error(
                        '%s force-base-url must be "true" or "false": %s.',
                        svc.title(),
                        repr(baseurl),
                    )
                    sys.exit(2)
                forcebaseurls[svc] = baseurl.lower() == 'true'
        if ports or prefixes or forcebaseurls:
            if 'ports' in orchestrator:
                # update to new orchestrator definition format
                services = {
                    svc: {'port': value} for svc, value in orchestrator['ports'].items()
                }
                del orchestrator['ports']
            else:
                services = {}
            orchestrator.setdefault('services', services)
            for svc, port in ports.items():
                orchestrator['services'].setdefault(svc, {})['port'] = port
            for svc, prefix in prefixes.items():
                orchestrator['services'].setdefault(svc, {})['prefix'] = prefix
            for svc, fbu in forcebaseurls.items():
                orchestrator['services'].setdefault(svc, {})['force-base-url'] = fbu

        _write_opentfconfig(conf_filename, config)
        print(msg)
    except Exception as err:
        _fatal_cannot_modify_configuration_file(conf_filename, err)


def delete_orchestrator(name: str) -> None:
    """Delete orchestrator."""
    conf_filename, config = _read_opentfconfig()
    try:
        _ensure_name_exists(name, 'orchestrator', config, conf_filename)
        config['orchestrators'] = [
            item for item in config['orchestrators'] if item['name'] != name
        ]
        _write_opentfconfig(conf_filename, config)
        print(f'Deleted orchestrator "{name}" from {conf_filename}.')
    except Exception as err:
        _fatal_cannot_modify_configuration_file(conf_filename, err)


def view_config() -> None:
    """Display currently used configuration file in stdout.

    The configuration is found using, in priority

    - the `--opentfconfig=` argument value
    - the `OPENTF_CONFIG` environment variable
    - the current user configuration located at `~/.opentf/config`

    # Raised exception

    Exits violently with error code 2 if no configuration file is found
    """
    _, config = _read_opentfconfig()
    for user in config['users']:
        if (entry := user.get('user', {})) is not None and entry.get('token'):
            user['user']['token'] = 'REDACTED'
    print(yaml.dump(config))


def generate_config() -> None:
    """
    Generate a config file from user input

    Configuration file is a kubeconfig-like file, in YAML:

    ```yaml
    apiVersion: opentestfactory.org/v1alpha1
    kind: CtlConfig
    current-context: default
    contexts:
    - context:
        orchestrator: default
        user: default
      name: default
    orchestrators:
    - name: default
      orchestrator:
        insecure-skip-tls-verify: true
        server: http://localhost
        services:
          receptionist:
            port: 7774
          observer:
            port: 7775
          killswitch:
            port: 7776
          eventbus:
            port: 38368
    users:
    - name: default
      user:
        token: ey...
    ```

    Optional command-line options:

    --name="
    --orchestrator-server=''
    --orchestrator-receptionist-port=''
    --orchestrator-observer-port=''
    --orchestrator-eventbus-port=''
    --orchestrator-killswitch-port=''
    --orchestrator-agentchannel-port=''
    --orchestrator-qualitygate-port=''
    --insecure-skip-tls-verify=false|true
    --token="
    """

    generated_conf: Dict[str, Any] = {
        'apiVersion': 'opentestfactory.org/v1alpha1',
        'kind': 'CtlConfig',
    }

    name = (
        _get_arg('--name=')
        or (input('Please specify a nickname for the orchestrator (default): ').strip())
        or 'default'
    )

    server = _get_arg('--orchestrator-server=')
    while not server:
        server = input('Please specify the orchestrator server: ').strip()

    receptionist_port = _get_port('receptionist', 7774)
    eventbus_port = _get_port('eventbus', 38368)
    observer_port = _get_port('observer', 7775)
    killswitch_port = _get_port('killswitch', 7776)
    agentchannel_port = _get_port('agentchannel', 24368)
    qualitygate_port = _get_port('qualitygate', 12312)

    skip_tls_verify = (
        _get_arg('--insecure-skip-tls-verify=')
        or (input('Skip TLS verification (false): ').strip())
        or False
    )
    if isinstance(skip_tls_verify, str):
        verify = skip_tls_verify.lower().strip()
        if verify == 'true':
            skip_tls_verify = True
        elif verify == 'false':
            skip_tls_verify = False
        else:
            _error(
                'Not a valid insecure-skip-tls-verify flag: %s (was expecting true or false).',
                skip_tls_verify,
            )
            sys.exit(2)

    token = _get_arg('--token=')
    while not token:
        token = input('Please specify the token: ').strip()

    contexts = [{'name': name, 'context': {'orchestrator': name, 'user': name}}]

    generated_conf['contexts'] = contexts
    generated_conf['current-context'] = name

    orchestrators = [
        {
            'name': name,
            'orchestrator': {
                'insecure-skip-tls-verify': skip_tls_verify,
                'server': server,
                'services': {
                    'receptionist': {'port': receptionist_port},
                    'observer': {'port': observer_port},
                    'eventbus': {'port': eventbus_port},
                    'killswitch': {'port': killswitch_port},
                    'agentchannel': {'port': agentchannel_port},
                    'qualitygate': {'port': qualitygate_port},
                },
            },
        }
    ]

    generated_conf['orchestrators'] = orchestrators

    users = [{'name': name, 'user': {'token': token}}]

    generated_conf['users'] = users

    print('#')
    print('# Generated opentfconfig')
    print('# (generated by opentf-ctl version %s)' % version('opentf-tools'))
    print('#')

    print(yaml.dump(generated_conf))


def print_config_help(args: List[str]) -> None:
    """Display config help."""
    if _is_command('config generate', args):
        print(CONFIG_GENERATE_HELP)
    elif _is_command('config use-context', args):
        print(CONFIG_USE_CONTEXT_HELP)
    elif _is_command('config set-context', args):
        print(CONFIG_SET_CONTEXT_HELP)
    elif _is_command('config set-orchestrator', args):
        print(CONFIG_SET_ORCHESTRATOR_HELP)
    elif _is_command('config set-credentials', args):
        print(CONFIG_SET_CREDENTIALS_HELP)
    elif _is_command('config delete-context', args):
        print(CONFIG_DELETE_CONTEXT_HELP)
    elif _is_command('config delete-orchestrator', args):
        print(CONFIG_DELETE_ORCHESTRATOR_HELP)
    elif _is_command('config delete-credentials', args):
        print(CONFIG_DELETE_CREDENTIALS_HELP)
    elif _is_command('config view', args):
        print(CONFIG_VIEW_HELP)
    elif _is_command('config', args):
        print(CONFIG_HELP)
    else:
        _error('Unknown config command.  Use --help to list known commands.')
        sys.exit(1)
