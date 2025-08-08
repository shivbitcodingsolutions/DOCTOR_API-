from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse 
import json
from model import Patient, Patientupdate


# Api object
app = FastAPI()



    
# Helper function
def load_data():
    with open ("patients.json","r") as f:
        data = json.load(f)
        
        return data
    
def save_data(data):
    with open ("patients.json", "w") as f:
        json.dump(data,f)


@app.get("/")
def method():
    return {"MSG" : "Wlc Doctor API"}


@app.get("/about")
def about():
    return {"Info" : "This is a doctor APP, use for view, create, update, delete patients health data !"}


@app.get("/view")
def view():
    data = load_data()
    return data

# Path Parameters
@app.get("/patient/{patient_id}")
def view_patients(patient_id : str = Path(...,description= "Id is must enter",example="POO1")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail= "Patients Not found!")


# Query Parameters  use--> /sort?sort_by=Hight&oder=asc
@app.get("/sort")
def sort_patients(sort_by: str = Query(...,deprecated="sort base on height, weight, bmi"), 
                  oder : str = Query("asc", description= "sort on asc and desc oder") ):
    
    valid_filed = ["height","weight","bmi"]
    
    if sort_by not in valid_filed:
        raise HTTPException (status_code=400, detail= f"Invalid field select from {valid_filed}")
    
    if oder not in ['asc','desc']:
        raise HTTPException (status_code=400, detail= "Invalid field select between asc and desc")
    
    data = load_data()
    
    sort_oder = True if oder=="desc" else False
    
    sorted_data = sorted(data.values(), key= lambda x: x.get(sort_by,0), reverse=sort_oder)
    
    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    
    #load data
    data = load_data()
    
    #check 
    if patient.id in data:
        raise HTTPException (status_code=400, detail="Patients al ready exists")
    
    # add database
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    # save in json
    save_data(data)
    
    return JSONResponse(status_code=201, content={"msg": "patient create successfully"})



@app.put("/edit/{patient_id}")
def update_patient(patient_id:str, patient_update: Patientupdate):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException (status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]
    
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
        
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    
    existing_patient_info = patient_pydandic_obj.model_dump(exclude="id")
    
    data[patient_id] = existing_patient_info
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={"msg": "patient update"})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id : str):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException (status_code=404 ,detail="Patient id is not in a database")
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse (status_code=200, content="Patient is delete successfully")