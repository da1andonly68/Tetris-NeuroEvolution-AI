import random

class Species():
    #no champ
    def __init__(self, player = None):
        self.players = []
        self.best_fitness = 0
        self.average_fitness = 0
        self.staleness = 0
        self.rep = None

        self.excess_coeff = 1
        self.weight_diff_coeff = 0.5
        self.compatibililty_threshold = 3
        
        self.players.append(player)
        self.best_fitness = player.fitness
        self.rep = player.brain.clone()
        
    def same_species(self, genome):
        compatibility = 0
        excess_and_disjoint = self.get_excess_disjoint(genome, self.rep)
        average_weight_diff = self.average_weight_diff(genome, self.rep)
        large_genome_normaliser = len(genome.genes) - 20
        if large_genome_normaliser < 1:
            large_genome_normaliser = 1
        compatibility = (self.excess_coeff * excess_and_disjoint/large_genome_normaliser) + (self.weight_diff_coeff * average_weight_diff)
        return self.compatibililty_threshold > compatibility

    def add_to_species(self, player):
        self.players.append(player)

    def get_excess_disjoint(self, brain1, brain2):
        matching = 0
        for b in range(len(brain1.genes)):
            for d in range(len(brain2.genes)):
                if brain1.genes[b].innovation_no == brain2.genes[d].innovation_no:
                    matching += 1
                    break
        return len(brain1.genes) + len(brain2.genes) - 2 * matching

    def average_weight_diff(self, brain1, brain2):
        if len(brain1.genes) == 0 or len(brain2.genes) == 0:
            return 0

        matching = 0
        total_diff = 0
        for g in range(len(brain1.genes)):
            for j in range(len(brain2.genes)):
                if brain1.genes[g].innovation_no == brain2.genes[j].innovation_no:
                    mathcing += 1
                    total_diff += abs(brain1.genes[g].weight - brain2.genes[j].weight)
                    break
        if matching == 0:
            return 100
        return total_diff / matching

    def sort_species(self):
        temp = []
        for p in range(len(self.players)):
            max = 0
            max_index = 0
            for q in range(len(self.players)):
                if self.players[q].fitness > max:
                    max = self.players[q].fitness
                    max_index = q
            temp.append(self.players[max_index])
            self.players.remove(self.players[max_index])
            if len(self.players) == 0:
                self.staleness = 200
                return
            if self.players[0].fitness > self.best_fitness:
                staleness = 0
                self.best_fitness = self.players[0].fitness
                self.rep = self.players[0].brain.clone()
            else:
                self.staleness += 1

    def set_average(self):
        sum = 0
        for p in range(len(self.players)):
            sum += self.players[p].fitness
        if len(self.players) != 0:
            average_fitness = sum / len(self.players)
        else:
            average_fitness = 0
    
    def give_me_baby(self, innovation_history):
        baby = None
        if random.random < 0.25:
            baby = self.select_player().clone()
        else:
            parent1 = self.select_player()
            parent2 = self.select_player()

            if parent1.fitness < parent1.fitness:
                baby = parent2.crossover(parent1)
            else:
                baby = parent1.crossover(parent2)

        baby.brain.mutate(innovation_history)
        return baby

    def select_player(self):
        fitness_sum = 0
        for p in range(len(self.players)):
            fitness_sum += self.players[p].fitness
        rand = random.uniform(0, fitness_sum)
        running_sum = 0
        for p in range(len(self.players)):
            running_sum += self.players[p].fitness
            if running_sum > rand:
                return self.players[p]
        return self.players[0]
    
    def cull(self):
        if len(self.players) > 2:
            for p in (range(len(self.players) / 2), range(len(self.players)), 1):
                self.players.remove(p)
                p -= 1
    def fitness_sharing(self):
        for p in range(len(self.players)):
            self.players[p].fitness /= len(self.players)



