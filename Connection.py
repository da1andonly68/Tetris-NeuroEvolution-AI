import random
import numpy as np
class Connection():

    def __init__(self, fro, to, w, inno):
        self.fro_node = fro
        self.to_node = to
        self.weight = w
        self.innovation_no = inno
        self.enabled = True

    def mutate_weight(self):
        rand2 = random.randint(0, 1)
        if rand2 < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += np.random.normal() /50
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1

    def clone(self, fro, to):
        connection = Connection(self.fro_node, self.to_node, self.weight, self.innovation_no)
        connection.enabled = self.enabled
        return connection