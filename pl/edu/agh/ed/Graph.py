from edu.agh.ed.Node import Node

class Graph(object):
    def __init__(self):
        self.nodes = {}

    def get_node(self,label):
        if not self.nodes.has_key(label):
            self.nodes[label]=Node(label)
        return self.nodes[label]

    def get_nodes(self):
        return self.nodes.values()

    def get_colored_nodes(self):
        nodes_colors = {}
        for node in self.get_nodes():
            if nodes_colors.has_key(node.get_color()):
                nodes_colors[node.get_color()].append(node)
            else:
                nodes_colors[node.get_color()]=[node]
        return nodes_colors