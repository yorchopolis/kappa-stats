#!/usr/bin/env python

from docopt import docopt
import numpy as np
import sys

usage = """Usage: kappa.py [--help] [--linear|--unweighted|--squared|--weighted <filename>] [--verbose] [--csv] --filename <filename>

-h, --help                            Show this
-l, --linear                          Linear weights for disagreements (default)
-u, --unweighted                      Cohen's Kappa (unweighted agreement/disagreement)
-s, --squared                         Squared weights for disagreements
-w <filename>, --weighted <filename>  The filename to get the Custom weights matrix from. If there are k categories, the file should contain k lines with k values in each line, whitespace-separated.
-v, --verbose                         Include number of categories and subjects in the output
-c, --csv                             For text files with comma-separated values
-f <filename>, --filename <filename>  The filename to process, with pairs of integers on each line. The values in each pair correspond to the rating that each of the two reviewers gave to a particular subject. The pairs must be whitespaced-separated (or comma-separated, with the -c flag).
"""

def get_mode(args):
    if args.get('--unweighted'):
        return 'unweighted'
    elif args.get('--squared'):
        return 'squared'
    elif args.get('--weighted'):
        weights_file = args.get('--weighted')
        return {'weighted': weights_file}
    else:
        return 'linear'

def read_ratings(csv, filename):
    try:
        if csv:
            return np.genfromtxt(filename, delimiter=',').astype(int)
        else:
            return np.genfromtxt(filename).astype(int)
    except(IOError):
        print('Bad filename: ' + filename)
        sys.exit(1)
    except(ValueError):
        print('Invalid input (the same number of integers required in each row)')
        sys.exit(1)

def read_or_build_weighted_matrix(ratings, mode):

    if isinstance(mode, dict):
        return read_weight_matrix(mode)
    else:
        try:
            categories = int(np.amax(ratings)) + 1
            return build_weight_matrix(categories, mode)
        except(ValueError):
            print('Invalid input (integers required)')
            sys.exit(1)


def read_weight_matrix(mode):
    weights_file = mode.get('weighted')
    try:
        weights = np.genfromtxt(weights_file)
    except(ValueError):
        raise ValueError("Invalid input from weights (same number of elements required in each row)")

    contains_nan = np.isnan(np.sum(weights))
    if contains_nan or weights.size == 0:
        raise ValueError("Invalid input from weights (numbers required)")
    symmetric = (weights.shape[0] == weights.shape[1] and np.allclose(weights, weights.T))
    if symmetric:
        return np.genfromtxt(weights_file)
    else:
        raise RuntimeError("Weights matrix has to be symmetric")


def build_weight_matrix(categories, mode):
    if mode == 'unweighted':
        # [[0, 1, 1],
        #  [1, 0, 1],
        #  [1, 1, 0]]
        return np.fromiter((i != j
            for i in range(categories)
            for j in range(categories)), np.int).reshape(categories, -1)
    elif mode == 'squared':
        # [[0, 1, 4],
        #  [1, 0, 1],
        #  [4, 1, 0]]
        return np.fromiter((abs(i - j) ** 2
            for i in range(categories)
            for j in range(categories)), np.int).reshape(categories, -1)
    else: # linear
        # [[0, 1, 2],
        #  [1, 0, 1],
        #  [2, 1, 0]]
        return np.fromiter((abs(i - j)
            for i in range(categories)
            for j in range(categories)), np.int).reshape(categories, -1)

def build_observed_matrix(categories, subjects, ratings):
    observed = np.zeros((categories, categories))
    for k in range(subjects):
        observed[ratings[k, 0], ratings[k, 1]] += 1

    return observed / subjects

def build_distributions_matrix(categories, subjects, ratings):
    distributions = np.zeros((categories, 2))
    for k in range(subjects):
        distributions[ratings[k, 0], 0] += 1
        distributions[ratings[k, 1], 1] += 1

    return distributions / subjects

def build_expected_matrix(categories, distributions):
    return np.fromiter((distributions[i, 0] * distributions[j, 1]
        for i in range(categories)
        for j in range(categories)), np.float).reshape(categories, -1)

def calculate_kappa(weighted, observed, expected):
    sum_expected = sum(sum(weighted * expected))
    return 1.0 - ((sum(sum(weighted * observed)) / sum_expected) if sum_expected != 0 else 0.0)

def main(args):
    mode = get_mode(args)
    ratings = read_ratings(args.get('--csv'), args.get('--filename'))
    weighted = read_or_build_weighted_matrix(ratings, mode)
    categories = weighted.shape[0]
    subjects = int(ratings.size / 2)
    observed = build_observed_matrix(categories, subjects, ratings)
    distributions = build_distributions_matrix(categories, subjects, ratings)
    expected = build_expected_matrix(categories, distributions)
    kappa = calculate_kappa(weighted, observed, expected)

    if args.get('--verbose'):
        if isinstance(mode, dict):
            mode = 'weighted with file [' + mode.get('weighted') + ']'
        print('Kappa (' + mode + '):')
        print(kappa)
        print('Categories: ' + str(categories))
        print('Subjects: ' + str(subjects))
    else:
        print(kappa)

    return kappa

if __name__ == "__main__":
    args = docopt(usage, argv=None, help=True, version=None, options_first=False)
    main(args)
