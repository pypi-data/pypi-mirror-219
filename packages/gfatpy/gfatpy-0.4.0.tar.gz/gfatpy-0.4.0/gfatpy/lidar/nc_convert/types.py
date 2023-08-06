from pathlib import Path
from datetime import datetime

from pydantic import BaseModel

from ..types import MeasurementType

class Measurement(BaseModel):
    path: Path
    type: MeasurementType
    time: datetime
    