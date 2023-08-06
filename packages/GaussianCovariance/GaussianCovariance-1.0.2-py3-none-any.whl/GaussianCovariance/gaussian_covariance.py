import numpy as np
from scipy import special
from scipy.integrate import quad, romb
from scipy.special import spherical_jn


class GaussianCovariance:

    def __init__(self, l_list, deg):
        """
        Initialize GaussianCovariance instance

a        :param l_list: list of multipoles
        :param deg Number of sample points and weights. It must be >= 1.
        """

        self.n_poles = len(l_list)

        self.l_list = l_list
        self.mu, self.weights = np.polynomial.legendre.leggauss(deg)
        self.legendre = dict(zip(self.l_list, [special.legendre(ll)(self.mu) for ll in self.l_list]))

    def compute_sigma_squared(self, k, p_k_mu, volume, number_density, l1, l2):
        """
        Compute the variance of the power spectrum multipoles following Grieb et al. 2016 (eq. 15)

        :param k: wavevector module
        :param p_k_mu: function to compute the polar power spectrum (callable)
        :param volume: survey volume
        :param number_density: number density
        :param l1: order of Legendre expansion, first index
        :param l2: order of Legendre expansion, second index
        :return: the variance of the power spectrum multipole
        """

        p_k_mu_tab = p_k_mu(k, self.mu)

        i1 = np.sum(self.weights * p_k_mu_tab ** 2 * self.legendre[l1] * self.legendre[l2])

        i2 = np.sum(self.weights * p_k_mu_tab * self.legendre[l1] * self.legendre[l2])

        i3 = 1 if l1 == l2 else 0

        normalisation = (2*l1+1) * (2*l2+1) / volume
        return normalisation * (i1 + 2. / number_density * i2 + 1./number_density**2 * i3)


class PowerSpectrumGaussianCovariance(GaussianCovariance):

    def __init__(self, k_edges, l_list, deg=21):
        """
        Initialize GaussianCovariance instance

        :param k_edges: edges of wave vector
        :param l_list: list of multipoles
        :param deg Number of sample points and weights. It must be >= 1.
        """
        super().__init__(l_list, deg)
        self.n_bins_k = len(k_edges) - 1
        self.data_vector_size = self.n_bins_k * self.n_poles

        self.k_edges = k_edges

    def compute_covariance_element(self, k_index, p_k_mu, volume, number_density, l1, l2):
        """
        Compute the element of the power spectrum multipoles covariance matrix
        following Grieb et al. 2016 (eq. 16)

        :param k_index: index of the k bin
        :param p_k_mu: function to compute the polar power spectrum (callable)
        :param volume: survey volume
        :param number_density: number density
        :param l1: order of Legendre expansion, first index
        :param l2: order of Legendre expansion, second index
        :return: the bin-averaged variance of the power spectrum multipole
        """

        k_min, k_max = self.k_edges[k_index], self.k_edges[k_index+1]
        k_volume = 4 * np.pi / 3 * (k_max ** 3 - k_min ** 3)

        def integrand(k):
            return k ** 2 * self.compute_sigma_squared(k, p_k_mu, volume, number_density, l1, l2)

        return 2 * (2 * np.pi) ** 4 * quad(integrand, k_min, k_max, epsrel=1.e-4, epsabs=0)[0] / k_volume ** 2

    def __call__(self, p_k_mu, volume, number_density):
        """
        Compute the full power spectrum multipoles covariance matrix following Grieb et al. 2016.

        :param p_k_mu: function to compute the polar power spectrum (callable)
        :param volume: survey volume
        :param number_density: number density
        :return: the covariance matrix
        """

        covariance = np.zeros(shape=(self.data_vector_size, self.data_vector_size))

        for i in range(self.data_vector_size):
            l1, k1 = int(i / self.n_bins_k), i - int(i / self.n_bins_k) * self.n_bins_k
            for j in range(self.data_vector_size):
                l2, k2 = int(j / self.n_bins_k), j - int(j / self.n_bins_k) * self.n_bins_k
                if (l1 <= l2) & (k1 == k2):
                    covariance[i, j] = self.compute_covariance_element(k1,
                                                                       p_k_mu,
                                                                       volume,
                                                                       number_density,
                                                                       self.l_list[l1],
                                                                       self.l_list[l2])
                    covariance[j, i] = covariance[i, j]

        return covariance


