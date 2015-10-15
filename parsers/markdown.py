import mistune


class MarkdownParser():

    def __init__(self, path):
        self.data = ""
        with open(path) as f:
            self.data = f.read()

    def parse(self):
        self.parsed_data = mistune.markdown(self.data)
        return self.parsed_data
