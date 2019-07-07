from Genome import Genome

class Player:

    def __init__(self):
        self.fitness = 0
        self.unadjusted_fitness = 0
        self.dead = 0
        self.score = 0
        self.gen = 0
        self.genome_input_count = 244
        self.genome_output_count = 5
        self.genome_inputs = []
        self.genome_outputs = []
        self.brain = Genome(self.genome_input_count, self.genome_output_count)

    def think(self, input):
        max = 0
        max_index = 0
        decision = self.brain.feed_forward(input)
        print(decision)
        for d in range(len(decision)):  
            if decision[d] > max:
                max = decision[d]
                max_index = d

        return max_index
    
    def clone(self):
        clone = Player()
        clone.brain = self.brain.clone()
        clone.fitness = self.fitness
        clone.brain.generate_network()
        clone.gen = self.gen
        clone.best_score = self.best_score
    
    def set_fitness(self, fitness):
        self.fitness = fitness

    def crossover(parent2):
        child = Player()
        child.brain = brain.crossover(parent2.brain)
        child.brain.generate_network()
        return child