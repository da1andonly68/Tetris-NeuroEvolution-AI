from Player import Player
from Species import Species
import numpy as np
class Population():
    
    def __init__(self, size):
        self.pop = []
        self.best_player = None
        self.best_score = 0 
        self.gen = 0
        self.innovation_history = []
        self.species = []
        
        self.mass_extinction_event = False
        self.new_stage = False

        self.current_player = 0

        for s in range(size):
            self.pop.append(Player())
            self.pop[s].brain.generate_network()
            for x in range(50):
                self.pop[s].brain.mutate(self.innovation_history)
                
    def get_player(self, player_index):
        return self.pop[player_index]

    def update(self, current_player):
        self.current_player = current_player
        if not current_player > self.size: 
            return self.pop[current_player].think()

    def done(self):
        if current_player > self.size:
            return True
        else: 
            return False

    def selection(self):
        self.speciate()
        self.sort_species()
        if self.mass_extinction_event:
            self.mass_extinction()
            self.mass_extinction_event = False
        self.cull_species()
        self.kill_stale_species()
        self.kill_bad_species()

        average_sum = self.get_avg_fitness_sum()
        children = []
        for s in range(len(self.species)):
            children.append(self.species[s].champ.clone())
            no_of_children = np.round(self.species[s].average_fitness / average_sum * len(self.pop)) - 1
            for c in range(no_of_children):
                children.append(self.species[s].give_me_baby(innovation_history))
            while len(children) < len(self.pop):
                children.append(self.species[s].give_me_baby(innovation_history))
            self.pop.clear()
            self.pop = children.clone()
            self.gen += 1
            for p in range(len(self.pop)):
                pop[p].brain.generate_network()
            
    def speciate(self):
        for s in self.species:
            s.players.clear()
        for x in range(len(self.pop)):
            species_found = False
            for s in self.species:
                if s.same_species(self.pop[x].brain):
                    s.add_to_species(self.pop[x])
                    species_found = True
                    break
        if not species_found:
            self.species.append(Species(self.pop[x]))
            
    def sort_species(self):
        for s in self.species:
            s.sort_species()
        temp = []
        for s in range(len(self.species)):
            max = 0
            max_index = 0
            for b in range(len(self.species)):
                if self.species[b].best_fitness > max:
                    max = self.species[b].best_fitness
                    max_index = b
            temp.append(self.species[max_index])
            self.species.remove(self.species[max_index])
            s -= 1
        self.species = temp.copy()
            
    def kill_stale_species(self):
        average_sum = self.get_avg_fitness_sum()
        for s in range(len(self.species)):
            if average_sum == 0 or self.species[s].average_fitness/average_sum * len(self.pop) < 1:
                self.species.remove(self.species[s])
                s -= 1
    
    def kill_bad_species(self):
        average_sum = self.get_avg_fitness_sum()

        for s in range(len(self.species)):
            if self.species[s].average_fitness/average_sum * len(self.pop) < 1:
                self.species.remove(s)
                s -= 1

    def get_avg_fitness_sum(self):
        average_sum = 0
        for s in self.species:
            average_sum += s.average_fitness
        return average_sum

    def cull_species(self):
        for s in self.species:
            s.cull()
            s.fitness_sharing()
            s.set_average()

    def mass_extinction(self):
        for s in range(len(self.species)):
            s.remove(s)
            s -= 1
