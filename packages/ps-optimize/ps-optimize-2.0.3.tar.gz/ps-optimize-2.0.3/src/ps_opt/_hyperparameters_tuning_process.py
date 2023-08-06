from ps_opt._base import _Base
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score


class _Initialization(_Base):
    """
    Class '_Initialization' consist of a single method '_initialize',
    and inherent class '_Base' as the sole parent class to inherent class
    method '_system_datetime'. 2 arguments are required to instantiate
    class '_Initialization'.
    """
    def __init__(self, n_particles, search_space, verbosity):
        """
        Parameters
        ----------
        n_particles : int
                      'n_particles' controls how many sets of probabilities
                      are generated during the initialization process.

        verbosity : int
                    'verbosity' controls if any messages are being print
                    out during feature selection processes.
        """
        if not isinstance(n_particles, int):
            raise ValueError("Argument 'n_particles' only accept integer as "
                             "input.")

        if not isinstance(verbosity, int):
            raise ValueError("Argument 'verbosity' only accept integer as "
                             "input.")

        _Base.__init__(self)
        self.n_particles = n_particles
        self.search_space = search_space
        self.categorical = [k for k, v in self.search_space.items() if v.space_type == 'Categorical']
        self.numerical = [k for k, v in self.search_space.items() if v.space_type != 'Categorical']
        self.all_one_hot_categorical_sub_space = {}
        self.space_map = []
        self.verbosity = verbosity

    def _initialize(self):
        """
        Returns
        -------
        ``particles``
            As described in 'Parameters' section.
        ``velocities``
            Another version of particles that used for evaluation process.
        ``global_best``
            As described in 'Parameters' section.
        ``global_best_particle``
            Another version of particles that used for evaluation process.
        """
        particles = []
        for hyperparameter, search_space in self.search_space.items():
            # if the search space is categorical, use the one-hot representation
            # of randomly assigned probabilities to express the subspace.
            if search_space.space_type == 'Categorical':
                categorical_sub_space = search_space.sub_space(self.n_particles)
                one_hot_categorical_sub_space = map(lambda x: f"__{x}_{hyperparameter}__", search_space.discrete_space)
                one_hot_categorical_sub_space = list(one_hot_categorical_sub_space)
                particle = pd.DataFrame(categorical_sub_space, columns=one_hot_categorical_sub_space)
                self.all_one_hot_categorical_sub_space[hyperparameter] = one_hot_categorical_sub_space
                space_map = pd.DataFrame([
                    [hyperparameter] * len(search_space.discrete_space),
                    one_hot_categorical_sub_space, search_space.discrete_space
                ], index=["categorical", "one_hot_categorical_sub_space", "sub_space"]).T
                self.space_map.append(space_map)
            else:
                particle = search_space.sub_space(self.n_particles).tolist()
                particle = pd.DataFrame(particle, columns=[hyperparameter])

            particles.append(particle)

        self.space_map = pd.concat(self.space_map)
        self.space_map.index = range(len(self.space_map))

        particles = pd.concat(particles, axis=1)
        global_best = None
        global_best_particle = None
        self.particles_dtypes = particles.dtypes.to_dict()

        return particles, global_best, global_best_particle


