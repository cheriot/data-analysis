# Lecture Notes

# Object baysian inference: minimize the information in the prior. "Non-informative priors"
# With a bernoulli Y ~ B(θ)
# Even a uniform prior θ ~ U[0,1] = beta(1,1) where the effective sample size is 2.
# Go further and use beta(.5, .5) or even beta(.001, .001).
# The limiting case of beta(0, 0) => f(θ) proportional to θ**-1 * (1-θ)**-1
# So beta(0, 0) is not a proper density because it integrates to infinity
# (pdf always integrates to 1). Called "improper prior".
# The posterior f(θ) proportional to θ**(y-1) * (1-θ)**(n-y-1) ~ beta(y, n-y)
# posterior mean y/n = θhat
# When are improper priors ok?
# 1. When the posterior is proper. In this case, it requires at least one H and on T to the
#    beta hyperparameters are not zero.
# 2. There's often an imporoper prior that yields the same point estimates as a frequentist
#    approach with the same data, but with a posterior and the ability to make baysian
#    probability statements. (point estimates -> mean, CI)

# non-informative priors for the normal distribution
# Y ~iid N(μ,σ**2)
# Assume that σ**2 is known.
# Prior μ ~ N(0, 1000000**2) contains minimal information about μ.
# Make the deviation infinite and the probability of the mean taking any value is constant.
# f(μ) proportional to 1
# This is an improper prior because integrating the real line is infinity.
# The posterior is f(μ|y) proportional to f(y|μ) * f(y)
# more calculations
# μ|y ~ N(ybar, σ**2/n) which is also the MLE (maximum likelihood estimate)

# If σ**2 is unknown, the f(σ**2) proportional to 1 / σ**2 ~ inversegamma(0,0).
# That's an improper prior that's uniform on the log scale.
# Posterior for σ**2|y ~ inversegamma((n-1)/2, (1/2)*sum((yi-ybar)**2))

# Y ~ N(μ,σ**2)
# Something about uniform priors are sensitive to transformation so sometimes
# f(σ**2) proportional to 1 / σ**2
# and sometimes
# f(σ**2) proportional to 1
# Somehow the parameterizatin of the normal or the uniform is different.
# Instead use:
# Jeffrey's prior f(θ) proportional to sqrt(I(θ)) where I is the fisher information.
# In most cases, Jeffrey's is an improper prior.
# For normal Y ~ N(μ,σ**2)
# f(μ) proportional to 1
# f(σ**2) proportional to 1 / σ**2
# With a bernoulli Y ~ B(θ), Jeffrey's is
# f(θ) proportional to θ**-(1/2) * (1-θ)**-(1/2) proportional to beta(1/2, 1/2), which
# is actually a proper prior.

# Other things are: reference priors and maximum entropy priors.
# "Emperical bayes" is using the data to determine a prior. Such as the data mean as the prior. Can lead to reasonable point estimates, but it's sort of cheating because it uses the data twice and can lead to improper uncertainty estimates.

# Quiz 11
# Question 1
# Suppose we flip a coin five times to estimate θ, the probability of obtaining heads. We use a Bernoulli likelihood for the data and a non-informative (and improper) Beta(0,0) prior for θ. We observe the following sequence: (H, H, H, T, H).
# Because we observed at least one H and at least one T, the posterior is proper. What is the posterior distribution for θ?
# beta(y, n-y)
# beta(4, 5-4)
# beta(4, 1)

# Question 2
# Continuing the previous question, what is the posterior mean for θ? Round your answer to one decimal place.
# y/n = 4/5 = .8

# Question 3
# Consider again the thermometer calibration problem from Lesson 10.
# Assume a normal likelihood with unknown mean θ and known variance σ2=0.25. Now use the non-informative (and improper) flat prior for θ across all real numbers. This is equivalent to a conjugate normal prior with variance equal to ∞.
# You collect the following n=5 measurements: (94.6, 95.4, 96.2, 94.9, 95.9). What is the posterior distribution for θ?
# (94.6 + 95.4 + 96.2 + 94.9 + 95.9)/5 = 95.4
# μ|y ~ N(ybar, σ**2/n) which is also the MLE (maximum likelihood estimate)
#       N(95.4, .25/5)
