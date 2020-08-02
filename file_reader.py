

class SqlFileReader:
    lines = []
    one_line = ''

    def __init__(self, filename):
        self.load_file(filename)

    def load_file(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.readlines()
            self.lines = list(filter(lambda l: not l.startswith('#'), self.lines))
            self.lines = list(map(lambda l: l.strip().lower(), self.lines))
            self.one_line = ' '.join(self.lines)

    def locate(self, token_value):
        for idx, line in enumerate(self.lines):
            if token_value in line:
                return idx + 1
        return 0
