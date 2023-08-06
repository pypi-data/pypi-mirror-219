from __future__ import annotations
from jax import Array, vmap
import jax.numpy as np
import matplotlib.pyplot as plt
import dLux
import dLux.utils as dlu

# TODO check if this lambda was necessary
Source = lambda: dLux.sources.BaseSource
Optics = lambda: dLux.core.BaseOptics

__all__ = ["AlphaCen"]  # , "MixedAlphaCen"]


class AlphaCen(dLux.sources.BaseSource):
    """
    A parametrised model of the Alpha Centauri binary pair.

    Parameters
    ----------
    n_wavels : int
        The number of wavelengths to model.
    separation : float
        The binary separation of the two stars in arcseconds.
    position_angle : float
        The position angle of the binary pair in degrees.
    x_position : float
        The horizontal offset of the image in arcseconds.
    y_position : float
        The vertical offset of the image in arcseconds.
    log_flux : float
        The log10 of the total number of photons in the image.
    contrast : float
        The flux ratio of Alpha Cen A / Alpha Cen B.
    bandpass : tuple
        The wavelength range of the image in nanometers, with syntax (min, max).
    weights : Array
    TODO im not actually sure

    Attributes
    ----------

    Methods
    -------
    TODO CONTINUE
    """
    separation: float
    position_angle: float
    x_position: float
    y_position: float
    log_flux: float
    contrast: float
    bandpass: tuple
    weights: Array
    wavelengths: Array

    # TODO : update default values
    # TODO: Add bandpass as a parameter?
    def __init__(self,
                 n_wavels=3,
                 separation=10.,  # arcseconds
                 position_angle=90,  # degrees
                 x_position=0.,  # arcseconds
                 y_position=0.,  # arcseconds
                 log_flux=6.832,  # Photons
                 contrast=3.37,
                 bandpass=(530, 640),  # nm
                 weights=None,
                 ):
        """
        
        """
        # Positional Parameters
        self.x_position = x_position
        self.y_position = y_position
        self.separation = separation
        self.position_angle = position_angle

        # Flux & Contrast
        self.log_flux = log_flux
        self.contrast = contrast

        # Spectrum (Uniform)  # TODO : Phoenix Models?
        self.bandpass = bandpass
        self.wavelengths = 1e-9 * np.linspace(bandpass[0], bandpass[1], n_wavels)
        if weights is None:
            self.weights = np.ones((2, n_wavels)) / n_wavels
        else:
            self.weights = weights

    def normalise(self):
        """
        
        """
        return self.multiply('weights', 1 / self.weights.sum(1)[:, None])

    @property
    def xy_positions(self):
        """
        
        """
        # Calculate
        r = self.separation / 2
        phi = dlu.deg_to_rad(self.position_angle)
        sep_vec = np.array([r * np.sin(phi), r * np.cos(phi)])

        # Add to Position vectors
        pos_vec = np.array([self.x_position, self.y_position])
        output_vec = np.array([pos_vec + sep_vec, pos_vec - sep_vec])
        return dlu.arcsec_to_rad(output_vec)

    @property
    def raw_fluxes(self):
        """
        This casts log flux to be the total (not mean) flux.
        """
        flux = (10 ** self.log_flux) / 2
        flux_A = 2 * self.contrast * flux / (1 + self.contrast)
        flux_B = 2 * flux / (1 + self.contrast)
        return np.array([flux_A, flux_B])

    @property
    def norm_weights(self):
        """
        
        """
        return self.weights / self.weights.sum(1)[:, None]

    def model(self: Source(), optics: Optics()) -> Array:
        """
        Method to model the psf of the point source through the optics.

        Parameters
        ----------
        optics : Optics
            The optics through which to model the source objects.
        detector : Detector = None
            The detector object that is observing the psf.
        filter_in : Filter = None
            The filter through which the source is being observed.

        Returns
        -------
        psf : Array
            The psf of the source modelled through the optics.
        """
        # Get Values
        weights = self.norm_weights
        fluxes = self.raw_fluxes
        positions = self.xy_positions

        # vmap propagator
        source_propagator = vmap(optics.propagate_mono, in_axes=(0, None))
        propagator = vmap(source_propagator, in_axes=(None, 0))

        # Model PSF
        input_weights = weights * fluxes[:, None]
        psfs = propagator(self.wavelengths, positions)
        psfs *= input_weights[..., None, None]
        return psfs.sum((0, 1))


