#!/usr/bin/python
# -*- coding: utf-8 -*-                                                                           

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Module purpose
==============

xPL PLCBUS client

Implements
==========

- plcbusMain.__init__(self)
- plcbusMain.plcbus_cmnd_cb(self, message)
- plcbusMain.plcbus_send_ack(self, message)

@author: François PINET <domopyx@gmail.com>
@copyright: (C) 2007-2009 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

from domogik.xpl.lib.xplconnector import *
from domogik.xpl.lib.plcbus import *
from domogik.common.configloader import Loader
from domogik.common import logger


class plcbusMain():

    def __init__(self):
        '''
        Create the plcbusMain class
        This class is used to connect PLCBUS to the xPL Network
        '''
        # Load config
        cfgloader = Loader('plcbus')
        config = cfgloader.load()[1]
        self.__myplcbus = Manager(source=config["source"],
                module_name='PLCBUS-1141')
        # Create listeners
        Listener(self.plcbus_cmnd_cb, self.__myplcbus, {
            'schema': 'control.basic',
            'type': 'xpl-cmnd',
        })
        self.api = PLCBUSAPI(int(config["port_com"]))
        # Create log instance
        l = logger.Logger('plcbus')
        self._log = l.get_logger()

    def plcbus_cmnd_cb(self, message):
        '''
        General callback for all command messages
        '''
        cmd = None
        dev = None
        user = None
        level = 0
        rate = 0
        if message.has_key('command'):
            cmd = message.get_key_value('command')
        if message.has_key('device'):
            dev = message.get_key_value('device')
        if message.has_key('usercode'):
            user = message.get_key_value('usercode')
        if message.has_key('level'):
            level = message.get_key_value('level')
        if message.has_key('rate'):
            rate = message.get_key_value('rate')
        self._log.debug("%s received : device = %s, user code = %s, level = "\
                "%s, rate = %s" % (cmd.upper(), dev, user, level, rate))
        if cmd == 'GET_ALL_ON_ID_PULSE':
            self.api.get_all_on_id(dev, user)
        else:
            self.api._send(cmd.upper(), dev, user, level, rate)

    def plcbus_send_ack(self, message):
        '''
        General ack sending over xpl network
        '''
        dt = localtime()
        mess = Message()
        mess.set_type("xpl-trig")
        mess.set_schema("sensor.basic")
        mess.set_data_key("type", "plcbus")
        mess.set_data_key("command", cmd)
        mess.set_data_key("device", dev)
        self.__myplcbus.send(mess)


if __name__ == "__main__":
    x = plcbusMain()
