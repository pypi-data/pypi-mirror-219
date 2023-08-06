import numpy as np
from mpmath import *


mp.dps = 400


def hullermeier(U: np.ndarray, V: np.ndarray):
    N = U.shape[1]
    d = mpf(0)

    for i in range(N):
        for j in range(i, N):
            Eu = fsub(1, np.linalg.norm(U[:, i] - U[:, j], ord=1) / 2.0)
            Ev = fsub(1, np.linalg.norm(V[:, i] - V[:, j], ord=1) / 2.0)

            d += fabs(fsub(Eu, Ev))

    d /= mpf((N * (N - 1)) / 2.0)

    resultado = fsub(1, d)

    assert resultado >= 0, "Indice de Hullermeier menor do que zero."
    return resultado