class _Evaluation(_Base):
    """
    Class '_Evaluation' consist of a single method '_evaluate_performance', and
    inherent class '_Base' as the sole parent class to inherent class
    method '_system_datetime'. 5 arguments are required to instantiate
    class '_Evaluation'.
    """
    def __init__(self, estimator, cv, scoring, n_jobs, verbosity):
        """
        Parameters
        ----------
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

        n_jobs : int, default=-1
            Number of jobs to run in parallel. At maximum there are
            ``n_points`` times ``cv`` jobs available during each iteration.

        verbosity : int
                    'verbosity' controls if any messages are being print
                    out during feature selection processes.
        """

        if not isinstance(cv, int):
            raise ValueError("Argument 'cv' only accept integer as input.")

        if not isinstance(scoring, str):
            raise ValueError("Argument 'cv' only accept string as input.")

        if not isinstance(n_jobs, int):
            raise ValueError("Argument 'n_jobs' only accept integer as input.")

        if not isinstance(verbosity, int):
            raise ValueError("Argument 'verbosity' only accept integer as input.")

        _Base.__init__(self)
        self.estimator = estimator
        self.cv = cv
        self.scoring = scoring
        self.candidates_score = {}
        self.n_jobs = n_jobs
        self.verbosity = verbosity

    def _evaluate_performance(self, X, y, particles):
        """
        Parameters
        ----------
        X : pandas.core.frame.DataFrame or numpy.ndarray of shape (n_samples, n_features)
            The data to fit.

        y : array-like of shape (n_samples,) or (n_samples, n_outputs),
            The target variable to try to predict in the case of
            supervised learning.

        particles : pandas.core.frame.DataFrame
                    The probability array of shape (n_particles, n_features), which contains
                    sets of different probabilities which determines if corresponding
                    features are being selected during the evaluation phase.

        Returns
        -------
        ``particles``
            As described in 'Parameters' section.
        ``particles_evaluate``
            Another version of particles that used for evaluation process.
        """
        if self.verbosity:
            print(f"{self._system_datetime} Evaluating particles:")

        if isinstance(X, pd.core.frame.DataFrame):
            X = X.to_numpy()

        # sample categorical variables base on probabilities.
        sub_space_to_categorical = self.space_map[["one_hot_categorical_sub_space", "sub_space"]].copy()
        sub_space_to_categorical = sub_space_to_categorical.set_index("one_hot_categorical_sub_space")["sub_space"].to_dict()
        particles_evaluate = particles[self.numerical].copy()
        for hyperparameter, search_space in self.search_space.items():
            if hyperparameter in self.all_one_hot_categorical_sub_space:
                one_hot_categorical_sub_space = self.all_one_hot_categorical_sub_space[hyperparameter]
                selected_one_hot_categorical_sub_space = particles[one_hot_categorical_sub_space] - np.random.random(particles[one_hot_categorical_sub_space].shape)
                selected_one_hot_categorical_sub_space = selected_one_hot_categorical_sub_space.idxmax(1)
                selected_one_hot_categorical_sub_space.name = hyperparameter

                particles_evaluate = pd.concat([selected_one_hot_categorical_sub_space, particles_evaluate], axis=1)
                particles_evaluate[hyperparameter] = particles_evaluate[hyperparameter].replace(sub_space_to_categorical)

        results = []
        for i in range(len(particles)):
            try:
                hyperparameters = particles_evaluate.iloc[i].to_dict()
                cv_score = cross_val_score(
                    estimator=self.estimator(**hyperparameters),
                    cv=self.cv,
                    X=X,
                    y=y,
                    scoring=self.scoring,
                    n_jobs=self.n_jobs
                )
                mean_cv_score = cv_score.mean()
            except ValueError:
                mean_cv_score = np.nan

            results.append(mean_cv_score)

        particles["__score__"] = results
        particles_evaluate["__score__"] = results

        particles['__score__'].fillna(0, inplace=True)
        particles_evaluate["__score__"].fillna(0, inplace=True)

        return particles, particles_evaluate


