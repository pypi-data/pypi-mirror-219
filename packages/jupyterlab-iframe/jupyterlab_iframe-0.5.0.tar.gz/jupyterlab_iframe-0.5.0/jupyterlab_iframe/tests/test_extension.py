# for Coverage
from unittest.mock import patch, MagicMock
from jupyterlab_iframe.extension import (
    load_jupyter_server_extension,
    IFrameHandler,
    ProxyHandler,
)  # noqa: F401


class TestExtension:
    def test_load_jupyter_server_extension(self):
        m = MagicMock()

        m.web_app.settings = {}
        m.web_app.settings["base_url"] = "/test"
        load_jupyter_server_extension(m)

    def test_handler(self):
        import tornado.web

        app = tornado.web.Application()
        m = MagicMock()

        h = IFrameHandler(app, m)
        h.current_user = h._jupyter_current_user = "blerg"
        h._transforms = []
        h.get()

    def test_proxy_handler(self):
        import tornado.web

        app = tornado.web.Application()
        m = MagicMock()

        h = ProxyHandler(app, m)
        h.current_user = h._jupyter_current_user = "blerg"
        h._transforms = []

        with patch("requests.get") as m2:
            m2.return_value.text = "test"
            h.get()
