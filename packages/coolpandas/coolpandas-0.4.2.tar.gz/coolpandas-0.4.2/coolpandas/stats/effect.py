import numpy as np
from scipy.stats import t


def pooled_standard_deviation(sample1: np.ndarray, sample2: np.ndarray) -> float:
    """
    Compute the pooled standard deviation for two samples.

    Args:
        sample1 (np.ndarray): The first sample as a 1D NumPy array.
        sample2 (np.ndarray): The second sample as a 1D NumPy array.

    Returns:
        float: The pooled standard deviation.
    """
    var1 = np.var(sample1, ddof=1)
    var2 = np.var(sample2, ddof=1)
    n1 = len(sample1)
    n2 = len(sample2)

    s_pooled = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

    return s_pooled


def two_sample_t_test_pooled(sample1: np.ndarray, sample2: np.ndarray) -> float:
    """
    Compute the independent two-sample t-test statistic using pooled standard deviation.

    Args:
        sample1 (np.ndarray): The first sample as a 1D NumPy array.
        sample2 (np.ndarray): The second sample as a 1D NumPy array.

    Returns:
        float: The t-test statistic.
    """
    # Calculate the means of the two samples
    mean1 = np.mean(sample1)
    mean2 = np.mean(sample2)
    n1 = len(sample1)
    n2 = len(sample2)
    # Calculate the pooled standard deviation
    s_pooled = pooled_standard_deviation(sample1, sample2)
    t = (mean1 - mean2) / (s_pooled * np.sqrt(1 / n1 + 1 / n2))
    return t


def cohens_d_from_data(sample1: np.ndarray, sample2: np.ndarray) -> float:
    """
    Compute Cohen's d effect size for two samples.

    Args:
        sample1 (np.ndarray): The first sample as a 1D NumPy array.
        sample2 (np.ndarray): The second sample as a 1D NumPy array.

    Returns:
        float: The Cohen's d effect size.
    """
    # Calculate the means of the two samples
    mean1 = np.mean(sample1)
    mean2 = np.mean(sample2)
    # Calculate the pooled standard deviation
    s_pooled = pooled_standard_deviation(sample1, sample2)
    # Calculate Cohen's d effect size
    d = (mean1 - mean2) / s_pooled
    return d


def cohens_d_from_statistics(
    mean1: float, mean2: float, std1: float, std2: float, n1: int, n2: int
) -> float:
    """
    Compute Cohen's d effect size for two samples given their means and standard
    deviations.

    Args:
        mean1 (float): The mean of the first sample.
        mean2 (float): The mean of the second sample.
        std1 (float): The standard deviation of the first sample.
        std2 (float): The standard deviation of the second sample.
        n1 (int): The size of the first sample.
        n2 (int): The size of the second sample.

    Returns:
        float: The Cohen's d effect size.
    """
    # Calculate the pooled standard deviation
    s_pooled = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
    # Calculate Cohen's d effect size
    d = (mean1 - mean2) / s_pooled
    return d


def hedges_g(sample1: np.ndarray, sample2: np.ndarray) -> float:
    """
    Compute Hedge's g as a measure of effect size for two samples.

    Args:
        sample1 (np.ndarray): The first sample as a 1D NumPy array.
        sample2 (np.ndarray): The second sample as a 1D NumPy array.

    Returns:
        float: The Hedge's g value.
    """
    n1 = len(sample1)
    n2 = len(sample2)
    g = cohens_d_from_data(sample1, sample2) * (1 - (3 / (4 * (n1 + n2) - 9)))
    return g


def cohens_d_from_mde_absolute(mde_absolute: float, pooled_std_dev: float) -> float:
    """
    Compute the Cohen's d effect size given a minimal detectable effect
    (MDE) in terms of an absolute difference in means and the pooled standard deviation
    of the groups.

    Args:
        mde_absolute (float): The minimal detectable effect in terms of an absolute.
                              difference in means.
        pooled_std_dev (float): The pooled standard deviation of the groups.

    Returns:
        float: The Cohen's d effect size.
    """
    return mde_absolute / pooled_std_dev


def cohens_d_from_mde_relative(
    sample1_mean: float, mde_relative: float, pooled_std: float
) -> float:
    """
    Compute the Cohen's d effect size given a minimal detectable effect
    (MDE) in terms of an percentage difference in means and the pooled standard deviation
    of the groups.

    Args:
        mde_relative (float): The minimal detectable effect in terms of a percentage.
                              difference in means.
        pooled_std (float): The pooled standard deviation of the groups.

    Returns:
        float: The Cohen's d effect size.
    """
    return cohens_d_from_mde_absolute(sample1_mean / 100 * mde_relative, pooled_std)


def compute_bootstrap_ci_cohens_d(
    sample1, sample2, num_bootstrap_samples=10000, ci=0.95
):
    """
    Compute a confidence interval around Cohen's d effect size using bootstrap
    resampling (for small sample size).

    Args:
        sample1 (np.array): The first group of samples.
        sample2 (np.array): The second group of samples.
        num_bootstrap_samples (int): The number of bootstrap samples to generate.
        Default is 10000.
        ci (float): The desired confidence level for the interval (e.g., 0.95
        for a 95% CI). Default is 0.95.

    Returns:
        tuple: The lower and upper bounds of the confidence interval.
    """
    # Generate bootstrap samples and compute Cohen's d for each sample
    bootstrap_samples = []
    for _ in range(num_bootstrap_samples):
        bootstrap_sample1 = np.random.choice(sample1, size=len(sample1), replace=True)
        bootstrap_sample2 = np.random.choice(sample2, size=len(sample2), replace=True)
        bootstrap_samples.append(
            cohens_d_from_data(bootstrap_sample1, bootstrap_sample2)
        )

    # Compute the percentiles of the bootstrap samples to get the confidence
    # interval
    lower_bound = np.percentile(bootstrap_samples, (1 - ci) / 2 * 100)
    upper_bound = np.percentile(bootstrap_samples, (1 + ci) / 2 * 100)

    return lower_bound, upper_bound


def compute_parametric_ci_cohens_d(sample1, sample2, ci=0.95):
    """
    Compute a confidence interval around Cohen's d effect size using a parametric
    method (for large sample size).

    Args:
        sample1 (np.array): The first group of samples.
        sample2 (np.array): The second group of samples.
        ci (float): The desired confidence level for the interval (e.g., 0.95
        for a 95% CI). Default is 0.95.

    Returns:
        tuple: The lower and upper bounds of the confidence interval.
    """
    # Calculate the parameters
    n1, n2 = len(sample1), len(sample2)
    d = cohens_d_from_data(sample1, sample2)

    # Compute the standard error of Cohen's d
    std_error_d = np.sqrt((n1 + n2) / (n1 * n2) + d**2 / (2 * (n1 + n2)))

    # Compute the confidence interval for Cohen's d
    df = n1 + n2 - 2  # degrees of freedom
    t_critical = t.ppf((1 + ci) / 2, df)
    ci_lower_d = d - t_critical * std_error_d
    ci_upper_d = d + t_critical * std_error_d

    return ci_lower_d, ci_upper_d
