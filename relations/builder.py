# This file should contain the placeholders for the relations
import networkx as nx
import random
from collections import defaultdict
import itertools as it
from actors.actor import Actor
from utils.utils import pairwise
from store.store import Store

store = Store()

class RelationBuilder:
    """
    RelationBuilder class.
    """
    def __init__(self, boundary=False,
                 min_distractor_relations=3,
                 backward=False):
        """
        Initialize relationbuilder class with a relationship file
        :param relations_file: json file containing relationship placeholders
        :param boundary: if True then put borders around name: `[name]`
        :param backward: if true, then connect nodes in both directions
        """
        self.relations_obj = store.relations_store
        self.inv_rel_type = {v:k for k,v in store.relationship_type.items()}
        self.family = None
        self.siblings = []
        self.boundary = boundary
        self.backward = backward
        self.min_distractor_relations = min_distractor_relations

    def init_family(self, anc):
        """
        Initial family
        :param anc: Ancestry object
        :return: None
        """
        self.family = anc.family
        self.siblings = self.extract_siblings()
        self.connect_everyone()

    def connect_everyone(self):
        """
        Convert the family tree into a almost fully connected graph by calculating the relations
        :return:
        """
        nodes = list(nx.dfs_preorder_nodes(self.family, 0))
        connected_graph = nx.DiGraph()
        connected_forward_graph = nx.DiGraph()
        if self.backward:
            connected_graph = nx.Graph()
        for node_a, node_b in it.combinations(nodes, 2):
            weight = self.get_weight(node_a, node_b)
            if weight >=0 and weight in self.inv_rel_type:
                if node_a not in connected_graph:
                    connected_graph.add_node(node_a, data=self.family.node[node_a]['data'])
                    connected_forward_graph.add_node(node_a, data=self.family.node[node_a]['data'])
                if node_b not in connected_graph:
                    connected_graph.add_node(node_b, data=self.family.node[node_b]['data'])
                    connected_forward_graph.add_node(node_b, data=self.family.node[node_b]['data'])
                connected_graph.add_edge(node_a, node_b, weight=weight)
                connected_forward_graph.add_edge(node_a, node_b, weight=weight)
        self.connected_family = connected_graph
        self.connected_forward = connected_forward_graph

    def get_weight(self, node_a, node_b):
        """
        Given two nodes of a graph, build a relation text from the store
        :param node_a: networkx node, e_1
        :param node_b: networkx node, e_2
        :return: weight of the relation
        """
        # determine the relation
        try:
            path = nx.shortest_path(self.family, node_a, node_b)
            if len(path) == 2:
                # direct path
                weight = self.family[node_a][node_b]['weight']
                return weight
            else:
                # indirect path
                weight = sum([self.family[na][nb]['weight'] for na, nb in pairwise(path)])
                return weight
        except nx.NetworkXNoPath as e:
            # no direct path exists, check if they are siblings
            for sibling in self.siblings:
                if node_a in sibling and node_b in sibling:
                    weight = 0
                    return weight
            return -1


    def stringify(self, node_a, node_b):
        """
        Stitch together relationships
        :param node_a:
        :param node_b:
        :return:
        """
        # if edge (node_a -> node_b) is not present in forward graph,
        # switch them
        flip = False
        if not self.connected_forward.has_edge(node_a, node_b):
            tmp = node_a
            node_a = node_b
            node_b = tmp
            flip = True
        # get node attributes
        node_a_attr = self.connected_family.node[node_a]['data']
        node_b_attr = self.connected_family.node[node_b]['data']
        weight = self.connected_family[node_a][node_b]['weight']
        relation = self.inv_rel_type[weight]
        placeholders = self.relations_obj[relation][node_b_attr.gender]
        flip_relation = relation + '_rev'
        if flip and flip_relation in self.relations_obj:
            placeholders = self.relations_obj[flip_relation][node_a_attr.gender]
        placeholder = random.choice(placeholders)
        node_a_name = node_a_attr.name
        node_b_name = node_b_attr.name
        assert node_a_name != node_b_name
        if self.boundary:
            node_a_name = '[{}]'.format(node_a_name)
            node_b_name = '[{}]'.format(node_b_name)
        text = placeholder.replace('e_1', node_a_name)
        text = text.replace('e_2', node_b_name)
        return text

    def extract_siblings(self):
        """
        Extract the siblings and store them in a variable
        Source: https://stackoverflow.com/questions/39328963/how-to-identify-unconnected-siblings-in-a-graph
        :return: None
        """
        lineage = defaultdict(list)
        siblings = []
        for node in self.family.nodes():
            lineage[frozenset(self.family.predecessors(node)), frozenset(self.family.successors(node))].append(node)
        for i in lineage.values():
            if len(i) > 1:
                siblings.append(i)
        return siblings

    def make_story(self, mode='story', lines=-1, allowed_relations=''):
        """
        Generate story
        :param mode: if story, only use "child" and "SO" relations. if abstract, only use "grand" and "sibling" relations
        :param allowed_relations: Allowed relations is a string separated by comma on which relations should feature in the abstract
        :return: text of the story
        """
        allowed_relations = allowed_relations.split(',')
        allowed_relations = list(filter(None, allowed_relations))
        if len(allowed_relations) == 0:
            allowed_relations = ['sibling','grand','in-laws']
        allowed_relations = [store.relationship_type[ar] for ar in allowed_relations]
        nodes = list(nx.dfs_preorder_nodes(self.family, 0))
        story = []
        story_w = {}
        for node_a, node_b in it.combinations(nodes, 2):
            node_a_obj = self.family.node[node_a]['data']
            node_b_obj = self.family.node[node_b]['data']
            if node_a_obj.name == node_b_obj.name:
                raise NotImplementedError("no same nodes can be in the sentence")
            weight = self.get_weight(node_a, node_b)
            if mode == 'story' and weight in [store.relationship_type['SO'], store.relationship_type['child']]:
                story.append(self.stringify(node_a_obj, node_b_obj, weight))
            elif mode == 'abstract' and weight in allowed_relations:
                if weight not in story_w:
                    story_w[weight] = []
                story_w[weight].append(self.stringify(node_a_obj, node_b_obj, weight))
        if mode == 'abstract':
            # check if all relations are present
            if len(allowed_relations) != len(story_w):
                story = []
            else:
                story = []
                for w in allowed_relations:
                    if len(story_w[w]) < lines:
                        story = []
                        break
                    story.extend(random.sample(story_w[w], lines))
                #story = random.sample(story, lines)
                if len(story) > 0:
                    assert len(story) == lines * len(allowed_relations)
        else:
            story = random.sample(story, len(story))
        story = '. '.join(story)
        return story

    def calc_all_pairs(self, num_relations=3):
        """
        Given a connected graph, calculate all possible pairs of
        paths, i.e all simple paths
        :return:
        """
        nodes = list(nx.dfs_preorder_nodes(self.connected_family, 0))
        all_pairs = []
        for node_a, node_b in it.combinations(nodes, 2):
            for path in nx.all_simple_paths(self.connected_family, node_a, node_b, cutoff=num_relations):
                path_len = len(path)
                if path_len == num_relations + 1:
                    min_path = [path[0], path[-1]]
                    if self.connected_family.has_edge(min_path[0],min_path[1]):
                        all_pairs.append((node_a, node_b, path, min_path))
                else:
                    continue
        # calculate path stats
        path_lens = [len(path_pairs[2]) - 1 for path_pairs in all_pairs]
        max_paths = max(path_lens)
        min_paths = min(path_lens)
        path_stats = {
            'max_path': max_paths,
            'min_path': min_paths,
            'num_path': len(all_pairs),
            'path_counts': [path_lens.count(pi) for pi in range(min_paths, max_paths + 1)]
        }
        return all_pairs, path_stats

    def make_single_story(self, num_relations=6, num_stories=10):
        """
        In single story mode, there will be only one abstract per story
        Idea: Select any two nodes, get its longest connected path, form the story out of the path,
        then form the abstract from the shortest connected path
        :param: min_relations: min path of relations to consider
        :param: max_relations: max path of relations to consider
        :return:
        """
        stories = []
        abstracts = []
        relation_path = [] # for debugging purposes
        # for all pairs, calculate the min paths and max paths
        all_pairs, _ = self.calc_all_pairs(num_relations=num_relations)
        if len(all_pairs) == 0:
            return [], []
        # create story-abstract pairs
        for path_pairs in all_pairs:
            node_a, node_b, max_path, min_path = path_pairs
            story = []
            path_str = ''
            for pi, (na, nb) in enumerate(pairwise(max_path)):
                text = self.stringify(na, nb)
                story.append(text)
                if pi==0:
                    story.extend(self._get_attributes(self.connected_family.node[na]['data']))
                story.extend(self._get_attributes(self.connected_family.node[nb]['data']))
                weight = self.inv_rel_type[self.connected_family[na][nb]['weight']]
                if not self.connected_forward.has_edge(na, nb) and weight not in ['sibling', 'SO']:
                    weight = 'inv-' + weight
                path_str += ' -- <{}> -- '.format(weight)
            #story = '. '.join(story) + '.'
            abstract = self.stringify(node_a, node_b) + '.'
            fw = self.inv_rel_type[self.connected_family[node_a][node_b]['weight']]
            path_str += ' ===> {}'.format(fw)
            stories.append(story)
            abstracts.append(abstract)
            relation_path.append(path_str)
            num_stories =- 1

            if num_stories == 0:
                break
        return stories, abstracts, relation_path

    def _get_attributes(self, node: Actor):
        """
        Select min_attr number of attribute text
        :param node:
        :param min_attr:
        :return:
        """
        num_attributes = len(node.attributes)
        num_select = random.randint(self.min_distractor_relations, num_attributes)
        sel_keys = random.sample(node.attributes.keys(), num_select)
        sel_attributes = [v for k,v in node.attributes.items() if k in sel_keys]
        return sel_attributes



