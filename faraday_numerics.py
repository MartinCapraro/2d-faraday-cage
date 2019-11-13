import math
import numpy as np

# TODO: Vectorise calculations properly
def run_simulation(n, r, zs):
    np.set_printoptions(threshold=np.inf)

    # centers of the n disks/wires
    a_list = range(1, n+1)
    unit_roots = np.array([math.e**(2j * math.pi * m/n) for m in a_list])

    # vector of radii
    rr = r*np.ones(unit_roots.shape)

    # number of terms in expansion
    # Note: this is empirical, see Appendix A. Numerical Method
    # in "Mathematics of the Faraday Cage"
    N = int(max(0, round(4.0 + 0.5 * np.log10(r))))

    # number of sample points on disk/wires
    npts = 3 * N + 2

    # Note on collocation: we are choosing a number npts of points on the
    # boundary of the circles of radius r, with centers at roots of unity.
    a_list = range(1, int(npts+1))
    circ = np.array([math.e**(m * 2j* math.pi/npts) for m in a_list])

    # this is a list containing n arrays
    # each array has shape npts*1, i.e. they are each a column
    # vector with one row per sample point on the circles
    z_list = [(unit_roots[i] + rr[i] * circ) for i in range(n)]

    # this stacks the n arrays on top of each other, for a column vector with
    # n*npts rows.
    z = np.concatenate(z_list)

    # the constant term
    A = np.concatenate([np.zeros(1), -np.ones(z.shape[0])])

    # right-hand side of Ax=b
    b = np.concatenate([np.zeros(1), -np.log(np.abs(z-zs))])

    for i in range(n):
        B = np.concatenate([np.ones(1), np.log(np.abs(z-unit_roots[i]))])
        # the logarithmic terms
        A = np.column_stack((A, B))
        for k in range(N):
            zck = np.power((z - unit_roots[i]), -(k+1))
            C = np.concatenate([np.zeros(1), zck.real])
            D = np.concatenate([np.zeros(1), zck.imag])
            # the algebraic terms
            A = np.column_stack((A, C, D))

    # this is an overdetermined system, fit a least-squares solution
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    x = np.delete(x, (0), axis=0)  # this deletes the first row

    # coeffs of the log terms, which correspond in some sense to the
    # Green's function for a singularity at the respective wires
    d = x[0:: 2 * N + 1]
    x = np.delete(x, np.s_[0::2*N+1], None)

    a = x[0::2]  # coeffs of the algebraic terms
    b = x[1::2]  # coeffs of the algebraic terms

    # Plotting
    # Note: the X and Y range here will limit what is plotted.
    X = np.linspace(-2.0*zs, 2.0*zs, 1000)
    Y = np.linspace(-2.0*zs, 2.0*zs, 1000)
    [xx, yy] = np.meshgrid(X, Y)

    zz = xx + 1j*yy
    uu = np.log(np.abs(zz - zs))

    for j in range(n):
        uu = uu + d[j]*np.log(np.abs(zz - unit_roots[j]))
        for k in range(N):
            zck = np.power((zz - unit_roots[j]), -(k+1))
            kk = k + j * N
            uu = uu + a[kk] * zck.real + b[kk] * zck.imag
    for j in range(n):
        uu[np.abs(zz - unit_roots[j]) <= rr[j]] = np.nan

    return xx, yy, uu
