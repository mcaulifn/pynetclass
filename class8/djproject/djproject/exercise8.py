#/usr/bin/env python
'''run show version on each device in db'''

from __future__ import print_function
from datetime import datetime
from multiprocessing import Process, Queue
import django
from net_system.models import NetworkDevice
import netmiko

def run_command_thread(device, cmd, q):
    '''run command in a process env'''

    output_temp = {}
    output = '*' * 80 + '\n'
    conn = netmiko.ConnectHandler(device_type=device.device_type, ip=device.ip_address,
                                  username=device.credentials.username, password=device.credentials.password,
                                  port=device.port)
    output += conn.send_command(cmd)
    output_temp[device.device_name] = output
    q.put(output_temp)
    
    conn.disconnect()

def main():
    '''main'''

    django.setup()

    command = 'show version'
    output_queue = Queue(maxsize=20)

    starttime = datetime.now()

    procs = []
    for each in NetworkDevice.objects.all():
        c_proc = Process(target=run_command_thread, args=(each, command, output_queue))
        c_proc.start()
        procs.append(c_proc)

    for each_proc in procs:
        each_proc.join()

    while not output_queue.empty():
        for key,value in output_queue.get().iteritems():
            print(key)
            print(value)

    print("Elapsed time: %s" %str(datetime.now()-starttime))

if __name__ == "__main__":
    main()
