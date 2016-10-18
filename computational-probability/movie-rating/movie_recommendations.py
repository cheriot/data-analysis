#!/usr/bin/env python
"""
movie_recommendations.py
Original author: Felix Sun (6.008 TA, Fall 2015)
Modified by:
- Danielle Pace (6.008 TA, Fall 2016),
- George H. Chen (6.008/6.008.1x instructor, Fall 2016)

Please read the project instructions beforehand! Your code should go in the
blocks denoted by "YOUR CODE GOES HERE" -- you should not need to modify any
other code!
"""

import movie_data_helper
import numpy as np
import scipy
import scipy.misc
from sys import exit


def compute_posterior(prior, likelihood, y):
    """
    Use Bayes' rule for random variables to compute the posterior distribution
    of a hidden variable X, given N i.i.d. observations Y_0, Y_1, ..., Y_{N-1}.

    Hidden random variable X is assumed to take on a value in {0, 1, ..., M-1}.

    Each random variable Y_i takes on a value in {0, 1, ..., K-1}.

    Inputs
    ------
    - prior: a length M vector stored as a 1D NumPy array; prior[m] gives the
        (unconditional) probability that X = m
    - likelihood: a K row by M column matrix stored as a 2D NumPy array;
        likelihood[k, m] gives the probability that Y = k given X = m
    - y: a length-N vector stored as a 1D NumPy array; y[n] gives the observed
        value for random variable Y_n

    Output
    ------
    - posterior: a length M vector stored as a 1D NumPy array: posterior[m]
        gives the probability that X = m given
        Y_0 = y_0, ..., Y_{N-1} = y_{n-1}
    """

    # -------------------------------------------------------------------------
    # ERROR CHECKS -- DO NOT MODIFY
    #

    # check that prior probabilities sum to 1
    if np.abs(1 - np.sum(prior)) > 1e-06:
        exit('In compute_posterior: The prior probabilities need to sum to 1')

    # check that likelihood is specified as a 2D array
    if len(likelihood.shape) != 2:
        exit('In compute_posterior: The likelihood needs to be specified as ' +
             'a 2D array')

    K, M = likelihood.shape

    # make sure likelihood and prior agree on number of hidden states
    if len(prior) != M:
        exit('In compute_posterior: Mismatch in number of hidden states ' +
             'according to the prior and the likelihood.')

    # make sure the conditional distribution given each hidden state value sums
    # to 1
    for m in range(M):
        if np.abs(1 - np.sum(likelihood[:, m])) > 1e-06:
            exit('In compute_posterior: P(Y | X = %d) does not sum to 1' % m)

    #
    # END OF ERROR CHECKS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (b)
    #
    # Place your code to compute the log of the posterior here: store it in a
    # NumPy array called `log_answer`. If you exponentiate really small
    # numbers, the result is likely to underflow (i.e., it will be so small
    # that the computer will just make it 0 rather than storing the right
    # value). You need to go to log-domain. Hint: this next line is a good
    # first step.
    # log_prior = np.log(prior)

    # The formula is a repeated use of the same terms. For each m, enumerate those terms.
    def px_py_given_x(m, prior_pm):
        return [likelihood[k,m] for k in y] + [prior_pm]
    px_py_given_x_for_each_m = [px_py_given_x(m, prior_pm) for [m], prior_pm in np.ndenumerate(prior)]

    # Numerical issues cause these multiplications by small numbers to at some point just produce 0 even when the
    # product is not actually 0. This will cause problems! To avoid this issue, work in the log domain (natural log,
    # implemented using NumPy's np.log). Recall that log⁡(ab)=log⁡a+log⁡b for any a>0, and b>0 (and so log⁡(a/b)=log⁡a−log⁡b.
    # The bottom line is that your code should not be multiplying together a large list of probabilities. It should be
    # adding the log of these probabilities instead.
    #
    # Note that once you take the log of the denominator term in your answer to (b), you should encounter a log of a sum
    # of exponential terms. Please use the SciPy function scipy.misc.logsumexp to compute this log of the denominator
    # (scipy.misc.logsumexp provides a numerically stable way to compute the log of the sum of exponential terms; check
    # the SciPy documentation for how to use this function).
    log_combined_terms_for_each_m = np.sum(np.log(px_py_given_x_for_each_m), axis=1) # calculate for each x: PX=x * PY|X
    log_denominator = scipy.misc.logsumexp(log_combined_terms_for_each_m)            # sum for all x: PX=x * PY|X
    log_answer = log_combined_terms_for_each_m - log_denominator                     # Divide numerator by denominator

    #
    # END OF YOUR CODE FOR PART (b)
    # -------------------------------------------------------------------------

    # do not exponentiate before this step
    posterior = np.exp(log_answer)
    return posterior


