#!/usr/bin/python
# Copyright (c) 2018 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems
from ansible.module_utils.net_tools.nios.api import WapiModule
from ansible.module_utils.net_tools.nios.api import NIOS_DTC_SERVER

DOCUMENTATION = '''
---
module: nios_dtc_server
version_added: "2.8"
author: "Mauricio Teixeira (@badnetmask)"
short_description: Configure Infoblox NIOS DTC server
description:
  - Adds and/or removes instances of DTC server objects from
    Infoblox NIOS servers.  This module manages NIOS C(dtc:server) objects
    using the Infoblox WAPI interface over REST.
requirements:
  - infoblox-client
extends_documentation_fragment: nios
options:
  name:
    description:
      - A name that identifies the DTC server in a pool
    required: true
  host:
    description:
      - Sets the IP address or FQDN of the host
    required: True
  auto_create_host_record:
    description:
      - Enabling this option will auto-create a single read-only A/AAAA/CNAME
        record corresponding to the configured hostname and update it if the
        hostname changes
    default: True
  comment:
    description:
      - Configures a text string comment to be associated with the instance
        of this object. The provided text string will be configured on the
        object instance.
  disable:
    description:
      - Sets whether the DTC Server is disabled or not. When this is set to
        False, the fixed address is enabled.
    default: False
  extattrs:
    description:
      - Allows for the configuration of Extensible Attributes on the
        instance of the object.  This argument accepts a set of key / value
        pairs for configuration.
'''

def main():
    ''' Main entry point for module execution
    '''

    ib_spec = dict(
        name=dict(required=True, ib_req=True),
        host=dict(required=True, ib_req=True),

        comment=dict(),
        disable=dict(type='bool', default=False),
        extattrs=dict(type='dict'),
        # TODO: implement this
        #monitors=dict(type='dict'),
        # TODO: infoblox-client only supports API 2.1, these are 2.7
        #sni_hostname=dict(),
        #auto_create_host_record=dict(type='bool', default=True),
        #use_sni_hostname=dict(type='bool', default=False),
    )

    argument_spec = dict(
        provider=dict(required=True),
        state=dict(default='present', choices=['present', 'absent'])
    )

    argument_spec.update(ib_spec)
    argument_spec.update(WapiModule.provider_spec)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    wapi = WapiModule(module)
    result = wapi.run(NIOS_DTC_SERVER, ib_spec)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
