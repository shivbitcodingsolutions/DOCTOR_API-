from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, computed_field

# pydantic model 1
class Patient(BaseModel):
    
    id: Annotated[str, Field (..., description="Id of the patients", example="P001")]
    name : Annotated[str, Field(..., description="Name of the patients")]
    city:Annotated[str, Field(..., description="City where patients living")]
    age:Annotated[int, Field (...,gt=0,lt=100,description="Age of the patients")]
    gender:Annotated[Literal["Male","Female","other"],Field(...,description="Gender of patients")]
    height : Annotated[float, Field(...,gt=0,description="Height of patient in mtrs")]
    weight : Annotated[float, Field(...,gt=0,description="weight of patient in kgs")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        if self.bmi < 18.5:
            return "Underweight"
        
        elif self.bmi < 24.9:
            return "Normal"
        
        elif self.bmi < 30:
            return "overweight"
        
        elif self.bmi < 34.9:
            return "obese"
        
        else:
            return "extremly obese"

    
# pydantic model 2
class Patientupdate(BaseModel):
    
    name :  Annotated[Optional[str], Field(default=None)]
    city:   Annotated[Optional[str], Field(default=None)]
    age:    Annotated[Optional[int], Field(default=None,gt=0)]
    gender: Annotated[Optional[Literal["Male","Female","other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None,gt=0)]
    weight: Annotated[Optional[float], Field(default=None,gt=0)]
    