import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_rows", default=5000, type=int, help='number of rows')
    parser.add_argument("--max_levels", default=3, type=int, help="max number of levels")
    parser.add_argument("--min_child", default=3, type=int, help="max number of children per node")
    parser.add_argument("--max_child", default=3, type=int, help="max number of children per node")
    parser.add_argument("--abstracts", default=1, type=int, help="Abstract lines per relation")
    parser.add_argument("--boundary",default=True, action='store_true', help='Boundary in entities')
    parser.add_argument("--output", default="gen_m3", type=str, help='Prefix of the output file')
    parser.add_argument("--min_distractor_relations", default=8, type=int, help="Distractor relations about entities")
    parser.add_argument("--relation_length", default=3, type=int, help="Max relation path length")
    parser.add_argument("--backward", default=False, action='store_true', help='if true then consider backward paths too')
    parser.add_argument("--train_test_split",default=0.8, type=float, help="Training and testing split")
    parser.add_argument("--calc", default=False, action='store_true', help="Calculate max path")
    parser.add_argument("-v","--verbose", default=False, action='store_true',
                        help='print the paths')

    return parser.parse_args()