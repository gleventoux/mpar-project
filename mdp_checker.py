import numpy as np
import random
from utils import choose
from scipy.linalg import null_space

class MDPChecker:

    def __init__(self,mdp):
        self.mdp = mdp
    
    def move(self,state,action):
        targets = self.mdp.states[state].transitions[action].targets
        weights = self.mdp.states[state].transitions[action].weights
        next = random.choices(targets,weights).pop()
        weight = weights[targets.index(next)]
        return next, weight/sum(weights)

    def launch(self):

        print("Welcome to the Markov Decision Process checker !")
        
        check = True

        while check:

            mode = choose("mode",["accessibility","itération de valeurs","q-learning","probabilités chaine de Markov","exit"])

            match mode:

                case "accessibility":
                    print("States : ",list(self.mdp.states.keys()))
                    depart = input("Sommet de départ : ")
                    fin = input("Sommet d'arrivée : ")
                    self.accessibilite(depart, fin)

                case "itération de valeurs":
                    gamma = float(input("Gamma : "))
                    epsilon = float(input("Epsilon : "))
                    self.itération_valeurs(gamma, epsilon)

                case "q-learning":
                    gamma = float(input("Gamma : "))
                    tot = int(input("Nombre d'itérations : "))
                    self.q_learning(gamma, tot)

                case "probabilités chaine de Markov":
                    self.chaine_Markov_prob()

                case "exit":
                    break

            print("Try another feature ?")
            check = "yes" == choose("answer",["yes","no"])
        
        print("See you soon !")


    def build_matrice(self):
        n = len(self.mdp.states)
        states_list = list(mdp.states.keys())
        for state in mdp.states.values() :
            for transition in state.transitions:
                vecteur = [0] * n
                somme_poids = sum(transition.weights)
                for target, weight in zip(transition.targets, transition.weights):
                    indice = states_list.index(target)
                    vecteur[indice] = weight/somme_poids
                matrice.append(vecteur)
        print(matrice)

   
    def accessibilite(self,start, end):
        states = self.mdp.states
        à_visiter = [start]
        visité = []
        accesssible = False
        while à_visiter != []:
            noeud = à_visiter.pop()
            visité.append(noeud)
            if noeud == end :
                accesssible =True
                break
            for transition in states[noeud].transitions.values() :
                for target in transition.targets :
                    if (not target in visité) and (not target in à_visiter):
                        à_visiter.append(target)
        if accesssible:
            print(f"L'état {end} est accessible depuis l'état {start}")
        else :
            print(f"L'état {end} n'est pas accessible depuis l'état {start}")


    def itération_valeurs(self,gamma, epsilon):
        states = self.mdp.states
        v0 = {state : 0 for state in states.keys()}
        v = {state : epsilon +2 for state in states.keys()}
        n = 0
        def norme(d1,d2):
            return max([abs(d1[k]-d2[k]) for k in d1.keys()])
        while norme(v,v0) > epsilon:
            v0 = v.copy()
            v={}
            v = {state.name : max([state.reward + gamma * sum([(weight/sum(transition.weights))*v0[target] for weight, target in zip(transition.weights,transition.targets) ]) for transition in state.transitions.values()]) for state in states.values()}
            n+=1
        sigma = {state.name : list(state.transitions.keys())[np.argmax([state.reward + gamma * sum([(weight/sum(transition.weights))*v0[target] for weight, target in zip(transition.weights,transition.targets) ]) for transition in state.transitions.values()])] for state in states.values()}
        print("algo itération de valeurs :\nV : ", v, "\nSigma : ", sigma)

    def q_learning(self,gamma, tot):
        states = self.mdp.states
        boucle = 1
        q = {state : {action : 0 for action in [t.action for t in states[state].transitions.values()]} for state in states.keys()}
        for k in range(tot):
            state = random.choices([key for key in states.keys()])[0]
            transition = random.choices(list(states[state].transitions.values()))[0]
            action = transition.action
            next_state, probability = self.move(state,action)
            reward = states[next_state].reward
            #update q
            actions = [t.action for t in states[next_state].transitions.values()]
            delta = reward + gamma*max([q[next_state][act] for act in actions]) -q[state][action]
            q[state][action] += delta/boucle
            boucle += 1
        print("q = ",q)

    def chaine_Markov_prob(self):
        states = self.mdp.states
        list_states = list(states.keys())
        n = len(list_states)
        P = []
        for state in list_states :
            state = states[state]
            vecteur = [0] * n
            transition = state.transitions[list(state.transitions.keys())[0]]
            somme_poids = np.sum(transition.weights)
            for target, weight in zip(transition.targets, transition.weights):
                indice = list_states.index(target)
                vecteur[indice] = weight/somme_poids
            P.append(vecteur)
        P = np.array(P)
        I = np.eye(n)
        IP = I-P
        ns = null_space(np.transpose(IP))
        q = ns[:, 0]
        if np.all(q == 0):
            print("Il n'y a pas de solution non nulle.")
        else:
            q = q / np.sum(q)
            print("La solution de l'équation est le vecteur q =", q, " où les états sont", list_states)

