class Connection_history():

    def __init__(self, fro, to, inno, innovation_nos):
        self.fro_node = fro
        self.to_node = to
        self.innovation_number = inno
        self.innovation_numbers = innovation_nos.copy()

    def matches(self, genome, fro, to):
        if len(genome.genes) == len(innovation_numbers):
            if(fro.number == self.fro_node and to.number == self.to_node):
                for o in range(len(genome.genes)):
                    if genome.genes[o] not in self.innovation_numbers:
                        return False
            else:
                return True
        else:
            return False