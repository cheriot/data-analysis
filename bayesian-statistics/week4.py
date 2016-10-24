from scipy.stats import beta, binom, gamma, invgamma

# Lecture
# y follows exp(lambda)
# gamma distribution is conjugate for exponential likelihood
# If the bus comes every 10 minutes then the rate is 1/10.
# So prior mean is 1/10.
# Select prior gamma(a, B) where a/B is 1/10.
# Choose gamma(100, 1000)
# Prior stdev is 1/100 (or sqrt(a)/B?)
# posterior = gamma(a+n, B+sum(yi))
#           = gamma(101, 1012)
# posterior mean 101/1012 = 1/10.02

# Quiz 1
# Question 1
# Recall that we used the conjugate gamma prior for λ, the arrival rate in busses per minute. Suppose our prior belief about this rate is that it should have mean 1/20 arrivals per minute with standard deviation 1/5. Then the prior is Gamma(a,b) with a=1/16.
# Find the value of b. Round your answer to two decimal places.
# a = 1/16
# a/b = 1/20
# *20, *b
# a*20 = b
# sub a
# 20/16 = b = 1.25

# Questions 2
# Bus waiting times:
# Suppose that we wish to use a prior with the same mean (1/20), but with effective sample size of one arrival. Then the prior for λ is Gamma(1,20).
# In addition to the original Y1=12, we observe the waiting times for four additional busses: Y2=15, Y3=8, Y4=13.5, Y5=25.
# Recall that with multiple (independent) observations, the posterior for λ is Gamma(α,β) where α=a+n and β=b+∑yi.
# What is the posterior mean for λ? Round your answer to two decimal places.
# prior gamma(1, 20)
# after observations is gamma(a+5, b+12+15+8+13.5+25)
# gamma(a+5, b+73.5)
# posterior gamma(6, 93.5)
# 6/(12+15+8+13.5+25+20)
# posterior mean 6/93.5 = 0.064 rounded

# Question 3
# Bus waiting times:
# Continuing Question 2, use R or Excel to find the posterior probability that λ<1/10? Round your answer to two decimal places.
g_bus = gamma(6, scale=93.5)
print('Q3) P(lambda < 1/10) = %s. Why is this so wrong?' % g_bus.cdf(1/10))
# Use R's pgamma(1/10, 6, 93.5)

# For Questions 4-10, consider the following earthquake data:
# The United States Geological Survey maintains a list of significant earthquakes worldwide. We will model the rate of earthquakes of magnitude 4.0+ in the state of California during 2015. An iid exponential model on the waiting time between significant earthquakes is appropriate if we assume: 
# * earthquake events are independent,
# * the rate at which earthquakes occur does not change during the year, and
# * the earthquake hazard rate does not change (i.e., the probability of an earthquake happening tomorrow is constant regardless of whether the previous earthquake was yesterday or 100 days ago).

# Question 4
# Let Yi denote the waiting time in days between the ith earthquake and the following earthquake. Our model is Yi∼iidExponential(λ) where the expected waiting time between earthquakes is E(Y)=1/λ days.
# Assume the conjugate prior λ∼Gamma(a,b). Suppose our prior expectation for λ is 1/30, and we wish to use a prior effective sample size of one interval between earthquakes.
# What is the value of a?

# Prior mean is 1/30
# Prior effective sample size of 1
# a/b = 1/30
# gamma(1, 30)

# Question 5
# What is the value of b?
# b = 30

# Question 6
# y = (16, 8, 114, 60, 4, 23, 30, 105)

# Question 7
# The posterior distribution is λ∣y∼Gamma(α,β). What is the value of α?
# prior gamma(1, 30)
# 8 events over sum(16, 8, 114, 60, 4, 23, 30, 105) =  days
# gamma(1+8, 30+360)
# gamma(9, 390)



# Lecture 2 Notes

