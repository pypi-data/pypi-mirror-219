import pandas as pd
from typing import Union, List, Tuple, Any
from yamet.chemistry.utils import Composition, UnbalanceableEquationError, balance
#from yamet.hull.vertical_distance import vertical_distance
from scipy.spatial import ConvexHull
import pandas as pd
import numpy as np
from pprint import pprint

class Hull:
    """Convex Hull Class

    desc.

    Attributes:
        hull_data:
            The dataframe containing hull data, referencing the primary table
        y
        
    """
    def __init__(
        self,
        structure_table: pd.DataFrame,
        compositions: Union[List[str], str],
        ignore: Any = None,        
                ) -> None:
        """ Initiliastion for Hull

        Args:
            data:
                The data source to build the hull from
        
        """
        if not isinstance(structure_table, pd.DataFrame):
            raise TypeError("The source data for a hull construction needs to be a dataframe object.")
        self.structure_table = structure_table.reset_index()

        if isinstance(compositions, list):
                self.compositions = [Composition(comp) for comp in compositions]
        elif isinstance(compositions, str):
                self.compositions = [Composition(comp) for comp in compositions.split(":")]

        # Ok, now we are done with the argument handling...
        self.reduced_formulae = [comp.get_formula(reduced = True) for comp in self.compositions]
        self.formulae = [comp.get_formula(reduced = False) for comp in self.compositions]

        self.concentration_interpolation()
        self.get_relative_formation_energies()
        self.make_hull()
        # with pd.option_context('display.max_rows', None,
        #         'display.max_columns', None,
        #         'display.precision', 3,
        #         'display.width', None
        #         ):
        #     print(self.hull_table)

    def concentration_interpolation(self, history = None) -> List[List[int]]:
        """Ascertain the concentration of each datapoint according to the sleceted endpoints.

        Args:

        Returns:
            A nested list of the indices of the endpoint in the parent dataframe, self.structure_table
        """
        def get_concs(ID, formula, endpoint_formulae, error_val = np.nan):
            ID = int(ID)
            if Composition(formula).get_formula(reduced=True) in endpoint_formulae:
                 nfu = Composition(formula).formula_units
                 ratios = [0] * len(endpoint_formulae)
                 ratios[endpoint_formulae.index(Composition(formula).get_formula(reduced=True))] = nfu
                 return ID, *ratios, 1
            try:
                ratios = balance([Composition(endpoint) for endpoint in endpoint_formulae], [Composition(formula)])
            except UnbalanceableEquationError:
                return ID, *[error_val] * (len(endpoint_formulae) + 1)
            sum_r_ratio = sum(ratios[0])
            return ID, *ratios[0], *ratios[1]
        
        endpoints_indices = []  
        missing = []
        for reduced_composition in self.reduced_formulae:
            indices = list(np.where(self.structure_table.formula_reduced == reduced_composition)[0])
            endpoints_indices.append(indices)

            # Doing this so user has a full picture of what's missing in one go, rather than adding something
            # only to find something else is missing.
            if len(indices) == 0:
                missing.append(reduced_composition)
        if any([len(idc) == 0 for idc in endpoints_indices]):
            newline = "\n" # f-strings are not as wonderful as they first appear
            raise Exception(f"\n\nMissing endpoint structure(s):\n{newline.join(missing)}\n")
        
        self.hull_table = pd.DataFrame(data = self.structure_table.apply(lambda x: get_concs(x["index"], x["formula"], self.reduced_formulae), axis=1, result_type="expand"))
        self.hull_table.rename(columns=dict(enumerate(["structIdx"] + self.reduced_formulae + ["prod"])), inplace=True)
        self.hull_table = self.hull_table.astype({"structIdx": int})
        self.hull_table.dropna(how = "any")

        self.hull_table = self.hull_table.assign(
             energy = lambda x: self.structure_table.iloc[x["structIdx"]]["energy"],
             atoms_count = lambda x: self.structure_table.iloc[x["structIdx"]]["atoms_count"],
             formula_units = lambda x: self.structure_table.iloc[x["structIdx"]]["formula_units"],
             pressure = lambda x: self.structure_table.iloc[x["structIdx"]]["pressure"],
        )
        self.hull_comps = self.hull_table.formula_units.tolist()
        self.hull_table.reset_index(inplace=True, drop=True)
        self.endpoints_indices = endpoints_indices

    def get_relative_formation_energies(self):
        """ Add the relative formation energies per atom to the hull dataframe.        """
        def relHf(row):
            refs = reference_fu_energies
            energy = row["energy"]
            r_ratios = [row[name] for name in self.reduced_formulae]
            p_ratio = row["prod"]
            min_fu_sum = 0

            # can't use sum as the lambda function uses eries objects, not single values.
            for ref, rto in zip(refs, r_ratios):
                min_fu_sum = min_fu_sum + (rto * ref)
            return ((energy - min_fu_sum) / row["atoms_count"] / row["prod"])
        
        def get_x(row):
            r_tot = 0
            for form in self.reduced_formulae:
                r_tot += row[form]
            return row[self.reduced_formulae[-1]] / r_tot

        mins = []
        
        indices = []
        reference_fu_energies = []
        for idx, epi in enumerate(self.endpoints_indices):
            table = self.hull_table[self.hull_table["structIdx"].isin(epi)]
            m = min(table["energy"])
            mins.append(m)
            indices.append(table['structIdx'][table["energy"] == m].values[0])
            reference_fu_energies.append(m/self.hull_comps[idx])

        if len(self.reduced_formulae) == 2:
            self.hull_table = self.hull_table.assign(
             x = lambda x: get_x(x)
        )


        self.hull_table = self.hull_table.assign(
             rel_form_energy_per_atom = lambda x: relHf(x)
        )
        
        # Keep the table pretty for the user <3
        self.hull_table.drop(labels = ["atoms_count", "formula_units"], axis = 1, inplace = True)


    def make_hull(self) -> pd.DataFrame:
        
        # Energy must always be on the final axis, no matter how many dimensions.

        sorted_hull = self.hull_table.drop(self.hull_table[self.hull_table.rel_form_energy_per_atom > 0].index)
        
        #cvx = ConvexHull()
        pass

    def in_simplex(simplex, points):
        pass