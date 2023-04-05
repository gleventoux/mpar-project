from mdp_error import *
import sys

class MarkovDecisionProcess:

    errors = [
        NegativeReward(),
        NegativeWeight(),
        UndeclaredState(),
        UndeclaredAction(),
        StateActionDuplication(),
        StateWAWAction()
        ]

    class State:

        def __init__(self, name, reward) :
            self.name = name
            self.transitions = {}
            self.reward = reward

    class Transitions:

        def __init__(self,start,action,targets,weights):
            self.action = action
            self.targets = targets
            self.weights = weights

    def __init__(self):
        self.states = {}
        self.actions = []

    def add_state(self,name,reward):
        self.check("state",name,reward)
        self.states[name] = MarkovDecisionProcess.State(name,reward)

    def add_action(self,action):
        self.actions.append(action)

    def add_transitions(self,start,action,targets,weights):
        self.check("transition",start,action,targets,weights)
        self.states[start].transitions[action] = MarkovDecisionProcess.Transitions(start,action,targets,weights)

    def check(self,component,*args):
        for error in MarkovDecisionProcess.errors:
            if error.component == component and error.condition(self,*args):
                error.print(*args)
                sys.exit()