# Assume the variance is known and we're interested in the mean.
# (this happens in the monitoring of industrial production processes)
# X ~ N(μ, σ**2)
# The normal distribution is conjugate for itself (for its mean parameter).
# Prior μ ~ N(m, s**2)
# f(μ|x) proportional to f(x|μ) * f(μ) aka likelihood * prior
# lots of calculations
# μ|x ~ N(new m, new s**2)
# new s**2 = 1 / (n/σ**2 + 1/s**2)
# new m = (n / (n + σ**2/s**2) * x + ((σ**2/s**2) / (n + σ**2/s**2)) * m
# The new m (posterior mean) is a weighted average of the prior mean and the data mean.
# The effective sample size of the prior is the σ**2/s**2. Intuitively, the more variance
# in the prior, the less information is in it.

# Assume both mean μ and variance σ**2 are unknown.
# We can specify a conjugate prior in a hierarchical fashion.
# X|μ,σ**2 ~ iid N(μ,σ**2)
# Prior for μ|σ**2 ~ N(m, σ**2/w) where w = σ**2/σμ**2 is the effective sample size of the prior. That σμ term is "some variance for the normal distribution". Whatever that means.
# Prior for σ**2 ~ inversegamma(a, B)
# lots of calculations
# Posterior for σ**2|x ~ inversegamma(
#    a + n/2,
#    B + 1/2 * sumalln((xi - xmean)**2) + n*w/(2*(n+w)) * (xmean - m)**2
# )
# Posterior for μ|σ**2,x ~ N(
#    (n*xmean + w*m) / (n+w),
#    σ**2 / (n + w)
# )
# That posterior mean can be written as the weighted average of the prior mean and data mean:
# (w / (m + w)) * m + (n / (m + w)) * xmean
# If we are interested in inference on μ and don't want to depend on σ**2 then we can
# marginalize out σ**2, integrating it out, and get
# a posterior for μ|xmean ~ t
# Also, the posterior predictive distribution is a t distribution.

# This can be extended in the multivariate case with vector notation and made increasingly
# hierarchical if we want to specify priors for m, w, a, or B.

# Quiz 2

# For Questions 1-6, consider the thermometer calibration problem from the quiz in Lesson 6.
# Suppose you are trying to calibrate a thermometer by testing the temperature it reads when water begins to boil. Because of natural variation, you take n independent measurements (experiments) to estimate θ, the mean temperature reading for this thermometer at the boiling point. Assume a normal likelihood for these data, with mean θ and known variance σ2=0.25 (which corresponds to a standard deviation of 0.5 degrees Celsius).
# Suppose your prior for θ is (conveniently) the conjugate normal. You know that at sea level, water should boil at 100 degrees Celsius, so you set the prior mean at m0=100.
# Facts:
# n measurements
# to estimate θ, the mean
# Assume a normal likelihood with mean θ and known variance σ2=0.25
# Prior is the conjugate normal with mean mnot = 100

# Question 1
# If you specify a prior variance snot**2 for θ, which of the following accurately describes the model for your measurements Yi, i=1,…,n?
# Y|θ ~ N(θ,.25) and θ ~ N(100, snot**2)

# Question 2
# You decide you want the prior to be equivalent (in effective sample size) to one measurement.
# What value should you select for s20 the prior variance of θ? Round your answer to two decimal places.
# The effective sample size of the prior is σ**2/s**2.
# σ**2/s**2 = 1 with σ**2 = .25
# s**2 = .25

# Question 3
# Thermometer calibration: 
# You collect the following n=5 measurements: (94.6, 95.4, 96.2, 94.9, 95.9).  
# What is the posterior distribution for θ?
# μ|x ~ N(
#     (n / (n + σ**2/s**2) * x + ((σ**2/s**2) / (n + σ**2/s**2)) * m,
#     1 / (n/σ**2 + 1/s**2)
# )
# m = 100
# n = 5
# σ**2 = .25 
# x = (94.6 + 95.4 + 96.2 + 94.9 + 95.9) / 5 = 95.4
# s**2 = .25
# Does this really ignore the standard deviation of the observed data? Maybe that's possible
# because we've assumed the population standard deviation is .25.
# Plug it all in to the posterior mean:
# (n / (n + σ**2/s**2) * x + ((σ**2/s**2) / (n + σ**2/s**2)) * m,
# (5 / (5 + .25/.25) * 95.4 + (.25/.25 / (5 + .25/.25)) * 100
# 5/6 * 95.4 + (1/6) * 100
# 96.1666666667
# Plug it all in to the posterior variance:
# 1 / (n/σ**2 + 1/s**2)
# 1 / (5/.25 + 1/.25)
# 0.04166666666
# Posterior mean ~ N(96.17, 0.0417)

