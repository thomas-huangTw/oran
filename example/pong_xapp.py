"""
Test xapp 2 that works with 1
"""
# ==================================================================================
#       Copyright (c) 2020 Nokia
#       Copyright (c) 2020 AT&T Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================
import json
from ricxappframe.xapp_frame import RMRXapp, rmr


def post_init(_self):
    """post init"""
    print("pong xapp could do some useful stuff here!")


def sixtyh(self, summary, sbuf):
    """callback for 60000"""
    self.logger.info("pong registered 60000 handler called!")
    # see comment in ping about this; bytes does not work with the ric mdc logger currently
    print("pong 60000 handler received: {0}".format(summary))
    jpay = json.loads(summary[rmr.RMR_MS_MSG_PAYLOAD])
    self.rmr_rts(sbuf, new_payload=json.dumps({"ACK": jpay["test_send"]}).encode(), new_mtype=60001, retries=100)
    """
        Allows the xapp to return to sender, possibly adjusting the
        payload and message type before doing so.  This does NOT free
        the sbuf for the caller as the caller may wish to perform
        multiple rts per buffer. The client needs to free.

        rmr_rts(self, sbuf, new_payload=None, new_mtype=None, retries=100)
        Parameters
        ----------
        sbuf: ctypes c_void_p
             Pointer to an rmr message buffer
        new_payload: bytes (optional)
            New payload to set
        new_mtype: int (optional)
            New message type (replaces the received message)
        retries: int (optional, default 100)
            Number of times to retry at the application level
        Returns
        -------
        bool
            whether or not the send worked after retries attempts
    """
    
    self.rmr_free(sbuf)
    """ 
        Frees an rmr message buffer after use
        Note: this does not need to be a class method, self is not
        used. However if we break it out as a function we need a home
        for it.

        rmr_free(self, sbuf)
        Parameters
        ----------
        sbuf: ctypes c_void_p
             Pointer to an rmr message buffer
    """

def defh(self, summary, sbuf):
    """default callback"""
    self.logger.info("pong default handler called!")
    print("pong default handler received: {0}".format(summary))
    self.rmr_free(sbuf)

xapp = RMRXapp(default_handler=defh, post_init=post_init, use_fake_sdl=True)
"""
    Represents an Xapp that reacts only to RMR messages; i.e., the Xapp
    only performs an action when a message is received.  Clients should
    invoke the run method, which has a loop that waits for RMR messages
    and calls the appropriate client-registered consume callback on each.
    If environment variable CONFIG_FILE is defined, and that variable
    contains a path to an existing file, this class polls a watcher
    defined on that file to detect file-write events, and invokes a
    configuration-change handler on each event. The handler is also
    invoked at startup.  If no handler function is supplied to the
    constructor, this class defines a default handler that only logs a
    message.
    
    RMRXapp(self, default_handler, config_handler=None, rmr_port=4562, rmr_wait_for_ready=True, use_fake_sdl=False, post_init=None)
    Parameters
    ----------
    default_handler: function
        A function with the signature (summary, sbuf) to be called when a
        message type is received for which no other handler is registered.
    default_handler argument summary: dict
        The RMR message summary, a dict of key-value pairs
    default_handler argument sbuf: ctypes c_void_p
        Pointer to an RMR message buffer. The user must call free on this when done.
    config_handler: function (optional, default is documented above)
        A function with the signature (json) to be called at startup and each time
        a configuration-file change event is detected. The JSON object is read from
        the configuration file, if the prerequisites are met.
    config_handler argument json: dict
        The contents of the configuration file, parsed as JSON.
    rmr_port: integer (optional, default is 4562)
        Initialize RMR to listen on this port
    rmr_wait_for_ready: boolean (optional, default is True)
        Wait for RMR to signal ready before starting the dispatch loop
    use_fake_sdl: boolean (optional, default is False)
        Use an in-memory store instead of the real SDL service
    post_init: function (optional, default None)
        Run this function after the app initializes and before the dispatch loop starts;
        its signature should be post_init(self)
"""

xapp.register_callback(sixtyh, 60000)
"""
        registers this xapp to call handler(summary, buf) when an rmr message is received of type message_type
        
        register_callback(self, handler, message_type)
        Parameters
        ----------
        handler: function
            a function with the signature (summary, sbuf) to be called
            when a message of type message_type is received
        summary: dict
            the rmr message summary
        sbuf: ctypes c_void_p
            Pointer to an rmr message buffer. The user must call free on this when done.
        message:type: int
            the message type to look for
        Note if this method is called multiple times for a single message type, the "last one wins".
"""

xapp.run()  # will not thread by default
