import itertools as it
import numpy as np
import csv
import pandas as pd


def pairwise(iterable):
    """
    Recipe from itertools
    :param iterable:
    :return: "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    """
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a, b)

def prob_dist(rows):
    row_dict = {}
    for row in rows:
        if row[-1] not in row_dict:
            row_dict[row[-1]] = []
        row_dict[row[-1]].append(row[:2])
    rel_probs = {k: (len(v) / len(rows)) for k, v in row_dict.items()}
    return rel_probs

def split_train_test(args, rows):
    # split training testing
    r1 = prob_dist(rows)
    indices = range(len(rows))
    mask_i = np.random.choice(indices,
                              int(len(indices) * args.train_test_split),
                              replace=False)
    test_indices = [i for i in indices if i not in set(mask_i)]
    train_indices = [i for i in indices if i in set(mask_i)]
    train_rows = [rows[ti] for ti in train_indices]
    r_train = prob_dist(train_rows)
    test_rows = [rows[ti] for ti in test_indices]
    r_test = prob_dist(test_rows)
    train_rows = [row[:-1] for row in train_rows]
    test_rows = [row[:-1] for row in test_rows]

    return train_rows, test_rows

def write2file(args, rows, filename):
    with open(filename, 'w') as fp:
        for argi in vars(args):
            fp.write('# {} {}\n'.format(argi, getattr(args, argi)))
        writer = csv.writer(fp)
        writer.writerow(['story','summary'])
        for row in rows:
            writer.writerow(row)

def sanity_check(filename, rows):
    ## sanity check
    df = pd.read_csv(filename, skip_blank_lines=True, comment='#')
    print('Total rows : {}'.format(len(df)))
    assert len(rows) == len(df)