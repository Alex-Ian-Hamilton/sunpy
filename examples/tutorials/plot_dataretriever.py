# -*- coding: utf-8 -*-
"""
=========================================
Using the Universal Data Retriever
=========================================

In this example you will be learning how to use SunPy's universal downloader interface.
"""

##############################################################################
# Start by importing the necessary modules.
from sunpy.net.jsoc.attrs import Series, Protocol, Notify, Compression, Segment
from sunpy.net.vso.attrs import Extent, Field, Provider, Source, Physobs, Pixels, Resolution, Detector, Filter, Sample, Quicklook, PScale
from sunpy.net.attrs import Time, Instrument, Level, Wavelength
from sunpy.net import Fido
from sunpy.time import parse_time
import astropy.units as u

##############################################################################
# A query is used to select the data you are looking for, you can use the
# Fido.search() method which returns a UnifiedResponse object.
# A basic query is run with simply the date from sunpy.net import vso.
results = Fido.search(Time('2012/3/4', '2012/3/4'))
# ERROR: this doesn't work!
#       TypeError: (<class 'sunpy.net.vso.attrs.Time'>,)
# The VSO can supposedly do this (the website can), but I can't get it to work:
inst_lis = ('512-CHANNEL MAGNETOGRAPH', '60-FT SHG', 'AIA', 'BCS', 'BIG BEAR', 'CDS', 'CELIAS', 'CERRO TOLOLO', 'CFDT1', 'CFDT2', 'CHP', 'CLIMSO', 'COSTEP', 'DPM', 'EIS', 'EIT', 'EL TEIDE', 'ERNE', 'EVE', 'GOLF', 'HMI', 'HXT', 'IMPACT', 'LASCO', 'LEARMONTH', 'LYRA', 'MAUNA LOA', 'MDI', 'MK4', 'MOF/60', 'MOTH', 'O-SPAN', 'OVSA', 'PLASTIC', 'RHESSI', 'SECCHI', 'SOLAR FTS SPECTROMETER', 'SOT', 'SPECTROHELIOGRAPH', 'SPECTROMAGNETOGRAPH', 'SUMER', 'SWAN', 'SWAP', 'SWAVES', 'SXI-0', 'SXT', 'TENERIFE', 'UDAIPUR', 'UVCS', 'VIRGO', 'VSM', 'WBS', 'XRT')
from sunpy.net import vso
client = vso.VSOClient()
for inst in inst_lis:
    print('\n' + str(inst))
    qr=client.query_legacy(tstart='2001/01/01 12:00', tend='2001/01/01 12:01', instrument=inst)
    print(qr)
# This will always stop on one of the instruments, seemingly at randon, generally with:
# ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host

##############################################################################
# You can be more specific by adding minutes to time strings:
results = Fido.search(Time('2012/3/4 12:00', '2012/3/6 12:01'), Instrument('AIA'))
# ERROR: again, doesn't work, see above!
# Note: you can pass a datetime ubject
##############################################################################
# The universal downloader has access to multiple data libraries, the two major ones are the `Virtual Solar Observatory (VSO)<http://sdac.virtualsolar.org/cgi/search>`_  and the `Joint Science Operations Center (JSOC)<http://jsoc.stanford.edu/>`_.
# Each data source may have unique attributes that can be used for filtering, but they can all be filtered by Time, Instrument, Level, Wavelength, as can be seen in the import:
from sunpy.net.attrs import Time, Instrument, Level, Wavelength
# To further filter the query, we can add an instrument:
results = Fido.search(Time('2012/3/4 12:00', '2012/3/6 12:01'), Instrument('AIA'))
# Add a level filter:
results = Fido.search(Time('2012/3/4 12:00', '2012/3/6 12:01'), Instrument('AIA'), Level(0))
# Add/or wavelength (range) filters:
results = Fido.search(Time('2012/3/4 12:00', '2012/3/6 12:01'), Instrument('AIA'), Wavelength(304 * u.AA, 304 * u.AA))
# Note: the wavelength range is given using astropy Quantity.