class _Communication(_Base):
    """
    Class '_Communication' consist of 2 methods '_update_global_best',
    and '_calculate_velocities'. Class '_Communication' inherent class
    '_Base' as the sole parent class to inherent class method
    '_system_datetime'. 1 argument are required to instantiate class
    '_Communication'.
    """
    def __init__(self, verbosity):
        """
        Parameters
        ----------
        verbosity : int
                    'verbosity' controls if any messages are being print
                    out during feature selection processes.
        """
        if not isinstance(verbosity, int):
            raise ValueError("Argument 'verbosity' only accept integer as input.")

        _Base.__init__(self)
        self.verbosity = verbosity

    def _update_global_best(self, results, results_evaluate, global_best, global_best_particle):
        """
        Update the global best variable found during evaluation phase.

        Parameters
        ----------
        results_evaluate : pd.core.frame.DataFrame
                      The scores array that uses a tuple of selected
                      features as index and stores the corresponding
                      scores evaluated.

        global_best : float
                      A variable that determines the velocities being calculated.
                      The value of 'global_best' is None when its first defined
                      during initiation and will be updated during communication
                      phase.

        global_best_particle : tuple
                            A variable that store the row and columns numbers of
                            the best particle found during the evaluation phase.
                            'global_best_particle' will be updated during the
                            communication phase.

        Returns
        -------
        ``global_best``
            As described in 'Parameters' section.
        ``global_best_particle``
            As described in 'Parameters' section.
        """
        if self.verbosity:
            print(f"\n{self._system_datetime} Update global best score and best particle.")

        # get the current best particle from evaluation results.
        current_best_particle = results.sort_values("__score__").iloc[[-1]]
        current_best = results.sort_values("__score__").iloc[-1]['__score__']
        current_best_particle.drop("__score__", axis=1, inplace=True)

        # get the current best score from evaluation results.
        current_best_particle_evaluate = results_evaluate.sort_values("__score__").iloc[[-1]]
        current_best_particle_evaluate.drop("__score__", axis=1, inplace=True)
        best_params = current_best_particle_evaluate.iloc[0].to_dict()
        winner_categorical = current_best_particle_evaluate[self.categorical].iloc[0].to_dict()

        # if the global best score is not defined or a better particle is found,
        # update the current best score and particle.
        is_global_best_not_defined = global_best is None and global_best_particle is None
        is_current_particle_better = global_best is None or global_best < current_best
        if is_global_best_not_defined or is_current_particle_better:
            global_best = current_best
            global_best_particle = current_best_particle
            self.best_params_ = best_params

        return global_best, global_best_particle, winner_categorical

    def _calculate_velocities(self, particles, winner_categorical, global_best_particle):
        """
        Update the global best variable found during evaluation phase.

        Parameters
        ----------
        particles : pandas.core.frame.DataFrame
            The probability array of shape (n_particles, n_features), which contains
            sets of different probabilities which determines if corresponding
            features are being selected during the evaluation phase.

        winner_categorical : dict
            The best hyperparameters and their corresponding probabilities.


        Returns
        -------
        `velocities``
            The velocity array of shape (n_particles, n_features), which is being
            used to update the velocities of the particles. 'velocities'
            will be calculated during the with the '_calculate_velocities' function
            from class 'Communication'.
        """
        if self.verbosity:
            print(f"{self._system_datetime} Calculate new velocities for particles.")

        particles.drop("__score__", axis=1, inplace=True)

        velocities_numeric = pd.concat([global_best_particle[self.numerical] for _ in range(len(particles))])
        velocities_numeric.index = particles.index
        velocities_numeric = velocities_numeric - particles[self.numerical] / self.n_iter

        is_winner = self.space_map['sub_space'].isin(winner_categorical.values())
        winner_of_one_hot_categorical_sub_space = self.space_map[is_winner]['one_hot_categorical_sub_space'].to_list()
        is_win_or_lose = particles[self.space_map['one_hot_categorical_sub_space']].columns.isin(winner_of_one_hot_categorical_sub_space).tolist()
        is_win_or_lose = pd.DataFrame([is_win_or_lose] * particles.shape[0])

        # calculate and store the velocities of the best and non-best particles.
        velocities_win = []
        velocities_lose = []
        for c in self.space_map['one_hot_categorical_sub_space'].to_list():
            win = (1 - particles[c]) / self.n_iter
            lose = (0 - particles[c]) / self.n_iter
            velocities_win.append(win)
            velocities_lose.append(lose)

        # combine best and non-best velocities as dataframes
        velocities_win = pd.DataFrame(velocities_win).T
        velocities_lose = pd.DataFrame(velocities_lose).T
        velocities_win.columns = self.space_map['one_hot_categorical_sub_space']
        velocities_lose.columns = self.space_map['one_hot_categorical_sub_space']

        # conditionally get the correct velocities according to conditions.
        velocities = np.where(is_win_or_lose, velocities_win, velocities_lose)
        velocities = pd.DataFrame(velocities)

        # set all numerical hyperparameters as 0 to match the dimensions.
        velocities[self.numerical] = velocities_numeric
        velocities.columns = self.space_map['one_hot_categorical_sub_space'].to_list() + self.numerical

        velocities.index = particles.index
        velocities = velocities.astype(self.particles_dtypes)
        velocities['__score__'] = 0
        return velocities

    def _calculate_chaotic_velocities(self, particles, winner_categorical, global_best_particle):
        """
        Update the global best variable found during evaluation phase.

        Parameters
        ----------
        particles : pandas.core.frame.DataFrame
            The probability array of shape (n_particles, n_features), which contains
            sets of different probabilities which determines if corresponding
            features are being selected during the evaluation phase.

        winner_categorical : dict
            The best hyperparameters and their corresponding probabilities.


        Returns
        -------
        `velocities``
            The velocity array of shape (n_particles, n_features), which is being
            used to update the velocities of the particles. 'velocities'
            will be calculated during the with the '_calculate_velocities' function
            from class 'Communication'.
        """
        if self.verbosity:
            print(f"{self._system_datetime} Calculate new velocities for particles.")

        particles.drop("__score__", axis=1, inplace=True)

        velocities_numeric = pd.concat([global_best_particle[self.numerical] for _ in range(len(particles))])
        velocities_numeric.index = particles.index
        #
        velocities_numeric = velocities_numeric - particles[self.numerical] / self.n_iter

        is_winner = self.space_map['sub_space'].isin(winner_categorical.values())
        winner_of_one_hot_categorical_sub_space = self.space_map[is_winner]['one_hot_categorical_sub_space'].to_list()
        is_win_or_lose = particles[self.space_map['one_hot_categorical_sub_space']].columns.isin(winner_of_one_hot_categorical_sub_space).tolist()
        is_win_or_lose = pd.DataFrame([is_win_or_lose] * particles.shape[0])

        # calculate and store the velocities of the best and non-best particles.
        velocities_win = []
        velocities_lose = []
        #
        for c in self.space_map['one_hot_categorical_sub_space'].to_list():
            win = (1 - particles[c]) / self.n_iter
            lose = (0 - particles[c]) / self.n_iter
            velocities_win.append(win)
            velocities_lose.append(lose)

        # combine best and non-best velocities as dataframes
        velocities_win = pd.DataFrame(velocities_win).T
        velocities_lose = pd.DataFrame(velocities_lose).T
        velocities_win.columns = self.space_map['one_hot_categorical_sub_space']
        velocities_lose.columns = self.space_map['one_hot_categorical_sub_space']

        # conditionally get the correct velocities according to conditions.
        velocities = np.where(is_win_or_lose, velocities_win, velocities_lose)
        velocities = pd.DataFrame(velocities)

        # set all numerical hyperparameters as 0 to match the dimensions.
        velocities[self.numerical] = velocities_numeric
        velocities.columns = self.space_map['one_hot_categorical_sub_space'].to_list() + self.numerical

        velocities.index = particles.index
        velocities = velocities.astype(self.particles_dtypes)
        velocities['__score__'] = 0
        return velocities