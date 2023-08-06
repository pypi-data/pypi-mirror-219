from typing import List, Tuple, Any
from contextlib import contextmanager
import os
import subprocess as sp
from yamet.analysis.symmetry import get_spacegroup_info
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.core import Structure
from ase.io.res import Res
from ase import Atoms


def flatten(l: List[List[Any]]) -> List[Any]:
    return [item for sublist in l for item in sublist]


def tail(f: str, lines: int = 20) -> List[str]:
    """Tailing with python!

    Args:
        f (str): Path to file to be tailed
        lines (int, optional): Number of lines. Defaults to 20.

    Returns:
        (List[str]): The last $n$ lines of file f.
    """
    p = sp.Popen(["tail", f"-n{lines}", f], stdout=sp.PIPE)
    return [line.strip() for line in p.stdout.readlines()]


def grep(f: str, query: str) -> Tuple[List[str], bool]:
    """Grepping with python!

    Args:
        f (str): The path to the file to be grepped
        query (str): The substring to be searched for

    Returns:
        Tuple[List[str], bool]: The lines coutaining the found query, and
            whether or not the search was successful
    """
    p = sp.Popen(["grep", query, f], stdout=sp.PIPE)
    lines = [line.strip() for line in p.stdout.readlines()]
    if len(lines) > 0:
        return lines, True
    else:
        return lines, False


@contextmanager
def cd(newdir):
    """Move to and operate in new dirctory.

    Best used in with statements, i.e:

    ```
        with cd("my_dir"):
            # Doing things in my_dir
        # Now we're back in the parent directory
    ```

    Args:
        newdir (_type_): _description_
    """
    prevdir = os.getcwd()
    npath = f"{prevdir}/{newdir}"
    if not os.path.exists(npath):
        os.mkdir(newdir)
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def atoms2res(
    atoms: Atoms,
    fname: str,
    energy: float = None,
    pressure: float = None,
    spacegroup: str = None,
):
    if energy == None:
        energy = atoms.get_potential_energy()
    if pressure == None:
        pressure = atoms.get_pressure()
    if spacegroup == None:
        struct = atoms2struct(atoms)
        spacegroup = get_spacegroup_info(struct)[0]

    res = Res(
        atoms, pressure=pressure, energy=energy, spacegroup=spacegroup, times_found=1
    )
    res.write_file(fname)


def atoms2struct(atoms) -> Structure:
    return AseAtomsAdaptor(atoms).get_struct()


def struct2atoms(struct) -> Atoms:
    return AseAtomsAdaptor(struct).get_atoms()
