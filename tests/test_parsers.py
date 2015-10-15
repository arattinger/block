import unittest
from bs4 import BeautifulSoup
import mistune

from docutils.core import publish_parts
from test_utils import read_file


def convert_rst_to_html(text):
    return publish_parts(text, writer_name="html")['html_body']


class Rst2Html(unittest.TestCase):

    def setUp(self):
        self.test1 = read_file('rst/test1.rst')
        self.test2 = read_file('rst/test2.rst')
        self.table = read_file('rst/table.rst')

    def test_simple1(self):
        result = convert_rst_to_html(self.test1)
        soup = BeautifulSoup(result, 'html.parser')
        self.assertEqual(soup.h1.text, 'Title')
        self.assertEqual(soup.h2.text, 'Subtitle')
        # print(result)

    # def test_simple2(self):
    #     result = convert_rst_to_html(self.test2)
    #     print(result)

    # def test_tables(self):
    #     result = convert_rst_to_html(self.table)
    #     print(result)


class Markdown2Html(unittest.TestCase):

    def setUp(self):
        self.test1 = read_file('markdown/test1.md')

    def test_simple1(self):
        result = mistune.markdown(self.test1)
        soup = BeautifulSoup(result, 'html.parser')
        self.assertEqual(soup.h1.text, 'An h1 header')
