from typing import List
from typing import Union

import pandas as pd
from dscribe.descriptors import SOAP
from matminer.featurizers.structure import OrbitalFieldMatrix

from yamet.common.utils import *
from yamet.collectors.singles import Data as YametDataObject


def get_soaps(df: pd.DataFrame, species: List[Union[int, str]] = None):
    if species == None:
        species = flatten(df["species"].to_list())
    soap = SOAP(
        species=species,
        r_cut=6.0,
        l_max=8,
        n_max=8,
        periodic=True,
        sparse=False,
        average="inner",
        crossover=True,
        rbf="gto",
        sigma=0.1,
    )
    soaps = soap.create(df["atom_obj"].to_list())


class UMAP:
    def __init__(self) -> None:
        pass
