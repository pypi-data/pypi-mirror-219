from pprint import pprint

def handle_magmoms(atoms, magmoms = None):
    """
    The magamoms variable should be a list parsed in the form:
    [...] -mgm Fe 5 Nb 0.6 O 0.6 [...]
    which is then converted to a dictionary:
    d = {
        'Fe': 5.,
        'Nb': 0.6,
        'O': 0.6
        }
        
        
    """
    if magmoms is None:
        return atoms
    else:    
        elements = magmoms[::2]
        values = magmoms[1::2]
        d = dict(zip(elements, values))
        init_mgm = []
        for s in atoms.get_chemical_symbols():
            if s not in elements:
                init_mgm.append(0)
            else:
                init_mgm.append(d[s])
        atoms.set_initial_magnetic_moments(init_mgm)
        return atoms

def handle_hubbard(atoms, luj):
    """Generate a dictionary of Hubbard parameters to be applied with ASE calculators

    Args:
        atoms (ase.Atoms): The ASE atoms object
        luj (list): A list of parameters in the form
        
        [<symbol>, <l_number>, <U_correction>, <J_corrrection>]
        
        This is so one can easily use this with nargs in argparse.

    Returns:
        dict: Dictionary to be applied to 
    """
    if luj is None:
        print("Hubbard corrections not set.")
        return None
    labels = ["L", "U", "J"]
    n = 4
    elements = []
    d = {}
    separated = [luj[i : i + n] for i in range(0, len(luj), n)]
    for indiv in separated:
        elements.append(indiv[0])
        d[indiv[0]] = dict(zip(labels, [float(x) for x in indiv[-3:]]))
    for s in atoms.symbols:
        if s not in elements:
            d[s] = dict(zip(labels, [-1, 0, 0])) # Negative 1 for no onsite interation added.
    pprint(d)
    return d