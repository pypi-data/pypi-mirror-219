=====================================================
skapex: Leveraged Affinity Propagation implementation
=====================================================
Features
--------
- Implements Leveraged Affinity Propagation (LAP).
- Maintains compatibility with scikit-learn, enabling seamless integration with existing scikit-learn workflows.

Installation
------------
You can install skapex via pip:

.. code-block:: bash

   pip install skapex

Usage
-----
Here's a basic example of how to use skapex LAP for clustering:

.. code-block:: python

   from skapex import LeveragedAffinityPropagation
   from sklearn.datasets import make_blobs
   from sklearn.metrics.pairwise import euclidean_distances

   # Generate sample data
   X, _ = make_blobs(n_samples=200, centers=3, random_state=0)

   # Create and fit the skapex Leveraged Affinity Propagation
   model = LeveragedAffinityPropagation(simf=lambda x,y : -euclidean_distances(x, y, squared=True), fraction=0.1, sweeps=5)
   model.fit(X)

   # Get cluster labels for the input data
   labels = model.labels_

   # Print the resulting cluster labels
   print(labels)

References
----------

B. J. Frey and D. Dueck, “Clustering by Passing Messages Between Data
Points,” Science, vol. 315, no. 5814, pp. 972–976, Feb. 16, 2007, issn: 0036-
8075, 1095-9203. doi: 10.1126/science.1136800.

U. Bodenhofer, A. Kothmeier, and S. Hochreiter, “APCluster: An R package
for affinity propagation clustering,” Bioinformatics, vol. 27, no. 17, pp. 2463–
2464, Sep. 1, 2011, issn: 1367-4803. doi: 10.1093/bioinformatics/btr406.
