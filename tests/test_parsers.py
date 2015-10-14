import unittest

from docutils.core import publish_parts
from test_utils import read_file


table = """

"""


class Rst2Html(unittest.TestCase):

    def setUp(self):
        self.test1 = read_file('rst/test1.rst')
        self.test2 = read_file('rst/test2.rst')
        self.table = read_file('rst/table.rst')

    def test_simple1(self):
        result = publish_parts(self.test1, writer_name="html")['html_body']
        # result = json.loads(simplicity.rst_to_json(self.test1))
        print(result)

    def test_simple2(self):
        result = publish_parts(self.test2, writer_name="html")['html_body']
        print(result)

    def test_tables(self):
        result = publish_parts(self.table, writer_name="html")['html_body']
        print(result)
