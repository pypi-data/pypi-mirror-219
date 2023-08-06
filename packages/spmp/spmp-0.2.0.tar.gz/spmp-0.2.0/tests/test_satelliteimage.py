"""
spmp
Satellite Products Parser

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
from spmp.__main__ import parse

pattern = r'([L])([COTEM])([078]+)_([L1GTPS]+)_(\d{6})_(\d{8})_(\d{8})_(\d{2})_([RT12]+)'

def test_basename():
    assert parse('LC08_L1TP_187021_20140328_20170424_01_T1')
    product = parse('LC08_L1TP_187021_20140328_20170424_01_T1')
    assert product.program == 'L'
    assert product.sensor == 'C'
    assert product.mission == '08'
    assert product.processing_level == 'L1TP'
    assert product.tile == '187021'
    assert product.sensing_date == '20140328'
    assert product.processing_year == "20170424"
    assert product.collection_number == '01'
    assert product.collection_category == 'T1'

def test_fullpath():
    fullpath = '/path/to/your/satellite/product/LC08_L1TP_187021_20140328_20170424_01_T1.tar.gz'
    assert parse(fullpath)
    product = parse(fullpath)
    assert product.program == 'L'
    assert product.sensor == 'C'
    assert product.mission == '08'
    assert product.processing_level == 'L1TP'
    assert product.tile == '187021'
    assert product.sensing_date == '20140328'
    assert product.processing_year == "20170424"
    assert product.collection_number == '01'
    assert product.collection_category == 'T1'