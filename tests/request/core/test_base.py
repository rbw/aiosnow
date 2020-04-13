"""from aiohttp.client_reqrep import ClientResponse
from aiohttp.helpers import TimerNoop
import unittest
from unittest import mock
from yarl import URL

from snow.request.core.base import ErrorResponse, Response


class TestResponse(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = mock.Mock()

    def client_response(self):
        loop = mock.Mock()
        request_info = mock.Mock()
        response = ClientResponse(
            'get', URL('http://python.org'),
            request_info=request_info,
            writer=mock.Mock(),
            continue100=None,
            timer=TimerNoop(),
            traces=[],
            loop=loop,
            session=self.session,
        )
        return response

    async def test_error(self):
        cr = self.client_response()
        cr._headers = {"content-type": "application/json"}
        cr._body = b'{"error":{"message":"User Not Authenticated","detail":"Required to provide Auth information"},"status":"failure"}'
        r = Response(cr)
        with self.assertRaises(ErrorResponse):
            await r.get_content()

    async def test_result(self):
        cr = self.client_response()
        cr._headers = {"content-type": "application/json"}
        cr._body = b'{"result":[{"sys_id":"3c0f7173db3fcc90f5899983ca96190e"}]}'
        r = Response(cr)
        self.assertEqual(await r.get_content(), [{"sys_id": "3c0f7173db3fcc90f5899983ca96190e"}])


if __name__ == '__main__':
    unittest.main()
"""
