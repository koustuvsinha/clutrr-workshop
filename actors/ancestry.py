import networkx as nx
import numpy as np
import names
import pdb
import copy
import random
from actors.actor import Actor
from store.store import Store

store = Store()

class Ancestry:
    """
    Ancestry of people to simulate
    """
    def __init__(self, max_levels=1, min_child=1, max_child=3, p_marry=1,
                 relationship_type={'SO':1,'child':2}, taken_names=None):
        self.family = nx.DiGraph()
        self.max_levels = max_levels
        self.min_child = min_child
        self.max_child = max_child
        self.p_marry = p_marry
        self.relationship_type = relationship_type
        self.levels = 0 # keep track of the levels
        self.node_ct = 0
        self.taken_names = taken_names if taken_names else copy.deepcopy(store.attr_names) # keep track of names which are already taken
        self.simulate()

    def simulate(self):
        """
        Main function to run the simulation to create a family tree

        :return:
        """
        self.node_ct = 0
        self.levels = random.randint(1,self.max_levels)
        # we are root, for now just add one head of family
        gender = 'male'
        nodes = self.add_members(gender=gender, num=1)
        parents = nodes

        for level in range(self.max_levels):
            # build generation
            generation_nodes = []
            for node in parents:
                # marry with probability p_marry
                decision_marry = np.random.choice([True,False],1,p=[self.p_marry, 1-self.p_marry])
                if decision_marry:
                    # add the partner
                    nodes =  self.add_members(gender=self.toggle_gender(node), num=1)
                    self.make_relation(node, nodes[0], relation='SO')
                    # add the children for this parent
                    num_childs = random.randint(self.min_child, self.max_child)
                    child_nodes = self.add_members(num=num_childs)
                    if len(child_nodes) > 0:
                        for ch_node in child_nodes:
                            self.make_relation(node, ch_node, relation='child')
                            self.make_relation(nodes[0], ch_node, relation='child')
                    generation_nodes.extend(child_nodes)
            parents = generation_nodes



    def add_members(self, gender='male', num=1):
        """
        Add members into family
        :param gender: male/female. if num > 1 then randomize
        :param num: default 1.
        :return: list of node ids added, new node id
        """
        node_ct = self.node_ct
        added_nodes = []
        for x in range(num):
            if num > 1:
                gender = random.choice(['male', 'female'])
            # select a name that is not taken
            name = names.get_first_name(gender=gender)
            while name in self.taken_names:
                name = names.get_first_name(gender=gender)
            self.taken_names.add(name)
            node = Actor(
                name=name, gender=gender, node_id=node_ct)
            added_nodes.append(node)
            self.family.add_node(node_ct, data=node)
            node_ct += 1
        self.node_ct = node_ct
        return added_nodes

    def make_relation(self, node_a, node_b, relation='SO'):
        """
        Add a relation between two nodes
        :param node_a: integer id of the node
        :param node_b: integer id of the node
        :param relation: either SO->1, or child->2
        :return:
        """
        self.family.add_edge(node_a.node_id, node_b.node_id, weight=self.relationship_type[relation])

    def toggle_gender(self, node):
        if node.gender == 'male':
            return 'female'
        else:
            return 'male'


if __name__=='__main__':
    pdb.set_trace()
    anc = Ancestry()
    anc.simulate()