def compute_movie_rating_likelihood(M):
    """
    Compute the rating likelihood probability distribution of Y given X where
    Y is an individual rating (takes on a value in {0, 1, ..., M-1}), and X
    is the hidden true/inherent rating of a movie (also takes on a value in
    {0, 1, ..., M-1}).

    Please refer to the instructions of the project to see what the
    likelihood for ratings should be.

    Output
    ------
    - likelihood: an M row by M column matrix stored as a 2D NumPy array;
        likelihood[k, m] gives the probability that Y = k given X = m
    """

    # define the size to begin with
    likelihood = np.zeros((M, M))

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (c)
    #
    # Remember to normalize the likelihood, so that each column is a
    # probability distribution.
    #

    alpha = 1 # normalization constant
    for y in range(M):
        for x in range(M):
            if y == x:
                likelihood[y][x] = 2 * alpha
            else:
                likelihood[y][x] = alpha / abs(y - x)

    # all columns will sum to 1
    likelihood = likelihood / np.sum(likelihood, axis=0)

    #
    # END OF YOUR CODE FOR PART (c)
    # -------------------------------------------------------------------------

    return likelihood


def infer_true_movie_ratings(num_observations=-1):
    """
    For every movie, computes the posterior distribution and MAP estimate of
    the movie's true/inherent rating given the movie's observed ratings.

    Input
    -----
    - num_observations: integer that specifies how many available ratings to
        use per movie (the default value of -1 indicates that all available
        ratings will be used).

    Output
    ------
    - posteriors: a 2D array consisting of the posterior distributions where
        the number of rows is the number of movies, and the number of columns
        is M, i.e., the number of possible ratings (remember ratings are
        0, 1, ..., M-1); posteriors[i] gives a length M vector that is the
        posterior distribution of the true/inherent rating of the i-th movie
        given ratings for the i-th movie (where for each movie, the number of
        observations used is precisely what is specified by the input variable
        `num_observations`)
    - MAP_ratings: a 1D array with length given by the number of movies;
        MAP_ratings[i] gives the true/inherent rating with the highest
        posterior probability in the distribution `posteriors[i]`
    """

    M = 11  # all of our ratings are between 0 and 10
    prior = np.array([1.0 / M] * M)  # uniform distribution
    likelihood = compute_movie_rating_likelihood(M)

    # get the list of all movie IDs to process
    movie_id_list = movie_data_helper.get_movie_id_list()
    num_movies = len(movie_id_list)

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (d)
    #
    # Your code should iterate through the movies. For each movie, your code
    # should:
    #   1. Get all the observed ratings for the movie. You can artificially
    #      limit the number of available ratings used by truncating the ratings
    #      vector according to num_observations.
    #   2. Use the ratings you retrieved and the function compute_posterior to
    #      obtain the posterior of the true/inherent rating of the movie
    #      given the observed ratings
    #   3. Find the rating for each movie that maximizes the posterior

    # These are the output variables - it's your job to fill them.
    posteriors = np.zeros((num_movies, M))

    for mIdx, movie_id in enumerate(movie_id_list):
        if mIdx != movie_id:
            exit('Confused indexes %s, %s' % (mIdx, movie_id))
        observations = movie_data_helper.get_ratings(movie_id)[:num_observations]
        posteriors[mIdx] = compute_posterior(prior, likelihood, observations)

    MAP_ratings = np.argmax(posteriors, axis=1)

    #
    # END OF YOUR CODE FOR PART (d)
    # -------------------------------------------------------------------------

    return posteriors, MAP_ratings


def compute_entropy(distribution):
    """
    Given a distribution, computes the Shannon entropy of the distribution in
    bits.

    Input
    -----
    - distribution: a 1D array of probabilities that sum to 1

    Output:
    - entropy: the Shannon entropy of the input distribution in bits
    """

    # -------------------------------------------------------------------------
    # ERROR CHECK -- DO NOT MODIFY
    #
    if np.abs(1 - np.sum(distribution)) > 1e-6:
        exit('In compute_entropy: distribution should sum to 1. Found %s' % np.sum(distribution))
    #
    # END OF ERROR CHECK
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (f)
    #
    # Be sure to:
    # - use log base 2
    # - enforce 0log0 = 0

    import math

    def calc_entropy(p):
        if p < 1e-8:
            return 0
        return p * math.log(1/p, 2)
    ventropy = np.vectorize(calc_entropy)
    entropy = ventropy(distribution).sum()

    #
    # END OF YOUR CODE FOR PART (f)
    # -------------------------------------------------------------------------

    return entropy


def compute_true_movie_rating_posterior_entropies(num_observations):
    """
    For every movie, computes the Shannon entropy (in bits) of the posterior
    distribution of the true/inherent rating of the movie given observed
    ratings.

    Input
    -----
    - num_observations: integer that specifies how many available ratings to
        use per movie (the default value of -1 indicates that all available
        ratings will be used)

    Output
    ------
    - posterior_entropies: a 1D array; posterior_entropies[i] gives the Shannon
        entropy (in bits) of the posterior distribution of the true/inherent
        rating of the i-th movie given observed ratings (with number of
        observed ratings given by the input `num_observations`)
    """

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (g)
    #
    # Make use of the compute_entropy function you coded in part (f).

    posteriors, MAP_ratings = infer_true_movie_ratings(num_observations)
    posterior_entropies = np.zeros(len(MAP_ratings))
    for i in range(len(MAP_ratings)):
        posterior_entropies[i] = compute_entropy(posteriors[i]) #[MAP_ratings[i]])

    #
    # END OF YOUR CODE FOR PART (g)
    # -------------------------------------------------------------------------

    return posterior_entropies


