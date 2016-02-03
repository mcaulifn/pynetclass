#!/usr/bin/env python
'''
This script polls a router for 60 minutes and creates graph a graph for four counters.
'''

from snmp_helper import snmp_get_oid_v3, snmp_extract
import time
import pygal
import yaml


'''
Poll devices
write data
write graph
wait
repeat
'''

TIMEF = '%Y-%m-%d %H:%M:%S'

def poll(device, oid):
    '''
    This function polls a device for the OID passed in.
    The 'device' variable is a tuple of IP and port.
    '''

    snmp_user = ('pysnmp', 'galileo1', 'galileo1')
    data = snmp_extract(snmp_get_oid_v3((device[1],device[2]),snmp_user, oid, auth_proto='sha', encrypt_proto='aes128', display_errors=True))

    return data

def writefile(device, p_time, poll_temp):
    '''
    writes data to file
    '''

    ''' 
    Output format of file:
    2016-02-02 19:40: {ifDescr_fa4: FastEthernet4, ifInOctets_fa4: '12075789', ifInUcastPkts_fa4: '106673',
      ifOutOctets_fa4: '19412573', ifOutUcastPkts_fa4: '137283'}
    2016-02-02 19:44: {ifDescr_fa4: FastEthernet4, ifInOctets_fa4: '12075789', ifInUcastPkts_fa4: '106673',
      ifOutOctets_fa4: '19412573', ifOutUcastPkts_fa4: '137283'}
    '''

    tempdict = {p_time: poll_temp}
    yfile = file('%s.yml' % device[0], 'a')
    yaml.dump(tempdict, yfile)
    yfile.close()

    return None


def writegraph(device, oids, ifname):
    '''
    pull data from files, write to graph
    '''


    '''
    To get keys (x labels):
    for key in data.iterkeys():
        print(key)

    To get values for each key (plot points):
    for value in data.itervalues():
        print(value['inoct'])
    '''


    g1 = {
        'bps': {
            'name': 'In/Out bps',
            'counters': ['ifInOctets_fa4', 'ifOutOctets_fa4']
            },
        'pps': {
            'name': 'In/Out Unicast pps',
            'counters': ['ifInUcastPkts_fa4', 'ifOutUcastPkts_fa4']
            }
        }

    #open file, load data, close file
    yfile = file('%s.yml' % device[0], 'r')
    filedata = yaml.load(yfile)
    yfile.close()

    poll_times = []
    time_labels = []
    for key in sorted(filedata.iterkeys()):
        poll_times.append(key)
        time_labels.append(time.strftime(TIMEF,time.gmtime(key)))

    #If the number of poll times is less than 2, don't make a graph
    if len(poll_times) < 2:
       return None

    for graph in g1.iterkeys():
        line_chart = pygal.Line(x_label_rotation=60)
        line_chart.title = '%s for %s on %s' %(g1[graph]['name'], device[0], ifname)
        line_chart.x_labels = time_labels[1:]
        #Each line on the current graph, counter is the OID name
        for counter in g1[graph]['counters']:
            data_temp = []
            for ptime in poll_times:
                data_temp.append(filedata[ptime][counter])

            #Calculate the difference between each polling
            xdiff = [data_temp[n]-data_temp[n-1] for n in range(1,len(data_temp))]
            tdiff = [poll_times[n]-poll_times[n-1] for n in range(1,len(poll_times))]

            if graph == 'bps':
                for i, each in enumerate(xdiff):
                    xdiff[i] = xdiff[i] * 8

            for i, x in enumerate(xdiff):
                xdiff[i] = xdiff[i] / tdiff[i]

            line_chart.add(counter, xdiff)
            line_chart.render_to_file('%s-%s.svg' % (device[0],graph))

    return None

def main():
    '''
    main function
    '''

    ifDescr_fa4 = '1.3.6.1.2.1.2.2.1.2.5'
    
    #list of OIDs to be graphed
    oids = [
        ('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5'),
        ('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5'),
        ('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
        ('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')
    ]

    device_list = [
        ('rtr1', '50.76.53.27', 7961), 
        ('rtr2', '50.76.53.27', 8061)
    ]

    for x in range(0, 3):
        for each in device_list:
        #iterate through each device, collecting stats for this period and writing graph
            p_time = int(time.time())
            poll_temp = {}
            for name, oid in oids:
                data = poll(each, oid)
                poll_temp[name] = int(data)
            ifname = poll(each, ifDescr_fa4)
            writefile(each, p_time, poll_temp)
            writegraph(each, oids, ifname)

        if x < 12:
            time.sleep(300)
        #if x < 4:
            #time.sleep(60)
    return None

if __name__ == "__main__":
    main()
