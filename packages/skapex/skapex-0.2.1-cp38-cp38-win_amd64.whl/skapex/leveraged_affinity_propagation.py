from math import ceil
import numbers

import warnings

from sklearn.exceptions import ConvergenceWarning
from sklearn.base import BaseEstimator, ClusterMixin
from sklearn.utils import check_random_state
from sklearn.utils import check_scalar

import numpy as np
from .inner_ap import inner_propagation


def lap(data, simf, fraction, sweeps, p, q, max_iter, conv_iter, damping, random_state):
    # Number of rows in the data
    n_data = data.shape[0]

    ## Create column selection using fraction
    # Compute number of exemplars per sweep
    n_sel = max(ceil(n_data * fraction), 2)
    # Store indexes of the random exemplars in sel_idx
    sel_idx = np.sort(
        random_state.choice(np.arange(n_data, dtype=np.intp), n_sel, replace=False)
    )

    best_net_similarity = np.NINF
    best_labels = np.zeros(n_data)
    sweep_net_similarity = np.zeros(sweeps)

    total_sweeps = 0

    for i in range(sweeps):
        total_sweeps += 1
        ## Create sub similarity matrix
        # vsf = np.vectorize(simf, otypes=[np.float32])
        S = simf(data, data[sel_idx])

        ## Run affinity propagation on S
        # cluster_centers, labels, net_similarity = ap(S, sel_idx, max_iter, conv_iter, damping)
        (
            cluster_centers,
            labels,
            dpsim,
            expref,
            net_similarity,
            pv,
            it,
        ) = affinity_propagation(
            S,
            sel_idx,
            convergence_iter=conv_iter,
            p=p,
            q=q,
            max_iter=max_iter,
            damping=damping,
            copy=False,
            verbose=True,
            random_state=random_state,
        )
        sweep_net_similarity[i] = net_similarity

        if net_similarity > best_net_similarity or best_net_similarity == np.NINF:
            # Substitute current best result
            best_net_similarity = net_similarity
            best_cluster_centers = cluster_centers
            best_labels = labels

        sel_idx = cluster_centers

        ## Create selection for next run
        # Conserve best net similarity columns
        if n_sel - len(sel_idx) > 0:
            others = np.setdiff1d(np.arange(n_data), sel_idx)

            sel_idx = np.sort(
                np.concatenate(
                    (
                        sel_idx,
                        random_state.choice(
                            others, n_sel - len(sel_idx), replace=False
                        ),
                    ),
                    axis=None,
                )
            )
        else:
            break
    return (
        best_cluster_centers,
        best_labels,
        total_sweeps,
        dpsim,
        expref,
        net_similarity,
        pv,
        it,
    )


def affinity_propagation(
    S,
    sel,
    convergence_iter=100,
    max_iter=1000,
    damping=0.9,
    p=None,
    q=None,
    copy=True,
    verbose=False,
    random_state=None,
):
    n_samples = S.shape[0]
    m = S.shape[1]

    if p is None:
        # Don't include S[sel, sel] in the mediam
        # Masked arrays and median may have issues
        # https://github.com/numpy/numpy/issues/7330
        nonSel = np.setdiff1d(
            np.where(S.flatten() > np.NINF), np.arange(m) * n_samples + sel
        )
        if q is None:
            p = np.median(S.flat[nonSel])
            pv = p
            p = np.full(n_samples, p)
        else:
            p = np.quantile(S.flat[nonSel], q=q)
            pv = p
            p = np.full(n_samples, p)
    elif np.ndim(p) == 0:
        pv = p
        p = np.full(n_samples, p)
    elif np.ndim(p) == 1:
        if len(p) >= n_samples:
            p = p[:n_samples]
            pv = p
    else:
        raise ValueError(
            "p must be None, a float or a vector of floats of length of data"
        )

    # Place preference on the diagonal of S
    S = np.append(S, p[:, np.newaxis], axis=1)
    m += 1

    # Remove degeneracies
    S += (
        np.finfo(S.dtype).eps * S + np.finfo(S.dtype).tiny * 100
    ) * random_state.standard_normal(size=(n_samples, m))

    ind = np.arange(n_samples)

    e = np.zeros((n_samples, convergence_iter), dtype=np.intp, order="C")
    I = np.full(n_samples, -1, dtype=np.intp, order="C")

    K, it, never_converged = inner_propagation(
        S, sel, damping, n_samples, m, e, I, max_iter, convergence_iter
    )

    if K > 0:
        if never_converged:
            warnings.warn(
                "Affinity propagation did not converge, this model "
                "may return degenerate cluster centers and labels.",
                ConvergenceWarning,
            )

        I = I[:K]
        I = I[np.isin(I, sel)]

        # ee contains the indexes of I elements in sel
        # such that sel[ee] == I
        ee = np.where(np.isin(sel, I))[0]
        K = len(ee)

        if K < 1:
            raise Exception("internal: no exemplars found in selected samples")

        c = np.zeros(n_samples, dtype=int)
        c[I] = np.arange(K)
        nonI = np.setdiff1d(np.arange(n_samples), I)
        # Which is each element's most similar exemplar?
        # c contains c[i] = cluster center index in I for element i
        c[nonI] = np.argmax(S[nonI[:, np.newaxis], ee], axis=1)

        for k in range(K):
            # jj = indexes of elements that have I[k] as exemplar
            jj = np.where(c == k)[0]
            # ii = indexes of elements in selection that have I[k] as exemplar
            ii = np.where(np.isin(sel, jj))[0]
            # preference of all elements that have I[k] as exemplar
            ns = S[jj, m - 1]

            # Indices in jj of all elements in sel that have I[k] as exemplar
            ind = np.where(np.isin(jj, sel[ii]))[0]

            ns[ind] = np.sum(S[jj[:, np.newaxis], ii], axis=0)
            ns[ind] += S[sel[ii], m - 1]
            ns[ind] -= S[sel[ii], ii]
            I[k] = jj[ind[np.argmax(ns[ind])]]

        I = np.sort(I)
        ee = np.where(np.isin(sel, I))[0]

        c = np.zeros(n_samples, dtype=int)
        c[I] = np.arange(K)
        nonI = np.setdiff1d(np.arange(n_samples), I)
        # Which is each element's most similar exemplar?
        # c containes c[i] = cluster center index in I for element i
        c[nonI] = np.argmax(S[nonI[:, np.newaxis], ee], axis=1)

        labels = I[c]
        cluster_centers_indices = np.unique(labels)
        labels = np.searchsorted(cluster_centers_indices, labels)

        nonISelIIdx = [np.where(sel == I[x])[0][0] for x in labels[nonI]]
        # Metrics
        dpsim = np.sum(S[nonI, nonISelIIdx])
        expref = np.sum(S[I, m - 1])
        netsim = expref + dpsim

    else:
        warnings.warn(
            "Affinity propagation did not converge and this model "
            "will not have any cluster centers.",
            ConvergenceWarning,
        )
        labels = np.array([-1] * n_samples)
        cluster_centers_indices = []
        dpsim = np.NaN
        expref = np.NaN
        netsim = np.NaN

    return cluster_centers_indices, labels, dpsim, expref, netsim, pv, it


