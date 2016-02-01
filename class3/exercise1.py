#!/usr/bin/env python
'''
This script polls and stores the uptime and last config change time.
If the config has changed since the last poll, an email is generated.
And more...
'''

from snmp_helper import snmp_get_oid_v3, snmp_extract
import yaml
from time import gmtime, strftime
import email_helper

'''
snmp_get_oid_v3(snmp_device, snmp_user, oid='.1.3.6.1.2.1.1.1.0', auth_proto='sha', encrypt_proto='aes128', display_errors=True):

a_user, auth_key, encrypt_key = snmp_user

snmp_device = ('10.10.10.10', 161)

'''


TIMEF = "%Y-%m-%d %H:%M:%S"

oids = {
        'sysName': '.1.3.6.1.2.1.1.5.0',
        'sysUpTime': '.1.3.6.1.2.1.1.3.0',
        'ccmHistoryRunningLastChanged': '.1.3.6.1.4.1.9.9.43.1.1.1.0'
        }

snmp_user = ('pysnmp', 'galileo1', 'galileo1')

devices = [('rtr1', '50.76.53.27', 7961), ('rtr2', '50.76.53.27', 8061)]

class a_poll:
    '''
    This is for writing the data to a file only
    '''

    def __init__(self, device_name, ip, poll_time, up_time, last_changed):
        self.device_name = device_name
        self.ip = ip
        self.poll_time = poll_time
        self.up_time = up_time
        self.last_changed = last_changed

    def __repr__(self):
        return "%s(device_name=%r, ip=%r, poll_time=%r, up_time=%r, last_changed=%r)" % (
            self.__class__.__name__, self.device_name, self.ip, self.poll_time, self.up_time, self.last_changed)
    


def write(filename, newdata):
    '''
    Write the data to the yaml file
    Accepts the file name and the data to be written
    '''

    yfile = file(filename, 'w')
 
    yaml.dump(a_poll(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4]), yfile)

    yfile.close()
    return

def readfile(device):
    '''
    Attempts to open the existing file
    '''

    try:
        filename = '%s.yaml' % device[0]
        yfile = file(filename, 'r')
        olddata = yaml.load(yfile)
        return olddata

    except IOError:
        print("No polling data exsists, nothing to compare to.")
        

def poll(device):
    '''
    Poll the device and return the new data.
    Accepts 'device' which is a tuple of name, ip, and snmp port.
    '''


    p_time = strftime(TIMEF, gmtime())
    poll_temp = []
    for name, oid in sorted(oids.items()):
        poll_temp.append(snmp_extract(snmp_get_oid_v3((device[1],device[2]),snmp_user, oid, auth_proto='sha', encrypt_proto='aes128', display_errors=True)))
    newdata = [poll_temp[1], device[1], p_time, int(poll_temp[2]), int(poll_temp[0])]
    return newdata



def compare():
    '''
    The compare function attempts to open the existing file. If none exist, new files are created.
    If the file exist, the last_changed value from the file is compared with current data.
    If the values are the same, new data is written and the function ends. If the values are not
    the same, the email function is called.
    '''

    for device in devices:
        try:
            filename = '%s.yaml' % device[0]
            yfile = file(filename, 'r')
            olddata = yaml.load(yfile)
            newdata = poll(device)

            if olddata.last_changed == newdata[4]:
                print("The configuration for %s has not changed." % device[0])
                write(filename, newdata)
            else:
                print("The configuration for %s has changed. Emailing alert." % device[0])
                email(olddata, newdata)
                write(filename, newdata)
        except IOError:
            print("No polling data exsists, nothing to compare to.")
            newdata = poll(device)
            write(filename, newdata)
        ''' Move the call to open here
        if olddata = None:
            newdata = poll(device)
        elif olddata.last_changed:
            '''
    return None

def email(olddata, newdata):
    '''
    email function to send an alert
    '''

    
    recipient = 'mcaulifn@outlook.com'
    subject = 'Configuration Changed for %s' % newdata[0]
    message = ''' 

A configuration change was detected. See event details below:

Device name: %s
IP: %s
Change detected at: %s UTC
Last poll: %s UTC

''' % (newdata[0], newdata[1], newdata[2], olddata.poll_time)

    sender = 'mcaulifn@outlook.com' 

    email_helper.send_mail(recipient, subject, message, sender)

    return None


def main():
    '''
    run the compare function?
    '''
    compare()



if __name__ == "__main__":
    main()

