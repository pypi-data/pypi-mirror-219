from astroquery.gaia import Gaia
from astroquery.sdss import SDSS

from astropy.io import fits
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
from astropy.coordinates import SkyCoord
import astropy.units as u

from reproject.mosaicking import find_optimal_celestial_wcs
from reproject import reproject_interp
from reproject.mosaicking import reproject_and_coadd

import matplotlib.pyplot as plt
import numpy as np


class DataTable():
    def __init__(self, coord, radius="10 arcsec", source_table="gaiadr3.gaia_source"):
        """ Initialize DataTable object to hold GAIA data information (+ other sources).
        Currently finds closest source to specified coordinates.

        Args:
            coord (SkyCoord): Coordinates of the target/field
            radius (str, optional): Search radius including units. Defaults to "10 arcsec".
            source_table (str, optional): Which gaia source table to query. Can specify dr2, dr3, etc.
                Needs to be a source table. Defaults to "gaiadr3.gaia_source".
        """
        self.radius = radius
        self.coord = coord
        # configure Gaia query environment
        self.set_source_table(source_table)
        Gaia.ROW_LIMIT = 1
        # query gaia-source, ensure we get a row
        self.query_result = Gaia.query_object_async(coord, radius)
        assert len(self.query_result) > 0, "Empty table returned."
        # set source ID
        self.source_id = self.query_result[0]["source_id"]
        self.has_epoch_photometry = self.query_result[0]["has_epoch_photometry"]
        # get epoch_photometry table and set it as attribute
        if self.has_epoch_photometry:
            self.get_epoch_photometry()

    def set_source_table(self, source_table):
        """Setting the source table variables with search output.
        (to do: have a list of available source tables and assert that
        specified table is in the list before continuing - display available
        source tables)

        Args:
            source_table (str): Name of the source table to be searched.
        """
        self.source_table = source_table
        Gaia.MAIN_GAIA_TABLE = self.source_table

    def get_epoch_photometry(self, verbose = False):
        """ Retrieves epoch photometry data from Gaia Datalink service for current object.

        Args:
            verbose (bool, optional): Prints verbose statements. Defaults to False.
        """

        #This is hardcoded so that this function does this one thing, should make it easier to test and validate
        retrieval_type = 'EPOCH_PHOTOMETRY'   # Options are: 'EPOCH_PHOTOMETRY', 'MCMC_GSPPHOT', 'MCMC_MSC', 'XP_SAMPLED', 'XP_CONTINUOUS', 'RVS', 'ALL'
        data_structure = 'INDIVIDUAL'   # Options are: 'INDIVIDUAL', 'COMBINED', 'RAW'
        data_release   = 'Gaia DR3'     # Options are: 'Gaia DR3' (default), 'Gaia DR2'

        assert np.ndim(self.source_id)==0, "Check that source id is scalar, just in case" 
        assert int(self.source_id), "Wrong type: source_id cannot be converted to int (needed by astroquery)"

        #int is necessary for astroquery to work, it doesn't like np.int64 
        datalink = Gaia.load_data(ids=int(self.source_id), data_release = data_release, 
                                retrieval_type=retrieval_type, 
                                data_structure = data_structure, 
                                verbose = False, output_file = None)

        dl_key = f"{retrieval_type}-{data_release} {self.source_id}.xml"

        if verbose:
            print(f'Datalink {retrieval_type} retrieved from {data_release}')
            
        #Convert datalink table to Astropytable and store as attribute   
        eptable = datalink[dl_key][0].to_table()  
        
        self.epoch_photometry  = dict()
        for band in ["G","BP","RP"]:
            self.epoch_photometry[band] = eptable[eptable["band"]==band]
  

    def plot_epoch_photometry(self, band = 'G', ax = None, fig = None, plot_kwargs = None):

        pass
        # if fig is None: fig = plt.figure(1)
        # if ax is None: ax = fig.add_subplot(111)
        # tab = ep[band]
        # #phase = tab["time"]/Period - np.floor(tab["time"]/Period)
        # ax.plot(phase, tab["mag"], plot_kwargs)
        # ax.invert_yaxis()

    def get_spectrum(self):
        pass

    def get_sdss(self):
        """ 
        Query SDSS for image of region surrounding ra, dec coords.    
        This function uses mosaicking of plate images provided by reproject:
        https://reproject.readthedocs.io/en/stable/mosaicking.html   
        Output image not advised for science, use at own peril.
        """
        
        # Query SDSS
        xid = SDSS.query_region(self.coord, radius=self.radius, spectro=False)
        if xid is None:
            print('No SDSS overlap with region of interest.')
            return None
        
        # Get images from SDSS (returns whole plate)
        imlist = SDSS.get_images(matches=xid, band='g') # returns whole plate, need to cutout region
        hdus = [im[0] for im in imlist]
        # for i in range(len(imlist)):
        #     w = WCS(imlist[i][0])
        #     data = imlist[i][0].data
        #     header = imlist[i][0].header
        #     hdu = fits.PrimaryHDU(data,header=header)
        #     hdu.writeto(f'test_{i}.fits',overwrite=True)

        # Make a mosaic from the images
        wcs_out, shape_out = find_optimal_celestial_wcs(hdus)
        array, footprint = reproject_and_coadd(
            hdus, wcs_out, shape_out=shape_out, reproject_function=reproject_interp
            )
        w = WCS(wcs_out.to_header())

        # Cutout the region of interest
        radius_qty = u.Quantity(self.radius,unit=self.radius.split(' ')[1])
        cutout = Cutout2D(array, self.coord, radius_qty, wcs=w)
        cutoutdata = cutout.data
        cutoutheader = cutout.wcs.to_header() 
        ## TODO: Header just contains WCS, need to update with more information ##
        
        # Construct HDU and assign to global variable
        hdu = fits.PrimaryHDU(cutoutdata, header=cutoutheader)
        self.sdss_im = hdu
        return self.sdss_im
    
    def plot_sdss(self):
        """ Plot the SDSS image that was retrieved in this.get_sdss.
        """
        if self.sdss_im is None:
            print('Need to run get_sdss to load an image first!')
            return None
        
        wnew = WCS(self.sdss_im.header)
        plt.subplot(projection=wnew)
        plt.imshow(
            self.sdss_im.data,vmin=0.1,vmax=0.8,interpolation='nearest',origin='lower')
        plt.show()