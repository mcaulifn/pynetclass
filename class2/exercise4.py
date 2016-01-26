#!/usr/bin/env python
'''SNMP get for sysName and sysDesc'''

from snmp_helper import snmp_get_oid, snmp_extract

class Router(object):
    '''
    creates a router object that has the community and port information
    '''
    #def __init__(self, ip, community, PORT=161):
    def __init__(self, a_dev):
        #self.ip = ip
        #self.community = community
        #self.PORT = PORT
        self.a_dev = a_dev


    def snmp_get_oid_v1(self, oid):
        '''Calls snmp_get_oid and snmp_extract from snmp_helper'''

        output = snmp_get_oid(self.a_dev, oid)
        return snmp_extract(output)


def main():
    """main function"""

    devices = [('50.76.53.27', 'galileo', 7961), ('50.76.53.27', 'galileo', 8061)]
    oids = ['.1.3.6.1.2.1.1.5.0', '.1.3.6.1.2.1.1.1.0']

    for each in devices:
        rtr = Router(each)
        for oid in oids:
            print(rtr.snmp_get_oid_v1(oid))


if __name__ == "__main__":
    main()
