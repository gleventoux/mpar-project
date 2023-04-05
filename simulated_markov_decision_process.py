from markov_decision_process import MarkovDecisionProcess
from utils import choose
import random as rd
from mdp_graph import MDPGraph

class SimulatedMarkovDecisionProcess:
    
    def __init__(self,mdp):
        self.mdp = mdp
        self.graph = MDPGraph(mdp)

    def move(self,state,action):
        targets = self.mdp.states[state].transitions[action].targets
        weights = self.mdp.states[state].transitions[action].weights
        next = rd.choices(targets,weights).pop()

    def again(self,count,iter):
        c1 = count < iter
        return c1

    def run(self,mode,iter,start):
        current = start
        count = 0
        path = [current]
        action = None
        while self.again(count,iter):
            actions = list(self.mdp.states[current].transitions.keys())
            match mode:
                case "automatique":
                    action = rd.choices(actions).pop()
                case "manuel":
                    action = choose("action",actions)
            next = self.move(current,action)
            path += [action,next]
            count += 1
        return path


    def launch(self):

        print("Welcome to the Markov Decision Process simulator !")
        
        resimulate = True

        while resimulate:

            mode = choose("mode",["automatique","manuel"])
            start = choose("fisrt state",list(self.mdp.states.keys()))
            iter = int(input("Number of iterations = "))

            self.run(mode,iter,start)

            print("Do a new simulation ?")
            resimulate = "yes" == choose("answer",["yes","no"])
        
        print("See you soon !")

    # AFFICHAGE GRAPHIQUE
    """
    def create_graph(self):
        
     
        #pos = g.vp["pos"]  # layout positions
       
      
        
       

      
                    


        pos = sfdp_layout(g)

        



     




        win.show_all()
        Gtk.main()

        """


        