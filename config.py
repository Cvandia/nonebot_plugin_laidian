from typing import Optional

from pydantic import Extra, BaseModel

class Config(BaseModel, extra=Extra.ignore):
    laidian_with: Optional[int] = None