def get_mixed_alpha_cen_spectra(
        nwavels: int,
        min_wavel: float = 545e-9,
        max_wavels: float = 645e-9
):
    """
    
    """
    # Import Here to prevent issues with google colab install, for example
    import pysynphot as S

    alpha_cen_a_spectrum: float = S.Icat("phoenix",
                                         5790,  # Surface temp (K)
                                         0.2,  # Metalicity (Unit?)
                                         4.0, )  # Surface gravity (unit?)
    alpha_cen_a_spectrum.convert('flam')
    alpha_cen_a_spectrum.convert('m')

    alpha_cen_b_spectrum: float = S.Icat("phoenix",
                                         5260,  # Surface temp (K)
                                         0.23,  # Metalicity (Unit?)
                                         4.37)  # Surface gravity (unit?)
    alpha_cen_b_spectrum.convert('flam')
    alpha_cen_b_spectrum.convert('m')

    spot_spectrum: float = S.Icat("phoenix",
                                  4000,  # Surface temp (K)
                                  0.23,  # Metalicity (Unit?)
                                  4.37)  # Surface gravity (unit?)
    spot_spectrum.convert('flam')
    spot_spectrum.convert('m')

    # Full spectrum
    wavelengths = np.linspace(545e-9, 645e-9, nwavels)
    Aspec = alpha_cen_a_spectrum.sample(wavelengths)
    Bspec = alpha_cen_b_spectrum.sample(wavelengths)
    Sspec = spot_spectrum.sample(wavelengths)

    Aspec /= Aspec.max()
    Bspec /= Bspec.max()
    Sspec /= Sspec.max()

    return np.array([Aspec, Bspec, Sspec]), wavelengths


class MixedAlphaCen(AlphaCen):
    mixing: float

    def __init__(self,
                 n_wavels=101,
                 x_position=0.,  # arcseconds
                 y_position=0.,  # arcseconds
                 separation=10.,  # arcseconds
                 position_angle=90,  # Degrees
                 weights=None,
                 mixing=0.05,
                 log_flux=5,  # Photons TODO: Find true flux
                 A_mag=1.33,
                 B_mag=0.01,
                 ):
        """
        
        """
        self.mixing = mixing
        weights, wavelengths = get_mixed_alpha_cen_spectra(n_wavels)
        super().__init__(n_wavels, x_position, y_position, separation,
                         position_angle, weights, log_flux, A_mag, B_mag)

        def plot(self):
            """
            
            """
            plt.figure(figsize=(12, 4))
            plt.subplot(1, 2, 1)
            plt.title(f"Alpha Cen A, f: {f}")
            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Weight")
            plt.plot(spec_wavelengths * 1e9, MixedA, label='Mixed')
            plt.plot(spec_wavelengths * 1e9, SpecA, label='Main')
            plt.plot(spec_wavelengths * 1e9, SpottedA, label='Spotted')
            plt.legend()

            SpecB = (1 - f) * Bspec
            SpottedB = f * Sspec
            MixedB = SpecB + SpottedB
            plt.subplot(1, 2, 2)
            plt.title("Alpha Cen B, f: {f}")
            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Weight")
            plt.plot(spec_wavelengths * 1e9, MixedB, label='Mixed')
            plt.plot(spec_wavelengths * 1e9, SpecB, label='Main')
            plt.plot(spec_wavelengths * 1e9, SpottedB, label='Spotted')
            plt.legend()
            plt.show()

    @property
    def norm_weights(self):
        """
        
        """
        # Get Spectra
        Spotted = self.mixing * self.weights[2]
        MixedA = (1 - self.mixing) * self.weights[0] + Spotted
        MixedB = (1 - self.mixing) * self.weights[1] + Spotted
        weights = np.array([MixedA, MixedB])

        # Normalise
        return weights / weights.sum(1)[:, None]

    def model(self: Source,
              optics: Optics) -> Array:
        """
        Method to model the psf of the point source through the optics.

        Parameters
        ----------
        optics : Optics
            The optics through which to model the source objects.
        detector : Detector = None
            The detector object that is observing the psf.
        filter_in : Filter = None
            The filter through which the source is being observed.

        Returns
        -------
        psf : Array
            The psf of the source modelled through the optics.
        """
        # Get Values
        weights = self.norm_weights
        fluxes = self.raw_fluxes
        positions = self.xy_positions

        # vmap propagator
        source_propagator = vmap(optics.propagate_mono, in_axes=(0, None))
        propagator = vmap(source_propagator, in_axes=(None, 0))

        # Model PSF
        input_weights = weights * fluxes[:, None]
        psfs = propagator(self.wavelengths, positions)
        psfs *= input_weights[..., None, None]
        return psfs.sum((0, 1))
