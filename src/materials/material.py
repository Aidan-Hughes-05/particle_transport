from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class Material:
    name: str
    absorption_cross_section: float  # [barn]
    scattering_cross_section: float  # [barn]
    density: float  # [g cm^-3]
    molar_mass: float  # [g mol^-1]

    avogadro_constant: ClassVar[float] = 6.022140857e+23
    barn_to_cm: ClassVar[float] = 1e-24
    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density cannot be zero or negative.")
        if self.molar_mass <= 0:
            raise ValueError("Molar mass cannot be zero or negative.")
        if self.absorption_cross_section < 0 or self.scattering_cross_section < 0:
            raise ValueError("Cross sections cannot be negative.")

    @property
    def number_density(self) -> float:
        return self.density / self.molar_mass * self.avogadro_constant # [cm^-3]


    @property
    def macro_absorb(self) -> float:
        return self.absorption_cross_section * self.number_density * self.barn_to_cm

    @property
    def macro_scatter(self) -> float:
        return self.scattering_cross_section * self.number_density * self.barn_to_cm

    @property
    def macro_total(self) -> float:
        return self.macro_absorb + self.macro_scatter

    @property
    def mean_free_path(self) -> float:
        if self.macro_total == 0:
            raise ValueError("Total cross section cannot be zero.")
        return 1 / self.macro_total