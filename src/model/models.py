from pydantic import BaseModel

class LRModel(BaseModel):
    edad: float
    peso: float
    altura: float
   