##############################################################################
# You can see the returned UnifiedResponse object as a table representation:
results
# You can also access an entry using it's index:
results[0]
# ERROR: this doesn't work!
# Note: results returned don't comprehensively cover the attribute/filters used, so if the search includes wavelength ten that should be in the columns shown.


# Test all the VSO instrument options
inst_lis = ('512-CHANNEL MAGNETOGRAPH', '60-FT SHG', 'AIA', 'BCS', 'BIG BEAR', 'CDS', 'CELIAS', 'CERRO TOLOLO', 'CFDT1', 'CFDT2', 'CHP', 'CLIMSO', 'COSTEP', 'DPM', 'EIS', 'EIT', 'EL TEIDE', 'ERNE', 'EVE', 'GOLF', 'HMI', 'HXT', 'IMPACT', 'LASCO', 'LEARMONTH', 'LYRA', 'MAUNA LOA', 'MDI', 'MK4', 'MOF/60', 'MOTH', 'O-SPAN', 'OVSA', 'PLASTIC', 'RHESSI', 'SECCHI', 'SOLAR FTS SPECTROMETER', 'SOT', 'SPECTROHELIOGRAPH', 'SPECTROMAGNETOGRAPH', 'SUMER', 'SWAN', 'SWAP', 'SWAVES', 'SXI-0', 'SXT', 'TENERIFE', 'UDAIPUR', 'UVCS', 'VIRGO', 'VSM', 'WBS', 'XRT')
for inst in inst_lis:
    print('\n' + str(inst))
    results=Fido.search(Time('2012/3/4 12:00', '2012/3/6 12:01'), Instrument(inst))
    print(results)

##############################################################################
# The Universal Data Retriever has specific source methods for:
# EVE, GOES, LYRA, NOAA, NORH and RHESSI
inst_lis = ('EVE', 'GOES', 'LYRA', 'NOAA', 'NORH', 'RHESSI')
for inst in inst_lis:
    print('\n' + str(inst))
    results=Fido.search(Time('2012/3/4 12:00', '2012/3/4 12:01'), Instrument(inst))
    print(results)
# GOES just doesn't work, I get 0 results back

##############################################################################
# There are further query/finder filter options, some of which are instrument
# specific:
ans1 = Fido.search(Time('2012/8/9 12:00','2012/8/10 12:01'), Instrument('eve'), Source('sdo'))
ans1 = Fido.search(Time('2012/8/9 12:00','2012/8/10 12:01'), Instrument('eve'), Level(0))
# ERROR: this doesn't work.
ans1 = eve.EVEClient._can_handle_query(Time('2012/8/9 12:00','2012/8/10 12:01'),Instrument('eve'),Level(0))

##############################################################################
# To download the files reference in the UnifiedResponse object, you can use the
# Fido.fetch() method:
results = Fido.search(Time('2012/3/4', '2012/3/4'), Instrument('BIG BEAR'))
downloaded = Fido.fetch(results, progress=True, wait=True)
# This returns a DownloadResponse object that is simply a list of the downloaded
# files:
print(downloaded)



