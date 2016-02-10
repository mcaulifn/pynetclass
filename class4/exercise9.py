#!/usr/bin/env python
''' This module uses netmiko to run commands.'''

from getpass import getpass
import multiprocessing
import sys
import netmiko


def display(results):
    '''prints output from all devices'''

    print('Sucessful:')
    for each in results:
        for rtr, value in each.iteritems():
            success, result = value
            if success:
                print(rtr)
                print result

    print('Failed:')
    for each in results:
        for rtr, value in each.iteritems():
            success, result = value
            if not success:
                print(rtr)


def mp_run_cmd(device, cmd, queue):
    '''Runs commands in a multiprocessing environment'''

    data = {}

    rtrid = device['ip'] + ':' +str(device['port'])
    cmd = cmd.strip()

    try:
        conn = netmiko.ConnectHandler(**device)

        output = conn.send_command(cmd)

        conn.disconnect()

        data[rtrid] = (True, output)
        queue.put(data)

    except:
        e = sys.exc_info()[0]
        data[rtrid] = (False, e)
        queue.put(data)
        return None





def main():
    '''main'''

    rtr1 = {
        'device_type': 'cisco_ios',
        'ip': '50.76.53.27',
        'port': 22,
        'username': 'pyclass',
        'password': getpass(),
        }

    rtr2 = {
        'device_type': 'cisco_ios',
        'ip': '50.76.53.27',
        'port': 8022,
        'username': 'pyclass',
        'password': getpass(),
        }

    srx = {
        'device_type': 'juniper',
        'ip': '50.76.53.27',
        'port': 9822,
        'username': 'pyclass',
        'password': getpass(),
        }

    routerlist = [rtr1, rtr2, srx]
    cmd = 'show arp'

    mpqueue = multiprocessing.Queue()
    procs = []

    for each in routerlist:
        p = multiprocessing.Process(target=mp_run_cmd, args=(each, cmd, mpqueue))
        procs.append(p)
        p.start()

    for proc in procs:
        proc.join()

    results = []
    for proc in procs:
        results.append(mpqueue.get())

    print(results)

if __name__ == "__main__":
    main()
