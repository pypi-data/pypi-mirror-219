# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import gzip
from pathlib import Path as path_t

import json_any as jsny
import pandas as pnds


def DataFrameFromJson(path: str | path_t, /) -> pnds.DataFrame:
    """"""
    with open(path, mode="rb") as json_accessor:
        compressed = json_accessor.read()
    jsoned = gzip.decompress(compressed)
    feature_book = jsny.ObjectFromJsonString(jsoned.decode())

    output = pnds.DataFrame(data=feature_book)
    output.columns.set_names(["Feature", "Track Label"], inplace=True)
    output.index.set_names("Time Point", inplace=True)

    return output


if __name__ == "__main__":
    #
    json_path = "/home/eric/Code/project/abc/cell-death/asma/thesis/_results-SKIP/TREAT02_13_R3D.dv-FromStart-To33/2023-06-30T10-47-32-852/json/features-cell.json"
    feature_book = DataFrameFromJson(json_path)
    print(
        feature_book.columns.names,
        feature_book.columns.levels[0],
        feature_book.columns.levels[1],
        feature_book.index,
        feature_book,
        feature_book["CFP"],
        feature_book["CFP", 1],
        feature_book["centroid", 1],
        feature_book["centroid", 1][0],
        feature_book["coords", 1],
        sep="\n\n",
    )
