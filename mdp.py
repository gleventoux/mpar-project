from antlr4 import *
from grammar.gramLexer import gramLexer
from grammar.gramListener import gramListener
from grammar.gramParser import gramParser

import os

from utils import choose
#from class_mdp import MDP
from markov_decision_process import MarkovDecisionProcess
from simulated_markov_decision_process import SimulatedMarkovDecisionProcess

        
class gramPrintListener(gramListener):

    def __init__(self , mdp2):
       # self.mdp = mdp
        self.mdp2 = mdp2
        
    def enterDefstates(self, ctx):
        for x, reward in zip(ctx.ID(),ctx.INT()):
            state = str(x)
            self.mdp2.add_state(str(x),int(str(reward)))
            """
            if self.mdp.init is None:
                self.mdp.init = state
            """
            print(f"States {state} with reward {reward}")
            #self.mdp.add_state_reward(state, reward)
                

    def enterDefactions(self, ctx):
        print("Actions: %s" % str([str(x) for x in ctx.ID()]))
        for x in ctx.ID():
            action = str(x)
            #self.mdp.add_action(action)
            self.mdp2.add_action(action)

    def enterTransact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        act = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with action "+ act + " and targets " + str(ids) + " with weights " + str(weights))
        #self.mdp.add_transAct(dep, act, ids, weights)
        self.mdp2.add_transitions(dep,act,ids,weights)
        
    def enterTransnoact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with no action and targets " + str(ids) + " with weights " + str(weights))
        #self.mdp.add_transNoAct(dep, ids, weights)
        self.mdp2.add_transitions(dep, None, ids, weights)

            

def main():
    mdp = MarkovDecisionProcess()
    file = choose("file", os.listdir("models"))
    lexer = gramLexer(FileStream(os.path.join("models",file)))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener(mdp)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    simulator = SimulatedMarkovDecisionProcess(mdp)
    simulator.launch()

    

    #printer.mdp.Graph(printer.mdp.init, 'mdp')
    #printer.mdp.mode()
    

   

if __name__ == '__main__':
    main()
