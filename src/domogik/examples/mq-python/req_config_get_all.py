#!/usr/bin/python
"""
@api {REQ} config.get Get a value for all configuration items of a client
@apiVersion 0.4.0
@apiName config.get (all)
@apiGroup Clients configuration
@apiDescription This request is used to ask Domogik's admin the value of a configuration item
* Source client : Domogik admin, any other interface which can manage the clients
* Target client : always 'admin' 

@apiExample {python} Example usage:
    cli = MQSyncReq(zmq.Context())
    msg = MQMessage()
    msg.set_action('config.get')
    msg.add_data('type', 'plugin')
    msg.add_data('host', 'darkstar')
    msg.add_data('name', 'diskfree')
    print(cli.request('admin', msg.get(), timeout=10).get())
    
@apiParam {String} type The client type
@apiParam {String} host The host on which is hosted the client
@apiParam {String} name The client name 

@apiSuccessExample {json} Success-Response:
[
    'config.result',
    '{
        "status": true,
        "name": "diskfree",
        "data": {
            "configured": true,
            "auto_startup": true
        },
        "host": "darkstar",
        "reason": "",
        "key": "*",
        "type": "plugin"
    }'
]
"""

import zmq
from zmq.eventloop.ioloop import IOLoop
from domogikmq.reqrep.client import MQSyncReq
from domogikmq.message import MQMessage

cli = MQSyncReq(zmq.Context())
msg = MQMessage()
msg.set_action('config.get')
msg.add_data('type', 'plugin')
msg.add_data('host', 'darkstar')
msg.add_data('name', 'diskfree')
print(cli.request('admin', msg.get(), timeout=10).get())

