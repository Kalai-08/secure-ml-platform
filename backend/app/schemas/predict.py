from pydantic import BaseModel, Field
# BaseModel to create our own data models
# Field to add additional validation rules


# gt -> greater than, le -> less or equal
class PredictIn(BaseModel):
    mean_radius: float = Field(gt=0, le=50)
    mean_texture: float = Field(gt=0, le=60)
    mean_perimeter: float = Field(gt=0, le=300)
    mean_area: float = Field(gt=0, le=3000)

class PredictOut(BaseModel):
    prediction: str
    probability_benign: float