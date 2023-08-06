"""Feature selection for machine learning models, using Particle Swarm
Optimization and cross-validation. pslearn have 3 pso variants implementations.
"""

# Author: Yuen Shing Yan Hindy <yuenshingyan@gmail.com>
# License: BSD 3 clause


__all__ = [
    "ParticleSwarmSearchCV",
    "SlicedParticleSwarmSearchCV",
    "MultiSwarmParticleSwarmSearchCV"
]
__version__ = '2.0.0'
__author__ = 'Yuen Shing Yan Hindy'


import numpy as np
import itertools
from ps_opt.search_space_characteristics import Categorical, Real, Integer
from ps_opt._error import ParticlesUnderFlowError
from ps_opt._hyperparameters_tuning_process import (
    _Initialization,
    _Evaluation,
    _Communication
)


class ParticleSwarmSearchCV(_Initialization, _Evaluation, _Communication):
    def __init__(self, search_space, n_particles, estimator, cv, scoring, max_iter, n_jobs=-1, verbosity=0):
        """
       Parameters
       ----------
       search_space : dict of hyperparameters of estimator and its corresponding
            search space and prior.

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
        if not isinstance(search_space, dict):
            raise ValueError("Argument 'search_space' only accepts dictionary as input.")

        if not isinstance(n_particles, int):
            raise ValueError("Argument 'n_particles' only accepts integer as input.")

        if not isinstance(cv, int):
            raise ValueError("Argument 'cv' only accepts integer as input.")

        if not isinstance(scoring, str):
            raise ValueError("Argument 'scoring' only accepts string as input.")

        if not isinstance(max_iter, int):
            raise ValueError("Argument 'max_iter' only accepts integer as input.")

        if not isinstance(n_jobs, int):
            raise ValueError("Argument 'n_jobs' only accepts integer as input.")

        if not isinstance(verbosity, int):
            raise ValueError("Argument 'verbosity' only accepts integer as input.")

        _Initialization.__init__(self, n_particles, search_space, verbosity)
        _Evaluation.__init__(self, estimator, cv, scoring, n_jobs, verbosity)
        _Communication.__init__(self, verbosity)

        self.best_score_ = None
        self.best_params_ = None
        self.best_proba_ = None

        self.search_space = search_space
        self.n_particles = n_particles
        self.estimator = estimator
        self.cv = cv
        self.scoring = scoring
        self.n_iter = max_iter
        self.first_iter = max_iter
        self.n_jobs = n_jobs
        self.verbosity = verbosity

    def fit(self, X, y):
        particles, global_best, global_best_particle = self._initialize()
        while self.n_iter > 0:
            if self.n_iter != self.first_iter and self.verbosity:
                print(f"{self._system_datetime} Update particles' velocities.")

            results, results_evaluate = self._evaluate_performance(X, y, particles)
            global_best, global_best_particle, winner_categorical = self._update_global_best(results, results_evaluate, global_best, global_best_particle)

            velocities = self._calculate_velocities(particles, winner_categorical, global_best_particle)
            if self.verbosity:
                print(f"{self._system_datetime} Iteration {self.first_iter - self.n_iter} is done.")

            particles += velocities

            self.n_iter -= 1

        self.best_proba_ = global_best_particle.iloc[0].to_dict()
        self.best_score_ = global_best


class SlicedParticleSwarmSearchCV(_Initialization, _Evaluation, _Communication):
    def __init__(self, search_space, n_particles, estimator, cv, scoring, max_iter, n_slice, n_jobs=-1, verbosity=0):
        """
       Parameters
       ----------
       search_space : dict of hyperparameters of estimator and its corresponding
            search space and prior.

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
        if not isinstance(search_space, dict):
            raise ValueError("Argument 'search_space' only accepts dictionary as input.")

        if not isinstance(n_particles, int):
            raise ValueError("Argument 'n_particles' only accepts integer as input.")

        if not isinstance(cv, int):
            raise ValueError("Argument 'cv' only accepts integer as input.")

        if not isinstance(scoring, str):
            raise ValueError("Argument 'scoring' only accepts string as input.")

        if not isinstance(max_iter, int):
            raise ValueError("Argument 'max_iter' only accepts integer as input.")

        if not isinstance(n_slice, int):
            raise ValueError("Argument 'n_slice' only accepts integer as input.")

        if not isinstance(n_jobs, int):
            raise ValueError("Argument 'n_jobs' only accepts integer as input.")

        if not isinstance(verbosity, int):
            raise ValueError("Argument 'verbosity' only accepts integer as input.")

        if n_particles < n_slice ** len(search_space):
            raise ParticlesUnderFlowError("Number of particles is not sufficient to be distributed to all sliced searching space."
                                          "\nPlease consider increase the number of particles ('n_particles'), "
                                          "decrease the number of slices or the dimension of searching spaces."
                                          f"\nThe current number of sliced searching space is {n_slice ** len(search_space)}.")

        _Initialization.__init__(self, n_particles, search_space, verbosity)
        _Evaluation.__init__(self, estimator, cv, scoring, n_jobs, verbosity)
        _Communication.__init__(self, verbosity)

        self.best_score_ = None
        self.best_params_ = None
        self.best_proba_ = None

        self.search_space = search_space
        self.n_particles = n_particles
        self.estimator = estimator
        self.cv = cv
        self.scoring = scoring
        self.n_iter = max_iter
        self.first_iter = max_iter
        self.n_slice = n_slice
        self.n_jobs = n_jobs
        self.verbosity = verbosity

    @property
    def _sliced_search_space(self):
        all_sliced_sub_space = []
        for hyperparameter, search_space in self.search_space.items():
            if search_space.space_type != "Categorical":
                lower = search_space.lower
                upper = search_space.upper

                lin_space = np.linspace(
                    start=lower,
                    stop=upper,
                    num=self.n_particles
                )

                sliced_sub_space = np.array_split(lin_space, self.n_slice)
                if search_space.space_type == 'Integer':
                    sliced_sub_space = list(
                        map(
                            lambda x: {hyperparameter: Integer(int(x.min()), int(x.min()), search_space.dist)},
                            sliced_sub_space)
                    )
                elif search_space.space_type == 'Real':
                    sliced_sub_space = list(
                        map(
                            lambda x: {hyperparameter: Real(x.min(), x.min(), search_space.dist)},
                            sliced_sub_space)
                    )
            else:
                sliced_sub_space = np.array_split(search_space.discrete_space, self.n_slice)
                sliced_sub_space = list(
                    map(
                        lambda x: {hyperparameter: Categorical(*x.tolist())},
                        sliced_sub_space)
                )

            all_sliced_sub_space.append(sliced_sub_space)

        for space in itertools.product(*all_sliced_sub_space):
            sub_search_space = {}
            for s in space:
                sub_search_space.update(s)

            yield sub_search_space

    def fit(self, X, y, pso_variant):
        n_particles = self.n_particles / len(list(self._sliced_search_space))
        n_particles = int(n_particles)
        for sub_search_space in self._sliced_search_space:
            psov = pso_variant(
                search_space=sub_search_space,
                n_particles=n_particles,
                estimator=self.estimator,
                cv=self.cv,
                scoring=self.scoring,
                max_iter=self.n_iter,
                n_jobs=self.n_jobs,
                verbosity=0
            )
            psov.fit(X, y)

            is_global_best_not_defined = self.best_score_ is None and self.best_params_ is None
            is_current_particle_better = self.best_score_ is None or self.best_score_ < psov.best_score_
            if is_global_best_not_defined or is_current_particle_better:
                self.best_score_ = psov.best_score_
                self.best_params_ = psov.best_params_
                self.best_proba_ = psov.best_proba_


