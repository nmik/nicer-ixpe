import os
import sys
import argparse
from astropy import log
from astropy.logger import logging
from astropy.io import fits
import numpy as np

def cut_pix(pi):
    ene=pi*0.04
    y=130+(ene-2)*30
    return y

def cut_fra(pi):
    ene=pi*0.04
    y=0.8*(1-np.exp(-(ene+0.25)/1.1))+ene*0.004
    return y

def rejection(path_lv2, path_lv1, output):
    #opening lv2
    data_lv2={}
    print(path_lv2,' opening')
    hdulist_input = fits.open(path_lv2)
    extension_names = list(map(lambda _ext: _ext.name, hdulist_input[1:]))
    events = hdulist_input['EVENTS'].data.T
    hdulist_input.info()
    _run = hdulist_input[1].data
    for _key in ['TRG_ID','X', 'Y', 'Q', 'U', 'PI', 'TIME']:
        data_lv2[_key] = _run[_key]


    # opening lv1
    keys=['NUM_PIX','EVT_FRA','TRK_BORD','TIME']
    file_list = {}
    data_lv1 = {_key: np.array([]) for _key in keys}
    
    for _file in path_lv1:
        print(_file,' opening')
        hdul = fits.open(_file)
        extension = list(map(lambda _ext: _ext.name, hdulist_input[1:]))
        events_l1 = hdul['EVENTS'].data.T
        hdul.info()
        _run = hdul[1].data
        for _key in keys:
            data_lv1[_key]=np.append(data_lv1[_key], _run[_key])

    print('START {} and {}'.format(data_lv1['TIME'][0],data_lv2['TIME'][0]))
    print('STOP {} and {}'.format(data_lv1['TIME'][-1],data_lv2['TIME'][-1]))
    
    # build the dictionary to filter
    data_filt={}
    a,_mask,c=np.intersect1d(data_lv1['TIME'],data_lv2['TIME'],return_indices=True)
    for _key in data_lv1:
        data_filt[_key]=data_lv1[_key][_mask]
    a,_mask,c=np.intersect1d(data_lv2['TIME'],data_lv1['TIME'],return_indices=True)
    data_filt['PI']=data_lv2['PI'][_mask]
    data_filt['X']=data_lv2['X'][_mask]
    data_filt['Y']=data_lv2['Y'][_mask]

    # filtering
    efra =  np.logical_and(data_filt['EVT_FRA']>cut_fra(data_filt['PI']),data_filt['EVT_FRA']<1.0)
    numpix = np.logical_and(efra,data_filt['NUM_PIX']<cut_pix(data_filt['PI']))
    trk_bord = np.logical_and(numpix,data_filt['TRK_BORD']<2)
    if output=='bkg':
        mask = np.where(np.logical_not(trk_bord))[0]
    else:
        mask = np.where(trk_bord)[0]

    times_filtered = data_filt['TIME'][mask]
    times_lv2 = events['TIME']
    intersect, lv2_idx, lv1_idx = np.intersect1d(times_lv2, times_filtered, return_indices=True)
    
    if output!='tag':
        dict_item = lambda _col: (_col, events[_col][lv2_idx])
        columns = list(map(lambda _col: _col.name, events.columns))
        dict_events = dict(map(dict_item, columns))

        #create new fits file
        _header_primary = hdulist_input[0].header
        primary_hdu = fits.PrimaryHDU(header=_header_primary)
        hdul_new = fits.HDUList([primary_hdu])
        for extname in extension_names:
            if extname == 'EVENTS':
                input_columns = hdulist_input[extname].columns
                columns = []
                for i, _input_column in enumerate(input_columns):
                    _name, _format = _input_column.name, _input_column.format
                    _array = dict_events[_name]
                    columns.append(fits.Column(name=_name, array=_array, format=_format))

                _header_table = hdulist_input[extname].header
                table_hdu = fits.BinTableHDU.from_columns(columns, header=_header_table)

                hdul_new.append(table_hdu)
        
            else:
                hdul_new.append(hdulist_input[extname])

        hdul_new.writeto(path_lv2[:-5]+'_'+output+'.fits', overwrite=True)
    else:
        #aggiungere la colonna con la maschera
        tag=np.zeros(len(data_lv2['TIME']))
        tag[lv2_idx]=1

        dict_item = lambda _col: (_col, events[_col])
        columns = list(map(lambda _col: _col.name, events.columns))
        dict_events = dict(map(dict_item, columns))

        #create new fits file
        _header_primary = hdulist_input[0].header
        primary_hdu = fits.PrimaryHDU(header=_header_primary)
        hdul_new = fits.HDUList([primary_hdu])
        for extname in extension_names:
            if extname == 'EVENTS':
                input_columns = hdulist_input[extname].columns
                columns = []
                for i, _input_column in enumerate(input_columns):
                    _name, _format = _input_column.name, _input_column.format
                    _array = dict_events[_name]
                    columns.append(fits.Column(name=_name, array=_array, format=_format))

                columns.append(fits.Column(name='BKG TAG', array=tag, format='B'))
                _header_table = hdulist_input[extname].header
                table_hdu = fits.BinTableHDU.from_columns(columns, header=_header_table)

                hdul_new.append(table_hdu)
        
            else:
                hdul_new.append(hdulist_input[extname])

        hdul_new.writeto(path_lv2[:-5]+'_'+output+'.fits', overwrite=True)
        
def main(args=None):
    
    parser = \
        argparse.ArgumentParser(description="Filter a lv2 file based on a lv1 cut")

    parser.add_argument("path_lv2", help="Input file lv2", type=str)
    parser.add_argument("path_lv1", help="Input file lv1", type=str, nargs='+')
    parser.add_argument("--output", default='rej',
                        help="Output file: rej (includes only source events), bkg (includes only rejected events) and tag (includes a tag column where events having 1 are src and 0 are bkg)", type=str)

    args = parser.parse_args(args)
    rejection(args.path_lv2, args.path_lv1, args.output)

if __name__ == '__main__':
    main(sys.argv[1:])
