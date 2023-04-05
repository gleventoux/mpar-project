import random
import graphviz 
import numpy as np

class MDP:
    states = {}

    def __init__(self):
        self.init = None
        self.actions = []


    def mode(self):
        while True:
            mode = input("1 : simulation \n2 : accessibilité \n" +
                         "3 : itération de valeurs \n4 : q-learning \n" +
                         "5 : probabilités chaine de Markov \n"
                         "Choix du mode : ")
            if mode in [f"{k}" for k in range(1, 6)]:
                break
            print("Format incorrect")
        self.mode = int(mode)
        if self.mode == 1:
            self.Simulation(self.states[self.init]).main()
        if self.mode == 2 :
            depart = input("Sommet de départ : ")
            fin = input("Sommet d'arrivée : ")
            self.Model_checking.accessibilite(depart, fin)
        if self.mode == 3 :
            gamma = float(input("Gamma : "))
            epsilon = float(input("Epsilon : "))
            self.Model_checking.itération_valeurs(gamma, epsilon)
        if self.mode == 4 :
            gamma = float(input("Gamma : "))
            tot = int(input("Nombre d'itérations : "))
            self.Model_checking.q_learning(gamma, tot)
        if self.mode == 5 :
            self.Model_checking.chaine_Markov_prob()
    class MDPException(Exception):
        pass

    class State: 
        def __init__(self,name):
            self.name = name
            self.transition_state = 0  # 0 pour N/A, 1 pour sans action, 2 pour avec actions 
            self.transitions = []
            self.reward = None
        
    class TransAct:
        def __init__(self,start,action,targets,weights):
            self.start = start
            self.action = action
            self.targets = targets
            self.weights = weights

        def actionToTarget(self):
            target = random.choices(self.targets, self.weights, k=1)[0]
            probability = self.weights[self.targets.index(target)]/np.sum(self.weights)
            return target, probability

    class TransNoAct:
        def __init__(self,start,targets,weights):
            self.start = start
            self.targets = targets
            self.weights = weights
            self.action = None
        
        def actionToTarget(self):
            target = random.choices(self.targets, self.weights, k=1)[0]
            probability = self.weights[self.targets.index(target)]/np.sum(self.weights)
            return target, probability

    def add_state(self,state):
        self.states[state] = MDP.State(state)

    def add_state_reward(self, state, reward):
        s = MDP.State(state)
        s.reward = int(str(reward))
        self.states[state] = s

    def add_action(self,action):
        self.actions.append(action)  

    def add_transAct(self, dep, act, ids, weights):
        state = self.states[dep]
        transAct = MDP.TransAct(dep, act, ids, weights)
        if state.transition_state == 1:
            raise MDP.MDPException("Un état ne peut pas avoir des transitions avec et sans actions")
        for transition in state.transitions :
            if act == transition.action:
                raise MDP.MDPException(f"L'état {dep} a 2 transitions avec l'action {act}")
        state.transitions.append(transAct)
        state.transition_state = 2        
        if not dep in MDP.states:
            #raise MDP.MDPException(f"L'état {dep} n'est pas défini")
            print(f"L'état {dep} n'est pas défini\n")
            self.states[dep] = MDP.State(dep)
        for target in ids:
            if not target in MDP.states :
                #raise MDP.MDPException(f"L'état {target} n'est pas défini")
                print(f"L'état {target} n'est pas défini\n")
                self.states[target] = MDP.State(target)
        if not act in self.actions :
            #raise MDP.MDPException(f"L'action {act} n'est pas définie")
            print(f"L'action {act} n'est pas définie\n")
            self.actions.append(act)
        for poids in weights:
            try:
                if int(poids) <= 0:
                    raise MDP.MDPException(f"Un poids de l'état {target} avec l'action {act} est négatif ou nul")
            except ValueError:
                print("Le poids est mal défini")

    def add_transNoAct(self, dep, ids, weights):
        state = self.states[dep]
        transNoAct = MDP.TransNoAct(dep, ids, weights)
        state.transitions.append(transNoAct)
        if state.transition_state == 2:
            raise MDP.MDPException("Un état ne peut pas avoir des transitions avec et sans actions")
        if state.transition_state == 1:
            raise MDP.MDPException("Un état ne peut pas avoir plusieurs transitions sans actions")
        state.transition_state = 1
        if not dep in MDP.states:
            raise MDP.MDPException(f"L'état {dep} n'est pas défini")
        for target in ids:
            if not target in MDP.states :
                raise MDP.MDPException(f"L'état {target} n'est pas défini")
        for poids in weights:
            try:
                if int(poids) <= 0:
                    raise MDP.MDPException(f"Un poids de l'état {target} est négatif ou nul")
            except ValueError:
                print("Le poids est mal défini")
        
    class Simulation:

        historique = []
        recompense = 0

        def __init__(self, curseur) -> None:
            self.curseur = curseur
            self.compteur = 0
            self.stop = False
        
        def choix_simulation(self):
            while True:
                choix = input("Types de simulation :\n1 : automatique \n2 : semi-automatique (choix des actions) \n3 : manuel \nChoix simulation : ")
                if choix in ('1', '2','3'):
                    break
                print("Format incorrect")
            while True :
                longueur = input("Nombre de transitions de la simulation : ")
                try:
                    if int(longueur) > 0:
                        longueur = int(longueur)
                        break
                    else:
                        print("Format incorrect")
                except ValueError:
                    print("Format incorrect")
            if choix == '3':
                    self.stop = True
            self.choix = int(choix)
            self.nb_transitions = longueur
        
        def next(self):
            state = self.curseur
            if state.transition_state == 0:
                return False
            if state.transition_state == 1 : # si pas d'actions
                next_state, probability = state.transitions[0].actionToTarget()
                choix_action = '*'
                if self.stop is True :
                    input("Appuyer sur Entrer pour continuer...")
            elif self.choix == 1 or len(state.transitions) == 1: # avec actions en auto ou une seule
                transition = random.choices(state.transitions)[0]
                next_state, probability = transition.actionToTarget()
                choix_action = transition.action
                if self.stop is True :
                    input("Appuyer sur Entrer pour continuer...")
            else: # avec actions en manuel
                actions = [transition.action for transition in state.transitions]
                while True :
                    print('Actions possibles : ' + ', '.join(actions))
                    choix_action = input()
                    if choix_action in actions:
                        break
                    print("Format incorrect")
                ind_action = actions.index(choix_action)
                transition = state.transitions[ind_action]
                next_state, probability = transition.actionToTarget()

            self.curseur = MDP.states[next_state]
            self.compteur += 1
            self.historique.append(choix_action)
            self.historique.append(next_state)

            #if next_state.reward != None :
            #    self.recompense += next_state.reward

            if state.transition_state == 1 :
                print(f'{self.compteur} : From {state.name} with no action to {next_state} with probability {probability}')
            else:
                print(f'{self.compteur} : From {state.name} with action {transition.action} to {next_state} with probability {probability}')
            return True

        def main(self):
            self.choix_simulation()
            self.historique.append(self.curseur.name)
            not_final_state = True
            if self.choix == 1:
                while not_final_state and self.compteur < self.nb_transitions:
                    not_final_state = self.next()    
            else:
                #graphe = MDP.Graph(self.curseur.name, 'mdp_manuel')
                while not_final_state and self.compteur < self.nb_transitions:
                    previous_node = self.curseur.name
                    not_final_state = self.next()  
                    #graphe.update(previous_node, self.curseur.name)
            if not not_final_state:
                print(f"{self.curseur.name} est un état final")
            if self.recompense != 0:
                print("reward = ", self.recompense)
            print('historique = ',self.historique)
    
    class Graph:
        
        def __init__(self, depart, nom) -> None:
            # Define the MDP as a directed graph
            g = graphviz.Digraph('G', filename='mdp.gv', engine='dot')

            # Define the nodes
            g.attr('node', shape='circle')
            g.node(depart, peripheries='2')
            for state in MDP.states.values():
                if state.name != depart:
                    g.node(state.name)

            # Define the actions and transitions
            g.attr('node', shape='point')
            colors = ['red', 'blue', 'magenta']
            ind_color = 0
            ind_action = 0
            for state in MDP.states.values():
                if state.transition_state == 0:
                    pass
                elif state.transition_state == 1:
                    transition = state.transitions[0]
                    somme_poids = np.sum(transition.weights)
                    for k in range(len(transition.targets)):
                        g.edge(state.name, transition.targets[k], label= str(transition.weights[k]/somme_poids))
                else:
                    for transition in state.transitions:
                        color = colors[ind_color%3]
                        ind_color += 1
                        g.edge(state.name, str(ind_action), label=transition.action,  dir='none', color='black', fontcolor=color)
                        somme_poids = np.sum(transition.weights)
                        for k in range(len(transition.targets)):
                            g.edge(str(ind_action), transition.targets[k], label= str(transition.weights[k]/somme_poids), color=color, fontcolor=color)
                        ind_action += 1
            # Render the graph
            g.render(nom, format='png', view=False)
            self.g = g
            self.nom = nom

        def update(self, previous_node, node):
            g = self.g
            g.node(previous_node, peripheries='1')
            g.node(node, peripheries='2')
            g.render(self.nom, format='png', view=False)
            self.g = g


    class Model_checking: # chaine de Markov ou MDP
        
        def build_matrice(states : dict):
            matrice = []
            n = len(states)
            states_list = [str(state) for state in states.keys()]
            for state in states.values() :
                for transition in state.transitions:
                    vecteur = [0 for k in range(n)]
                    somme_poids = np.sum(transition.weights)
                    for target, weight in zip(transition.targets, transition.weights):
                        indice = states_list.index(target)
                        vecteur[indice] = weight/somme_poids
                    matrice.append(vecteur)
            print(matrice)

        def accessibilite(start, end):
            states = MDP.states
            à_visiter = [start]
            visité = []
            accesssible = False
            while à_visiter != []:
                noeud = à_visiter.pop()
                visité.append(noeud)
                if noeud == end :
                    accesssible =True
                    break
                for transition in states[noeud].transitions :
                    for target in transition.targets :
                        if (not target in visité) and (not target in à_visiter):
                            à_visiter.append(target)
            if accesssible:
                print(f"L'état {end} est accessible depuis l'état {start}")
            else :
                print(f"L'état {end} n'est pas accessible depuis l'état {start}")


        def itération_valeurs(gamma, epsilon):
            states = MDP.states
            v0 = {state : 0 for state in states.keys()}
            v = {state : epsilon +2 for state in states.keys()}
            n = 0
            def norme(d1,d2):
                return max([abs(d1[k]-d2[k]) for k in d1.keys()])
            while norme(v,v0) > epsilon:
                v0 = v.copy()
                v={}
                v = {state.name : max([state.reward + gamma * sum([(weight/sum(transition.weights))*v0[target] for weight, target in zip(transition.weights,transition.targets) ]) for transition in state.transitions]) for state in states.values()}
                #for s in states.values():
                    #v[s.name] = max([0 + gamma * sum([(w/sum(t.weights))*v0[target] for w, target in zip(t.weights,t.targets) ]) for t in s.transitions])
                n+=1
            sigma = {state.name : state.transitions[np.argmax([state.reward + gamma * sum([(weight/sum(transition.weights))*v0[target] for weight, target in zip(transition.weights,transition.targets) ]) for transition in state.transitions])].action for state in states.values()}
            print("algo itération de valeurs :\nV : ", v, "\nSigma : ", sigma)

        def q_learning(gamma, tot):
            states = MDP.states
            boucle = 1
            q = {state : {action : 0 for action in [t.action for t in states[state].transitions]} for state in states.keys()}
            for k in range(tot):
                state = random.choices([key for key in states.keys()])[0]
                transition = random.choices(states[state].transitions)[0]
                action = transition.action
                next_state, probability = transition.actionToTarget()
                reward = states[next_state].reward
                #update q
                actions = [t.action for t in states[next_state].transitions]
                delta = reward + gamma*max([q[next_state][act] for act in actions]) -q[state][action]
                q[state][action] += delta/boucle
                boucle += 1
            print(q)

        def chaine_Markov_prob():
            from scipy.linalg import null_space
            states = MDP.states
            list_states = [key for key in states.keys()]
            n = len(list_states)
            P = []
            for state in list_states :
                state = states[state]
                vecteur = [0 for k in range(n)]
                transition = state.transitions[0]
                somme_poids = np.sum(transition.weights)
                for target, weight in zip(transition.targets, transition.weights):
                    indice = list_states.index(target)
                    vecteur[indice] = weight/somme_poids
                P.append(vecteur)
            P = np.array(P)
            I = np.eye(n)
            IP = I-P
            null_space = null_space(np.transpose(IP))
            q = null_space[:, 0]
            if np.all(q == 0):
                print("Il n'y a pas de solution non nulle.")
            else:
                q = q / np.sum(q)
                print("La solution de l'équation est le vecteur q =", q, " où les états sont", list_states)






if __name__=='__main__':
    pass