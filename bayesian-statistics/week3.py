import numpy as np
from scipy.stats import beta, binom, gamma, invgamma
import matplotlib.pyplot as plt

# Suppose we are giving two students a multiple-choice exam with 40 questions, 
# where each question has four choices. We don't know how much the students
# have studied for this exam, but we think that they will do better than just
# guessing randomly. 
# 1) What are the parameters of interest?
# 2) What is our likelihood?
# 3) What prior should we use?
# 4) What is the prior probability P(theta>.25)? P(theta>.5)? P(theta>.8)?
# 5) Suppose the first student gets 33 questions right. What is the posterior
#    distribution for theta1? P(theta1>.25)? P(theta1>.5)? P(theta1>.8)?
#    What is a 95% posterior credible interval for theta1?
# 6) Suppose the second student gets 24 questions right. What is the posterior
#    distribution for theta2? P(theta2>.25)? P(theta2>.5)? P(theta2>.8)?
#    What is a 95% posterior credible interval for theta2?
# 7) What is the posterior probability that theta1>theta2, i.e., that the 
#    first student has a better chance of getting a question right than
#    the second student?

############
# Solutions:

# 1) What are the parameters of interest?
# 1) Parameters of interest are theta1=true probability the first student
#    will answer a question correctly, and theta2=true probability the second
#    student will answer a question correctly.

# 2) What is our likelihood?
# 2) Likelihood is Binomial(40, theta), if we assume that each question is 
#    independent and that the probability a student gets each question right 
#    is the same for all questions for that student.

# 3) What prior should we use?
# 3) The conjugate prior is a beta prior. Plot the density with dbeta.
# theta=seq(from=0,to=1,by=.01)
# plot(theta,dbeta(theta,1,1),type="l")
# plot(theta,dbeta(theta,4,2),type="l")
# plot(theta,dbeta(theta,8,4),type="l")
theta = np.linspace(0, 1)
y1 = beta.pdf(theta, 1, 1)
y2 = beta.pdf(theta, 4, 2)
y3 = beta.pdf(theta, 8, 4)
plt.plot(theta, y1, 'r-', theta, y2, 'b-', theta, y3, 'g-')
plt.show()

# 4) What is the prior probability P(theta>.25)? P(theta>.5)? P(theta>.8)?
# 4) Find probabilities using the pbeta function.
# 1-pbeta(.25,8,4)
# 1-pbeta(.5,8,4)
# 1-pbeta(.8,8,4)
print('4a P(theta > .25) = %s' % (1 - beta(8, 4).cdf(.25)))
print('4b P(theta > .5) = %s' % (1 - beta(8, 4).cdf(.5)))
print('4c P(theta > .8) = %s' % (1 - beta(8, 4).cdf(.8)))
print('Expect 0.9988117, 0.8867188, 0.1611392')

# 5) Suppose the first student gets 33 questions right. What is the posterior
#    distribution for theta1? P(theta1>.25)? P(theta1>.5)? P(theta1>.8)?
#    What is a 95% posterior credible interval for theta1?
# 5) Posterior is Beta(8+33,4+40-33) = Beta(41,11)
# 41/(41+11)  # posterior mean is a / (a + b)
# 33/40       # MLE, Maximum Likelihood Estimate
# The posterior mean will be between the prior mean and the MLE.

# lines(theta,dbeta(theta,41,11))

# plot posterior first to get the right scale on the y-axis
# plot(theta,dbeta(theta,41,11),type="l")
# lines(theta,dbeta(theta,8,4),lty=2) # lty=2 means dashed line
# plot likelihood
# lines(theta,dbinom(33,size=40,p=theta),lty=3)
# plot scaled likelihood
# lines(theta,44*dbinom(33,size=40,p=theta),lty=3)
beta5 = beta(41, 11)
plt.figure()
plt.title('problem 5: beta(41,11)')
plt.plot(theta, beta.pdf(theta, 41, 11), 'r-', theta, beta.pdf(theta, 8, 4), 'b-', theta, 44*binom.pmf(theta, 40, 33/40), 'g-')
print('theta %s' % theta)
print('binom %s' % binom.pmf(theta, 40, 33/40))
plt.show()

# posterior probabilities
# 1-pbeta(.25,41,11)
# 1-pbeta(.5,41,11)
# 1-pbeta(.8,41,11)
print('5 P(theta > .25) = %s' % (1 - beta5.cdf(.25)))
print('5 P(theta > .5) = %s' % (1 - beta5.cdf(.5)))
print('5 P(theta > .8) = %s' % (1 - beta5.cdf(.8)))
print('Expect 1, 0.9999..., 0.4444...') 

