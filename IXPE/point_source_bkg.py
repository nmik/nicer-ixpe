# Copyright (C) 2022, the ixpeobssim team.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU GengReral Public Licensese as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Toy point source with (non-negligible) instrumental background.

This is useful to study the background subtraction in spectro-polarimetric analysis.
"""

from __future__ import print_function, division

import numpy

from ixpeobssim.config import file_path_to_model_name, bootstrap_display
from ixpeobssim.srcmodel.bkg import xTemplateInstrumentalBkg
from ixpeobssim.srcmodel.polarization import constant
from ixpeobssim.srcmodel.roi import xPointSource, xROIModel
from ixpeobssim.srcmodel.spectrum import power_law
from ixpeobssim.utils.fmtaxis import fmtaxis
from ixpeobssim.utils.matplotlib_ import plt, setup_gca


__model__ = file_path_to_model_name(__file__)


# Source coordinates, in decimal degrees.
SRC_NAME = 'Toy point surce w/ bkg'
SRC_RA, SRC_DEC = 45., 45.

# Pointing coordinates
PNT_RA, PNT_DEC = SRC_RA, SRC_DEC

# Spectral and polarimetric parameters
PL_NORM = 5e-2
PL_INDEX = 2.
PA = 30.
PD_INT = 0.1
PD_SLOPE = 0.05

spec = power_law(PL_NORM, PL_INDEX)

def pol_deg(E, t=None, ra=None, dec=None):
    """Linear model for the polarization degree vs. energy.
    """
    return numpy.clip(PD_INT + PD_SLOPE * (E - 1.), 0., 1.)

pol_ang = constant(numpy.radians(PA))

# Definition of the sources and the region of interest.
src = xPointSource('Point source', SRC_RA, SRC_DEC, spec, pol_deg, pol_ang)
bkg = xTemplateInstrumentalBkg()
ROI_MODEL = xROIModel(PNT_RA, PNT_DEC, src, bkg)


def display(emin=1., emax=12., area=3.e-2):
    """Display the source model.

    Note the background needs to be multiplied for an effective area on the
    readout plane to be compared with the source. A circle with 1~mm radius is
    a sensible proxy for a source cut.
    """
    energy = numpy.linspace(emin, emax, 100)
    plt.figure('%s spectrum' % __model__)
    plt.plot(energy, src.photon_spectrum(energy), label='Source')
    plt.plot(energy, area * bkg.photon_spectrum(energy), label='Background')
    setup_gca(xmin=emin, xmax=emax, logx=True, logy=True, grids=True, legend=True, **fmtaxis.spec)


if __name__ == '__main__':
    bootstrap_display()
