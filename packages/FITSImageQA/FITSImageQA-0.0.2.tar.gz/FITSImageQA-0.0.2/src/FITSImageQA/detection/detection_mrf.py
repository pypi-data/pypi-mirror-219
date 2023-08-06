from __future__ import annotations

# Standard library
from pathlib import Path
from collections.abc import Sequence
from dataclasses import dataclass

# Third-party
import sep
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table
from astropy.coordinates import SkyCoord

# Project
from . import utils
from .. import io
from ..log import logger


sep.set_extract_pixstack(500000)
default_kernel = np.array([[1,2,1], [2,4,2], [1,2,1]])
default_flux_aper = [2.5, 5, 10]
default_flux_ann = [(3, 6), (5, 8)]


__all__ = [
    'extract_sources',
    'generate_flux_model',
    'generate_lsb_source_mask',
    'get_source_segments', 
    'remove_segments_from_segmap',
]


def _byteswap(arr):
    """
    If array is in big-endian byte order (as astropy.io.fits
    always returns), swap to little-endian for SEP.
    """
    if arr is not None and arr.dtype.byteorder=='>':
        arr = arr.byteswap().newbyteorder()
    return arr


@dataclass
class Sources:
    """Data class to hold a source catalog and its associated segmentation map."""
    cat: Table
    segmap: np.ndarray


