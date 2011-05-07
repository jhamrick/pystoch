import numpy as np

def binomial(n, p, PYSTOCHOBJ=None):
    """Draw a sample from a binomial distribution.

    The sample is drawn from a Binomial distribution with specified
    parameters, n trials and p probability of success where n is an
    integer > 0 and p is in the interval [0,1]. (n may be input as a
    float, but it is truncated to an integer in use)

    Parameters
    ----------
    n : float (but truncated to an integer)
            parameter, > 0.
    p : float
            parameter, >= 0 and <= 1

    Returns
    -------
    sample : integer
            with the value in the range [0, n]

    Notes
    -----
    The probability density for the Binomial distribution is

    .. math:: P(N) = \binom{n}{N}p^N(1-p)^{n-N},

    where :math:`n` is the number of trials, :math:`p` is the
    probability of success, and :math:`N` is the number of successes.

    When estimating the standard error of a proportion in a population
    by using a random sample, the normal distribution works well
    unless the product p*n <=5, where p = population proportion
    estimate, and n = number of samples, in which case the binomial
    distribution is used instead. For example, a sample of 15 people
    shows 4 who are left handed, and 11 who are right handed. Then p =
    4/15 = 27%. 0.27*15 = 4, so the binomial distribution should be
    used in this case.

    References
    ----------
    .. [1] Dalgaard, Peter, "Introductory Statistics with R",
           Springer-Verlag, 2002.
    .. [2] Glantz, Stanton A. "Primer of Biostatistics.", McGraw-Hill,
           Fifth Edition, 2002.
    .. [3] Lentner, Marvin, "Elementary Applied Statistics", Bogden
           and Quigley, 1972.
    .. [4] Weisstein, Eric W. "Binomial Distribution." From MathWorld--A
           Wolfram Web Resource.
           http://mathworld.wolfram.com/BinomialDistribution.html
    .. [5] Wikipedia, "Binomial-distribution",
           http://en.wikipedia.org/wiki/Binomial_distribution
                                              

    """
    if n <= 0:
        raise ValueError, "n must be greater than 0"
    if p < 0 or p > 1:
        raise ValueError, "p must be between 0 and 1"
     
    return np.random.binomial(n, p)

def dirichlet(alpha, PYSTOCHOBJ=None):
    """Draw a sample from the Dirichlet distribution.

    Draw a sample of dimension k from a Dirichlet distribution. A
    Dirichlet-distributed random variable can be seen as a
    multivariate generalization of a Beta distribution. Dirichlet pdf
    is the conjugate prior of a multinomial in Bayesian inference.
    
    P1arameters
    ----------
    alpha : 1-d array
        Parameter of the distribution (k dimension for sample of
        dimension k).
        
    Notes
    -----
    .. math:: X \approx \prod_{i=1}^{k}{x^{\alpha_i-1}_i}

    Uses the following property for computation: for each dimension,
    draw a random sample y_i from a standard gamma generator of shape
    `alpha_i`, then
    :math:`X = \frac{1}{\sum_{i=1}^k{y_i}} (y_1, \ldots, y_n)` is
    Dirichlet distributed.

    References
    ----------
    .. [1] David McKay, "Information Theory, Inference and Learning
           Algorithms," chapter 23,
           http://www.inference.phy.cam.ac.uk/mackay/
                  
    """

    if not isinstance(alpha, np.ndarray):
        alpha = np.array(alpha)
    if len(alpha.shape) > 1:
        raise ValueError, "alpha must be 1-dimensional"
    
    return np.random.dirichlet(alpha)

def exponential(scale, PYSTOCHOBJ=None):
    """Draw a sample from an exponential distribution.

    Its probability density function is
    
    .. math:: f(x; \frac{1}{\beta}) = \frac{1}{\beta} \exp(-\frac{x}{\beta}),
    
    for ``x > 0`` and 0 elsewhere. :math:`\beta` is the scale
    parameter, which is the inverse of the rate parameter
    :math:`\lambda = 1/\beta`.  The rate parameter is an alternative,
    widely used parameterization of the exponential distribution [3]_.
    
    The exponential distribution is a continuous analogue of the
    geometric distribution.  It describes many common situations, such
    as the size of raindrops measured over many rainstorms [1]_, or
    the time between page requests to Wikipedia [2]_.
    
    Parameters
    ----------
    scale : float
        The scale parameter, :math:`\beta = 1/\lambda`.
    
    References
    ----------
    .. [1] Peyton Z. Peebles Jr., "Probability, Random Variables and
           Random Signal Principles", 4th ed, 2001, p. 57.
    .. [2] "Poisson Process", Wikipedia,
           http://en.wikipedia.org/wiki/Poisson_process
    .. [3] "Exponential Distribution", Wikipedia,
           http://en.wikipedia.org/wiki/Exponential_distribution

    """
    
    return np.random.exponential(scale)

def flip(weight=0.5, PYSTOCHOBJ=None):
    """Flip a fair or biased coin.

    Given the weight, flip a coin and return True if it comes up heads
    and False if it comes up tails.  If weight is not specified, then
    a fair coin is flipped.

    Parameters
    ----------
    weight : float, optional
        The weight of the coin, in the interval [0, 1].

    """
    if weight < 0.0 or weight > 1.0:
        raise ValueError, "weight must be between 0 and 1"
    
    return np.random.uniform(0, 1) <= weight

