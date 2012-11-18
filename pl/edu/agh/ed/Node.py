class Node(object):
    def __init__(self,word):
        self.neighbours = []
        self.word=word
        self.color = None

    def connect_to(self,node):
        self.neighbours.append(node)

    def get_neighbours(self):
        return self.neighbours

    def get_word(self):
        return self.word

    def set_color(self,color):
        self.color=color

    def get_color(self):
        return self.color

    def size(self):
        return len(self.neighbours)