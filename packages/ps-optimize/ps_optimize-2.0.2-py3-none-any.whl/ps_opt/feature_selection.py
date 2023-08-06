"""Feature selection for machine learning models, using Particle Swarm
Optimization and cross-validation.

Particle swarm optimization (PSO) is a computational method that
optimizes a problem by iteratively improving a candidate solution
based on a given measure of quality. The algorithm works by having
a population of candidate particles called particles, which move
around in the search space according to simple mathematical formulas
over their position and velocity. Each particle's movement is
influenced by its local best-known position and the best-known
positions in the search-space, which are updated as better positions
are found by other particles.

The basic PSO algorithm starts by initializing the position and
velocity of each particle, and setting the initial best-known
position for both the particle and the entire swarm. During each
iteration, the algorithm updates each particle's velocity based
on its own best-known position and the swarm's best-known position,
and then updates the particle's position accordingly. If a particle
finds a better position, it updates its best-known position and
potentially the swarm's best-known position. This process is
repeated until a termination criterion is met.
"""

# Author: Yuen Shing Yan Hindy <yuenshingyan@gmail.com>
# License: BSD 3 clause

__all__ = ['ParticleSwarmFeatureSelectionCV']
__version__ = '2.0.0'
__author__ = 'Yuen Shing Yan Hindy'


from ps_opt._feature_selection_process import (
    _Initialization,
    _Evaluation,
    _Communication
)


class ParticleSwarmFeatureSelectionCV(_Initialization, _Evaluation, _Communication):
    """
    Class 'ParticleSwarmFeatureSelectionCV' consist of 1 method 'fit'.
    Class 'ParticleSwarmFeatureSelectionCV' inherent classes
    '_Initialization', '_Evaluation' and '_Communication' as the parent
    classes to inherent class methods from them. 5 arguments and 2 optional
    arguments are required to instantiate class 'ParticleSwarmFeatureSelectionCV'.
    """
    def __init__(self, n_particles, estimator, cv, scoring, max_iter, n_jobs=-1, verbosity=0):
        """
        Parameters
        ----------
        n_particles : int
              'n_particles' controls how many sets of probabilities
              are generated during the initialization process.

        estimator : estimator object.
            An object of that type is instantiated for each search point.
            This object is assumed to implement the scikit-learn estimator api.
            Either estimator needs to provide a ``score`` function,
            or ``scoring`` must be passed.

        cv : int, cross-validation generator or an iterable, optional
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:
              - None, to use the default 3-fold cross validation,
              - integer, to specify the number of folds in a `(Stratified)KFold`,
              - An object to be used as a cross-validation generator.
              - An iterable yielding train, test splits.
            For integer/None inputs, if the estimator is a classifier and ``y`` is
            either binary or multiclass, :class:`StratifiedKFold` is used. In all
            other cases, :class:`KFold` is used.

        scoring : string, callable or None, default=None
            A string (see model evaluation documentation) or
            a scorer callable object / function with signature
            ``scorer(estimator, X, y)``.
            If ``None``, the ``score`` method of the estimator is used.

        max_iter : int
            Determines the maximum number of iterations or how many steps
            that particles or probabilities will be updated.

        n_jobs : int, default=-1
            Number of jobs to run in parallel. At maximum there are
            ``n_points`` times ``cv`` jobs available during each iteration.

        verbosity : int, default=0
            'verbosity' controls if any messages are being print
            out during feature selection processes.
        """

        if not isinstance(n_particles, int):
            raise ValueError("Argument 'n_particles' only accept integer as input.")

        if not isinstance(cv, int):
            raise ValueError("Argument 'cv' only accept integer as input.")

        if not isinstance(scoring, str):
            raise ValueError("Argument 'scoring' only accept string as input.")

        if not isinstance(max_iter, int):
            raise ValueError("Argument 'max_iter' only accept integer as input.")

        if not isinstance(verbosity, int):
            raise ValueError("Argument 'verbosity' only accept integer as input.")

        _Initialization.__init__(self, n_particles, verbosity)
        _Evaluation.__init__(self, estimator, cv, scoring, n_jobs, verbosity)
        _Communication.__init__(self, verbosity)

        self.best_score_ = None
        self.best_features_ = None
        self.best_proba_ = None
        self.n_particles = n_particles
        self.estimator = estimator
        self.cv = cv
        self.scoring = scoring
        self.n_iter = max_iter
        self.first_iter = max_iter
        self.n_jobs = n_jobs
        self.verbosity = verbosity

    def fit(self, X, y):
        particles, velocities, global_best, global_best_particle = self._initialize(X)
        while self.n_iter > 0:
            if self.n_iter != self.first_iter and self.verbosity:
                print(f"{self._system_datetime} Update particles' velocities.")

            particles += velocities
            results = self._evaluate_performance(X, y, particles)
            global_best, global_best_particle = self._update_global_best(results, global_best, global_best_particle)
            velocities = self._calculate_velocities(particles, global_best_particle, self.n_iter)

            if self.verbosity:
                print(f"{self._system_datetime} Iteration {self.first_iter - self.n_iter} is done.")

            self.n_iter -= 1

        self.best_proba_ = particles.loc[global_best_particle[0], list(global_best_particle[1])].to_list()
        self.best_features_ = global_best_particle[1]
        self.best_score_ = global_best