def gamma(k, theta, PYSTOCHOBJ=None):
    """Draw a sample from a Gamma distribution.
    
    A sample is drawn from a Gamma distribution with specified
    parameters, `k` (the shape of the distribution) and `theta` (the
    scale of the distribution), where both parameters are > 0.
    
    Parameters
    ----------
    k : scalar > 0
        The shape of the gamma distribution.
    theta : scalar > 0
        The scale of the gamma distribution.
    
    Returns
    -------
    out : float
        A sample drawn from the gamma distribution.
    
    Notes
    -----
    The probability density for the Gamma distribution is
    
    .. math:: p(x) = x^{k-1}\frac{e^{-x/\theta}}{\theta^k\Gamma(k)},
    
    where :math:`k` is the shape and :math:`\theta` the scale, and
    :math:`\Gamma` is the Gamma function.
    
    The Gamma distribution is often used to model the times to failure
    of electronic components, and arises naturally in processes for
    which the waiting times between Poisson distributed events are
    relevant.
    
    References
    ----------
    .. [1] Weisstein, Eric W. "Gamma Distribution." From MathWorld--A
           Wolfram Web Resource.
           http://mathworld.wolfram.com/GammaDistribution.html
    .. [2] Wikipedia, "Gamma-distribution",
           http://en.wikipedia.org/wiki/Gamma-distribution

    """

    if k <= 0:
        raise ValueError, "k must be greater than 0"
    if theta <= 0:
        raise ValueError, "theta must be greater than 0"
    
    return np.random.gamma(shape, scale)

def gaussian(mean, std, PYSTOCHOBJ=None):
    """Draw a random sample from a normal (Gaussian) distribution.
    
    The probability density function of the normal distribution, first
    derived by De Moivre and 200 years later by both Gauss and Laplace
    independently [2]_, is often called the bell curve because of its
    characteristic shape (see the example below).
    
    The normal distributions occurs often in nature.  For example, it
    describes the commonly occurring distribution of samples
    influenced by a large number of tiny, random disturbances, each
    with its own unique distribution [2]_.
    
    Parameters
    ----------
    mean : float
        Mean ("centre") of the distribution.
    std : float
        Standard deviation (spread or "width") of the distribution.
    
    Notes
    -----
    The probability density for the Gaussian distribution is
    
    .. math:: p(x) = \frac{1}{\sqrt{ 2 \pi \sigma^2 }}
                     e^{ - \frac{ (x - \mu)^2 } {2 \sigma^2} },
    
    where :math:`\mu` is the mean and :math:`\sigma` the standard
    deviation.  The square of the standard deviation,
    :math:`\sigma^2`, is called the variance.
    
    The function has its peak at the mean, and its "spread"
    increases with the standard deviation (the function reaches 0.607
    times its maximum at :math:`x + \sigma` and :math:`x - \sigma`
    [2]_).  This implies that `pystoch.erps.gaussian` is more likely
    to return samples lying close to the mean, rather than those far
    away.
    
    References
    ----------
    .. [1] Wikipedia, "Normal distribution",
           http://en.wikipedia.org/wiki/Normal_distribution
    .. [2] P. R. Peebles Jr., "Central Limit Theorem" in "Probability, Random
           Variables and Random Signal Principles", 4th ed., 2001,
           pp. 51, 51, 125.

    """

    return np.random.normal(mu, sigma)

def log_flip(weight=-0.69314718055994529, PYSTOCHOBJ=None):
    """Flip a fair or biased coin.

    Given the weight, flip a coin with weight e ** weight and return
    True if it comes up heads and False if it comes up tails.  If
    weight is not specified, then a fair coin is flipped.

    Parameters
    ----------
    weight : float, optional
        The weight of the coin, <= 0

    """

    if weight > 0:
        raise ValueError, "weight must be less than or equal to 0"
    
    return flip(np.e ** weight)

def poisson(lam, PYSTOCHOBJ=None):
    """Draw a sample from a poisson distribution.

    Given the `lam` parameter (for lambda), which is both the mean and
    variance of the Poisson distribution, draw a sample from said
    distribution.  The sample corresponds to the number of occurrences.

    Parameters
    ----------
    lam : integer
        The parameter of the poisson distribution

    Returns
    -------
    k : integer
        The number of occurrences

    Notes
    -----
    If the expected number of occurrences in this interval is lambda,
    then the probability that there are exactly k occurrences (k being
    a non-negative integer, k = 0, 1, 2, ...) is equal to f(k,
    \lambda)=\frac{\lambda^k e^{-\lambda}}{k!},\,\!

    As the lambda parameter gets larger, the Poisson distribution
    approaches a Gaussian distribution (see pystoch.erps.gaussian).

    References
    ----------
    .. [1] Wikipedia, "Poisson distribution",
           http://en.wikipedia.org/wiki/Poisson_distribution
           
    """

    return np.random.poisson(lam)

def uniform(low, high, PYSTOCHOBJ=None):
    """Draw a sample from a uniform distribution.
    
    Samples are uniformly distributed over the half-open interval
    ``[low, high)`` (includes low, but excludes high).  In other
    words, any value within the given interval is equally likely to be
    drawn by `uniform`.
    
    Parameters
    ----------
    low : float, optional
        Lower boundary of the output interval.  All values generated will be
        greater than or equal to low.  The default value is 0.
    high : float
        Upper boundary of the output interval.  All values generated will be
        less than high.  The default value is 1.0.
    
    Returns
    -------
    out : float
        Drawn sample
    
    Notes
    -----
    The probability density function of the uniform distribution is
    
    .. math:: p(x) = \frac{1}{b - a}
    
    anywhere within the interval ``[a, b)``, and zero elsewhere.

    """
    
    return np.random.uniform(low, high)