def extract_sources(
    path_or_pixels: Path | str | np.ndarray, 
    thresh: float = 2.5, 
    minarea: int = 5, 
    filter_kernel: np.ndarray = default_kernel, 
    filter_type: str = 'matched', 
    deblend_nthresh: int = 32, 
    deblend_cont: float = 0.005, 
    clean: bool = True, 
    clean_param: float = 1.0,
    bw: int = 64, 
    bh: int = None, 
    fw: int = 3, 
    fh: int = None, 
    mask: np.ndarray = None,
    subtract_sky: bool = True,
    flux_aper: list[float] = default_flux_aper,
    flux_ann: list[tuple[float, float]] = default_flux_ann,
    zpt=None,
    **kwargs
):
    """
    Extract sources using sep.
    
    https://sep.readthedocs.io

    Parameters
    ----------
    path_or_pixels : pathlib.Path or str or np.ndarray
        Image path or pixels.
    thresh : float, optional
        Threshold pixel value for detection., by default 2.5.
    minarea : int, optional
        Minimum number of pixels required for an object, by default 5.
    filter_kernel : np.ndarray, optional
        Filter kernel used for on-the-fly filtering (used to enhance detection). 
        Default is a 3x3 array: [[1,2,1], [2,4,2], [1,2,1]].
    filter_type : str, optional
        Filter treatment. This affects filtering behavior when a noise array is 
        supplied. 'matched' (default) accounts for pixel-to-pixel noise in the filter 
        kernel. 'conv' is simple convolution of the data array, ignoring pixel-to-pixel 
        noise across the kernel. 'matched' should yield better detection of faint 
        sources in areas of rapidly varying noise (such as found in coadded images 
        made from semi-overlapping exposures). The two options are equivalent 
        when noise is constant. Default is 'matched'.
    deblend_nthresh : int, optional
        Number of thresholds used for object deblending, by default 32.
    deblend_cont : float, optional
        Minimum contrast ratio used for object deblending. Default is 0.005. 
        To entirely disable deblending, set to 1.0.    
    clean : bool, optional
        If True (default), perform cleaning.
    clean_param : float, optional
        Cleaning parameter (see SExtractor manual), by default 1.0.
    bw : int, optional
        Size of background box width in pixels, by default 64.
    bh : int, optional
        Size of background box height in pixels. If None, will use value of `bw`.
    fw : int, optional
        Filter width in pixels, by default 3.
    fh : int, optional
        Filter height in pixels.  If None, will use value of `fw`.
    mask : np.ndarray, optional
        Mask array, by default None.
    subtract_sky : bool, optional
        If True (default), perform sky subtraction. 
    flux_aper : list of float, optional
        Radii of aperture fluxes, by default [2.5, 5, 10].
    flux_ann : list of tuple, optional
        Inner and outer radii for flux annuli, by default [(3, 6), (5, 8)].
    zpt : float, optional
        Photometric zero point. If not None, magnitudes will be calculated.
    **kwargs
        Arguments for sep.Background. 

    Returns
    -------
    source : Sources
        Source object with `cat` and `segmap` as attributes. 
    """
    pixels = io.load_pixels(path_or_pixels)

    # Use square boxes if heights not given.
    bh = bw if bh is None else bh
    fh = fw if fh is None else fh
    
    # Build background map using sep.
    mask = _byteswap(mask)
    data = _byteswap(pixels)
    bkg = sep.Background(pixels, bw=bw, bh=bh, fw=fw, fh=fh, mask=mask, **kwargs)

    # If desired, subtract background. 
    if subtract_sky:
        data = data - bkg

    # Extract sources using sep.
    cat, segmap = sep.extract(
        data, 
        thresh,  
        err=bkg.rms(),
        mask=mask, 
        minarea=minarea, 
        filter_kernel=filter_kernel, 
        filter_type=filter_type,
        deblend_nthresh=deblend_nthresh, 
        deblend_cont=deblend_cont, 
        clean=clean, 
        clean_param=clean_param, 
        segmentation_map=True    
    )
    
    logger.info(f'{len(cat)} sources detected.')

    # Convert catalog to astropy table.
    cat = Table(cat)
    
    # Save segment IDs for future reference.
    cat['seg_id'] = np.arange(1, len(cat) + 1, dtype=int)

    theta = cat['theta']    
    x, y = cat['x'], cat['y']
    a, b = cat['a'], cat['b']

    # Calculate SExtractor's FLUX_AUTO.
    r_kron, _ = sep.kron_radius(data, x, y, a, b, theta, 6.0)
    flux, _, _ = sep.sum_circle(data, x, y, 2.5 * (r_kron), subpix=1)

    r_min = 1.75  
    use_circ = r_kron * np.sqrt(a * b) < r_min
    flux_circ, _, _ = sep.sum_circle(data, x[use_circ], y[use_circ], r_min, subpix=1)
    
    flux[use_circ] = flux_circ
    cat['flux_auto'] = flux
    cat['r_kron'] = r_kron
    
    # HACK: see https://github.com/kbarbary/sep/issues/34.
    cat['fwhm'] = 2 * np.sqrt(np.log(2) * (a**2 + b**2))

    # If zero point given, calculate magnitudes.
    if zpt is not None:
        cat['mag'] = zpt - 2.5 * utils.log10(cat['flux'], fill_val=-99)
        cat['mag_auto'] = zpt - 2.5 * utils.log10(cat['flux_auto'], fill_val=-99)
        
    # Calculate aperture fluxes.
    for r_aper in flux_aper:
        cat[f'f_aper({r_aper})'] = sep.sum_circle(data, x, y, r_aper)[0]
        
    for r_in, r_out in flux_ann:
        cat[f'f_ann({r_in}, {r_out})'] = sep.sum_circann(data, x, y, r_in, r_out)[0]
        
    sources = Sources(
        cat=cat, 
        segmap=segmap, 
    )

    return sources
            
            
def generate_flux_model(
    segmap: np.ndarray, 
    fluxes: Sequence[float], 
    segments: Sequence[int]
) -> np.ndarray:
    """
    Generate flux model image, which replaces each segment in the segmentation map 
    with the measured flux of the associated source. 

    Parameters
    ----------
    segmap : np.ndarray
        Segmentation map.
    fluxes : list-like
        Fluxes associated with the segments.
    segments : list-like
        ID numbers of the segments that correspond to the given fluxes.

    Returns
    -------
    flux_model : np.ndarray
        The generated flux model.
    """
    flux_model = np.zeros_like(segmap, dtype=float)
    for seg_id, flux in zip(segments, fluxes):
        flux_model[segmap == seg_id] = flux
    return flux_model


