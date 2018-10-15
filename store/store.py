import os
import json

class Store:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.realpath(__file__)).split('store')[0]
        self.attribute_store = json.load(open(os.path.join(self.base_path, 'store', 'attribute_store.json')))
        self.relations_store = json.load(open(os.path.join(self.base_path, 'store', 'relations_store.json')))

        ## Relationship type has basic values 0,1 and 2, whereas the
        ## rest should be inferred. Like, child + child = 4 = grand
        self.relationship_type = {
            'SO': 1,
            'child': 2,
            'sibling': 0,
            'in-laws': 3,
            'grand': 4,
            'no-relation': -1
        }

        attr_names = [v["options"] for k,v in self.attribute_store.items()]
        self.attr_names = set([x for p in attr_names for x in p])