class Node:
    def __init__(self, name, node_id=-1):
        self.id = node_id
        self.name = str(name)  # The node's name is the class key

    def set_id(self, node_id):
        self.id = node_id

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "node " + self.name
