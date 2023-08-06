import enum
from typing import Dict

from sympy import Basic, Integer

from classiq.interface.generator.expressions.classical_enum import ClassicalEnum


class Element(ClassicalEnum):
    H = 1
    He = enum.auto()
    Li = enum.auto()
    Be = enum.auto()
    B = enum.auto()
    C = enum.auto()
    N = enum.auto()
    O = enum.auto()  # noqa: E741
    F = enum.auto()
    Ne = enum.auto()
    Na = enum.auto()
    Mg = enum.auto()
    Al = enum.auto()
    Si = enum.auto()
    P = enum.auto()
    S = enum.auto()
    Cl = enum.auto()
    Ar = enum.auto()
    K = enum.auto()
    Ca = enum.auto()
    Sc = enum.auto()
    Ti = enum.auto()
    V = enum.auto()
    Cr = enum.auto()
    Mn = enum.auto()
    Fe = enum.auto()
    Co = enum.auto()
    Ni = enum.auto()
    Cu = enum.auto()
    Zn = enum.auto()
    Ga = enum.auto()
    Ge = enum.auto()
    As = enum.auto()
    Se = enum.auto()
    Br = enum.auto()
    Kr = enum.auto()
    Rb = enum.auto()
    Sr = enum.auto()
    Y = enum.auto()
    Zr = enum.auto()
    Nb = enum.auto()
    Mo = enum.auto()
    Tc = enum.auto()
    Ru = enum.auto()
    Rh = enum.auto()
    Pd = enum.auto()
    Ag = enum.auto()
    Cd = enum.auto()
    In = enum.auto()
    Sn = enum.auto()
    Sb = enum.auto()
    Te = enum.auto()
    I = enum.auto()  # noqa: E741
    Xe = enum.auto()
    Cs = enum.auto()
    Ba = enum.auto()
    La = enum.auto()
    Ce = enum.auto()
    Pr = enum.auto()
    Nd = enum.auto()
    Pm = enum.auto()
    Sm = enum.auto()
    Eu = enum.auto()
    Gd = enum.auto()
    Tb = enum.auto()
    Dy = enum.auto()
    Ho = enum.auto()
    Er = enum.auto()
    Tm = enum.auto()
    Yb = enum.auto()
    Lu = enum.auto()
    Hf = enum.auto()
    Ta = enum.auto()
    W = enum.auto()
    Re = enum.auto()
    Os = enum.auto()
    Ir = enum.auto()
    Pt = enum.auto()
    Au = enum.auto()
    Hg = enum.auto()
    Tl = enum.auto()
    Pb = enum.auto()
    Bi = enum.auto()
    Po = enum.auto()
    At = enum.auto()
    Rn = enum.auto()
    Fr = enum.auto()
    Ra = enum.auto()
    Ac = enum.auto()
    Th = enum.auto()
    Pa = enum.auto()
    U = enum.auto()
    Np = enum.auto()
    Pu = enum.auto()
    Am = enum.auto()
    Cm = enum.auto()
    Bk = enum.auto()
    Cf = enum.auto()
    Es = enum.auto()
    Fm = enum.auto()
    Md = enum.auto()
    No = enum.auto()
    Lr = enum.auto()
    Rf = enum.auto()
    Db = enum.auto()
    Sg = enum.auto()
    Bh = enum.auto()
    Hs = enum.auto()
    Mt = enum.auto()
    Ds = enum.auto()
    Rg = enum.auto()
    Cn = enum.auto()
    Nh = enum.auto()
    Fl = enum.auto()
    Mc = enum.auto()
    Lv = enum.auto()
    Ts = enum.auto()
    Og = enum.auto()

    def to_name(self) -> str:
        return f"Element_{self.name}"


class MolecularBasis(enum.Enum):
    sto3g = 0

    def to_sympy(self) -> Basic:
        return Integer(self.value)

    @staticmethod
    def sympy_locals() -> Dict[str, Basic]:
        return {f"Basis_{basis.name}": basis.to_sympy() for basis in MolecularBasis}


class FermionMapping(ClassicalEnum):
    JORDAN_WIGNER = 0
    PARITY = 1
    BRAVYI_KITAEV = 2
    FAST_BRAVYI_KITAEV = 3

    def to_sympy(self) -> Basic:
        return Integer(self.value)

    def to_name(self) -> str:
        return f"FermionMapping_{self.name}"
