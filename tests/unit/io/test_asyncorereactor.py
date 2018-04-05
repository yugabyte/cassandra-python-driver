# Copyright DataStax, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
try:
    import unittest2 as unittest
except ImportError:
    import unittest # noqa

from mock import patch
import socket
import cassandra.io.asyncorereactor
from cassandra.io.asyncorereactor import AsyncoreConnection, AsyncoreLoop
from tests import is_monkey_patched
from tests.unit.io.utils import ReactorTestMixin, TimerTestMixin, noop_if_monkey_patched


class AsyncorePatcher(unittest.TestCase):

    @classmethod
    @noop_if_monkey_patched
    def setUpClass(cls):
        if is_monkey_patched():
            return
        AsyncoreConnection.initialize_reactor()

        socket_patcher = patch('socket.socket', spec=socket.socket)
        channel_patcher = patch(
            'cassandra.io.asyncorereactor.AsyncoreConnection.add_channel',
            new=(lambda *args, **kwargs: None)
        )

        cls.mock_socket = socket_patcher.start()
        cls.mock_socket.connect_ex.return_value = 0
        cls.mock_socket.getsockopt.return_value = 0
        cls.mock_socket.fileno.return_value = 100

        channel_patcher.start()

        cls.patchers = (socket_patcher, channel_patcher)

    @classmethod
    @noop_if_monkey_patched
    def tearDownClass(cls):
        for p in cls.patchers:
            try:
                p.stop()
            except:
                pass


class AsyncoreConnectionTest(ReactorTestMixin, AsyncorePatcher):

    connection_class = AsyncoreConnection
    socket_attr_name = 'socket'

    def setUp(self):
        if is_monkey_patched():
            raise unittest.SkipTest("Can't test asyncore with monkey patching")

    def test_subclasses_share_loop(self):
        cassandra.io.asyncorereactor.global_loop = None
        class C1(AsyncoreConnection):
            pass

        class C2(AsyncoreConnection):
            pass

        c1 = C1
        c1.initialize_reactor()

        c2 = C2
        c2.initialize_reactor()
        import threading
        event_loops_threads = [thread for thread in threading.enumerate() if thread.name == "cassandra_driver_event_loop"]
        self.assertEqual(len(event_loops_threads), 1)

class TestAsyncoreTimer(TimerTestMixin, AsyncorePatcher):
    connection_class = AsyncoreConnection

    @property
    def create_timer(self):
        return self.connection.create_timer

    @property
    def _timers(self):
        return self.connection._loop._timers

    def setUp(self):
        if is_monkey_patched():
            raise unittest.SkipTest("Can't test asyncore with monkey patching")
        super(TestAsyncoreTimer, self).setUp()
