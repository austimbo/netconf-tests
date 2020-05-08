#!/usr/bin/env python

"""
    Netconf python example by yang-explorer (https://github.com/CiscoDevNet/yang-explorer)

    Installing python dependencies:
    > pip install lxml ncclient

    Running script: (save as example.py)
    > python example.py -a 192.168.0.122 -u netconf -p cisco --port 830
#Testing github. THis should appear in the fix a bug branch!
"""

import lxml.etree as ET
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError

payload = """
<create-subscription xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0"> 
     <stream>snmpevents</stream> 
   </create-subscription>
"""

payload_int="""
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
   <edit-config>
      <target>
         <running />
      </target>
      <config>
         <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
               <name>GigabitEthernet2</name>
               <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
               <enabled>true</enabled>
            </interface>
         </interfaces>
      </config>
   </edit-config>
</rpc>
"""

interfaces_payload="""
<rpc message-id="101” xmlns=”urn:ietf:param <get>
      <filter type="subtree">
         <top xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces";
            <interfaces>
            </interfaces>
          </top>
       </filter>
   </get>
</rpc>
"""


if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-a', '--host', type=str, required=False, default='192.168.0.122',
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=False, default='netconf',
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required=False, default='cisco',
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'csr'}) as m:

            # execute netconf operation
            #response = m.dispatch(ET.fromstring(payload_int)).xml
            #response = m.get_config('running').xml
            #data = ET.fromstring(response)

            yang_schemas=['ietf-ip','ietf-interfaces','ietf-yang-types','ietf-inet-types']


            for zz in yang_schemas:
                schema = m.get_schema(zz)
                root = ET.fromstring((schema.xml).encode('ascii')) #.encode ascii is required otherwise we get an error
                #print(schema.xml)  # Test Code Only
                #Now we need to extract the yang and write it to a file.
                yang_text = list(root)[0].text
                with open(zz + ".yang","w+") as f:
                    f.write(yang_text)
