class Pet(object):
    def __init__(self, name, species, level, experience, evolution, happiness, energy, hunger, money, inventory):
        self.name = name
        self.species = species
        self.level = level
        self.experience = experience
        self.evolution = evolution
        self.happiness = happiness
        self.energy = energy
        self.hunger = hunger
        self.money = money
        self.inventory = inventory

    def stats(self):
        return str(self.name)+"\t"+str(self.species)+"\t"+\
               str(self.level)+"\t"+str(self.experience)+"\t"+\
               str(self.evolution)+"\t"+str(self.happiness)+"\t"+\
               str(self.energy)+"\t"+str(self.hunger)+"\t"+\
               str(self.money)+"\t"+str(self.inventory)
