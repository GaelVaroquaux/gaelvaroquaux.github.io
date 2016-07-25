"""
Scrape GPS city coordinnates from world-gazetter.

Requires beautifulsoup.

Produces a tab separated file with city name, longitude, latitude on each
line.
"""

import unicodedata
from BeautifulSoup import BeautifulStoneSoup

def unicode2ascii(name):
    """ Tries to convert a unicode name to an ascii name, matching as
        well as possible unicode to an ascii translation.
    """
    try:
        name = name.decode('ascii')
    except UnicodeEncodeError:
        chars = list()
        for char in name:
            try:
                chars.append(char.decode('ascii'))
            except UnicodeEncodeError:
                charcode = 257
                while charcode > 255:
                    decomposition = unicodedata.decomposition(char)
                    if decomposition == '':
                        charcode = 63 # '?'
                        break
                    charcode = int(decomposition.split()[0], 16)
                    char = unichr(charcode)
                chars.append(chr(charcode))
        name = ''.join(chars)
    return name

# Download the data
import urllib
opener = urllib.urlopen(
    'http://www.world-gazetteer.com/kml.php?geo=1&dat=1000&lng=en'
    )

# Use beautifulsoup to scrape the data
tree = BeautifulStoneSoup(opener.read())
outfile = file('cities.txt', 'w')
outfile.write('# name\tlongitude\tlatitude\n')
for placemark in tree.findAll('placemark'):
    name = placemark.findChild('name').contents[0]
    name = unicode2ascii(name)
    coords = placemark.findChild('coordinates').contents[0]
    long, lat, _ = coords.split(',')
    outfile.write('%s\t%s\t%s\n' % (name, long, lat))


