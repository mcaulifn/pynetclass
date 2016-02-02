#!/usr/bin/env python
'''
This script polls a router for 60 minutes and creates graph a graph for four counters.
'''

from snmp_helper import snmp_get_oid_v3, snmp_extract
from time import gmtime, strftime, timedelta, sleep
from datetime import datetime
import pygal
import yaml


'''
Poll devices
write data
write graph
wait
repeat
'''

TIMEF = '%Y-%m-%d %H:%M'

def poll(device, oid):
    '''
	This function polls a device for the OID passed in.
	The 'device' variable is a tuple of IP and port.
	'''
	
	
	
	data = snmp_extract(snmp_get_oid_v3((device[1],device[2]),snmp_user, oid, auth_proto='sha', encrypt_proto='aes128', display_errors=True))))

	return data

def writefile():
    '''
    writes data to file
    '''

    ''' 
	Output format of file:
    2016-01-30 14:55:
        inoct: 2
        outoct: 55
        inpks: 4
        outpks: 2
    2016-02-01 20:55:
        inoct: 2
        outoct: 55
        inpks: 4
        outpks: 20
    '''
	
	yfile = file('%s.yml' % device_name +'_' + if_name, 'a')
	


    return None


def writegraph():
    '''
    pull data from files, write to graph
    '''


    '''
    To get keys (x labels):
	for key in data[0].iterkeys():
        print(key)

	To get values for each key (plot points):
	for value in data[0].itervalues():
        print(value['inoct'])
    '''

    '''
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    line_chart.render()
    '''

    line_chart = pygal.line(x_label_rotation=90)
    line_chart.title = 'In/Out Bits - %s' % device_name
    line_chart.x_labels = poll_times #this is a list passed in
    line_chart.add('In bps', inOctets)
    line_chart.add('Out bps', outOctets)
    line_charte.render_to_file('%s.svg' % device_name)

    return None

def main():
    '''
    main function
    '''
    '''
	('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5')
    ('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5')
    ('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5')
    ('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
    ('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')
	'''

	oids = [
	    ('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5')
        ('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5')
        ('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5')
        ('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
        ('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5'
	]
    for x in range(0, 12):
        for each in device_list:
		#iterate through each device, collecting stats for this period
		    p_time = strftime(TIMEF, gmtime())

			for name, oid in sorted(oids):
			    data = poll(each, oid)
            writefile()
            writegraph()
        
		sleep(300)


if __name__ == "__main__":
    main()
