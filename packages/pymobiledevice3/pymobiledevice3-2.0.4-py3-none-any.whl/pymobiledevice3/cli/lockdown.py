import logging
import plistlib

import click

from pymobiledevice3.cli.cli_common import Command, CommandWithoutAutopair, print_json
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.heartbeat import HeartbeatService

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """ apps cli """
    pass


@cli.group('lockdown')
def lockdown_group():
    """ lockdown options """
    pass


@lockdown_group.command('recovery', cls=Command)
def lockdown_recovery(lockdown: LockdownClient):
    """ enter recovery """
    print_json(lockdown.enter_recovery())


@lockdown_group.command('service', cls=Command)
@click.argument('service_name')
def lockdown_service(lockdown: LockdownClient, service_name):
    """ send-receive raw service messages """
    lockdown.start_service(service_name).shell()


@lockdown_group.command('info', cls=Command)
@click.option('-a', '--all', is_flag=True, help='include all domain information')
@click.option('--color/--no-color', default=True)
def lockdown_info(lockdown: LockdownClient, all, color):
    """ query all lockdown values """
    print_json(lockdown.all_domains if all else lockdown.all_values, colored=color)


@lockdown_group.command('get', cls=Command)
@click.argument('domain', required=False)
@click.argument('key', required=False)
@click.option('--color/--no-color', default=True)
def lockdown_get(lockdown: LockdownClient, domain, key, color):
    """ query lockdown values by their domain and key names """
    print_json(lockdown.get_value(domain=domain, key=key), colored=color)


@lockdown_group.command('set', cls=Command)
@click.argument('value')
@click.argument('domain', required=False)
@click.argument('key', required=False)
@click.option('--color/--no-color', default=True)
def lockdown_set(lockdown: LockdownClient, value, domain, key, color):
    """ set a lockdown value using python's eval() """
    print_json(lockdown.set_value(value=eval(value), domain=domain, key=key), colored=color)


@lockdown_group.command('remove', cls=Command)
@click.argument('domain')
@click.argument('key')
@click.option('--color/--no-color', default=True)
def lockdown_remove(lockdown: LockdownClient, domain, key, color):
    """ remove a domain/key pair """
    print_json(lockdown.remove_value(domain=domain, key=key), colored=color)


@lockdown_group.command('unpair', cls=CommandWithoutAutopair)
@click.argument('host_id', required=False)
def lockdown_unpair(lockdown: LockdownClient, host_id: str = None):
    """ unpair from connected device """
    lockdown.unpair(host_id=host_id)


@lockdown_group.command('pair', cls=CommandWithoutAutopair)
def lockdown_pair(lockdown: LockdownClient):
    """ pair device """
    lockdown.pair()


@lockdown_group.command('save-pair-record', cls=CommandWithoutAutopair)
@click.argument('output', type=click.File('wb'))
def lockdown_save_pair_record(lockdown: LockdownClient, output):
    """ save pair record to specified location """
    if lockdown.pair_record is None:
        logger.error('no pairing record was found')
        return
    plistlib.dump(lockdown.pair_record, output)


@lockdown_group.command('date', cls=Command)
def lockdown_date(lockdown: LockdownClient):
    """ get device date """
    print(lockdown.date)


@lockdown_group.command('heartbeat', cls=Command)
def lockdown_heartbeat(lockdown: LockdownClient):
    """ start heartbeat service """
    HeartbeatService(lockdown).start()


@lockdown_group.command('language', cls=Command)
def lockdown_language(lockdown: LockdownClient):
    """ get current language settings """
    print(f'{lockdown.language} {lockdown.locale}')


@lockdown_group.command('device-name', cls=Command)
@click.argument('new_name', required=False)
def lockdown_device_name(lockdown: LockdownClient, new_name):
    """ get/set current device name """
    if new_name:
        lockdown.set_value(new_name, key='DeviceName')
    else:
        print(f'{lockdown.get_value(key="DeviceName")}')


@lockdown_group.command('wifi-connections', cls=Command)
@click.argument('state', type=click.Choice(['on', 'off']), required=False)
def lockdown_wifi_connections(lockdown: LockdownClient, state):
    """ get/set wifi connections state """
    if not state:
        # show current state
        print_json(lockdown.get_value(domain='com.apple.mobile.wireless_lockdown'))
    else:
        # enable/disable
        lockdown.enable_wifi_connections = state == 'on'
