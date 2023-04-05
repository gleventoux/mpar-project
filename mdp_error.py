
class MDPError : 

        def __init__(self):
            self.component = None
            self.msg = "ERROR : "
        
        def condition(self,mdp,*args):
            pass

        def print(self,*args):
            pass

class NegativeReward(MDPError):

    def __init__(self):
        super().__init__()
        self.component = "state"
        self.msg += "State {} has negative reward : {}"
        

    def print(self,*args):
        name, reward = args[0], args[1]
        print(self.msg.format(name,reward))

    def condition(self,mdp,*args):
        reward = args[1]
        return reward < 0

class NegativeWeight(MDPError):

    def __init__(self):
        super().__init__()
        self.component = "transition"
        self.msg += "Transition from state {} to state {} for action {} has negative weight : {}"


    def print(self,*args):
        start, action, targets, weights  = args[0], args[1], args[2], args[3]
        ind = [w < 0 for w in weights].index(True)
        print(self.msg.format(start,targets[ind],action,weights[ind]))

    def condition(self,mdp,*args):
        weights = args[3]
        return any([w < 0 for w in weights])

class UndeclaredState(MDPError):

    def __init__(self):
        super().__init__()
        self.component = "transition"
        self.msg += "Transition from state {} for action {} has undeclared states : {}"


    def print(self,*args):
        start, action = args[0], args[1]
        print(self.msg.format(start,action,self.undeclared_states))

    def condition(self,mdp,*args):
        start, targets = args[0], args[2]
        states = targets + [start]
        declared_states = list(mdp.states)
        self.undeclared_states = [state for state in states if state not in declared_states]
        return self.undeclared_states != []

class UndeclaredAction(MDPError):

    def __init__(self):
        super().__init__()
        self.component = "transition"
        self.msg += "Transition from state {} has undeclared action {}"

    def print(self,*args):
        start, action = args[0], args[1]
        print(self.msg.format(start,action))

    def condition(self,mdp,*args):
        action = args[1]
        return action != None and action not in mdp.actions

class StateActionDuplication(MDPError):

    def __init__(self):
        super().__init__()
        self.component = "transition"
        self.msg += "Transition from state {} for action {} is defined two times !"

    def print(self,*args):
        start, action = args[0], args[1]
        print(self.msg.format(start,action))

    def condition(self,mdp,*args):
        start, action = args[0], args[1]
        return action in list(mdp.states[start].transitions.keys())

class StateWAWAction(MDPError):

    def __init__(self):
        super().__init__()
        self.component = "transition"
        self.msg += "Transition from state {} is defined with and without action !"

    def print(self,*args):
        start = args[0]
        print(self.msg.format(start))

    def condition(self,mdp,*args):
        start, action = args[0], args[1]
        actions = list(mdp.states[start].transitions.keys())
        if action == None:
            return actions != [] and (None not in actions) 
        else:
            return actions == [None]


