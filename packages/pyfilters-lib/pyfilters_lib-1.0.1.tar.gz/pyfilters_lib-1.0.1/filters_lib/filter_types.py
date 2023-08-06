from dataclasses import dataclass
from enum import Enum


class FilterType(Enum):
    ft_hp = 0
    ft_lp = 1
    ft_band_stop = 2
    ft_band_pass = 3
    ft_none = 4


@dataclass
class FilterParam:
    type: FilterType
    sampling_freq: int
    cutoff_freq: float
