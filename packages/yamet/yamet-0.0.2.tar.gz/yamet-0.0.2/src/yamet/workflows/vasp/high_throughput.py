from glob import glob
from yamet.common.utils import *
from yamet.workflows.vasp.getters import get_pressure
from yamet.workflows.vasp.handlers import handle_hubbard, handle_magmoms
from yamet.analysis.symmetry import *
from copy import copy, deepcopy
from ase.calculators.vasp import Vasp
from ase.io import read as ase_read
from ase.core import Atoms
from xml.etree.ElementTree import ParseError
import shutil
from typing import List, Tuple, Any, Dict, Union
import os
from pymatgen.io.vasp.outputs import Vasprun, BSVasprun

#TODO:
# * Check dirs for unfinished calcs at start before loop
# * Check for keyword in INCAR, like KSPACING, LWAVE etc.
# * TESTING!

class Workflow:
    def __init__(self, inputs: Union[List[str], str], incars: List[str], names: List[str], kpoints: Union[None, List[str]] = None, HPC_mode = True) -> None:
        
        self.globbed_inputs = []
        self.inp_type = type(inputs)
        self.wf_dirs = ["inputs", "convered", "misc"]
        if isinstance(inputs, List):
            for inp in inputs:
                self.globbed_inputs += glob(inp)
        elif isinstance(inputs, str):
            self.globbed_inputs = glob(inputs)
        else:
            raise TypeError("Inputs must be given as a list or wildcarded (with '*')\nstring of the file locations")
        
        for d in self.wf_dirs:
            os.mkdir(d)
        # As the function says
        self.ensure_exist(incars)
        if kpoints is not None:
            self.ensure_exist(kpoints)
            
        self.init_magmoms = []
        self.hubbard = []
            
        # Also make sure that incars contain lines to print WAVECAR and CHGCAR for mult-step runs, and kpoints are present if kspacing not defined.
        for incar in incars:
            pass
        self.incars = incars
        self.kpoints = kpoints
        
        
    def run_vasp(self, atoms: Atoms, incar: str, restart: bool = False) -> Atoms:
        calc = Vasp(restart = restart, txt = "vasp.out")
        calc.set(ldua_luj = handle_hubbard(c_atoms, self.hubbard))
        if restart:
            c_atoms = calc.get_atoms()
        else:
            c_atoms = atoms
            calc.read_incar(filename = incar)
            calc.set(setups = "recommended")
            c_atoms.set_calculator(calc)
            c_atoms = handle_magmoms(c_atoms, self.init_magmoms)
        
        # Running the damn calculation
        energy = atoms.get_potential_energy()
        return atoms
    
    
    def post_vasp(self, name: str, solo = True, continue_if_not_converged: bool = True, next_calc: Any = None, index:int = 0) -> Any:
        readable, vasprun = self.read_vasprun_xml()
        if readable:
            atoms = ase_read("vasprun.xml")
        else:
            print(f"ERROR: {name} {index} need attention - unreadble vasprun.xml")
            return 1, None            
        if vasprun.converged_ionic:
            if not vasprun.converged_electronic:
                print(f"WARN: Final electronic step in {name} run {index} not converged.")
            return 0, atoms
        else:
            print(f"WARN: Geomtery not converged in {name} run {index}")
            if solo or not continue_if_not_converged:
                return 2, atoms
            elif continue_if_not_converged:
                return 0, atoms
                
                
                               
    
    def input_iteration(self, inputf: str, ignore_intermediate_warnings: bool = False, remove_wavecar: bool = False) -> bool:
        """The function to be used for each input in the main running loop.

        Args:
            inputf (str): The path of the input geometry.
            ignore_intermediate_warnings (bool, optional): Defaults to False.
            remove_wavecar (bool): Delete the WAVECAR from the previous calculation. Defaults to False

        Returns:
            bool: Whether the final structure was converged.
        """
        name = ".".join(inputf.split("/")[0].split(".")[:-1])
        skip = False
        with cd(name):
            pwd = os.getcwd()
            shutil.copy2(f"../{inputf}", pwd)
            shutil.move(f"../{inputf}", "../inputs")
            atoms = ase_read(inputf)
            if len(self.incars) == 1:
                shutil.copy2(f"../{incar[0]}", ".")
                out_atoms = self.run_vasp(atoms, incar=self.incars[0])
                
                # Finishing up
                exit_code = self.post_vasp(name = name)
                    
                
            else:
                for idx, incar in enumerate(self.incars):
                    with cd(incar):
                        if not skip:
                            shutil.copy2(f"../../{incar}", ".")
                            if idx > 0:
                                shutil.copy2(f"../{self.incars[idx-1]}/CONTCAR", "./POSCAR")
                                
                                """
                                We need the WAVECAR to carry over the information regarding the magnetic moments
                                determined from the previous run. It will also help with starting the 
                                calculations as VASP won't be beginning from nothing.
                                """
                                shutil.copy2(f"../{self.incars[idx-1]}/WAVECAR", ".")
                            try:
                                shutil.copy2(f"../../{self.kpoints[idx]}", ".")
                            except FileNotFoundError:
                                print(f"INFO: KPOINTS not found for run {idx} in {name}")
                            
                            out_atoms = self.run_vasp(atoms, incar=self.incars)
                            exit_code, atoms = self.post_vasp(name=name, index=idx, solo=False, continue_if_not_converged=True)
                            if exit_code != 0:
                                skip = True # Since breaking inside the with cd() won't return to parent dir...
                            if len(self.incars) == idx + 1:
                                vasprun = Vasprun("vasprun.xml")
                                struct = atoms2struct(atoms)
                                atoms2res(atoms=atoms, fname=f"{name}_final.res", pressure=get_pressure(), energy=vasprun.final_energy, spacegroup=get_spacegroup_info(struct=struct))
                                shutil(f"{name}_final.res", "../../converged")
                        else:
                            pass

            
    def check_dirs(self):
        print("Checking directories for unfinished runs.")
        dirs = glob("*/")
        
        
    def read_vasprun_xml(self, fname: str = "vasprun.xml"):
        assert os.path.exists(f"{os.getcwd()}/{fname}")
        v = None
        try:
            v = Vasprun(fname)
            success = True
        except ParseError:
            print("XML could not be read. Likely that the job scheduler killed the run before VASP could terminate cleanly/successfully. Consider adding a flag to you script to generate a STOPCAR before the job scheduler kills the run.")
            success = False
        except:
            print("Well I din't expect this error. What have you done?")
            success = False
        return success, v
     
    
    def ensure_exist(self, files):
        for f in files:
            if not os.path.exists(f"{os.getcwd()}/{f}"):
                if not os.path.exists(f):
                    raise FileNotFoundError(f"File '{f}' not found.")
        
        
        
        