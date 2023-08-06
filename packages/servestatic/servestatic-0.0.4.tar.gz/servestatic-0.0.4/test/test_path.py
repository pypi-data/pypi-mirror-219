from unittest import TestCase

from servestatic.server import Server


class TestPath(TestCase):
    server: Server

    def setUp(self) -> None:
        self.server = Server(host_="localhost", port_=8080, search_for_="index.html")

    def test__with_simple_path(self):
        path = self.server.arrange_path("/asd/")
        self.assertEqual("asd/index.html", path)

    def test__with_multi_slash_path(self):
        path = self.server.arrange_path("///asd///")
        self.assertEqual("asd/index.html", path)

    def test__with_path_to_file(self):
        path = self.server.arrange_path("/asd/style.css")
        self.assertEqual("asd/style.css", path)

    def test__with_url_query(self):
        path = self.server.arrange_path("/asd?hello=world")
        self.assertEqual("asd/index.html", path)

    def test__with_url_query_ends_with_slash(self):
        path = self.server.arrange_path("/asd/?hello=world")
        self.assertEqual("asd/index.html", path)
