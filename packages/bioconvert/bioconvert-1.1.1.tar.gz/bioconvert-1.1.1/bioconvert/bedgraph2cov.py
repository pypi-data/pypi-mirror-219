###########################################################################
# Bioconvert is a project to facilitate the interconversion               #
# of life science data from one format to another.                        #
#                                                                         #
# Copyright © 2018-2022  Institut Pasteur, Paris and CNRS.                #
#                                                                         #
# bioconvert is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# bioconvert is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program (COPYING file).                                 #
# If not, see <http://www.gnu.org/licenses/>.                             #
#                                                                         #
# Repository: https://github.com/bioconvert/bioconvert                    #
# Documentation: http://bioconvert.readthedocs.io                         #
###########################################################################
"""Convert :term:`BEDGRAPH` file to :term:`COV` format"""
import colorlog

from bioconvert import ConvBase

_log = colorlog.getLogger(__name__)


__all__ = ["BEDGRAPH2COV"]


class BEDGRAPH2COV(ConvBase):
    """Converts a :term:`BEDGRAPH` (4 cols) to :term:`COV` format (3 cols)

    Input example::

        chr19   49302000    4930205    -1
        chr19   49302005    4930210    1

    becomes::

        chr19   4930201    -1
        chr19   4930202    -1
        chr19   4930203    -1
        chr19   4930204    -1
        chr19   4930205    -1
        chr19   4930206    1
        chr19   4930207    1
        chr19   4930208    1
        chr19   4930209    1
        chr19   4930210    1

    Method available is a Bioconvert implementation (Python).

    """

    #: Default value
    _default_method = "python"

    def __init__(self, infile, outfile):
        """.. rubric:: constructor

        :param str infile: input :term:`BEDGRAPH` file.
        :param str outfile: output :term:`COV` file
        """
        super(BEDGRAPH2COV, self).__init__(infile, outfile)

    def _method_python(self, *args, **kwargs):
        """Convert bedgraph file in coverage. Internal method."""
        with open(self.infile, "r") as fin:
            with open(self.outfile, "w") as fout:
                for i, line in enumerate(fin.readlines()):
                    chrom, start, end, score = line.split()
                    assert start < end
                    for this in range(int(start), int(end) + 1):
                        fout.write("{}\t{}\t{}\n".format(chrom, this, score))
