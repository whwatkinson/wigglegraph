from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WiggleGraphMetalData(BaseModel):
    # Internal
    wn: int
    created_at: float = datetime.now().timestamp()
    updated_at: Optional[float] = None
