from Node import Node
from Connection import Connection
from Connection_history import Connection_history
import random
import numpy as np
class Genome():
    
    def __init__(self, in_p, out_p, crossover = False):
        self.genes = []
        self.nodes = []
        self.inputs = in_p
        self.outputs = out_p
        self.layers = 2
        self.next_node = 0
        self.bias_node = 0
        self.innovation_history = []
        self.next_connection_no = 0
        #input nodes
        for i in range(self.inputs):
            self.nodes.append(Node(i))
            self.next_node += 1
            self.nodes[i].layer = 0
        
        #output nodes
        for i in range(self.outputs):
            self.nodes.append(Node(i + self.inputs))
            self.nodes[i + self.inputs].layer = 1
            self.next_node += 1

        #bias node
        self.nodes.append(Node(self.next_node))
        self.bias_node = self.next_node
        self.next_node += 1
        self.nodes[self.bias_node].layer = 0

    def get_node(self, node_number):
            for n in range(len(self.nodes)):
                if self.nodes[n].number == node_number:
                    return self.nodes[n]
            return None

    def connect_nodes(self):
        for n in range(len(self.genes)):
            self.genes[n].fro_node.output_connections.append(self.genes[n])
            #print("added connection ", self.genes[n].innovation_no, " to ", self.genes[n].fro_node.number, "/'s output connections list which now reads as: ", self.genes[n].fro_node.output_connections)
    
    def feed_forward(self, input_values):
        for i in range(self.inputs):
            self.nodes[i].output_value = input_values[i]
        self.nodes[self.bias_node].output_value = 1
        for s in range(len(self.network)):
            self.network[s].engage()
        outs = []
        for x in range(self.outputs):
            outs.append(self.nodes[self.inputs + x].output_value)
        return outs

    def generate_network(self):
        self.connect_nodes()
        self.network = []
        for l in range(self.layers):
            for n in range(len(self.nodes)):
                self.network.append(self.nodes[n])

    def add_node(self, innovation_history):
        if len(self.genes) == 0:
            self.add_connection(innovation_history)
            return
        random_connection = random.randint(0, len(self.genes) -1)
        self.genes[random_connection].enabled = False
        new_node_no = self.next_node
        self.nodes.append(Node(new_node_no))
        self.next_node += 1
        connection_innovation_number = self.get_innovation_number(innovation_history, self.genes[random_connection].fro_node, self.get_node(new_node_no))
        self.genes.append(Connection(self.genes[random_connection].fro_node, self.get_node(new_node_no), 1, connection_innovation_number))
        connection_innovation_number = self.get_innovation_number(innovation_history, self.nodes[self.bias_node], self.get_node(new_node_no))
        self.genes.append(Connection(self.nodes[self.bias_node], self.get_node(new_node_no), 0, connection_innovation_number))
        if self.get_node(new_node_no).layer == self.genes[random_connection].to_node.layer:
            for n in range(len(self.nodes)):
                if self.nodes[n].layer >= self.get_node(new_node_no).layer:
                    self.nodes[n].layer += 1
            self.layers += 1
        self.connect_nodes() 
    
    def add_connection(self, innovation_history):
        if self.fully_connected():
            return
        
        random_node_1 = random.randint(0, len(self.nodes) - 1)
        random_node_2 = random.randint(0, len(self.nodes) - 1)
        while self.random_connections_undesirable(random_node_1, random_node_2):
            random_node_1 = random.randint(0, len(self.nodes) - 1)
            random_node_2 = random.randint(0, len(self.nodes) - 1)
        temp = 0
        if self.nodes[random_node_1].layer > self.nodes[random_node_2].layer:
            temp = random_node_2
            random_node_2 = random_node_1
            random_node_1 = temp
        connection_innovation_number = self.get_innovation_number(innovation_history, self.nodes[random_node_1], self.nodes[random_node_2])
        self.genes.append(Connection(self.nodes[random_node_1], self.nodes[random_node_2], random.uniform(-1, 1), connection_innovation_number))
        self.connect_nodes()

    def random_connections_undesirable(self, n1, n2):
        if self.nodes[n1].layer == self.nodes[n2].layer:
            return True
        if self.nodes[n1].is_connected_to(self.nodes[n2]):
            return True
        return False

    def get_innovation_number(self, innovation_history, fro, to):
        is_new = True
        connection_innovation_number = self.next_connection_no
        for i in range(len(innovation_history)):
            if innovation_history[i].matches(self, fro, to):
                is_new = False
                connection_innovation_number = innovation_history[i].innovation_number
                break
        if is_new:
            inno_numbers = []
            for g in range(len(self.genes)):
                inno_numbers.append(self.genes[g].innovation_no)
            self.innovation_history.append(Connection_history(fro.number, to.number, connection_innovation_number, inno_numbers))
            self.next_connection_no += 1
        return connection_innovation_number

    def fully_connected(self):
        max_connections = 0
        nodes_in_layers = np.zeros(self.layers)

        for n in range(len(self.nodes)):
            nodes_in_layers[self.nodes[n].layer] += 1

        for l in range(self.layers - 1):
            nodes_in_front = 0
            for j in (l + 1, self.layers - 1, 1):
                nodes_in_front += nodes_in_layers[j]

            max_connections += nodes_in_layers[l] * nodes_in_front
        
        if max_connections == len(self.genes):
            return True
    
        return False

    def mutate(self, innovation_history):
        if len(self.genes) == 0:
            self.add_connection(innovation_history)

        rand_1 = random.random()
        if rand_1 < 0.8:
            for g in range(len(self.genes)):
                self.genes[g].mutate_weight()

        rand_2 = random.random()
        if rand_2 < 0.08:
            self.add_connection(innovation_history)
        
        rand_3 = random.random()
        if rand_3 < 0.02:
            self.add_node(innovation_history)

    def crossover(self, parent2):
        child = Genome(self.inputs, self.ouputs, True)

        child.genes.clear()
        child.nodes.clear()
        child.layers = self.layers
        child.next_node = self.next_node
        child.bias_node = self.bias_node
        child_genes = []
        is_enabled = []

        for g in range(len(self.genes)):
            set_enabled = True
            parent2_gene = self.matching_gene(parent2, self.genes[g].innovation_no)
            if parent2_gene != -1:
                if not self.genes[g].enabled or not parent2.genes[parent2_gene].enabled:
                    if random.random() < 0.75:
                        set_enabled = False
                rand = random.random()
                if rand < 0.5:
                    child_genes.append(self.genes[g])
                else:
                    child_genes.add(parent2.genes[parent2_gene])
            else:
                child_genes.append(self.genes[g])
                set_enabled = self.genes[g].enabled
            is_enabled.append(set_enabled)
            
        for g in range(len(child_genes)):
            child.genes.append(child_genes[g].clone(child.get_node(child_genes.get[g].fro_node.number), child.get_node(child_genes.get[g].to_node.node_number)))
            child.genes[g].enabled = is_enabled[g]

    def matching_gene(self, parent2, innovation_number):
        for g in range(len(parent2.genes)):
            if parent2.genes[g].innovation_no == innovation_number:
                return g
        return -1

    def clone(self):
        clone = Genome(self.inputs, self.outputs, True)
        for n in range(len(self.nodes)):
            clone.nodes.append(self.nodes[n].clone())
        for g in range(len(self.genes)):
            clone.genes.append(self.genes[g].clone(clone.get_node(self.genes[g].fro_node.number), clone.get_node(self.genes[g].to_node.number)))
        clone.layers = self.layers
        clone.next_node = self.next_node
        clone.bias_node = self.bias_node
        clone.connect_nodes()

        return clone