def average_spherical_jn (order, r_min, r_max, k, deg=6):
    """
    Compute the average spherical Bessel function

    :param order: order of the Bessel function (n >= 0).
    :param r_min: minimum separation
    :param r_max: maximum separation
    :param k: wave-vector module
    :return: the spherical-averaged spherical Bessel function
    """
    volume = 4*np.pi * (r_max**3 - r_min**3)/3
    rr = np.linspace(r_min, r_max, 2**deg+1)
    X, Y = np.meshgrid(rr, k)
    integral = romb(X**2 * spherical_jn(order, X*Y), rr[1]-rr[0], axis=1)

    return 4 * np.pi / volume * integral

class TwoPointGaussianCovariance(GaussianCovariance):

    def __init__(self, r_edges, l_list, deg=21, min_k = 1.e-4, max_k = 1.e1, deg_k = 6):
        """
        Initialize GaussianCovariance instance

        :param r_edges: edges of separations
        :param l_list: list of multipoles
        :param deg: Number of sample points and weights. It must be >= 1.
        :param min_k: minimum k-vector module
        :param max_k: maximum k-vector module
        :param deg_k: degree for wavevector modules k = 2**deg + 1
        """
        super().__init__(l_list, deg)

        self.n_bins_r = len(r_edges) -1
        self.data_vector_size = self.n_bins_r * self.n_poles
        self.r_edges = r_edges

        self.n_bins_k = 2**deg_k + 1
        self.k = np.logspace(np.log10(min_k), np.log10(max_k), self.n_bins_k)
        self.delta_log_k = np.log10(self.k[1]) - np.log10(self.k[0])
        self.bessels = {}
        self.sigma_squared_tabulated = {}

        print("Computing Bessels functions...")
        for l in l_list:
            for i in range(self.n_bins_r):
                r_min, r_max = r_edges[i], r_edges[i+1]
                self.bessels[(l, i)] = average_spherical_jn (l, r_min, r_max, self.k, deg=8)
        print("Done!")


    def compute_covariance_element(self, r_index_1, r_index_2, l1, l2):
        """
        Compute the element of the power spectrum multipoles covariance matrix
        following Grieb et al. 2016 (eq. 16)

        :param r_index_1: first index of the r bin
        :param r_index_2: second index of the r bin
        :param l1: order of Legendre expansion, first index
        :param l2: order of Legendre expansion, second index

        :return: the bin-averaged variance of the power spectrum multipole
        """

        norm = (-1) ** int(0.5*(l1 + l2)) / ( 2 * np.pi**2) * np.log(10)
        integrand = self.k**3 * self.sigma_squared_tabulated[(l1, l2)] * self.bessels[(l1, r_index_1)] * self.bessels[(l2, r_index_2)]
        return norm * romb(integrand, self.delta_log_k)

    def tabulate_sigma_squared(self, p_k_mu, volume, number_density):
        """
        Tabulate sigma squared

        :param l1:
        :param l2:
        :param p_k_mu: function to compute the polar power spectrum (callable)
        :param volume: survey volume
        :param number_density: number density
        :return: tabulated sigma2
        """

        print("Computing tabulated sigma squared...")

        for l1 in self.l_list:
            for l2 in self.l_list:
                self.sigma_squared_tabulated[(l1, l2)]  = np.array([self.compute_sigma_squared(_k,
                                                                                     p_k_mu,
                                                                                     volume,
                                                                                     number_density,
                                                                                     l1,
                                                                                     l2) for _k in self.k])
        print("Done!")

    def __call__(self, p_k_mu, volume, number_density):
        """
        Compute the full power spectrum multipoles covariance matrix following Grieb et al. 2016.

        :param p_k_mu: function to compute the polar power spectrum (callable)
        :param volume: survey volume
        :param number_density: number density
        :return: the covariance matrix
        """

        self.tabulate_sigma_squared(p_k_mu, volume, number_density)

        covariance = np.zeros(shape=(self.data_vector_size, self.data_vector_size))

        for i in range(self.data_vector_size):
            l1, r1 = int(i / self.n_bins_r), i - int(i / self.n_bins_r) * self.n_bins_r
            for j in range(self.data_vector_size):
                l2, r2 = int(j / self.n_bins_r), j - int(j / self.n_bins_r) * self.n_bins_r
                #if (i>=j):
                covariance[i, j] = self.compute_covariance_element(r1,
                                                                      r2,
                                                                      self.l_list[l1],
                                                                      self.l_list[l2])
                #    covariance[j, i] = covariance[i, j]

        return covariance