class LeveragedAffinityPropagation(ClusterMixin, BaseEstimator):
    """Perform Leveraged Affinity Propagation Clustering of data

    Parameters
    ----------
    simf : function
        Similarity function
    fraction : float
        Fraction of samples to use as posible exemplars
    sweeps : int
        _description_
    damping : float, default=0.9
        Damping factor in the range `[0.5, 1.0)` is the extent to
        which the current value is maintained relative to
        incoming values (weighted 1 - damping). This in order
        to avoid numerical oscillations when updating these
        values (messages).
    max_iter : int, default=1000
        Maximum number of iterations.
    convergence_iter : int, default=100
        Number of iterations with no change in the number
        of estimated clusters that stops the convergence.
    p : array-like of shape (n_samples,) or float, default=None
        Preferences for each point - points with larger values of
        preferences are more likely to be chosen as exemplars. The number
        of exemplars, ie of clusters, is influenced by the input
        preferences value. If the preferences are not passed as arguments,
        they will be set to the median of the input similarities.
    q : float, default=None
        Quantile to be used as preference for all points
    verbose : bool, default=None
        Whether to be verbose.
    random_state : int, RandomState instance or None, default=None
        Pseudo-random number generator to control the starting state.
        Use an int for reproducible results across function calls.
    """

    def __init__(
        self,
        simf,
        fraction,
        sweeps,
        damping=0.9,
        max_iter=1000,
        convergence_iter=100,
        p=None,
        q=None,
        verbose=False,
        random_state=0,
    ):
        self.simf = simf
        self.fraction = fraction
        self.sweeps = sweeps
        self.damping = damping
        self.max_iter = max_iter
        self.convergence_iter = convergence_iter
        self.verbose = verbose
        self.p = p
        self.q = q
        self.random_state = random_state

    def fit(self, X, y=None):
        X = self._validate_data(X, accept_sparse="csr")
        check_scalar(
            self.fraction,
            "fraction",
            target_type=numbers.Real,
            min_val=0,
            max_val=1,
            include_boundaries="left",
        )
        check_scalar(
            self.damping,
            "damping",
            target_type=numbers.Real,
            min_val=0.5,
            max_val=1,
            include_boundaries="left",
        )
        check_scalar(self.max_iter, "max_iter", target_type=numbers.Integral, min_val=1)
        check_scalar(
            self.convergence_iter,
            "conv_iter",
            target_type=numbers.Integral,
            min_val=1,
        )
        check_scalar(
            self.sweeps,
            "sweeps",
            target_type=numbers.Integral,
            min_val=1,
        )
        self.random_state = check_random_state(self.random_state)
        (
            self.cluster_centers_indices_,
            self.labels_,
            self.n_sweeps_,
            self.dpsim,
            self.expref,
            self.netsim,
            self.pv,
            self.iterations,
        ) = lap(
            X,
            self.simf,
            self.fraction,
            self.sweeps,
            p=self.p,
            q=self.q,
            max_iter=self.max_iter,
            conv_iter=self.convergence_iter,
            damping=self.damping,
            random_state=self.random_state,
        )

        self.cluster_centers_ = X[self.cluster_centers_indices_]

        return self
