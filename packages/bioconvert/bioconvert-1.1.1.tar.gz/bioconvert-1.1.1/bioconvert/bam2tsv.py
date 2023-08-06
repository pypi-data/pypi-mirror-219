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
"""Convert :term:`BAM` file to :term:`TSV` format"""
import os

import colorlog

from bioconvert import ConvBase
from bioconvert.core.decorators import requires

logger = colorlog.getLogger(__name__)


class BAM2TSV(ConvBase):
    """Convert sorted :term:`BAM` file into :term:`TSV` stats

    This is not a conversion per se but the extraction of BAM
    statistics saved into a TSV format. The 4 columns of the TSV file
    are::

        Reference sequence name, Sequence length,Mapped reads, Unmapped reads


    Methods are based on samtools [SAMTOOLS]_ and pysam [PYSAM]_.
    """

    #: Default value
    _default_method = "samtools"

    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile: BAM file
        :param str outfile: TSV file

        Methods are based on samtools [SAMTOOLS]_ and pysam [PYSAM]_.

        """
        super(BAM2TSV, self).__init__(infile, outfile, *args, **kargs)

    @requires("samtools")
    def _method_samtools(self, *args, **kwargs):
        """Here we use the SAMtools tool.

        `SAMtools documentation <http://www.htslib.org/doc/samtools.html>`_"""
        with open(self.outfile, "wt") as out:
            out.write("Reference sequence name\tSequence length\t" "Mapped reads\tUnmapped reads{}".format(os.linesep))
        cmd = "samtools index {0} && samtools idxstats {0} >> {1}".format(self.infile, self.outfile)
        self.execute(cmd)

    @requires(python_library="pysam", external_binary="samtools")
    def _method_pysam(self, *args, **kwargs):
        """We use here the python module Pysam.

        `Pysam documentation <https://pysam.readthedocs.io/en/latest/api.html>`_"""
        import pysam

        # index the bam file
        pysam.index(self.infile)
        # create count table
        with open(self.outfile, "wt") as out:
            out.write("Reference sequence name\tSequence length\t" "Mapped reads\tUnmapped reads{}".format(os.linesep))
            for line in pysam.idxstats(self.infile):
                out.write(line)
