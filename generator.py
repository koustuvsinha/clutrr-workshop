# Generate story-summary pairs

from actors.ancestry import Ancestry
from relations.builder import RelationBuilder
from tqdm import tqdm
import random
import pprint

from args import get_args
from utils.utils import split_train_test, write2file, sanity_check
from store.store import Store

store = Store()

def generate_rows(args):
    # generate
    pb = tqdm(total=args.num_rows)
    num_stories = args.num_rows
    stories_left = num_stories
    stories = []
    abstracts = []
    relation_paths = []
    anc_num = 0
    while stories_left > 0:
        anc_num += 1
        anc = Ancestry(max_levels=args.max_levels,
                       min_child=args.min_child,
                       max_child=args.max_child,
                       relationship_type=store.relationship_type)
        rb = RelationBuilder(boundary=args.boundary,
                             min_distractor_relations=args.min_distractor_relations,
                             backward=args.backward)
        rb.init_family(anc)
        sts, abs, relp = rb.make_single_story(args.relation_length, stories_left)
        stories.extend(sts)
        abstracts.extend(abs)
        relation_paths.extend(relp)
        stories_left = num_stories - len(stories)

    rows = []
    # aggregating
    for sindx in range(len(stories)):
        if sindx > num_stories:
            break
        story = stories[sindx]
        # shuffle the story
        story = random.sample(story, len(story))
        story = '. '.join(story) + '.'
        rows.append([story, abstracts[sindx], relation_paths[sindx]])
        pb.update(1)
    pb.close()
    print("{} ancestries created".format(anc_num))
    return rows


def current_config_path_stats(args):
    """
    Calculate the max path for the current configuration
    :return:
    """
    anc = Ancestry(max_levels=args.max_levels,
                   min_child=args.min_child,
                   max_child=args.max_child,
                   relationship_type=store.relationship_type)
    taken_names = anc.taken_names
    rb = RelationBuilder(boundary=args.boundary,
                         min_distractor_relations=args.min_distractor_relations,
                         backward=args.backward)
    rb.init_family(anc)
    all_paths, path_stats = rb.calc_all_pairs(num_relations=args.relation_length)
    path_rel = {}
    for path in all_paths:
        long_path = path[2]
        len_long_path = len(long_path)
        if len_long_path not in path_rel:
            path_rel[len_long_path] = []
        path_str = ''
        for mi in range(len_long_path - 1):
            na = long_path[mi]
            nb = long_path[mi + 1]
            weight = rb.inv_rel_type[rb.connected_family[na][nb]['weight']]
            if not rb.connected_forward.has_edge(na, nb) and weight not in ['sibling', 'SO']:
                weight = 'inv-' + weight
            path_str += ' -- <{}> -- '.format(weight)
        nb = long_path[len_long_path - 1]
        fw = rb.inv_rel_type[rb.connected_family[long_path[0]][nb]['weight']]
        path_str += ' ===> {}'.format(fw)
        path_rel[len_long_path].append(path_str)
    for key, val in path_rel.items():
        print("Relation length : {}".format(key - 1))
        uniq_paths = set(val)
        print("Unique paths : {}".format(len(uniq_paths)))
        print("With gender : {}".format(len(uniq_paths) * 2))
        if args.verbose:
            pprint.pprint(uniq_paths)
        #for up in uniq_paths:
        #    print(up, val.count(up))
    return path_stats


if __name__ == '__main__':
    args = get_args()
    if args.calc:
        print(current_config_path_stats(args))
        exit(0)
    rows = generate_rows(args)
    train_rows, test_rows = split_train_test(args, rows)
    train_filename = '{}_train.csv'.format(args.output)
    test_filename = '{}_test.csv'.format(args.output)
    write2file(args, train_rows, train_filename)
    write2file(args, test_rows, test_filename)
    sanity_check(train_filename, train_rows)
    sanity_check(test_filename, test_rows)







