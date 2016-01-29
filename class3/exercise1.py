#!/usr/bin/env python
'''
This script polls and stores the uptime and last config change time.
If the config has changed since the last poll, an email is generated.
And more...
'''

from snmp_helper import snmp_get_oid_v3, snmp_extract
import yaml
from time import gmtime, strftime

'''
snmp_get_oid_v3(snmp_device, snmp_user, oid='.1.3.6.1.2.1.1.1.0', auth_proto='sha', encrypt_proto='aes128', display_errors=True):

a_user, auth_key, encrypt_key = snmp_user

snmp_device = ('10.10.10.10', 161)

'''

'''
Thoughts: poll uptime, poll last change, compare to last entry in file, write new entry, send email if necessary
'''

TIMEF = "%Y-%m-%d %H:%M:%S"

oids = {
        'sysName': '.1.3.6.1.2.1.1.5.0',
        'sysUpTime': '.1.3.6.1.2.1.1.3.0',
        'ccmHistoryRunningLastChanged': '.1.3.6.1.4.1.9.9.43.1.1.1.0'
        }

snmp_user = ('pysnmp', 'galileo1', 'galileo1')

devices = [('50.76.53.27', 7961), ('50.76.53.27', 8061)]

class a_poll:
    def __init__(self, device_name, ip, poll_time, up_time, last_changed):
        self.device_name = device_name
        self.ip = ip
        self.poll_time = poll_time
        self.up_time = up_time
        self.last_changed = last_changed

    def __repr__(self):
        return "%s(device_name=%r, ip=%r, poll_time=%r, up_time=%r, last_changed=%r)" % (
            self.__class__.__name__, self.device_name, self.ip, self.poll_time, self.up_time, self.last_changed)

def poll():
    '''
    the polling function...
    '''

    yfile = file('polling.yaml', 'a')

    for device in devices:
        p_time = strftime(TIMEF, gmtime())
        poll_temp = []
        for name, oid in sorted(oids.items()):
            poll_temp.append(snmp_extract(snmp_get_oid_v3(device, snmp_user, oid, auth_proto='sha', encrypt_proto='aes128', display_errors=True)))
        yaml.dump(a_poll(poll_temp[1], device[0], p_time, int(poll_temp[2]), int(poll_temp[0])), yfile)

    yfile.close()



def compare():
    yfile = file('polling.yaml', 'r')

    print(yaml.load(yfile))
    pass


def email():
    pass


def main():
    poll()
    compare()



if __name__ == "__main__":
    main()