# Question 4
# qnorm(.975, 96.17,0.042)
# 96.25232 is WRONG
# Attempt 2
# > qnorm(p=0.975, mean=96.17, sd=sqrt(0.042))
# 96.57167

# Question 5
# After collecting these data, is it reasonable to conclude that the thermometer is biased toward low values?
# Yes, we have P(θ<100∣y)>0.9999

# Question 6
# What is the posterior predictive distribution of a single future observation Y∗?
# f(y2|y1) = Integrate out theta from f(y2|theta,y1) * f(theta|y1)
# y2 independent from y1 means f(y2|theta,y1) becomes f(y2|theta)
# f(y2|y1) = f(y2|theta) * f(theta|y1)
# I have no idea what formula to plug in for those values.
# I'm guessing the posterior predictive has the same mean as the posterior for theta with
# a different standard deviation. There's a single option that fits those criteria.

# For Questions 7-10, consider the following scenario:
# Your friend moves from city A to city B and is delighted to find her favorite restaurant chain at her new location. After several meals, however, she suspects that the restaurant in city B is less generous. She decides to investigate.
# She orders the main dish on 30 randomly selected days throughout the year and records each meal's weight in grams. You still live in city A, so you assist by performing the same experiment at your restaurant. Assume that the dishes are served on identical plates (measurements subtract the plate's weight), and that your scale and your friend’s scale are consistent.

# Question 7
# Does it look normal? Mostly, but there are a few outliers.

# Question 8
# Your friend investigates the three observations above 700 grams and discovers that she had ordered the incorrect meal on those dates. She removes these observations from the data set and proceeds with the analysis using n=27.
# She assumes a normal likelihood for the data with unknown mean μ and unknown variance σ2. She uses the model presented in Lesson 10.2 where, conditional on σ2, the prior for μ is normal with mean m and variance σ2/w. Next, the marginal prior for σ2 is Inverse-Gamma(a,b).
# Your friend's prior guess on the mean dish weight is 500 grams, so we set m=500. She is not very confident with this guess, so we set the prior effective sample size w=0.1. Finally, she sets a=3 and b=200.
# We can learn more about this inverse-gamma prior by simulating draws from it. If a random variable X follows a Gamma(a,b) distribution, then 1X follows an Inverse-Gamma(a,b) distribution. Hence, we can simulate draws from a gamma distribution and take their reciprocals, which will be draws from an inverse-gamma.
# To simulate 1000 draws in R (replace a and b with their actual values):
# > z <- rgamma(n=1000, shape=a, rate=b)
# > x <- 1/z
# Simulate a large number of draws (at least 300) from the prior for σ2 and report your approximate prior mean from these draws. It does not need to be exact.
# > a=3
# > b=200
# > z <- rgamma(n=1000, shape=a, rate=b)
# > x <- 1/z
# > mean(x)
# [1] 105.7857
# n=27
# normal likelihood for the data with unknown mean μ and unknown variance σ**2

