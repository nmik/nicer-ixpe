############################################################
###                                                      ###
### Script credit: Stefano Silvestri (UniPi, INFN-Pisa) ###
###                                                      ###
############################################################

from glob import glob

import numpy


from ixpeobssim.core import pipeline
from ixpeobssim.core.hist import xHistogram1d
from ixpeobssim.evt.event import xEventFileFriend, xEventFile
from ixpeobssim.utils.logging_ import logger
from ixpeobssim.utils.argparse_ import xArgumentParser
from ixpeobssim.instrument import DU_IDS



__description__ = \
"""Split the provided level 2 file in identical time bins according to the
 duration input by the user."""

parser = xArgumentParser(description=__description__)
parser.add_argument('--path', nargs='+',
                    help='root folder containing the unzipped event_l1 and'
                    'event_l2 sub_folders')
parser.add_argument('--duration', type=float,
                     help='Tentative time bin size'
                    ' (will be rounded to make identical bins)')


def lvl1_file_list(root_folder):
    '''
    '''
    return numpy.sort(glob(root_folder + '/event_l1/*evt1*'))

def lvl1_du_file_list(root_folder, du_id):
    '''
    '''
    return numpy.sort(glob(root_folder + f'event_l1/*det{du_id}*evt1*'))

def lvl2_file(root_folder, du_id):
    '''
    '''
    return glob(root_folder + f'/event_l2/*det{du_id}*evt2*')[0]

def make_tgrid(bin_size, lvl2_path):
    ''' Given a bin size, returns a time grid approximating that bin size
    '''
    evt = xEventFile(lvl2_path)
    t0 = evt.primary_header['TSTART']
    t1 = evt.primary_header['TSTOP']
    nbins = numpy.int((t1-t0)//bin_size)
    return numpy.linspace(t0, t1, nbins)


def build_livetime_hist(evt_friend, t_bins):
    ''' Create a livetime histogram, each time bin containing the livetime
    for the provided time interval
    '''
    l1_time = evt_friend.l1value('TIME', all_events=True)
    livetime = evt_friend.l1value('LIVETIME', all_events=True)
    #Maybe this is the best spot to place GTI filtering
    gti_start = evt_friend.file_list2[0].gti_data()['START']
    gti_stop = evt_friend.file_list2[0].gti_data()['STOP']
    l1_time = evt_friend.l1value('TIME', all_events=True)
    filter_l1=[]
    for j in range (len(gti_start)):
        filter_l1.append(numpy.logical_and((l1_time<gti_stop[j]),
                                         (l1_time>gti_start[j])))
    l1_mask = numpy.logical_or.reduce(filter_l1)
    lvt_hist = xHistogram1d(t_bins, xlabel='MET [s]', ylabel='Livetime [s]')
    return lvt_hist.fill(l1_time[l1_mask], weights = livetime[l1_mask] / 1.e6)

#Once you have the livetime histogram you can split the file and modify their
#Livetime information in the header

def update_livetime(evt_file_path, livetime):
    ''' Modify the header(s) with the correct livetime
    '''
    evt_file = xEventFile(evt_file_path)
    for hdu_list in evt_file.hdu_list:
        hdu_list.header['LIVETIME']=livetime
        logger.info(f'Updating livetime of {evt_file_path}: {livetime}...')
    evt_file.write(evt_file_path, overwrite=True)

def split_file(root_folder, du_id, t_bins):
    '''
    '''
    evt_friend = xEventFileFriend(lvl2_file(root_folder, du_id),
                                  *lvl1_du_file_list(root_folder,du_id))
    n_bins = len(t_bins)
    #create a livetime histogram with livetime content per time interval
    lt_hist = build_livetime_hist(evt_friend, t_bins)
    for nbin in range (n_bins-1):
        tstart = t_bins[nbin]
        tstop = t_bins[nbin+1]
        selected = pipeline.xpselect(lvl2_file(root_folder, du_id), tmin=tstart,
                                     tmax=tstop, suffix=f'tbin_{nbin:05}')
        lt = lt_hist.content[nbin]
        update_livetime(selected[0], lt)

def process(**kwargs):
    '''
    '''
    root_folder=kwargs.get('path')[0]
    duration=kwargs.get('duration')
    grid = make_tgrid(duration, lvl2_file(root_folder, 1))
    for du_id in DU_IDS:
        split_file(root_folder, du_id, grid)

def main():
    '''
    '''
    process(**parser.parse_args().__dict__)

if __name__ == '__main__':
    main()