class Node:
    def __init__(self, name, line, column):
        self.name = str(name)
        self.line = line
        self.column = column

    def get_name(self):
        return self.name

    def get_line(self):
        return self.line

    def get_column(self):
        return self.column

    def set_line(self, new_line):
        self.line = new_line

    def set_column(self, new_column):
        self.column = new_column

    def __eq__(self, other):
        return self.line == other.line and self.column == other.column

    def __hash__(self):
        return 31 * hash(self.column) + hash(self.line)

    def __str__(self):
        return f"node: ({self.name}, {self.line}, {self.column})"
