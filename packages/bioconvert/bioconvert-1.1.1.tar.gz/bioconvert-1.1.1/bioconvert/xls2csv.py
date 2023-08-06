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

"""Convert :term:`XLS` format to :term:`CSV` format"""

import csv

import colorlog

from bioconvert import ConvBase
from bioconvert.core.base import ConvArg
from bioconvert.core.decorators import compressor, requires

logger = colorlog.getLogger(__name__)


class XLS2CSV(ConvBase):
    """Convert :term:`XLS` file into :term:`CSV` file

    Extra arguments when using  **Bioconvert** executable.

    =================== ============================================
    name                 Description
    =================== ============================================
    --sheet-name        The name or id of the sheet to convert
    --out-sep           The separator used in the output file
    --line-terminator   The line terminator used in the output file
    =================== ============================================

    Methods available are based on  pandas [PANDAS]_ and  pyexcel [PYEXCEL]_.

    """

    _default_method = "pandas"
    DEFAULT_OUT_SEP = ","
    DEFAULT_LINE_TERMINATOR = "\n"

    def __init__(self, infile, outfile):
        """.. rubric:: Constructor

        :param str infile:
        :param str outfile:
        """
        super(XLS2CSV, self).__init__(infile, outfile)

    @requires(python_libraries=["pyexcel", "pyexcel-xls"])
    @compressor
    def _method_pyexcel(
        self, out_sep=DEFAULT_OUT_SEP, line_terminator=DEFAULT_LINE_TERMINATOR, sheet_name=0, *args, **kwargs
    ):
        """Do the conversion :term:`XLS` -> :term:`CSV` using pyexcel library

        `pyexcel documentation <http://docs.pyexcel.org/en/latest/>`_"""
        import pyexcel

        with open(self.outfile, "w") as out_stream:
            writer = csv.writer(out_stream, delimiter=out_sep, lineterminator=line_terminator)
            first_row = True
            for row in pyexcel.get_records(file_name=self.infile):
                if first_row:
                    writer.writerow([k for k, v in row.items()])
                    first_row = False
                writer.writerow([v for k, v in row.items()])

    @requires(python_libraries=["pandas", "xlrd"])
    @compressor
    def _method_pandas(
        self, out_sep=DEFAULT_OUT_SEP, line_terminator=DEFAULT_LINE_TERMINATOR, sheet_name=0, *args, **kwargs
    ):
        """Do the conversion :term:`XLSX` -> :term:`CSV` using Pandas library.

        `pandas documentation <https://pandas.pydata.org/docs/>`_"""
        import pandas as pd

        df = pd.read_excel(self.infile, sheet_name=sheet_name)
        df.to_csv(
            self.outfile,
            sep=out_sep,
            lineterminator=line_terminator,
            index=False,
            header="infer",
        )

    @classmethod
    def get_additional_arguments(cls):
        yield ConvArg(
            names=[
                "--sheet-name",
            ],
            default=0,
            help="The name or id of the sheet to convert",
        )
        yield ConvArg(
            names=[
                "--out-sep",
            ],
            default=cls.DEFAULT_OUT_SEP,
            help="The separator used in the output file",
        )
        yield ConvArg(
            names=[
                "--line-terminator",
            ],
            default=cls.DEFAULT_LINE_TERMINATOR,
            help="The line terminator used in the output file",
        )
