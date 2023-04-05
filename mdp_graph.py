import graphviz

class MDPGraph:

    def __init__(self,  nom, mdp):

        depart = list(mdp.states.keys())[0]
        # Define the MDP as a directed graph
        g = graphviz.Digraph('G', filename='mdp.gv', engine='dot')

        # Define the nodes
        g.attr('node', shape='circle')
        g.node(depart, peripheries='2')
        for state in mdp.states.values():
            if state.name != depart:
                g.node(state.name)

        # Define the actions and transitions
        g.attr('node', shape='point')
        colors = ['red', 'blue', 'magenta']
        ind_color = 0
        ind_action = 0
        for state in mdp.states.values():
            for transitions in state.transitions.values():
                action = transitions.action
                targets = transitions.targets
                weights = transitions.weights
                total_weight = sum(weights)
                if action == None:
                    for target, weight in zip(targets,weights):
                        g.edge(state.name, target, label= str(weight/total_weight))
                else:
                    color = colors[ind_color%3]
                    ind_color += 1
                    g.edge(state.name, str(ind_action), label=action,  dir='none', color='black', fontcolor=color)
                    for target, weight in zip(targets,weights):
                        g.edge(str(ind_action),target, label= str(weight/total_weight),color=color, fontcolor=color)
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


        