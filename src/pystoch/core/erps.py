"""
pystoch.core.erps
-----------------

"""

import numpy as np
import scipy.stats.distributions as dists

def erp(func):
    func.erp = True
    return func

def prob(prob_func):
    def wrap(func):
        func.prob = prob_func
        return func
    return wrap

def continuous(func):
    func.continuous = True
    return func

def kernel(kernel_func, kernel_prob_func):
    def wrap(func):
        func.kernel = kernel_func
        func.kernel.prob = kernel_prob_func
        return func
    return wrap

#########################################################################

def _beta_pdf(x, a, b):
    """Probability density function at x of the given beta
    distribution with parameters a and b.

    See Also
    --------
    scipy.stats.distributions.beta.pmf

    """

    return dists.beta.pdf(x, a, b)

def _beta(a, b):
    if a < 0:
        raise ValueError, "a must be non-negative"
    if b < 0:
        raise ValueError, "b must be non-negative"

    return np.random.beta(a, b)

def _beta_kernel(val, a, b):
    return _beta(a, b)

def _beta_kernel_prob(new_val, val, a, b):
    return _beta_pdf(new_val, a, b)

@erp
@prob(_beta_pdf)
@kernel(_beta_kernel, _beta_kernel_prob)
def beta(a, b):
    """Draw a sample from the Beta distribution over ``[0, 1]``.
    
    Parameters
    ----------
    a : float
        Alpha, non-negative.
    b : float
        Beta, non-negative.
    size : tuple of ints, optional
        The number of samples to draw.  The ouput is packed according to
        the size given.
    
    Returns
    -------
    out : ndarray
        Array of the given shape, containing values drawn from a
        Beta distribution.

    See Also
    --------
    numpy.random.beta

    """

    return _beta(a, b)

#########################################################################

def _binomial_pmf(x, n, p):
    """Probability mass function at x of the given binomial
    distribution with parameters n and p.

    See Also
    --------
    scipy.stats.distributions.binom.pdf
    
    """
    
    return dists.binom.pmf(x, n, p)

def _binomial(n, p):
    if n <= 0:
        raise ValueError, "n must be greater than 0"
    if p < 0 or p > 1:
        raise ValueError, "p must be between 0 and 1"
     
    return np.random.binomial(n, p)

def _binomial_kernel(val, n, p):
    return _binomial(n, p)

def _binomial_kernel_prob(new_val, val, n, p):
    return _binomial_pmf(new_val, n, p)

@erp
@prob(_binomial_pmf)
@kernel(_binomial_kernel, _binomial_kernel_prob)
def binomial(n, p):
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

    See Also
    --------
    numpy.random.binomial

    """

    return _binomial(n, p)

#########################################################################

def _exponential_pdf(x, lam):
    """Probabiliy density function at x for the exponential
    distribution with scale 1 / lam.

    See Also
    --------
    scipy.stats.distributions.expon.pdf

    """
    
    return dists.expon.pdf(x, scale=(1. / lam))

def _exponential(lam):
    return np.random.exponential(1. / lam)

def _exponential_kernel(val, lam):
    return _exponential(lam)

def _exponential_kernel_prob(new_val, val, lam):
    return _exponential_pdf(new_val, lam)

@erp
@continuous
@prob(_exponential_pdf)
@kernel(_exponential_kernel, _exponential_kernel_prob)
def exponential(lam):
    """Draw a sample from an exponential distribution with scale 1 /
    lam.

    Parameters
    ----------
    lam : number
        The inverse scale parameter of the distribution

    Returns
    -------
    sample : float
        A sample from the specified distribution

    See Also
    --------
    numpy.random.exponential
    
    """
    
    return _exponential(lam)

#########################################################################

def _flip_pmf(x, weight=0.5):
    """The probability mass function for a single coin flip.

    """
    
    if x:
        return weight
    else:
        return 1 - weight

def _flip(weight=0.5):
    return np.random.uniform(0, 1) <= weight

def _flip_kernel(val, weight=0.5):
    if _flip(0.1):
        return val
    return not val

def _flip_kernel_prob(new_val, val, weight=0.5):
    if new_val == (not val):
        return 0.9
    return 0.1

@erp
@prob(_flip_pmf)
@kernel(_flip_kernel, _flip_kernel_prob)
def flip(weight=0.5):
    """Flip a fair or biased coin.

    Given the weight, flip a coin and return True if it comes up heads
    and False if it comes up tails.  If weight is not specified, then
    a fair coin is flipped.

    Parameters
    ----------
    weight : float (default=0.5)
        The weight of the coin, in the interval [0, 1].

    Returns
    -------
    sample : bool
        True with probability `weight`

    """

    if not isinstance(weight, (int, float)) or isinstance(weight, bool):
        raise ValueError, "weight must be a number"
    if weight < 0.0 or weight > 1.0:
        raise ValueError, "weight must be between 0 and 1"

    return _flip(weight)

#########################################################################

def _gamma_pdf(x, k, theta):
    """The probability density at x for a gamma distribution with
    shape k and scale theta.

    See Also
    --------
    scipy.stats.distributions.gamma.pdf

    """
    
    return dists.gamma.pdf(x, k, scale=theta)

def _gamma(k, theta):
    if k <= 0:
        raise ValueError, "k must be greater than 0"
    if theta <= 0:
        raise ValueError, "theta must be greater than 0"
    
    return np.random.gamma(k, theta)

def _gamma_kernel(val, k, theta):
    return _gamma(k, theta)

def _gamma_kernel_prob(new_val, val, k, theta):
    return _gamma_pdf(new_val, k, theta)

@erp
@continuous
@prob(_gamma_pdf)
@kernel(_gamma_kernel, _gamma_kernel_prob)
def gamma(k, theta):
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
    
    See Also
    --------
    numpy.random.gamma

    """

    return _gamma(k, theta)

