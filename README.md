# Kappa Stats

This is a little Python script to generate Cohen's Kappa and Weighted Kappa measures for inter-rater reliability (or inter-rater agreement).

Cohen's Kappa is used to find the agreement between two raters and two categories. Weighted Kappa can be used for two raters and any number of ordinal categories.

A good source to understand these measures:
http://en.wikipedia.org/wiki/Cohen%27s_kappa

## Requirements
* Python 3.x
* NumPy
* docopt

## Usage

Run kappa.py from the command line.

### Example
For a quick example you can run kappa.py with one of the fixture files, e.g.

    python kappa.py -cv -f test/fixtures/comma_separated.txt -u

### Command line Options

    kappa.py [--help] [--linear|--unweighted|--squared] [--verbose] [--csv] --filename <filename>

    -h, --help                            Show this
    -l, --linear                          Linear weights for disagreements (default)
    -u, --unweighted                      Cohen's Kappa (unweighted agreement/disagreement)
    -s, --squared                         Squared weights for disagreements
    -v, --verbose                         Include number of categories and subjects in the output
    -c, --csv                             For text files with comma-separated values
    -f <filename>, --filename <filename>  The filename to process, with pairs of integers on each line. The values in each pair correspond to the rating that each of the two reviewers gave to a particular subject. The pairs must be whitespaced-separated (or comma-separated, with the -c flag).

## Running the Tests

From the command line, use the following command to run the test cases
    
    python -m pytest 

## Math
**Samples** are called **subjects** in the code.

### Matrices and Lists
What do the different lists, arrays and matrices in the code contain? Find answeres below

#### Ratings
Contains the numbers of the input file as an ndarray. For example, the missing_data.txt would produce an ndarray starting with

              [[ 1.,  0.],
               [ 2.,  1.],
               [ 2.,  3.]]
Dimensions: samples x raters = samples x 2 (= 3 x 2)
Values: ratings of type category (here, one of `{0, 1, 2, 3}`)

#### Distributions
Converts the ratings into containers of categories.
For the example above (with possible ratings out of `{0, 1, 2, 3}`) that would be
 
               [[0, 1],
                [1, 1],
                [2, 0],
                [0, 1]]
* Dimensions: categories x raters = categories x 2 (= 4 x 2)
* Values: counts
* Characteristics: sum of all values = rater x samples = 2 x samples (= 2 x 3 = 6), because every rater rated each sample once

#### Weight
Contains weights for the differences of different categories. Also an ndarray. Non-weighted with 4 categories looks like below. Find 3 x3 examples as comments in the code of `build_weight_matrix()`:

    [[0, 1, 1, 1],
      [1, 0, 1, 1],
      [1, 1, 0, 1],
      [1, 1, 1, 0]]
      
* Dimensions: categories x categories
* Characteristics: symmetric matrix, i.e. `weight_matrix[2][5] = weight_matrix[5][2]`

#### Expected
Contains a matrix obtained from the distributions matrix. For the example in this section it is:

    [[0, 0, 0, 0],
      [1, 1, 0, 1],
      [2, 2, 0, 2],
      [0, 0, 0, 0]]