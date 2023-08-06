# spmp [![LICENSE](https://img.shields.io/github/license/pierre-manchon/INPMT)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8114950.svg)](https://doi.org/10.5281/zenodo.8114950)
[![WIP](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

*An easy to use Satellite Product Metadata Parser*
## Installation
`spmp` uses only built-in packages.

``pip install spmp``

## Usage
The package can be used both as a module and a cli which invoke the same
function.

#### module
```python
>>> from spmp import parse
>>> product = parse('path/to/LC08_L1TP_187021_20140328_20170424_01_T1.tar.gz')
>>> product['title']
'187021'
```
#### command-line
```shell
$ python spmp -p path/to/LC08_L1TP_187021_20140328_20170424_01_T1.tar.gz
{'program': 'L',
 'sensor': 'C',
 'mission': '08',
 'processing_level': 'L1TP',
 'tile': '187021',
 'sensing_date': '20140328',
 'processing_year': '20170424',
 'collection_number': '01',
 'collection_category': 'T1'
 }
```

It is quite fast so don't worry about it impacting your performance:

```shell
 $ python -m timeit -s "from spmp import parse" "parse('path/to/LC08_L1TP_187021_20140328_20170424_01_T1.tar.gz')"
100000 loops, best of 5: 2.01 usec per loop
```