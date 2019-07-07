import numpy as np

class Node():

    def __init__(self, no):
        self.number = no
        self.input_sum = 0
        self.output_value = 0
        self.output_connections = []
        self.layer = 0

    def engage(self):
        for o in range(len(self.output_connections)):
            if self.output_connections[o].enabled:
                self.output_connections[o].to_node.input_sum += self.output_connections[o].weight * self.output_value

        if self.layer != 0:
            self.output_value = np.tanh(self.input_sum)

    def is_connected_to(self, node):
        if node.layer == self.layer:
            return False
        
        if node.layer < self.layer:
            for o in range(len(node.output_connections)):
                if node.output_connections[o].to_node == self:
                    return True
        else:
            for o in range(len(self.output_connections)):
                if self.output_connections[o].to_node == node:
                    return True

    def clone(self):
        clone = Node(self.number)
        clone.layer = self.layer
        return clone