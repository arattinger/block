from docutils.core import publish_parts


class RSTParser():

    def __init__(self, path):
        self.data = ""
        with open(path) as f:
            self.data = f.read()

    def parse(self):
        self.parsed_data = publish_parts(
            self.data, writer_name="html")['html_body']
        return self.parsed_data
