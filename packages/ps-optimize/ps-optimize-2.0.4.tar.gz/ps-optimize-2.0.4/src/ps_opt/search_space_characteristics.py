import numpy as np


class Categorical:
    def __init__(self, *discrete_space):
        if len(discrete_space) == 0:
            raise ValueError("No discrete space is specified in argument 'discrete_space'.")

        if not hasattr(discrete_space, "__iter__"):
            raise ValueError("Argument 'discrete_space' must be iterable.")

        if not all(isinstance(d, str) or d is None for d in discrete_space):
            raise ValueError("Argument 'discrete_space' must only contains str or NoneType variables.")

        self.discrete_space = discrete_space
        self.space_type = "Categorical"

    def sub_space(self, sample_size):
        n_discrete_space = len(self.discrete_space)
        return [np.random.dirichlet(np.ones(n_discrete_space)).tolist() for _ in range(sample_size)]


class Real:
    def __init__(self, lower, upper, dist):
        if not np.isnan(lower) and not isinstance(lower, float):
            raise ValueError("Argument 'lower' only accepts integer as input.")

        if not np.isnan(upper) and not isinstance(upper, float):
            raise ValueError("Argument 'upper' only accepts integer as input.")

        if not isinstance(dist, str):
            raise ValueError("Argument 'dist' only accepts string as input.")

        if dist not in ("uniform", "normal", "log-normal"):
            raise ValueError("Argument 'dist' only accepts 'uniform', 'normal' or 'log-normal' as input.")

        self.lower = lower
        self.upper = upper
        self.dist = dist
        self.space_type = "Real"

    def sub_space(self, sample_size):
        if self.dist == "uniform":
            return np.random.uniform(low=self.lower, high=self.upper, size=sample_size)
        elif self.dist == "normal":
            sampling = np.arange(self.lower, self.upper + 1)
            mu = sampling.mean()
            sigma = sampling.std()
            return np.random.normal(loc=mu, scale=sigma, size=sample_size)
        elif self.dist == "log-normal":
            sampling = np.arange(self.lower, self.upper + 1)
            mu = sampling.mean()
            sigma = sampling.std()
            return np.random.lognormal(mean=mu, sigma=sigma, size=sample_size)


class Integer:
    def __init__(self, lower, upper, dist):
        if not isinstance(lower, int):
            raise ValueError("Argument 'lower' only accepts integer as input.")

        if not isinstance(upper, int):
            raise ValueError("Argument 'upper' only accepts integer as input.")

        if not isinstance(dist, str):
            raise ValueError("Argument 'dist' only accepts string as input.")

        if dist not in ("uniform", "normal", "log-normal", "exponential"):
            raise ValueError("Argument 'dist' only accepts 'uniform', 'normal', 'log-normal' or 'exponential' as input.")

        self.lower = lower
        self.upper = upper
        self.dist = dist
        self.space_type = "Integer"

    def sub_space(self, sample_size):
        sampling = np.arange(self.lower, self.upper + 1)
        mu = sampling.mean()
        sigma = sampling.std()

        if self.dist == "uniform":
            return np.random.uniform(low=self.lower, high=self.upper, size=sample_size).round().astype(int)
        elif self.dist == "normal":
            return np.random.normal(loc=mu, scale=sigma, size=sample_size).round().astype(int)
        elif self.dist == "log-normal":
            return np.random.lognormal(mean=mu, sigma=sigma, size=sample_size).round().astype(int)
        elif self.dist == "exponential":
            return np.random.exponential(scale=mu, size=sample_size).round().astype(int)
