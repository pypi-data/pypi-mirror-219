import string
from collections import Counter
from functools import reduce
from math import gcd
from fractions import Fraction
from typing import Any, Dict, List, Literal, Tuple, Union

import chemparse
import numpy as np
from sympy import Matrix, symbols as sympy_symbols
from sympy.solvers.solveset import linsolve
from yamet.common.utils import *

class UnbalanceableEquationError(Exception):
    """Raised when an equation cannot be balanced"""
    pass

class Composition:
    def __init__(self, formula) -> None:
        if isinstance(formula, dict):
            self.composition = formula
        elif isinstance(formula, str):
            self.composition = self._from_string(formula)
        elif isinstance(formula, list):
            self.composition = self._from_list(formula)
        else:
            raise TypeError("Unexcepted type. Must be a string, list, or dictionary.")
        self.reduced, self.formula_units = self._reduce()

    def get_composition(self, reduced: bool = False):
        if reduced:
            return self.reduced
        else:
            return self.composition

    def get_formula(self, reduced: bool = False, style: Union[None, str] = None):
        assert style in [None, "tex", "pretty"]
        if reduced:
            comp = self.reduced
        else:
            comp = self.composition

        tex = style == "tex"
        counts = []
        # For correctness, we should put chalcogen/halogen stuff at the end
        terminations = ["C", "N", "P", "S", "Br", "Cl", "F", "O", "H"]
        for element, count in comp.items():
            counts.append((element, count))
        counts.sort(key=lambda x: x[0])
        elements = list(map(list, zip(*counts)))[0]
        # Moving the termination elements to the end in turn
        for termination in terminations:
            if termination in elements:
                idx = elements.index(termination)
                counts.append(counts.pop(idx))
        list_str = []
        for symbol, count in counts:
            if count > 0:
                list_str.append(symbol)
            if count != 1:
                if float(count).is_integer():
                    count = int(count)
                if tex:
                    list_str.append(f"_{{{count}}}")
                else:
                    list_str.append(count)

        if tex:
            return f"${''.join(list_str)}$"
        elif style == "pretty":
            s = "".join([str(s) for s in list_str])
            sb = s.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
            return s.translate(sb)
        else:
            return "".join([str(s) for s in list_str])

    def get_atom_count(self) -> int:
        """ Get the total number of atoms in a composition object
    
        Returns (int):
            Number of atoms in a composition
        """
        count = 0
        for k, v in self.composition.items():
            count += v
        return count

    # Type handling functions    
    
    def _from_string(self, formula) -> Dict:
        return chemparse.parse_formula(formula)

    def _from_list(self, formula) -> Dict:
        comp = dict()
        if isinstance(formula[0], str):
            return dict(Counter(formula))
        elif isinstance(formula, (tuple, list)):
            santised = [(s, float(c)) for s, c in formula]
            for symbol, count in santised:
                if symbol not in comp.keys():
                    comp[symbol] = count
                else:
                    comp[symbol] += count
            return comp

    def _reduce(self) -> Dict:
        (elements, counts) = zip(*self.composition.items())
        if not any([float(x).is_integer() for x in counts]):
            print("Cannot reduce non-integer compositions (yet!)")
            return self.composition
        counts = [int(count) for count in counts]
        denom = reduce(gcd, counts)
        rratio = [n / denom for n in counts]
        return dict(zip(elements, rratio)), denom
    

def balance(reactants: List[Composition], products: List[Composition], set_missing_to_zero: bool = True) -> Tuple[List[float], List[float]]:
    """Using linear algebra to solve chemical equation balancing
    
        Args:
            reactants:
                A list of YAMET Compositions for the reactants
                of the equation (LHS)

            product:
                A list of YAMET Compositions for the products
                of the equation (RHS)
                
        Returns:
            A nested tuple of the ratios of the products and reactants.
            i.e ((reactant ratios in order of input), (product ratios in order of input))
    
    """
    def lcm(a, b):
        return a*b // gcd(a, b)
    
    def frac_gcd(*nums):
        fractions = [Fraction(num).limit_denominator() for num in nums]
        mult = reduce(lcm, [frac.denominator for frac in fractions])
        mints = [int(frac*mult) for frac in fractions]
        div = reduce(gcd, mints)
        return [int(n / div) for n in mints]

    r_compositions = [r.get_composition() for r in reactants]
    p_compositions = [p.get_composition() for p in products]

    nve_p_comp = []

    rset = set(flatten([list(r.keys()) for r in r_compositions]))
    pset = set(flatten([list(p.keys()) for p in p_compositions]))
    if pset != rset:
        print(f"Unable to balance equation:\n reactants:\t{rset}\n products:\t{pset}\n\n")
        raise UnbalanceableEquationError
    

    chem_matrix = np.zeros((len(rset), len(reactants + products)))

    #SymPy symbols...
    chars = [string.ascii_lowercase[i] for i, _ in enumerate(reactants + products)]
    syms = sympy_symbols(f"{' ,'.join(chars)}")

    for p_comp in p_compositions:
        npc = p_comp
        for k, v in p_comp.items():
            npc[k] = -v
        nve_p_comp.append(npc)

    compositions = r_compositions + nve_p_comp
    for idx, comp in enumerate(compositions):
        for jdx, elem in enumerate(list(rset)):
            chem_matrix[jdx][idx] = comp.get(elem, 0.0)
    
    A = Matrix(chem_matrix)
    b = Matrix(np.zeros((np.shape(A)[0], 1)))

    solution = linsolve((A, b), syms)
    sols = []
    for sol in list(solution)[0]:
        sols.append(sol.subs(syms[-1], 1))
    try:
        amounts = frac_gcd(*[str(s) for s in sols])
    except ZeroDivisionError:
        raise UnbalanceableEquationError
    return [amounts[:len(r_compositions)], amounts[-len(p_compositions):]] 

# General python helper shenanigans
def cprint(s, colour = None):
    if colour == None:
        print(s)

def stop():
    cprint("Exitting.")
    exit()