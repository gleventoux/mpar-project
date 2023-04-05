from markov_decision_process import MarkovDecisionProcess
from utils import choose
import random as rd
from mdp_graph import MDPGraph

class MDPSimulator:
    
    def __init__(self,mdp):
        self.mdp = mdp
        

    def move(self,state,action):
        targets = self.mdp.states[state].transitions[action].targets
        weights = self.mdp.states[state].transitions[action].weights
        next = rd.choices(targets,weights).pop()
        return next

    def again(self,mode,count,iter):
        match mode:
            case "manual":
                print("Continue ?")
                answer = choose("answer",["yes","no"])
                return answer == "yes"
            case _:
                return count < iter


    def run(self,mode,iter,start):
        current = start
        count = 0
        path = [current]
        action = None
        while self.again(mode,count,iter):
            actions = list(self.mdp.states[current].transitions.keys())
            match mode:
                case "automatic":
                    action = rd.choices(actions).pop()
                case "semi-automatic":
                    action = choose("action",actions)
                case "manual":
                    action = choose("action",actions)
            next = self.move(current,action)
            self.graph.update(current,next)
            path += [action,next]
            count += 1
            current = next
        return path


    def launch(self):

        print("Welcome to the Markov Decision Process simulator !")
        
        resimulate = True

        while resimulate:

            self.graph = MDPGraph("G",self.mdp)
            mode = choose("mode",["automatic","semi-automatic","manual","pass to the checker"])
            if mode == "pass to the checker":
                break
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


        