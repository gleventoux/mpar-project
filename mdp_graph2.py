from graph_tool.all import *
from gi.repository import Gtk, Gdk

class MDPGraph:

    def __init__(self,mdp):
        self.g = g = Graph()
        self.vertex = {}
        self.edges = {}
        self.actions_vertex = {}

        # Define vertex proprieties
        vname = g.new_vertex_property("string")
        vsize = g.new_vertex_property("int")
        vcurrent = g.new_vertex_property("bool")

        # Define edge proprieties
        eweight = g.new_edge_property("string")

        # Add state to the graphe
        for state in mdp.states.values():
            v = g.add_vertex()
            self.vertex[state.name] = v
            vname[v] = state.name
            vsize[v] = 10

        # Add edge to the graph
        for state in mdp.states.values():
            start = self.vertex[state.name]
            for transitions in state.transitions.values():
                action = transitions.action
                total_weight = sum(transitions.weights)
                if action != None:
                    a = g.add_vertex()
                    vname[a] = action
                    g.add_edge(start,a)
                    start = a
                for target, weight in zip(transitions.targets,transitions.weights):
                    v = self.vertex[target]
                    e = g.add_edge(start,v)
                    eweight[e] = str(weight/total_weight)

        graph_draw(self.g,output_size=(1000, 1000), vertex_color=[1,1,1,0],vertex_text=vname,edge_text=eweight,vertex_font_size=18,edge_font_size=18,
            vertex_size=vsize, edge_pen_width=1.2,
           output="price.pdf")
        

    
                

                    
            
                    
                    