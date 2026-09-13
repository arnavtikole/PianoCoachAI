from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Note:
    pitch: Optional[str]
    octave: Optional[int]
    midi_number: Optional[int]
    duration: float
    measure: int
    beat: float
    staff: int
    voice: int
    is_rest: bool = False
    is_chord: bool = False
    accidental: Optional[str] = None
    tie_start: bool = False
    tie_stop: bool = False
    dynamic: Optional[str] = None
    articulation: Optional[str] = None
    start_time: Optional[float] = None
    absolute_beat: Optional[float] = None

@dataclass
class Measure:
    number: int
    notes: List[Note] = field(default_factory=list)
    beats_per_measure: Optional[int] = None
    beat_unit: Optional[int] = None
    key_sig: Optional[str] = None

@dataclass
class Score:
    title: Optional[str] = None
    composer: Optional[str] = None
    tempo: Optional[float] = None
    measures: List[Measure] = field(default_factory=list)