def generate_lsb_source_mask(
    hires_source_pixels: np.ndarray, 
    scaled_lores_model: np.ndarray, 
    segmap: np.ndarray, 
    sb_lim_cpp: float, 
    max_ratio: float, 
    min_area: int
) -> np.ndarray:
    """
    Generate a mask that identifies which pixels belong to LSB sources.

    Parameters
    ----------
    hires_source_pixels : np.ndarray
        High resolution image pixels that are associated with detected sources.
    scaled_lores_model : np.ndarray
        Normalized low resolution model.
    segmap : np.ndarray
        Segmentation map.
    sb_lim_cpp : float
        Surface brightness limit in counts per pixel.
    max_ratio : float
        Max ratio hires_source_pixels / scaled_lores_model allowed for LSB sources.
    min_area : int
        Minimum area of LSB source in pixels.

    Returns
    -------
    lsb_mask : np.ndarray
        Mask with pixels that are associated with a LSB source set to one. All other 
        pixels will be set to  zero.
    """
    lsb_mask = np.zeros_like(segmap)
    segments = np.unique(segmap[segmap>0])
    flux_ratio = utils.divide_pixels(hires_source_pixels, scaled_lores_model)

    num_removed = 0
    for seg_id in segments:
        mask = segmap == seg_id
        if mask.sum() > min_area:
            ratio = np.nanmax(flux_ratio[mask])
            flux = np.nanmax(hires_source_pixels[mask])
            if (flux < sb_lim_cpp) and (ratio < max_ratio):  
                num_removed += 1
                lsb_mask[mask] = 1
                
    logger.info(f'Found {num_removed} LSB sources with at least {min_area} pixels.')
    
    return lsb_mask


def get_source_segments(
    segmap: np.ndarray, 
    coords: list | tuple | SkyCoord, 
    wcs_or_header: WCS | fits.Header
) -> np.ndarray:
    """[summary]

    Parameters
    ----------
    segmap : np.ndarray
        Segmentation map from which to find segment IDs.
    coords : list or tuple or SkyCoord
        RA and DEC of source(s).
    wcs_or_header : WCS or astropy.fits.Header
        WCS or header object to convert RA and DEC to xy coordinates.

    Returns
    -------
    segments : np.ndarray
        Segment ID numbers associated with given source(s).
    """
    if isinstance(coords, (list, tuple)):
        sc = SkyCoord([coords[0]], [coords[1]], unit='deg')
    elif isinstance(coords, np.ndarray):
        sc = SkyCoord(coords[:, 0], coords[:, 1], unit='deg')
    elif isinstance(coords, SkyCoord):
        sc = coords
    else:
        raise TypeError(f'{type(coords)} not a valid coords type.')
        
    if isinstance(wcs_or_header, fits.Header):
        wcs = WCS(wcs_or_header)
    elif isinstance(wcs_or_header, WCS):
        wcs = wcs_or_header
    else:
        raise TypeError(f'{type(wcs_or_header)} not a valid WCS type.')

    x_arr, y_arr = sc.to_pixel(wcs)

    segments = []
    for src_num, (x, y) in enumerate(zip(x_arr, y_arr)):
        c = sc[src_num].to_string('hmsdms')
        if 0 < int(y) < segmap.shape[0] and 0 < int(x) < segmap.shape[1]:
            logger.debug(f'Found source at {c} in segmap.')
            seg_id = segmap[int(y), int(x)]
            segments.append(seg_id)
        else:
            logger.warning(f'Source at {c} is not in footprint.')
    segments = np.array(segments)
    
    return segments


def remove_segments_from_segmap(
    segmap: np.ndarray, 
    segments: Sequence[int]
) -> np.ndarray:
    """
    Remove given segments from segmentation map. 

    Parameters
    ----------
    segmap : np.ndarray
        Segmentation map from which to remove sources.
    segments : list-like
        Segment ID numbers to be removed from segmentation map.

    Returns
    -------
    s : np.ndarray
        Updated segmentation map.
    """
    s = segmap.copy()
    for seg_id in segments:
        s[s == seg_id] = 0
    return s