inst_dict = {'512-CHANNEL MAGNETOGRAPH':'512-channel Magnetograph',
'60-FT SHG':'60-foot Tower Spectroheliograph',
'AIA':'Atmospheric Imaging Assembly',
'BCS':'Bragg Crystal Spectrometer',
'BIG BEAR':'Big Bear Solar Observatory, California TON and GONG+ sites',
'CDS':'Coronal Diagnostic Spectrometer',
'CELIAS':'Charge, Element, and Isotope Analysis System',
'CERRO TOLOLO':'Cerro Tololo, Chile GONG+ site',
'CFDT1':'Cartesian Full-Disk Telescope No.1',
'CFDT2':'Cartesian Full-Disk Telescope No.2',
'CHP':'Chromospheric Helium-I Imaging Photometer',
'CLIMSO':'Christian Latouche IMageur SOlaire',
'COSTEP':'Comprehensive Suprathermal and Energetic Particle Analyzer',
'DPM':'Digital Prominence Monitor',
'EIS':'EUV Imaging Spectrometer',
'EIT':'Extreme ultraviolet Imaging Telescope',
'EL TEIDE':'Canary Islands GONG+ site',
'ERNE':'Energetic and Relativistic Nuclei and Electron experiment',
'EVE':'Extreme Ultraviolet Variability Experiment',
'GOLF':'Global Oscillations at Low Frequencies',
'HMI':'Helioseismic and Magnetic Imager',
'HXT':'Hard X-Ray Telescope',
'IMPACT':'In-situ Measurements of Particles and CME Transients',
'LASCO':'Large Angle and Spectrometric Coronagraph',
'LEARMONTH':'Australian GONG+ site',
'LYRA':'LYman alpha RAdiometer',
'MAUNA LOA':'Hawaiian GONG+ site',
'MDI':'Michelson Doppler Imager',
'MK4':'Mk. IV coronagraph',
'MOF/60':'Mt. Wilson 60-Foot Tower Telescope',
'MOTH':'Magneto Optical filters at Two Heights',
'O-SPAN':'O-SPAN (formerly known as ISOON)',
'OVSA':'Owens Valley Solar Array',
'PLASTIC':'PLasma And SupraThermal Ion Composition',
'RHESSI':'Reuven Ramaty High Energy Solar Spectroscopic Imager',
'SECCHI':'Sun Earth Connection Coronal and Heliospheric Investigation',
'SOLAR FTS SPECTROMETER':'Solar FTS Spectrometer',
'SOT':'Solar Optical Telescope',
'SPECTROHELIOGRAPH':'SpectroHeliograph',
'SPECTROMAGNETOGRAPH':'SpectroMagnetograph',
'SUMER':'Solar Ultraviolet Measurements of Emitted Radiation',
'SWAN':'Solar Wind Anisotropies',
'SWAP':'Sun Watcher using Active pixel system detector and image Processing',
'SWAVES':'STEREO/WAVES',
'SXI-0':'Solar X-ray Imager',
'SXT':'Soft X-Ray Telescope',
'TENERIFE':'Canary Islands TON site',
'UDAIPUR':'Indian GONG+ site',
'UVCS':'Ultraviolet Coronagraph Spectrometer',
'VIRGO':'Variability of Solar Irradiance and Gravity Oscillations',
'VSM':'Vector SpecroMagnetograph',
'WBS':'Wide Band Spectrometer',
'XRT':'X-Ray Telescope'}


inst_lis = ('512-CHANNEL MAGNETOGRAPH',
'60-FT SHG',
'AIA',
'BCS',
'BIG BEAR',
'CDS',
'CELIAS',
'CERRO TOLOLO',
'CFDT1',
'CFDT2',
'CHP',
'CLIMSO',
'COSTEP',
'DPM',
'EIS',
'EIT',
'EL TEIDE',
'ERNE',
'EVE',
'GOLF',
'HMI',
'HXT',
'IMPACT',
'LASCO',
'LEARMONTH',
'LYRA',
'MAUNA LOA',
'MDI',
'MK4',
'MOF/60',
'MOTH',
'O-SPAN',
'OVSA',
'PLASTIC',
'RHESSI',
'SECCHI',
'SOLAR FTS SPECTROMETER',
'SOT',
'SPECTROHELIOGRAPH',
'SPECTROMAGNETOGRAPH',
'SUMER',
'SWAN',
'SWAP',
'SWAVES',
'SXI-0',
'SXT',
'TENERIFE',
'UDAIPUR',
'UVCS',
'VIRGO',
'VSM',
'WBS',
'XRT')