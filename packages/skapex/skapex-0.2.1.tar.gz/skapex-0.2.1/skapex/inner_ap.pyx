# distutils: language = c++

import cython
from cython cimport floating

import numpy as np
cimport numpy as np
np.import_array()

from libcpp cimport bool
from libc.float cimport FLT_MAX, DBL_MAX

@cython.boundscheck(False)
@cython.wraparound(False)
def inner_propagation(  floating[:,::1] S not None,
                        Py_ssize_t[::1] sel not None,
                        floating damping,
                        int n_samples,
                        int m,
                        Py_ssize_t[:, ::1] e not None,
                        Py_ssize_t[::1] I not None,
                        int max_iter,
                        int convergence_iter):

    if floating is float:
        dtype = np.float32
    else:
        dtype = np.float64

    cdef floating[:, ::1] R
    cdef floating[:, ::1] A
    cdef floating[::1] auxsum
    cdef Py_ssize_t[::1] se
    # Used for calculating the two maximum numbers
    cdef floating minf = -FLT_MAX if floating is float else -DBL_MAX
    cdef floating max1 = minf
    cdef floating max2 = minf
    cdef floating sumAS, newVal
    cdef Py_ssize_t yMax
    cdef Py_ssize_t K, ex, it = 0
    cdef bool never_converged = False
    cdef bool dn = False
    
    A = np.zeros((n_samples, m), dtype=dtype, order='C')
    R = np.zeros((n_samples, m), dtype=dtype, order='C')
    auxsum = np.zeros(m-1, dtype=dtype, order='C')
    se = np.zeros(n_samples, dtype=np.intp, order='C')

    # Define indexes
    cdef Py_ssize_t ii = 0, j = 0

    while not dn:
        for ii in range(n_samples):
            max1 = minf
            max2 = minf
            yMax = 0
            sumAS = 0
            for j in range(m):
                if j < m - 1  and sel[j] == ii:
                    continue
                
                sumAS = A[ii, j] + S[ii, j]
                if sumAS > max1:
                    max2 = max1
                    max1 = sumAS
                    yMax = j
                elif sumAS > max2:
                    max2 = sumAS
            
            for j in range(m):
                if j < m - 1 and sel[j] == ii:
                    continue

                newVal = (1 - damping) * (S[ii, j] - (max2 if j == yMax else max1)) + R[ii, j] * damping

                R[ii, j] = DBL_MAX if newVal > DBL_MAX else newVal

                if R[ii, j] > <floating>0 and j < m - 1:
                    auxsum[j] += R[ii, j]

        for ii in range(m-1):
            auxsum[ii] = auxsum[ii] + R[sel[ii], j]

        for ii in range(m - 1):
            for j in range(n_samples):
                newVal = auxsum[ii]

                if R[j, ii] > 0:
                    newVal -= R[j, ii]
                
                if sel[ii] == j:
                    A[j, m -1] = (1 - damping) * (newVal - R[j, m - 1]) + damping* A[j, m-1]
                    newVal = 0
                else:
                    if newVal > 0:
                        newVal = 0
                A[j, ii] = (1 - damping) * newVal + damping* A[j, ii]
            auxsum[ii] = 0

        never_converged = False
        K = 0
        for j in range(n_samples):
            ex = 1 if (A[j, m-1] + R[j, m-1]) > 0 else 0
            se[j] = se[j] - e[j, it % convergence_iter] + ex
            if se[j] > 0 and se[j] < convergence_iter:
                never_converged = True
            
            e[j, it % convergence_iter] = ex
            if ex:
                I[K]=j

            K += ex

        if it >= (convergence_iter - 1) or it >= (max_iter - 1):
            dn = (((not never_converged) and K > 0) or (it >= max_iter - 1))
        it += 1
        
    return K, it, never_converged

"""
Si no se incluye una funcion que no utilice nada de Cython
después de una que sí line_profiler no es capaz de mostrar
el resultado línea por línea

https://github.com/cython/cython/issues/1947

Aunque en la issue se diga que tiene que ocurre en funciones
cpdef parece que también se da el caso con def
"""
def _needed_for_line_profiler(n):
    return n + 2
