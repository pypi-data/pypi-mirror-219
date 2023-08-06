from pymatgen.symmetry.analyzer import SpacegroupAnalyzer as SGA

def get_spacegroup_info(struct):
    sga = SGA(struct)
    return sga.get_space_group_symbol(), sga.get_space_group_number(), sga.get_crystal_system()