"""
spmp
Satellite Products Metadata Parser

Copyright (C) <2023>  <Manchon Pierre>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
"""
Naming convention regexs and their meaning.

Sources for the naming conventions:
########################################################################################################################

Landsat scenes:
 https://gisgeography.com/landsat-file-naming-convention/
Landsat-C1:
 https://www.usgs.gov/faqs/what-naming-convention-landsat-collections-level-1-scenes?qt-news_science_products=0#qt-news_science_products
Landsat-MSS (p. 4-5):
 https://www.usgs.gov/media/files/landsat-1-5-multispectral-scanner-level-1-data-format-control-book
Landsat-TM (p. 5):
 https://www.usgs.gov/media/files/landsat-4-5-thematic-mapper-level-1-data-format-control-book
Landsat-ETM (p. 5-6):
 https://www.usgs.gov/media/files/landsat-7-level-1-data-format-control-book
Landsat-ETM+ (p. 3-4):
 https://www.usgs.gov/media/files/landsat-8-level-1-data-format-control-book

Sentinel1-SAR:
 https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/naming-conventions
Sentinel2-MSI:
 https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi/naming-convention
Sentinel3-SLSTR:
 https://sentinel.esa.int/web/sentinel/user-guides/sentinel-3-olci/naming-convention
Sentinel3-Synergy:
 https://sentinel.esa.int/web/sentinel/user-guides/sentinel-3-synergy/naming-conventions
Sentinel3-Altimetry:
 https://sentinel.esa.int/web/sentinel/user-guides/sentinel-3-altimetry/naming-conventions

Source of the sensors specs:
########################################################################################################################

MSS:
https://landsat.gsfc.nasa.gov/the-multispectral-scanner-system/
https://www.indexdatabase.de/db/s-single.php?id=6
https://eos.com/landsat-4-mss/

TM:
https://landsat.gsfc.nasa.gov/the-thematic-mapper/
https://www.indexdatabase.de/db/bs.php?sensor_id=7
https://eos.com/landsat-5-tm/

ETM:
https://landsat.gsfc.nasa.gov/the-enhanced-thematic-mapper-plus/
https://www.indexdatabase.de/db/bs.php?sensor_id=8
https://eos.com/landsat-7/

OLI-TIRS:
https://www.usgs.gov/core-science-systems/nli/landsat/landsat-8-oli-and-tirs-calibration-notices
https://www.usgs.gov/centers/eros/science/usgs-eros-archive-landsat-archives-landsat-8-oli-operational-land-imager-and?qt-science_center_objects=0#qt-science_center_objects
https://landsat.gsfc.nasa.gov/operational-land-imager-oli/
https://landsat.gsfc.nasa.gov/thermal-infrared-sensor-tirs/
https://www.indexdatabase.de/db/bs.php?sensor_id=168
https://eos.com/landsat-8/

MSI:
https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/msi-instrument
https://sentinel.esa.int/documents/247904/685211/Sentinel-2_User_Handbook
https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi/document-library/-/asset_publisher/Wk0TKajiISaR/content/sentinel-2-user-handbook
https://www.indexdatabase.de/db/bs.php?sensor_id=96
https://eos.com/sentinel-2/

import re

test_pattern = '([L])([COTEM])([078]+)_([L1GTPS]+)_(\d{6})_(\d{8})_(\d{8})_(\d{2})_([RT12]+)'
test_str = 'LC08_L1TP_187021_20140328_20170424_01_T1'
"""

naming_convention = {
    r'([L])([COTEM])([078]+)_([L1GTPS]+)_(\d{6})_(\d{8})_(\d{8})_(\d{2})_([RT12]+)':
        {#'pattern': 'LXSS_LLLL_PPPRRR_YYYYMMDD_yyyymmdd_CC_TX',
         #'pattern_name': 'Landsat Product Identifier',
         'program': 1,
         'sensor': 2,
         'mission': 1 + 3,
         'processing_level': 4,
         'tile': 5,
         'sensing_date': 6,
         'processing_year': 7,
         'collection_number': 8,
         'collection_category': 9,
         },
    r'([L])([COTEM])(\d{1})(\d{6})(\d{7})(\D{3})(\d{2})':
        {#'pattern': 'LXSPPPRRRYYYYDDDGSIVV',
         #'pattern_name': 'Landsat Scene ID',
         'program': 1,
         'sensor': 2,
         'satellite': 3,
         'processing_level': 4,
         'tile': 5,
         'sensing_date': 6,
         'processing_year': 7,
         'collection_number': 8,
         'collection_category': 9,
         },
    r'(S)(\d{1})(A|B)_(MSI)(L1C|L2C)_(\d{8})([T])(\d{6})_([N])(\d{4})_([R])(\d{3})_([T])(\d{2})(\D{3})_(\d{8})([T])(\d{6})':
        {#'pattern': 'MMM_MSIXXX_YYYYMMDDHHMMSS_Nxxyy_ROOO_Txxxxx_<Product Discriminator>',
         #'pattern_name': 'New format Naming Convention for Sentinel-2 Level-1C products',
         'program': 1,
         'mission': 2 + 3,
         'sensor': 4,
         'processing_level': 5,
         'processing_year': 16,
         'sensing_date': 6,
         'tile': 13 + 14 + 15,  # Also called pathrow ; Tile is more versatile
         'PBN': 10,  # Processing Baseline Number
         'RON': 12,  # Relative Orbit Number
         },
    r'(S)(\d{1})(A|B)_(MSI)(L1C|L2C)_(\d{8})([T])(\d{6})_([N])(\d{4})_([R])(\d{3})_([T])(\d{2})(\D{3})':
        {#'pattern': 'MMM_CCCC_TTTTTTTTTT_ssss_yyyymmddThhmmss_ROOO_VYYYYMMTDDHHMMSS_YYYYMMTDDHHMMSS.SAFE',
         #'pattern_name': 'Old format product naming convention',
         'program': 1,
         'mission': 2 + 3,
         'sensor': 4,
         'processing_level': 5,
         'processing_year': 16,
         'sensing_date': 6,
         'tile': 13 + 14 + 15,  # Also called pathrow ; Tile is more versatile
         'PBN': 10,  # Processing Baseline Number
         'RON': 12,  # Relative Orbit Number
         },
    r'(S)(\d{1})(A|B)_(MSI)(L1C|L2C)_(\d{8})([T])(\d{6})_([N])(\d{4})_([R])(\d{3})':
        {#'pattern': 'MMM_CCCC_TTTTTTTTTT_ssss_yyyymmddThhmmss_ROOO_VYYYYMMTDDHHMMSS_YYYYMMTDDHHMMSS.SAFE',
         #'pattern_name': 'Old format granule (Granule and Tile) naming convention',
         'program': 1,
         'mission': 2 + 3,
         'sensor': 4,
         'processing_level': 5,
         'processing_year': 16,
         'sensing_date': 6,
         'tile': 13 + 14 + 15,  # Also called pathrow ; Tile is more versatile
         'PBN': 10,  # Processing Baseline Number
         'RON': 12,  # Relative Orbit Number
         }
}
