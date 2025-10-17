import numpy
class organism:
    def __init__(self, name, birth_rate, death_rate, population:list,reasources:list = []):
        self.name = name
        self.birth_rate = birth_rate
        self.death_rate = death_rate
        self.population = population
        self.reasources = reasources
def overshoot_population_model(Total_Time=100, birth_rate=0.15,Resource_Inputs=0):
    
    # Variables
    #-----------
    # Total_Time - number of years to run the model
    # birth_rate - rate of new births per year
    # death_rate - rate of deaths per year
    # Resource_Inputs - extra resources added each year via e.g. technological processes
    # consumption_rate - resources used by each person in each year
    consumption_rate = 1.0
    
    # Initial_Population - number of people at the start of the experiment
    # Initial_Resources - amount of resources at the start of the experiment (generic units)
    Initial_Population = 100
    Initial_Resources = 5000
    
    # Set up time array: Use spacing based on elapsed_time and Total_Time
    time = numpy.arange(0,Total_Time,step=1)
    
    # Set up arrays to track change over time
    Population = numpy.zeros(len(time))
    Resources = numpy.zeros(len(time))
    
    # Set initial conditions
    Population[0] = Initial_Population
    Resources[0] = Initial_Resources
    
    # Loop over time steps
    for i in range(1,len(time)):
        
        # Resources per person is the relationship between the two reservoirs
        resources_per_person = Resources[i-1]/Population[i-1]
        
        # death_rate now depends on the resources per person available
        if resources_per_person <= 9:
            death_rate = -0.1 * resources_per_person + 1.0
        else:
            death_rate = 0.1
        
        # Calculate the number of births that happened over the last year
        #   based on the population at the previous time [i-1]
        Births = birth_rate * Population[i-1]
        
        # Calculate the number of deaths that happened over the last year
        #   based on the population at the previous time [i-1]
        Deaths = death_rate * Population[i-1]
        
        # Population at time t is population the year before, plus the births, minus the deaths
        Population[i] = Population[i-1] + Births - Deaths
        
        # Population can't be less than zero!
        if Population[i] < 0:
            Population[i] = 0    

        # How many resources were used up? 1 resource for each person
        Resources_Used = consumption_rate * Population[i-1]
        
        # Resources at time i is resources the year before minus the consumption
        Resources[i] = Resources[i-1] - Resources_Used + Resource_Inputs
        
        # Resources can't be less than zero!
        if Resources[i] < 0:
            Resources[i] = 0
        
    return time,Population,Resources