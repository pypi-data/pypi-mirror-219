import shelve
import traceback
import warnings
from copy import copy
from copy import deepcopy
from glob import glob
from typing import Any
from typing import Callable
from typing import List
from typing import Tuple
from typing import Union
from xml.etree.ElementTree import ParseError as XMLParseError

import numpy as np
import pandas as pd
from ase.io import read as ase_read
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.vasp.outputs import Vasprun
from tqdm import tqdm

from yamet.analysis.symmetry import get_spacegroup_info
from yamet.chemistry.utils import Composition
from yamet.common.utils import *


warnings.filterwarnings("ignore")

# TODO
# [] Check for convergence when loading in a actual output file, not just a geometry file etc.


class Data:
    """The object used by YAMET to access, analyse, and alter provided structure information.

    Essentially, this is a fancy wrapper for a pandas dataframe object but with some additional
    bits and pieces stuck on the side. That is not to say it's inhereited from pd.DataFrame().
    Rather, the data is stored in a dataframe produced within the class.

    Attributes:
        name: a name for the data collection.
        description: a description of the data collection.
        data: the pd.DataFrame() onject with, you guessed it, the data.
        columns: the columns for the pd.DataFrame which can be appended to at initialisation.

    """

    def __init__(
        self,
        name: str = "",
        description: str = "",
        cache: bool = True,
        cache_id: str = "ALL_DATA",
        additional_fields: Union[List[str], None] = None,
        additional_field_functions: Union[List[Tuple[Any, Any]], None] = None,
        no_property_default: Any = None,
    ) -> None:
        """Initialises the Data class


        name:
            a name for the data collection.

        description:
            a description of the data collection.

        additional_fields:
            A list of strings naming custom columns to add to the dataframe at the initial import phase.

        additional_field_functions:
            A list of tuples of functions and arguments that return the information desired for the
            user defined field. For example:

            [(func_one, args), (func_two, args)]

            The first argument of the user-defined function is assumed to be the file with the
            structure information, such as a .cif, .res etc., so define your
            function as follows:

            def my_function(structure_file, foo, bar):
                # Import the file with your favourite tool
                # Do things with foo, bar and the stuff from the structure file.
                return result # Which will be added to the dataframe in the matching column name in additional_fields

        no_property_default:
                The value to default to if a property cannot be found. Currently used when trying to get energy, stress, and pressures only.
                Others properties are considered too critical so should always be present.

        """
        self.name = name
        self.description = description
        self.sources = []
        self.data = pd.DataFrame()
        self.no_prop_override = no_property_default
        self.cache = cache
        init_columns = [
            "source",
            "atoms_obj",
            "a",
            "b",
            "c",
            "alpha",
            "beta",
            "gamma",
            "cell",
            "formula",
            "formula_reduced",
            "formula_units",
            "species",
            "atoms_count",
            "positions_cart",
            "positions_frac",
            "energy",
            "energy_per_atom",
            "energy_per_formula_unit",
            "pressure",
            "stress",
            "spacegroup",
            "spacegroup_number",
            "crystal_system",
            "converged_ionic",
            "label",
        ]
        if additional_fields is not None:
            assert len(additional_fields) == len(additional_field_functions)
            self.columns = tuple(init_columns + additional_fields)
            self.additional_field_functions = tuple(additional_field_functions)
        else:
            self.additional_field_functions = []
            self.columns = init_columns
            self.no_prop_override = np.nan

        self.cache_id = cache_id
        if self.cache:
            self.from_cache()

    def load(
        self,
        files_location: str,
        label: Union[int, float, str] = ".",
        ignore_unreadable: bool = False,
    ) -> pd.DataFrame:
        """Imports listed files into a dataframe.

        Args:
            files_locations:
                A string or list of strings that can be queried, for example:

                'my_directory/*.cif'
                or
                ['directory1/*.res', directory2/*/vasprun.xml]

            label:
                A user-defined label or tag for the dataset being loaded to
                distinguish it from other data in the frame.

            ignore_unreadable:
                Ignore structures that have properties that cannot be read, such
                as NoneType energies or pressures.

            Returns:
                A pandas dataframe with each row assigned to an imported structure
        """

        df = pd.DataFrame(columns=self.columns)
        files = glob(files_location)
        self.sources += files

        # There must be some way to speed this up?? Parallelisation?
        for idx, f in tqdm(enumerate(files), total=len(files)):
            atoms = ase_read(f)
            struct = AseAtomsAdaptor.get_structure(atoms)
            symbols = atoms.get_chemical_symbols()
            comp = Composition(symbols)
            cell = np.array(atoms.get_cell())
            energy = self._check(atoms.get_potential_energy)
            pressure = self._check(atoms.info.get, ["pressure"])
            stress = self._check(atoms.get_stress)
            additionals = [
                func(f, *args) for func, args in self.additional_field_functions
            ]
            df.loc[idx] = [
                f,
                atoms,
                *atoms.cell.cellpar(),
                cell,
                comp.get_formula(),
                comp.get_formula(reduced=True),
                comp.formula_units,
                tuple(symbols),
                len(symbols),
                atoms.get_positions(),
                atoms.get_scaled_positions(),
                energy,
                energy / len(symbols),
                energy / comp.formula_units,
                pressure,
                stress,
                *get_spacegroup_info(struct),
                "Unknown",
                label,
            ] + additionals
        self.data = pd.concat([self.data, df])
        if ignore_unreadable:
            self.data.dropna(inplace=True)
        self.data = self.data.reset_index(drop=True)
        if self.cache:
            self.to_cache()

    def to_cache(self, overwrite=True, clean=True):
        if clean:
            self.clean()
        with shelve.open("yamet.cache", writeback=True) as cache:
            if self.cache_id == "":
                self.cache_id = f"ALL_DATA"
                print(f"Using {self.cache_id} as cache ID")
            present_keys = cache.keys()
            if self.cache_id in present_keys and not overwrite:
                print(f"Cannot overwrite cache entry {self.cache_id}")
            else:
                cache[self.cache_id] = self.data

    def insert_data(self, df: pd.DataFrame, clean=True):
        bkp = deepcopy(self.data)
        try:
            self.df = pd.concat([self.data, df])
        except:
            print("\nOh no!\n")
            print(traceback.format_exc() + "\n")
            self.df = bkp
            del bkp

    def from_cache(self):
        with shelve.open("yamet.cache") as cache:
            if self.cache_id in cache:
                self.data = cache[self.cache_id]
            else:
                print(
                    f"Cannot find cache entry with ID: {self.cache_id}.\nNothing loaded."
                )

    def clean(self, ignore_fields: list = [], verbose=True):
        """A santisation function for the Data.data data.

        Args:
            A list of fields to ignore when looking for duplicates.
        """

        # Ignoring uncomparable fields
        ignore_fields += [
            "cell",
            "composition",
            "positions_cart",
            "positions_frac",
            "label",
            "converged_ionic",
        ]
        ignore_fields = list(set(ignore_fields))
        subset = [field for field in self.columns if field not in ignore_fields]
        original_length = len(self.data.index)

        # We need this hack to remove the non-hashable arrays
        self.data["cell_tuple"] = self.data.cell.apply(lambda x: tuple(x.flatten()))
        self.data["posfrac_tuple"] = self.data.positions_frac.apply(
            lambda x: tuple(x.flatten())
        )

        tupled = ["cell_tuple", "posfrac_tuple"]
        subset += tupled

        duplicates = self.data.duplicated(subset=subset)
        self.data = self.data[~duplicates]
        num_removed = original_length - len(self.data.index)
        if verbose:
            print(f"{int(num_removed)} duplicates found and removed.")
        for tup in tupled:
            self.data.drop(tup, axis=1, inplace=True)
        self.data.reset_index(inplace=True, drop=True)

    def get_converged(self):
        def from_vasprun(src):
            try:
                v = Vasprun(src)
                return v.converged_ionic
            except XMLParseError:
                return "Unknown"

        self.data["converged_ionic"] = self.data.source.apply(lambda x: from_vasprun(x))

    def _check(self, x, args=[]) -> Any:
        """Catch and return a default if a property cannot be found."""
        try:
            prop = x(*args)
        except:
            prop = self.no_prop_override
        return prop

    def get_data(self):
        return copy(self.data)
