## CLUTRR

**C**ompositional **L**anguage **U**nderstanding with **T**ext-based **R**elational **R**easoniong

A benchmark dataset generator to test relational reasoning on text.

This work will be presented at [Relational Representation Learning Workshop](https://r2learning.github.io/) during [NIPS 2018](https://nips.cc/Conferences/2018). If you use the dataset, please cite our [paper](https://arxiv.org/abs/1811.02959):

```
@ARTICLE{2018arXiv181102959S,
   author = {{Sinha}, K. and {Sodhani}, S. and {Hamilton}, W.~L. and {Pineau}, J.
  },
    title = "{Compositional Language Understanding with Text-based Relational Reasoning}",
  journal = {ArXiv e-prints},
archivePrefix = "arXiv",
   eprint = {1811.02959},
 primaryClass = "cs.CL",
 keywords = {Computer Science - Computation and Language, Computer Science - Artificial Intelligence},
     year = 2018,
    month = nov,
   adsurl = {http://adsabs.harvard.edu/abs/2018arXiv181102959S},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

### Dependencies

- [NetworkX](https://networkx.github.io/)
- [pandas](https://pypi.org/project/pandas/)
- [names](https://pypi.org/project/names/)
- [tqdm](https://pypi.org/project/tqdm/)

### Generate

```
python generator.py
```

#### Usage

```
usage: generator.py [-h] [--num_rows NUM_ROWS] [--max_levels MAX_LEVELS]
                    [--min_child MIN_CHILD] [--max_child MAX_CHILD]
                    [--abstracts ABSTRACTS] [--boundary] [--output OUTPUT]
                    [--min_distractor_relations MIN_DISTRACTOR_RELATIONS]
                    [--relation_length RELATION_LENGTH] [--backward]
                    [--train_test_split TRAIN_TEST_SPLIT] [--calc] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --num_rows NUM_ROWS   number of rows
  --max_levels MAX_LEVELS
                        max number of levels
  --min_child MIN_CHILD
                        max number of children per node
  --max_child MAX_CHILD
                        max number of children per node
  --abstracts ABSTRACTS
                        Abstract lines per relation
  --boundary            Boundary in entities
  --output OUTPUT       Prefix of the output file
  --min_distractor_relations MIN_DISTRACTOR_RELATIONS
                        Distractor relations about entities
  --relation_length RELATION_LENGTH
                        Max relation path length
  --backward            if true then consider backward paths too
  --train_test_split TRAIN_TEST_SPLIT
                        Training and testing split
  --calc                Calculate max path
  -v, --verbose         print the paths

```

#### CLUTRR v0.1

To generate the dataset used in the paper, use the following arguments

`python generate.py --num_rows 5000 --max_levels 3 --min_child 3 --max_child 3 --min_distractor_relations 8 --relation_length 3/4/5/6`

## Author

Koustuv Sinha