#########################################################################

def _gaussian_pdf(x, mean, std):
    """The probability density at x for the gaussian distribution with
    mean `mean` and standard deviation `std`.

    See Also
    --------
    scipy.stats.distributions.norm.pdf

    """
    
    return dists.norm.pdf(x, loc=mean, scale=std)

def _gaussian(mean, std):
    return np.random.normal(mean, std)

def _gaussian_kernel(val, mean, std):
    return _gaussian(mean, std)

def _gaussian_kernel_prob(new_val, val, mean, std):
    return _gaussian_pdf(new_val, mean, std)

@erp
@continuous
@prob(_gaussian_pdf)
@kernel(_gaussian_kernel, _gaussian_kernel_prob)
def gaussian(mean, std):
    """Draw a random sample from a normal (Gaussian) distribution.
        
    Parameters
    ----------
    mean : float
        Mean ("centre") of the distribution.
    std : float
        Standard deviation (spread or "width") of the distribution.

    Returns
    -------
    sample : float
        A sample drawn from the specified Gaussian

    See Also
    --------
    numpy.random.gaussian

    """

    return _gaussian(mean, std)

#########################################################################

def _poisson_pmf(x, lam):
    """The probability mass at x for the poisson distribution with parameter `lam`.

    See Also
    --------
    scipy.stats.distributions.poisson.pmf

    """
    
    return dists.poisson.pmf(x, lam)

def _poisson(lam):
    return np.random.poisson(lam)

def _poisson_kernel(val, lam):
    return _poisson(lam)

def _poisson_kernel_prob(new_val, val, lam):
    return _poisson_pmf(new_val, lam)

@erp
@prob(_poisson_pmf)
@kernel(_poisson_kernel, _poisson_kernel_prob)
def poisson(lam):
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

    See Also
    --------
    numpy.random.poisson
           
    """
    
    return _poisson(lam)

#########################################################################

def _uniform_pdf(x, low, high):
    """The probability density at x for the uniform distribution from
    `low` to `high`.

    """
    
    return 1.0 / (high - low)

def _uniform(low, high):
    return np.random.uniform(low, high)

def _uniform_kernel(val, low, high):
    return _uniform(low, high)

def _uniform_kernel_prob(new_val, val, low, high):
    return _uniform_pdf(new_val, low, high)

@erp
@continuous
@prob(_uniform_pdf)
@kernel(_uniform_kernel, _uniform_kernel_prob)
def uniform(low, high):
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
    
    See Also
    --------
    numpy.random.uniform

    """
    
    return _uniform(low, high)

#########################################################################

def _sample_integer_pmf(x, low, high):
    if x < low or x >= high:
        return 0.0
    return 1.0 / (high - low)

def _sample_integer(low, high):
    val = np.random.randint(low, high)
    return val

def _sample_integer_kernel(val, low, high):
    return _sample_integer(low, high)

def _sample_integer_kernel_prob(new_val, val, low, high):
    return _sample_integer_pmf(new_val, low, high)

@erp
@prob(_sample_integer_pmf)
@kernel(_sample_integer_kernel, _sample_integer_kernel_prob)
def sample_integer(low, high):
    """Uniformly sample an integer in the range ``[low, high)`` (low
    inclusive, high exclusive).

    Parameters
    ----------
    low : int
        The inclusive lower bound
    high : int
        The exclusive upper bound

    Returns
    -------
    sample : int
        An integer in the range ``[low, high)``

    """
    
    return _sample_integer(low, high)

#########################################################################

def uniform_draw(values, PYSTOCHOBJ=None):
    idx = PYSTOCHOBJ.call(sample_integer, 0, len(values))
    return values[idx]
uniform_draw.random = True

#########################################################################