# Question 9
# With the n=27 data points, your friend calculates the sample mean y¯=609.7 and sample variance s2=1n−1∑(yi−y¯)2=401.8.
# Using the update formulas from Lesson 10.2, she calculates the following posterior distributions:
#     σ2∣y∼Inverse-Gamma(a′,b′)
#     μ∣σ2,y∼N(m′,σ2w+n)
#     where
# 
#     a′=a+n2=3+272=16.5
#     b′=b+n−12s2+wn2(w+n)(y¯−m)2=200+27−12401.8+0.1⋅272(0.1+27)(609.7−500)2=6022.9
#     m′=ny¯+wmw+n=27⋅609.7+0.1⋅5000.1+27=609.3
#     w=0.1, and w+n=27.1.
# 
#     To simulate draws from this posterior, begin by drawing values for σ2 from its posterior using the method from the preceding question. Then, plug these values for σ2 into the posterior for μ and draw from that normal distribution.
# 
#     To simulate 1000 draws in R:
#     > z <- rgamma(1000, shape=16.5, rate=6022.9)
#     > sig2 <- 1/z
#     > mu <- rnorm(1000, mean=609.3, sd=sqrt(sig2/27.1))

# Facts:
# sample mean ybar = 609.7 
# sample variance s**2 = 401.8
# Use the ditributions calculated above in R to approximate inference on μ and σ**2:
# > z <- rgamma(1000, shape=16.5, rate=6022.9)
# > sig2 <- 1/z
# > mu <- rnorm(1000, mean=609.3, sd=sqrt(sig2/27.1))
#       2.5%    97.5% 
#   601.8634 617.1776 

# Question 10
# You complete your experiment at Restaurant A with n=30 data points, which appear to be normally distributed. You calculate the sample mean y¯=622.8 and sample variance s2=1n−1∑(yi−y¯)2=403.1.
# Repeat the analysis from Question 9 using the same priors and draw samples from the posterior distribution of σ2A and μ2A (where the A denotes that these parameters are for Restaurant A).
# Treating the data from Restaurant A as independent from Restaurant B, we can now attempt to answer your friend's original question: is restaurant A more generous? To do so, we can compute posterior probabilities of hypotheses like μA>μB. This is a simple task if we have simulated draws for μA and μB. For i=1,…,N (the number of simulations drawn for each parameter), make the comparison μA>μB using the ith draw for μA and μB. Then count how many of these return a TRUE value and divide by N, the total number of simulations.
# In R (using 1000 simulated values):
# > sum( muA > muB ) / 1000
# or
# > mean( muA > muB )
# where the first argument is the logical test which compares the value of cell A1 with that of B1, 1=value_if_true, and 0=value_if_false. Copy this formula to compare all μA, μB pairs. This will yield a column of binary (0 or 1) values, which you can sum or average to approximate the posterior probability.
# Would you conclude that the main dish from restaurant A weighs more than the main dish from restaurant B on average?

# n=30
# ybar = 622.8
# s**2 = 403.1
# Priors from question 8
# a = 3
# B = 200
# w = 0.1
# m = 500
# Prior σ**2 ~ inversegamma(3, 200)
# Prior μ|σ**2 ~ N(m, something)
# Posterior for σ**2|x ~ inversegamma(
#    a + n/2,
#    B + 1/2 * sumalln((xi - xmean)**2) + n*w/(2*(n+w)) * (xmean - m)**2
# )
# a' = a + n/2 = 3 + 30/2 = 18
# b' = b + (n-1)/2 * s**2 + (w*n / (2 * (w+n))) * (ybar - m)**2
# b' = 200 + (30-1)/2 * 403.1 + (.1*30 / (2 * (.1+30)) * (622.8 - 500)**2 = 6796.437
# Posterior for σ**2|x ~ inversegamma(18, 6796.437)
# Posterior μ|σ**2,x ~ N(
#    (n * ybar + w * m) / (w + n),
#    σ**2 / (w + n)
# )
# (30 * 622.8 + .1 * 500) / (.1+30) = 622.39
# w = .1 and w+n = 30.1

# > z <- rgamma(1000, shape=18, rate=6796.437)
# > sig2 <- 1/z
# > muA <- rnorm(1000, mean=622.39, sd=sqrt(sig2/30.1))

# > z <- rgamma(1000, shape=16.5, rate=6022.9)
# > sig2 <- 1/z
# > muB <- rnorm(1000, mean=609.3, sd=sqrt(sig2/27.1))
# > quantile(x=mu, probs=c(0.025, 0.975))

# > mean( muA > muB )
