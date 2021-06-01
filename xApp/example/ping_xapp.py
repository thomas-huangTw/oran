"""
Test xapp 1
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


import time
import json
from ricxappframe.xapp_frame import Xapp


def entry(self):
    my_ns = "myxapp"
    number = 0
    while True:
        # test healthcheck
        print("ping is healthy? {}".format(xapp.healthcheck()))

        # rmr send to default handler
        self.rmr_send(json.dumps({"ping": number}).encode(), 6660666)

        # rmr send 60000, should trigger registered callback
        val = json.dumps({"test_send": number}).encode()
        self.rmr_send(val, 60000)
        """
        rmr_send(self, payload, mtype, retries=100)
        Allocates a buffer, sets payload and mtype, and sends
        Parameters
        ----------
        payload: bytes
            payload to set
        mtype: int
            message type
        retries: int (optional)
            Number of times to retry at the application level before excepting RMRFailure
        Returns
        -------
        bool
            whether or not the send worked after retries attempts
        """

        number += 1

        # store it in SDL and read it back; delete and read
        self.sdl_set(my_ns, "ping", number)
        """
        ** Deprecate Warning **
        ** Will be removed in a future function **
        
        sdl_set(self, namespace, key, value, usemsgpack=True)
        Stores a key-value pair to SDL, optionally serializing the value
        to bytes using msgpack.
        Parameters
        ----------
        namespace: string
            SDL namespace
        key: string
            SDL key
        value:
            Object or byte array to store.  See the `usemsgpack` parameter.
        usemsgpack: boolean (optional, default is True)
            Determines whether the value is serialized using msgpack before storing.
            If usemsgpack is True, the msgpack function `packb` is invoked
            on the value to yield a byte array that is then sent to SDL.
            Stated differently, if usemsgpack is True, the value can be anything
            that is serializable by msgpack.
            If usemsgpack is False, the value must be bytes.
        """
        
        self.logger.info(self.sdl_get(my_ns, "ping"))
        """
        ** Deprecate Warning **
        ** Will be removed in a future function **
        Gets the value for the specified namespace and key from SDL,
        optionally deserializing stored bytes using msgpack.
        
        sdl_get(self, namespace, key, usemsgpack=True)
        Parameters
        ----------
        namespace: string
            SDL namespace
        key: string
            SDL key
        usemsgpack: boolean (optional, default is True)
            If usemsgpack is True, the byte array stored by SDL is deserialized
            using msgpack to yield the original object that was stored.
            If usemsgpack is False, the byte array stored by SDL is returned
            without further processing.
        Returns
        -------
        Value
            See the usemsgpack parameter for an explanation of the returned value type.
            Answers None if the key is not found.
        """

        self.logger.info(self.sdl_find_and_get(my_ns, "pin"))
        """
        ** Deprecate Warning **
        ** Will be removed in a future function **
        Gets all key-value pairs in the specified namespace
        with keys that start with the specified prefix,
        optionally deserializing stored bytes using msgpack.
        
        sdl_find_and_get(self, namespace, prefix, usemsgpack=True)
        Parameters
        ----------
        nnamespaces: string
           SDL namespace
        prefix: string
            the key prefix
        usemsgpack: boolean (optional, default is True)
            If usemsgpack is True, the byte array stored by SDL is deserialized
            using msgpack to yield the original value that was stored.
            If usemsgpack is False, the byte array stored by SDL is returned
            without further processing.
        Returns
        -------
        Dictionary of key-value pairs
            Each key has the specified prefix.
            The value object (its type) depends on the usemsgpack parameter,
            but is either a Python object or raw bytes as discussed above.
            Answers an empty dictionary if no keys matched the prefix.
        """
        
        self.sdl_delete(my_ns, "ping")
        """
        ** Deprecate Warning **
        ** Will be removed in a future function **
        Deletes the key-value pair with the specified key in the specified namespace.
        
        sdl_delete(self, namespace, key)
        Parameters
        ----------
        namespace: string
           SDL namespace
        key: string
            SDL key
        """
        
        self.logger.info(self.sdl_get(my_ns, "ping"))

        # rmr receive
        for (summary, sbuf) in self.rmr_get_messages():
            """
            rmr_get_messages(self)
            Returns a generator iterable over all items in the queue that
            have not yet been read by the client xapp. Each item is a tuple
            (S, sbuf) where S is a message summary dict and sbuf is the raw
            message. The caller MUST call rmr.rmr_free_msg(sbuf) when
            finished with each sbuf to prevent memory leaks!
            """    
        
            # summary is a dict that contains bytes so we can't use json.dumps on it
            # so we have no good way to turn this into a string to use the logger unfortunately
            # print is more "verbose" than the ric logger
            # if you try to log this you will get: TypeError: Object of type bytes is not JSON serializable
            print("ping: {0}".format(summary))
            self.rmr_free(sbuf)

        time.sleep(2)


xapp = Xapp(entrypoint=entry, rmr_port=4564, use_fake_sdl=True)
"""
    Represents a generic Xapp where the client provides a single function
    for the framework to call at startup time (instead of providing callback
    functions by message type). The Xapp writer must implement and provide a
    function with a loop-forever construct similar to the `run` function in
    the `RMRXapp` class.  That function should poll to retrieve RMR messages
    and dispatch them appropriately, poll for configuration changes, etc.
    
    Xapp(self, entrypoint, rmr_port=4562, rmr_wait_for_ready=True, use_fake_sdl=False)
    Parameters
    ----------
    entrypoint: function
        This function is called when the Xapp class's run method is invoked.
        The function signature must be just function(self)
    rmr_port: integer (optional, default is 4562)
        Initialize RMR to listen on this port
    rmr_wait_for_ready: boolean (optional, default is True)
        Wait for RMR to signal ready before starting the dispatch loop
    use_fake_sdl: boolean (optional, default is False)
        Use an in-memory store instead of the real SDL service
"""

xapp.run()
