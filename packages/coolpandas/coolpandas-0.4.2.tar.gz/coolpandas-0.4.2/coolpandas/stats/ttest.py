import numpy as np
import statsmodels.stats.power as smp
from statsmodels.stats.weightstats import ttest_ind

from .effect import (
    cohens_d_from_mde_absolute,
    cohens_d_from_mde_relative,
    compute_bootstrap_ci_cohens_d,
    compute_parametric_ci_cohens_d,
    pooled_standard_deviation,
)


class TTestInd:
    """
    Class to perform Independent T-Test and related statistics.

    Attributes:
        control (np.ndarray): Sample data for control group.
        treatment (np.ndarray): Sample data for treatment group.
        mde_absolute (float | None): Minimum detectable effect in absolute terms.
        mde_relative (float | None): Minimum detectable effect in relative terms.
        control_n (int): Number of observations in control group.
        treatment_n (int): Number of observations in treatment group.
        ratio (float): Ratio of number of observations in treatment group to control group.
        control_mean (float): Mean of control group.
        treatment_mean (float): Mean of treatment group.
        control_std (float): Standard deviation of control group.
        treatment_std (float): Standard deviation of treatment group.
        pooled_std (float): Pooled standard deviation of control and treatment group.
        effect_size (float): Calculated effect size.
        power (float | None): Calculated test power.
        t_stat (float | None): Calculated t-statistic.
        p_value (float | None): Calculated p-value.
        ci_lower (float | None): Lower limit of confidence interval.
        ci_upper (float | None): Upper limit of confidence interval.
    """

    control: np.ndarray
    treatment: np.ndarray

    mde_absolute: float | None
    mde_relative: float | None

    control_n: int
    treatment_n: int
    ratio: float
    control_mean: float
    treatment_mean: float
    control_std: float
    treatment_std: float
    pooled_std: float
    effect_size: float

    power: float | None = None
    t_stat: float | None = None
    p_value: float | None = None
    ci_lower: float | None = None
    ci_upper: float | None = None

    def __init__(
        self,
        control: np.ndarray,
        treatment: np.ndarray,
        mde_absolute: float | None = None,
        mde_relative: float | None = None,
    ):
        """
        Initialize TTestInd with control and treatment data, and either of
        mde_absolute or mde_relative.

        Args:
            control (np.ndarray): Sample data for control group.
            treatment (np.ndarray): Sample data for treatment group.
            mde_absolute (float | None): Minimum detectable effect in absolute
            terms.
            mde_relative (float | None): Minimum detectable effect in relative
            terms.
        """
        if not mde_absolute and not mde_relative:
            raise ValueError("Either mde_absolute or mde_relative must be provided.")
        if mde_absolute and mde_relative:
            raise ValueError(
                "Only one of mde_absolute or mde_relative can be provided."
            )
        self.control = control
        self.treatment = treatment
        self.mde_absolute = mde_absolute
        self.mde_relative = mde_relative
        self.compute_samples_statistics()
        self.compute_effect_size()

    def compute_samples_statistics(self) -> None:
        """
        Compute basic statistics for control and treatment data.
        """
        self.control_n = len(self.control)
        self.treatment_n = len(self.treatment)
        self.ratio = self.treatment_n / self.control_n
        self.control_mean = np.mean(self.control)
        self.treatment_mean = np.mean(self.treatment)
        self.control_std = np.std(self.control)
        self.treatment_std = np.std(self.treatment)
        self.pooled_std = pooled_standard_deviation(self.control, self.treatment)

    def compute_effect_size(self) -> float:
        """
        Compute the effect size based on the provided minimum detectable effect.

        Returns:
            float: The computed effect size.
        """
        if self.mde_absolute:
            self.effect_size = cohens_d_from_mde_absolute(
                self.mde_absolute, self.pooled_std
            )
        else:
            self.effect_size = cohens_d_from_mde_relative(
                self.control_mean, self.mde_relative, self.pooled_std
            )
        return self.effect_size

    def conduct_test(self, alternative: str = "two-sided") -> tuple[float, float]:
        """
        Conduct the independent t-test.

        Args:
            alternative (str, optional): The alternative hypothesis, can be
            "two-sided", "larger" or "smaller". Defaults to "two-sided".

        Returns:
            tuple[float, float]: The computed t-statistic and p-value.
        """
        self.t_stat, self.p_value, _ = ttest_ind(
            self.control, self.treatment, alternative
        )
        return self.t_stat, self.p_value

    def compute_confidence_interval(
        self, percentage: float = 0.95
    ) -> tuple[float, float]:
        """
        Compute the confidence interval for the effect size.

        Args:
            percentage (float, optional): The confidence level. Defaults to 0.95.

        Returns:
            tuple[float, float]: The lower and upper limit of the confidence
            interval.
        """
        if self.control_n > 30 and self.treatment_n > 30:
            self.ci_lower, self.ci_upper = compute_parametric_ci_cohens_d(
                self.control, self.treatment, percentage
            )
        else:
            self.ci_lower, self.ci_upper = compute_bootstrap_ci_cohens_d(
                self.control, self.treatment, percentage
            )
        return self.ci_lower, self.ci_upper

    def compute_power(self, alpha: float = 0.05) -> float:
        """
        Compute the power of the test.

        Args:
            alpha (float, optional): The significance level. Defaults to 0.05.

        Returns:
            float: The computed power.
        """
        self.power = smp.tt_ind_solve_power(
            self.effect_size,
            power=None,
            nobs1=self.control_n,
            ratio=self.ratio,
            alpha=alpha,
        )
        return self.power

    def report(self) -> dict[str, int | float | str]:
        """
        Generate a report of the analysis.

        Returns:
            dict[str, int | float | str]]: A dictionary containing the number of
            samples, means, standard deviations for control and treatment groups,
            minimum detectable effects (absolute and relative), power of the
            test, t-statistic, p-value, effect size (Cohen's d), and the
            confidence interval for the effect size.
        """
        return {
            "control_n": self.control_n,
            "control_mean": round(self.control_mean, 3),
            "control_std": round(self.control_std, 3),
            "treatment_n": self.treatment_n,
            "treatment_mean": round(self.treatment_mean, 3),
            "treatment_std": round(self.treatment_std, 3),
            "mde_absolute": self.mde_absolute,
            "mde_relative": self.mde_relative,
            "power": round(self.power, 3),
            "t_stat": round(self.t_stat, 3),
            "p_value": round(self.p_value, 3),
            "cohens_d": round(self.effect_size, 3),
            "CI": f"[{round(self.ci_lower, 3)}, {round(self.ci_upper, 3)}]",
        }