class MultiSwarmParticleSwarmSearchCV(_Initialization, _Evaluation, _Communication):
    def __init__(self, search_space, n_particles, estimator, cv, scoring, max_iter, n_swarm, n_jobs=-1, verbosity=0):
        """
       Parameters
       ----------
       search_space : dict of hyperparameters of estimator and its corresponding
            search space and prior.

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

       n_swarm : int
            Determines how many swarm of particles will be used to search the
            hyperparameter space.

       n_jobs : int, default=-1
           Number of jobs to run in parallel. At maximum there are
           ``n_points`` times ``cv`` jobs available during each iteration.

       verbosity : int, default=0
           'verbosity' controls if any messages are being print
           out during feature selection processes.
       """
        if not isinstance(search_space, dict):
            raise ValueError("Argument 'search_space' only accepts dictionary as input.")

        if not isinstance(n_particles, int):
            raise ValueError("Argument 'n_particles' only accepts integer as input.")

        if not isinstance(cv, int):
            raise ValueError("Argument 'cv' only accepts integer as input.")

        if not isinstance(scoring, str):
            raise ValueError("Argument 'scoring' only accepts string as input.")

        if not isinstance(max_iter, int):
            raise ValueError("Argument 'max_iter' only accepts integer as input.")

        if not isinstance(n_swarm, int):
            raise ValueError("Argument 'n_slice' only accepts integer as input.")

        if not isinstance(n_jobs, int):
            raise ValueError("Argument 'n_jobs' only accepts integer as input.")

        if not isinstance(verbosity, int):
            raise ValueError("Argument 'verbosity' only accepts integer as input.")

        _Initialization.__init__(self, n_particles, search_space, verbosity)
        _Evaluation.__init__(self, estimator, cv, scoring, n_jobs, verbosity)
        _Communication.__init__(self, verbosity)

        self.best_score_ = None
        self.best_params_ = None
        self.best_proba_ = None

        self.search_space = search_space
        self.n_particles = n_particles
        self.estimator = estimator
        self.cv = cv
        self.scoring = scoring
        self.n_iter = max_iter
        self.first_iter = max_iter
        self.n_swarm = n_swarm
        self.n_jobs = n_jobs
        self.verbosity = verbosity

    def fit(self, X, y, pso_variant):
        for _ in range(self.n_swarm):
            psov = pso_variant(
                search_space=self.search_space,
                n_particles=self.n_particles,
                estimator=self.estimator,
                cv=self.cv,
                scoring=self.scoring,
                max_iter=self.n_iter,
                n_jobs=self.n_jobs,
                verbosity=0
            )
            psov.fit(X, y)

            is_global_best_not_defined = self.best_score_ is None and self.best_params_ is None
            is_current_particle_better = self.best_score_ is None or self.best_score_ < psov.best_score_
            if is_global_best_not_defined or is_current_particle_better:
                self.best_score_ = psov.best_score_
                self.best_params_ = psov.best_params_
                self.best_proba_ = psov.best_proba_
