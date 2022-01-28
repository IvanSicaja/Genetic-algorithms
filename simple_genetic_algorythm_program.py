
#### Potrebno instalirati fuzzywuzzy modul ####

#Uključivanje potrebnih modula

from fuzzywuzzy import fuzz
import random
import string


#Definiranje željenog stringa
in_str = None

#Dužina željenog stringa
in_str_len = None

#Određivanje broja populacije
population = 20

#Određivanje maksimalnog broja generacija kroz koje će se tražiti riješenje
generations = 10000



#Definiranje klase "Agent"
class Agent:

#Definiranje konstruktora
    def __init__(self, length):

#Nasumičan odabir određenog broja slova i pridriživanje i jedan string
        self.string = ''.join(random.choice(string.ascii_letters) for _ in range(length))
        
        #Predefinirana vrijednost poklapanja s ulaznim stringom
        self.fitness = -1

#Metoda za ispisivanje "random" stringa i postotka poklapanja sa željenim stringom
    def __str__(self):

        return 'String: ' + str(self.string) + ' Fitness: ' + str(self.fitness)


 
#Definiranje funkcije Genetskih Algoritama, skraćeno ga()
def main_genetic_algorythm_function():

#Kreiranje liste agenata
    agents = init_agents(population, in_str_len)

#Iplementiranje funkcija fitness,selection, crossover, mutation kroz predefinirani broj generacija
    for generation in range(generations):
        
        #Ispis vrijednosti trenutne generacije te postotka poklapanja
        print ("Generation:"+ str(generation))

        #Proračun poklapanja određenog agenta (random primjera) s željenom sekvencom
        agents = fitness(agents)

        #Odabir 20% najboljih aganata
        agents = selection(agents)

        #Križanje određenih odabranih agenata s dobrim svojstvima
        agents = crossover(agents)

        #Mutrianje određenih agenata
        agents = mutation(agents)

#Postavljanje zadovoljavajućeg praga poklapanja određenog primjera s traženom sekvencom
        if any(agent.fitness >= 90 for agent in agents):

            print ('\nPrag poklapanja je zadovoljen! \n')
            exit(0)


#Definiranje funkcije za inicijalizacuju agenata
def init_agents(population, length):

#Inicijaliziranje određenog broja aganata
    return [Agent(length) for _ in range(population)]


#Definiranje funkcije za proračun poklapanja vrijednosti agenta s traženom sekvencom
def fitness(agents):

#Pretraživanje liste aganata
    for agent in agents:

        #Proračun postotka poklapanja vrijednosti određenog agenta s traženom vrijednošću
        agent.fitness = fuzz.ratio(agent.string, in_str)

    return agents


#Definiranje funkcije za odabir 20% najboljih primjera
def selection(agents):

#Sortiranje liste agenata pomoću funkcije "lambda" u obrnutom smijeru tj. od boljih prema lošijima
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    print ("\n".join(map(str, agents)))

    #Odabir 20% trenutno najboljih sekvenci
    agents = agents[:int(0.2 * len(agents))]

    return agents


#Definiranje funkcije za križanje odabranih primjera
def crossover(agents):


    #Kreiranje niza za dodavanje primjere nastalih križanjem
    offspring = []

    for _ in range((population - len(agents)) // 2):

        #Slučajni odabir nekog od agenta za "roditelja 1"
        parent1 = random.choice(agents)
        #Slučajni odabir nekog od agenta za "roditelja 2"
        parent2 = random.choice(agents)
        #Kreiranje novnog agenta "child1"
        child1 = Agent(in_str_len)
        #Kreiranje novnog agenta "child2"
        child2 = Agent(in_str_len)
        #Odabir "random indexa" u rasponu od vrijednosti 0 do vrijednosti dužine ulazne sekvence odnosno dužine sekvence agenta
        split = random.randint(0, in_str_len)
        #Križanje dva "roditalja" te pridavanje vrijednosti novokreiranim agentima child1 i child2
        child1.string = parent1.string[0:split] + parent2.string[split:in_str_len]
        child2.string = parent2.string[0:split] + parent1.string[split:in_str_len]

        #Dodavanje novokreiranih agenata child1 i child2 u niz "offspring" 
        offspring.append(child1)
        offspring.append(child2)
        
    #Proširivanje niza agenata nizom "offspring"
    agents.extend(offspring)
    #Vraćanje cjelokupnog izmjenjenog niza agenta
    return agents


#Definiranje funkcije za mutiranje određenih agenta
def mutation(agents):

    #Pretraživanje lista agenata
    for agent in agents:

        #Odabir djela sekvence koju je potrebno promjeniti tj. generiranje indeksa od kojeg je poželjno mutriati
        for idx, param in enumerate(agent.string):

            #Odlučijemo da ćemo mutriati 10% ili manje sekvence
            if random.uniform(0.0, 1.0) <= 0.1:

                #Zadržavanje "dobrih" dijelova sekvence te promjena dijela sekvence koji ne odgovara našim zahtjevima
                agent.string = agent.string[0:idx] + random.choice(string.ascii_letters) + agent.string[idx+1:in_str_len]
                
                return agents


if __name__ == '__main__':

    #Definiranje sekvence koju želimo dobiti pomoću genetskih algoritama
    in_str = 'Split'

    #Određivanje dužine ulazne sekvence
    in_str_len = len(in_str)

    #Primjena genetičkih funkcija za dati primjer
    main_genetic_algorythm_function()
