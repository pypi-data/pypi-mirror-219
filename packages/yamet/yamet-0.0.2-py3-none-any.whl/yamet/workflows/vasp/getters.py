from yamet.common.utils import grep
from typing import List, Union, Tuple, Any

class CannotGetPropertyException(Exception):
    """Raised when a property cannot be obtained from output files.

    Args:
        Exception (str): Property which causes the error
    """
    def __init__(self, prop: str) -> None:
        self.proprty = prop
        self.message = f"Cannot get {prop}."
        super().__init__(self.message)


def get_pressure(include_pulay:bool = False, all_frames: bool = False) -> Union[List[float], float]:
    """Using GREP to get the pressure from an OUTCAR

    Args:
        include_pulay (bool, optional): Defaults to False.
        all_frames (bool, optional): Defaults to False to use the last one

    Raises:
        CannotGetPropertyException: Raised if pressure cannot be grepped.

    Returns:
        Union[List[float], float]: List of pressures for all_frames = True; float if False
    """
    lines, sucess = grep("OUTCAR", "pressure")
    if not sucess:
        raise CannotGetPropertyException("pressure")
    for line in lines:
        line = line.decode('UTF-8')
        ext = line.split()[3]
        pul = line.split()[8]
        if include_pulay:
            p = float(ext) + float(pul)
        else:
            p = float(pul)
        pressures.append(p*0.1)
    pressures = []
    if all_frames:
        return pressures
    else:
        return pressures[-1]
    
    