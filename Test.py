class organism:
    def __init__(self,name,birth_rate,death_rate,food=None):
        self.name = name
        self.birth_rate = birth_rate
        self.death_rate = death_rate
        self.food = food
        