# equal-tailed 95% credible interval
# qbeta(.025,41,11)
# qbeta(.975,41,11)
print('5 equal-tailed 95 percent credible interval %s' % beta5.ppf([.025, .975]))
print('Expect 0.6688..., 0.8871...')

# 6) Suppose the second student gets 24 questions right. What is the posterior
#    distribution for theta2? P(theta2>.25)? P(theta2>.5)? P(theta2>.8)?
#    What is a 95% posterior credible interval for theta2?
# 6) Posterior is Beta(8+24,4+40-24) = Beta(32,20)
# 32/(32+20)  # posterior mean
# 24/40       # MLE
beta6 = beta(32, 20)
print('6 P(theta > .25) = %s' % (1 - beta6.cdf(.25)))
print('6 P(theta > .5) = %s' % (1 - beta6.cdf(.5)))
print('6 P(theta > .8) = %s' % (1 - beta6.cdf(.8)))
print('6 equal-tailed 95 percent credible interval %s' % beta6.ppf([.025, .975]))

# plot(theta,dbeta(theta,32,20),type="l")
# lines(theta,dbeta(theta,8,4),lty=2)
# lines(theta,44*dbinom(24,size=40,p=theta),lty=3)

# 1-pbeta(.25,32,20)
# 1-pbeta(.5,32,20)
# 1-pbeta(.8,32,20)

# qbeta(.025,32,20)
# qbeta(.975,32,20)

# 7) What is the posterior probability that theta1>theta2, i.e., that the 
#    first student has a better chance of getting a question right than
#    the second student?
# 7) Estimate by simulation: draw 1,000 samples from each and see how often 
#    we observe theta1>theta2
rv5 = beta5.rvs(size=1000)
rv6 = beta6.rvs(size=1000)
print((rv5 > rv6).mean())
# theta1=rbeta(1000,41,11)
# theta2=rbeta(1000,32,20)
# mean(theta1>theta2)


# Note for other distributions:
# dgamma,pgamma,qgamma,rgamma
# dnorm,pnorm,qnorm,rnorm

# Quiz 2
print('5 P(theta < .5) = %s' % beta(1,5).cdf(.5))

# 6
# prior Beta(2, 2)
# 20 trials, 14 success, 6 failure
# posterior Beta(2+14, 2+20-14), beta(16, 8)
betaQuiz = beta(16,8)
print('7 upper end of 95 percent credible interval = %s' % betaQuiz.ppf(.975))
print('8 P(theta < .35) = %s' % (1 - betaQuiz.cdf(.35)))
# beta(16+5, 8+5-5)
# beta(2+14+5, 2+25-14-5)
# beta(21, 8)
# Effective sample size is 21 + 8 = 29, which equals a prior effective sample size of 4 + 25 observations.

# Quiz trick is that fails are the success because we're estimating failure rate!
# prior beta(2, 2)
# posterior beta(2+6, 2+20-6)
betaQuiz = beta(8, 16)
print('7 upper end of 95 percent credible interval = %s' % betaQuiz.ppf(.975))
print('8 P(theta < .35) = %s' % (betaQuiz.cdf(.35)))
# 5 more trials, 5 more success, 0 failures
# beta(8+0, 16+5-0)
betaQuiz2 = beta(8, 21)
print('9 P(theta < .35) = %s' % (betaQuiz2.cdf(.35)))

# Quiz 3
# Poisson distribution
# Gamma prior -> Gamma posterior
# gamma(a, b) -> gamma(a + sum of yi's, b + n)
# effective sample size is b
# mean of gamma = a/b
# std deviation sqrt(a)/b
# Warning: there are other ways to define parameters of gamma. They make for different
# formulas than above.

# gamma(67,5)
quizGamma = gamma(67, scale=5)
x = np.linspace(0, 20)
y1 = quizGamma.pdf(x)
print(x)
print(y1)
plt.plot(x, y1, 'r-')
plt.show()
print('gamma half %s' % quizGamma.cdf(11.2))

# Quiz 4
quiz4_beta = beta(2, 2)
print('Quiz 4, Answer 3 P(y=1) = %s' % quiz4_beta.ppf(.5))
# beta(2,2) after 10 trials and 3 successes = beta(2+3, 2+10-3)
quiz4_beta = beta(5, 9)
print('Quiz 4, Answer 4 P(y=1) = %s' % quiz4_beta.ppf(.5))
