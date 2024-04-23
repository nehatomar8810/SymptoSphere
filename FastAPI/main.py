from fastapi import FastAPI,status,HTTPException,Depends
from .database import get_db,engine
from sqlalchemy.orm import Session
from . import schemas,tablesmodel,utils, oAuth2, disease_predictor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tablesmodel.Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
    return {"message" : "Welcome to my API...."}

""" {
    "email": "neha@gmail.com",
    "password": "password",
    "name": "Neha Tomar", 
    "age": 19,
    "gender": "female",
    "phone_num": "1234567893"
} """
@app.post("/signup-patient", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user_found = db.query(tablesmodel.User).filter(tablesmodel.User.email == user.email).first()

    if user_found:
       raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Email already exists")
    
    hashed_password = utils.hash(user.password)
    new_user = tablesmodel.User(
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    utils.send_email(user.email)

    user_details = tablesmodel.Patient(
        email=user.email,
        name=user.name, 
        age=user.age,
        gender=user.gender,
        phone_num=user.phone_num
    )
    db.add(user_details)
    db.commit()
    db.refresh(user_details)

    return new_user 

""" {
    "email": "ifi2022001@iiita.ac.in",
    "password": "password",
    "name": "Neha Tomar", 
    "specialty": "Jaundice", 
    "availability": "9:00 AM to 4:00 PM",
    "location": "Famous Hospital near IIITA, prayagraj",
    "phone_num": "1234567893"
} """
@app.post("/signup-healthprovider", response_model=schemas.UserOut)
async def create_health_provider(user:schemas.HealthcareProviderCreate, db: Session = Depends(get_db)):
    
    user_found = db.query(tablesmodel.User).filter(tablesmodel.User.email==user.email).first()

    if user_found:
       raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Email already exists")
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = tablesmodel.User(
        email = user.email,
        password = user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    utils.send_email(user.email)

    doctor_details = tablesmodel.HealthcareProvider(
        email = user.email,
        name = user.name, 
        specialty = user.specialty,
        availability = user.availability,
        location = user.location,
        phone_num = user.phone_num
    )
    db.add(doctor_details)
    db.commit()
    db.refresh(doctor_details)

    return new_user 

""" {
    "email": "neha@gmail.com",
    "password": "password"
} """
@app.post("/login")
async def loginPage(user_credentials:schemas.UserLogin ,db: Session = Depends(get_db)):

    user = db.query(tablesmodel.User).filter(tablesmodel.User.email==user_credentials.email).first()

    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = oAuth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}

""" {
   "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"]
} """
@app.post("/get-diseases-prediction")
async def predict_diseases(input_data: schemas.SymptomsInput, current_user: int = Depends(oAuth2.get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UnAuthorized User to perform action")

    symptoms = input_data.symptoms
    predicted_disease = disease_predictor.predict_disease(symptoms)

    db_value = tablesmodel.PredictedDisease(
        disease = predicted_disease,
        owner_id = current_user.id
    )

    db.add(db_value)
    db.commit()
    db.refresh(db_value)

    precautions = db.query(tablesmodel.Precaution).filter(tablesmodel.Precaution.diseases == predicted_disease).first()
    if not precautions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    
    precautions_out = schemas.PrecautionsOut(
        precaution_1=precautions.precaution_1,
        precaution_2=precautions.precaution_2,
        precaution_3=precautions.precaution_3,
        precaution_4=precautions.precaution_4
    )
    
    return {
        "disease": predicted_disease,
        "precautions": precautions_out
    }

""" {
    "doctor_email": "ifi2022001@iiita.ac.in",
    "rating": 4
} """
@app.post("/rate-doctor", response_model=schemas.UserOut)
async def rate_doctor(rating_info: schemas.RatingCreate, current_user: int = Depends(oAuth2.get_current_user), db: Session = Depends(get_db)):
    user = db.query(tablesmodel.User).filter(tablesmodel.User.id == current_user.id).first()
    doctor = db.query(tablesmodel.HealthcareProvider).filter(tablesmodel.HealthcareProvider.email == rating_info.doctor_email).first()

    if not user or not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or doctor not found")

    existing_rating = db.query(tablesmodel.Rating).filter(
        tablesmodel.Rating.user_id == current_user.id,
        tablesmodel.Rating.doctor_email == rating_info.doctor_email
    ).first()

    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already rated this doctor")

    new_rating = tablesmodel.Rating(
        user_id=current_user.id,
        doctor_email=rating_info.doctor_email,
        rating=rating_info.rating
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    all_ratings = db.query(tablesmodel.Rating).filter(tablesmodel.Rating.doctor_email == rating_info.doctor_email).all()
    total_ratings = sum(r.rating for r in all_ratings)
    average_rating = total_ratings / len(all_ratings)

    doctor.rating = average_rating
    db.commit()

    return user

@app.get("/suggest-doctors", response_model=list[schemas.HealthcareProviderOut])
async def suggest_doctors_for_patient(current_user: int = Depends(oAuth2.get_current_user), db: Session = Depends(get_db)):

    predicted_disease = db.query(tablesmodel.PredictedDisease.disease).filter(
        tablesmodel.PredictedDisease.owner_id == current_user.id
    ).first()

    if not predicted_disease:
        raise HTTPException(status_code=404, detail="Predicted disease not found")

    doctors = db.query(tablesmodel.HealthcareProvider).filter(
        tablesmodel.HealthcareProvider.specialty == predicted_disease[0]).order_by(
        tablesmodel.HealthcareProvider.rating.desc()).limit(5).all()

    return doctors