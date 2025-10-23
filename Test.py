import numpy as np
import math
import json
class species:
    '''The species class represents the entire population of an species and contains its base birth rate, death rate, current population, resources, name, consumption rate, and it's population history. 
    Additonaly resources expects a numpy array of numpy arrays, and population expects a simple numpy array.
    "experiment_length" is a class variable, and is thus accesable to all instances of this class. it tracks how long the experiment will go for, and is used to establish the array that will note the population over the years
    "cycle_counter" is  a class variable that tracks the ammount of cycles that have occured so far'''
    experiment_length = 100
    cycle_counter = 0
    def __init__(self,birth_rate, death_rate, population:np.ndarray,resources:np.ndarray = np.array([0]),name:str="",consumption_rate:int = 1):
        self.name = name
        self.birth_rate = birth_rate
        self.death_rate = death_rate
        self.population = population
        self.resources = resources
        self.consumption_rate = consumption_rate
        self.population_history = np.zeros(self.experiment_length)
        self.population_history[0] = self.population[0]
    def overshoot_population_model(self):
        '''This is a modified version of the standard overshoot population model that has been modified to not loop, and work within the context of the function class. 
        Thus this function can be called by species_object.overshoot_population_model() instead of overshoot_population_model(vars). 
        Since this is a function within a class, calling it on the object will automaticly use the object with no propting due to the "self" argument'''
        # Variables
        #-----------
        # self.birth_rate - base rate of new births per year
        # self.death_rate - base rate of deaths per year
        # self.consumption_rate - resources used by each organism of the species in each year
        # self.population - current population of this species of organisms
        # self.resources - array of the resources avalible to this species of organisms, with each entry in the array representing the population of another species this species prays on
        # current_reasource_total - the total amount of resources avalible to this species 
        # shortage_death_rate - an additonal deathrate representing the additonal amount of deaths during reasource scarcity
        # population_change - represents the total change in population
        # resources_ratio - tracks the percentage make of the diffrent resources in current_reasource_total
        # all_remainders - tracks the remainders, and the associated position of it's associated number in the reasources array
        
        # Checks to see if poupulation is 0, if it is we can skip all the future calculations,  and return 0 if applicable
        if self.population == 0:
            if self.name == "plants":
                return
            else:
                return 0
        # Use the sum function to sum all the values of the self.resources array together giving current_reasource_total
        current_reasource_total = 0
        for i in range(0,len(self.resources),1):
            current_reasource_total += self.resources[i][0]

        # creates an array to store the remainders later and using the dtype argument creating a custom datatype so it can be sort in the order of remainders datatype instead of ordering each elmenet individualy. (both datatypes are using int64 as a base, indicated by the "i8") 
        all_remainders = np.zeros((len(self.resources),),dtype=[("remainders","i8"),("position","i8")])

        # resources_per_person is the relationship between the two reservoirs
        resources_per_person = current_reasource_total/self.population[0]
        
        # if resources_per_person is sufficently low enough, impose an additonal death rate
        if resources_per_person <= 9:
            shortage_death_rate = -0.1 * resources_per_person + 1.0
        else:
            shortage_death_rate = 0
        
        # Calculate the number of births that will happen with this current population
        births = self.birth_rate * self.population[0] 
        
        # Calculate the number of deaths that will happen with this current population
        deaths = (self.death_rate+shortage_death_rate) * self.population[0]
        
        # Calculate the total change in population
        population_change = births - deaths

        # How many resources were used up? 1 resource for each person
        resources_used = self.consumption_rate * self.population[0]
        

        # Apply the population change
        self.population[0] += round(population_change)

        # Population can't be less than zero!
        if self.population[0] < 0:
            self.population[0] = 0    
        
        # Record the population
        self.population_history[self.cycle_counter] = self.population[0]
        
        # Calculate what percentage a type of reasources make up the total current resources
        remainders_sum = 0
        for i in range(0,len(self.resources),1):
            if self.resources[i][0] != 0: # If statment for the value not bein 0 to prevent div by 0 error
                resource_ratio = self.resources[i][0]/current_reasource_total
            else:
                resource_ratio = 0 # If the else statment is false, then there must be 0 resources, and as there are 0 resources, there is no way to contribute to the ratio. Thus ratio is set to 0
            # Calculate the change in resources by multiplying the resources used by the fractional resource ratio
            catch_val = self.resources[i][0]
            self.resources[i][0] -= resources_used * resource_ratio
            # Caluclate the remainder of divison by 1 so that we know the numbers after the decimal point
            remainder = self.resources[i][0] % 1.0
            # Store this remainder and it's index to the all_remainders array
            all_remainders[i] = remainder,i
            # Add the remainder to the growing sum of remainders
            remainders_sum += remainder
        
        # Round the remainders_sum
        remainders_sum.round()
        remainders_sum = int(remainders_sum)
        all_remainders = np.sort(all_remainders,order="remainders")[::-1]
        # Round up a number of individual resource amounts based on the closest interger to the remainder
        for i in range(0,remainders_sum,1):
            self.resources[all_remainders[i][1]][0] = math.ceil(self.resources[all_remainders[i][1]][0])
            if self.resources[all_remainders[i][1]][0] <= 0:
                self.resources[all_remainders[i][1]][0] = 0
        # Round down all remaing resource values
        for i in range(remainders_sum,len(self.resources),1):
            self.resources[all_remainders[i][1]][0] = math.floor(self.resources[all_remainders[i][1]][0])
            if self.resources[all_remainders[i][1]][0] <= 0:
                self.resources[all_remainders[i][1]][0] = 0
        if self.name == "plants":
            return
        elif self.name == "decomposers":
            self.resources[0][0] += deaths
            return round(resources_used)
        corpses = round(deaths)
        return corpses
    
inital_corpses = np.array([1000000])
inital_plant_food = np.array([1000000])
# inital neutrtion values for the hard coded decomposers, and plants
plant_reproduction_rate = 0.5
plant_death_rate = 0
inital_plants = np.array([100000])
decomposers_reproduction_rate = 0.2
decomposers_death_rate = 0
initial_decomposers = np.array([10000])

decomposers = species(decomposers_reproduction_rate,decomposers_death_rate,initial_decomposers,[inital_corpses],"decomposers")
plants = species(plant_reproduction_rate,plant_death_rate,inital_plants,[inital_plant_food],"plants")
thing_a = species(0.15,0,np.array([1000]),[plants.population])
thing_b = species(0.15,0,np.array([1000]),[plants.population,thing_a.population])
thing_c = species(0.1,0,np.array([500]),[thing_a.population,thing_b.population])
ecosystem = np.array([thing_a,thing_b,thing_c])
for i in range(0,99,1):
    species.cycle_counter += 1 
    plants.overshoot_population_model()
    for x in range(0,len(ecosystem),1):
        corpses = ecosystem[x].overshoot_population_model()
        decomposers.resources[0][0] += corpses
    plants.resources[0][0] += decomposers.overshoot_population_model()
a = 5