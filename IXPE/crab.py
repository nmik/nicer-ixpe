import numpy
from astropy.coordinates import SkyCoord
from astropy import units as u
from regions import CircleSkyRegion

from ixpeobssim.core.spline import xInterpolatedUnivariateSpline
from ixpeobssim.core.spline import xUnivariateSpline
from ixpeobssim.srcmodel.roi import xChandraObservation, xChandraROIModel
from ixpeobssim.srcmodel.roi import xPeriodicPointSource, xROIModel
from ixpeobssim.srcmodel.bkg import xPowerLawInstrumentalBkg
from ixpeobssim.srcmodel.ephemeris import xEphemeris
from ixpeobssim.srcmodel.spectrum import power_law
from ixpeobssim.srcmodel.polarization import xTangentialPolarizationField
from ixpeobssim.utils.logging_ import logger
from ixpeobssim.utils.matplotlib_ import plt, setup_gca
from ixpeobssim.utils.time_ import mjd_to_met
from ixpeobssim.utils.units_ import arcmin_to_degrees

INPUT_EVT_FILE_PATH = 'acisf16364_repro_evt2.fits'
PSRcoord = SkyCoord('05h34m31.93830s', '22d00m52.1758s', frame='icrs')
ra_psr = PSRcoord.ra.deg
dec_psr = PSRcoord.dec.deg
epoch  = 59380.000   # in MJD  
nu0    = 29.5948563919  # in Hz
nudot0 = -3.6770137e-10
nuddot = 1.18e-20
pl_index = 1.6

def parse_pulsar_data(file_path='crab_pulsar2.txt'):
    logger.info('Reading data from %s...' % file_path)
    phase, norm, pd, pa = numpy.loadtxt(file_path, unpack=True)
    pa = numpy.deg2rad(pa - 90.)
    return phase, norm, pd, pa

# Parse the phase-resolved pulsar parameters.
phase, norm, pd, pa = parse_pulsar_data()

# Build the spline for the PL normalization
fmt = dict(xlabel='Pulse phase',
           ylabel='Power-law normalization [cm$^{-2}$ s$^{-1}$ keV$^{-1}$]')
pl_norm_spline = xInterpolatedUnivariateSpline(phase, norm, k=3, **fmt)

# Build the actual phase-resolved energy spectrum.
spec = power_law(pl_norm_spline, pl_index)

fmt = dict(xlabel='Pulse phase', ylabel='Polarization degree')
pol_deg_spline = xInterpolatedUnivariateSpline(phase, pd, k=3, **fmt)

# And this needs to be wrapped into a function with the proper signature.
def pol_deg(E, phase, ra=None, dec=None):
    return pol_deg_spline(phase)

fmt = dict(xlabel='Pulse phase', ylabel='Polarization angle [rad]')
pol_ang_spline = xInterpolatedUnivariateSpline(phase, pa, k=3, **fmt)

# And this needs to be wrapped into a function with the proper signature.
def pol_ang(E, phase, ra=None, dec=None):
    return pol_ang_spline(phase)

# Build the ROI model.
ROI_MODEL = xChandraROIModel(INPUT_EVT_FILE_PATH, acis='S')

# Remove the pulsars
region = CircleSkyRegion(center=PSRcoord, radius=1.5 * u.arcsec)
remove_psr = xChandraObservation('Remove', None, None, region, exclude=True)
ROI_MODEL.add_source(remove_psr)

def pol_radial_profile(r, E=None, t=None):
    """Radial profile of the polarization degree.

    This is going from zero at the center of the pulsar to the target maximum 
    value at the specified radius. (Note the return value is clipped between 0 
    and 1 to avoid unphysical values.)
    """
    return numpy.clip((0.5 * r / arcmin_to_degrees(1.5)), 0., 1.)

pwn_pol_field = xTangentialPolarizationField(ra_psr, dec_psr, pol_radial_profile)
pwn_pol_deg = pwn_pol_field.polarization_degree_model()
pwn_pol_ang = pwn_pol_field.polarization_angle_model()

crab_pwn = xChandraObservation('Crab_PWN', pwn_pol_deg, pwn_pol_ang)
ROI_MODEL.add_source(crab_pwn)

# Add the pulsar
ephemeris = xEphemeris(mjd_to_met(epoch), nu0, nudot0, nuddot)
src = xPeriodicPointSource('Crab_pulsar', ra_psr, dec_psr, spec, pol_deg, pol_ang, ephemeris)
ROI_MODEL.add_source(src)

# Add also the instrumental background
#bkg = xPowerLawInstrumentalBkg()
#ROI_MODEL.add_source(bkg)

def overlay_light_curve():
    """Overlay the light curve to an existing plot.

    Note this is not calling the underlying spline.plot() method in order
    not to overwrite the axis labels everytime. (And, in addition, we do need
    to able to offset and scale the curve anyway.)

    Note also that we need the additional call to plt.legend() to update the
    legend with the new line.
    """
    ymin, ymax = plt.gca().get_ylim()
    scale = 0.9 * (ymax - ymin) / pl_norm_spline.y.max()
    x = numpy.linspace(0., 1., 250)
    y = scale * pl_norm_spline(x) + ymin
    plt.plot(x, y, color='lightgray', label='Power-law normalization')
    plt.legend()


def display():
    """Display all the relevant plots.
    """
    data_label = 'Input data'
    model_label = 'Model'
    source = 'Crab Pulsar'

    # PL normalization as a function of the pulse phase.
    plt.figure('%s PL normalization' % source)
    #plt.errorbar(pl_norm_spline.x, norm, norm_err, fmt='o', label=data_label)
    pl_norm_spline.plot(label=model_label)
    setup_gca(legend=True)

    # Polarization degree as a function of the pulse phase.
    plt.figure('%s polarization degree' % source)
    #plt.errorbar(pol_deg_spline.x, pol_deg_data, fmt='o', label=data_label)
    pol_deg_spline.plot(label=model_label)
    setup_gca(legend=True)
    overlay_light_curve()

    # Polarization angle as a function of the pulse phase.
    plt.figure('%s polarization angle' % source)
    #plt.errorbar(pol_ang_spline.x, numpy.rad2deg(pol_ang_data), fmt='o',
    #             label=data_label)
    pol_ang_spline.plot(scale=numpy.rad2deg(1.), label=model_label)
    setup_gca(ymin=-30., ylabel='Polarization angle [$^\\circ$]', legend=True)
    overlay_light_curve()



if __name__ == '__main__':
    from ixpeobssim.config import bootstrap_display
    bootstrap_display()