def main():

    # -------------------------------------------------------------------------
    # ERROR CHECKS
    #
    # Here are some error checks that you can use to test your code.

    print("Posterior calculation (few observations)")
    prior = np.array([0.6, 0.4])
    likelihood = np.array([
        [0.7, 0.98],
        [0.3, 0.02],
    ])
    y = [0]*2 + [1]*1
    print("My answer:")
    print(compute_posterior(prior, likelihood, y))
    print("Expected answer:")
    print(np.array([[0.91986917, 0.08013083]]))

    print("---")
    print("Entropy of fair coin flip")
    distribution = np.array([0.5, 0.5])
    print("My answer:")
    print(compute_entropy(distribution))
    print("Expected answer:")
    print(1.0)

    print("Entropy of coin flip where P(heads) = 0.25 and P(tails) = 0.75")
    distribution = np.array([0.25, 0.75])
    print("My answer:")
    print(compute_entropy(distribution))
    print("Expected answer:")
    print(0.811278124459)

    print("Entropy of coin flip where P(heads) = 0.75 and P(tails) = 0.25")
    distribution = np.array([0.75, 0.25])
    print("My answer:")
    print(compute_entropy(distribution))
    print("Expected answer:")
    print(0.811278124459)

    #
    # END OF ERROR CHECKS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR TESTING THE FUNCTIONS YOU HAVE WRITTEN,
    # for example, to answer the questions in part (e) and part (h)
    #
    # Place your code that calls the relevant functions here.  Make sure it's
    # easy for us graders to run your code. You may want to define multiple
    # functions for each of the parts of this problem, and call them here.

    # part (c)
    size = 2**4
    print('(c) likelihood %s' % size)
    likelihood = compute_movie_rating_likelihood(size)
    if likelihood.shape != (16, 16):
        exit('In compute_movie_rating_likelihood: Matrix size is not (M, Mj')

    print('compute_movie_rating_likelihood(3)')
    print('Mine:')
    print(compute_movie_rating_likelihood(3))
    print("""
    [[ 0.57142857  0.25        0.14285714]
     [ 0.28571429  0.5         0.28571429]
     [ 0.14285714  0.25        0.57142857]]
    """)
    # part (d)
    posteriors, MAP_ratings = infer_true_movie_ratings()

    # part (e)
    # Assume this list is stable.
    # movie_id_list = movie_data_helper.get_movie_id_list()
    # movie_titles = [movie_data_helper.get_movie_name(movie_id) for movie_id in movie_id_list]
    # print('result lengths movie_id_list %s, MAP_ratings %s, posteriors %s' % (len(movie_id_list), len(MAP_ratings), posteriors.shape))
    # results = np.column_stack((movie_id_list, MAP_ratings))
    # sort_by_map_rating = results[:,1].argsort()[::-1]
    # top_results = results[sort_by_map_rating]
    # print('top_results')
    # There are 72 movies rated 10
    # for row in top_results[:73,]:
    #     print('%s %s' % (row, movie_titles[row[0]]))

    # plt.figure(1)
    # plt.title("Average of Entropies")
    # plt.xlabel("Number of Samples")
    # plt.ylabel("E (bits)", rotation='horizontal', position=(0, 1.01))
    # plt.plot(num_entropy[0], num_entropy[1])
    # plt.show()

    print('Found row 0 %s %s' % (posteriors[0].sum(), posteriors[0]))
    zero = np.array([0.00000000e+000,   0.00000000e+000,   0.00000000e+000, 0.00000000e+000,   0.00000000e+000,   0.00000000e+000, 2.08691952e-217,   7.41913971e-104,   1.00000000e+000, 3.12235460e-048,   2.56768318e-058])
    print('Expect row 0 %s %s' % (zero.sum(), zero))
    print('Found row 368 %s %s' % (posteriors[368].sum(), posteriors[368]))
    row_368 = np.array([  1.09994247e-310,   2.34454016e-230,   6.94968263e-101, 5.15112217e-056,   1.00000000e+000,   2.01073200e-027, 3.68109845e-071,   5.25671748e-185,   5.83312733e-293, 0.00000000e+000,   0.00000000e+000])
    print('Expect row 368 %s %s' % (row_368.sum(), row_368))

    print('compute_true_movie_rating_posterior_entropies 3 %s' % len(compute_true_movie_rating_posterior_entropies(3)))
    print('compute_true_movie_rating_posterior_entropies 6 %s' % len(compute_true_movie_rating_posterior_entropies(6)))
    #
    # END OF YOUR CODE FOR TESTING
    # -------------------------------------------------------------------------


if __name__ == '__main__':
    main()
