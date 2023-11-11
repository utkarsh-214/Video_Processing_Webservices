from sqlalchemy.orm import Session
from models import AudioExtractionData, UploadData, ProcessedData
from db import Session as DbSession, engine
from models import Base


# Database operations functions
def add_data_audio(db: Session, uid: str, uploaded_by, filename: str):
    new_upload = AudioExtractionData(uid=uid, uploaded_by=uploaded_by, filename=filename)
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)
    return new_upload

Base.metadata.create_all(bind=engine)

# methods to be used for api and other files
def insert_data_audio(uid, uploaded_by, filename):
    with DbSession() as db:
        new_upload = add_data_audio(db=db, uid=uid, uploaded_by=uploaded_by, filename=filename)
        print(
            f"Data added successfully with UID: {new_upload.uid}, uploaded_by: {new_upload.uploaded_by} Filename: {new_upload.filename}"
        )


# Database operations functions
def add_data_watermark(db: Session, uid: str, uploadBy: str):
    new_upload = UploadData(uid=uid, uploadBy=uploadBy)
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)
    return new_upload


def print_all_data(db: Session):
    all_data = db.query(UploadData).all()
    print("All data in 'upload_data' table:")
    for data in all_data:
        print(
            f"UID: {data.uid}, Filename: {data.filename}, uploaded_by: {data.uploaded_by}, Upload Time: {data.uploadTime}"
        )


def add_data_processed_watermark(db: Session, uid: str):
    new_upload = ProcessedData(uid=uid)
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)
    return new_upload

Base.metadata.create_all(bind=engine)


# methods to be used for api and other files
def insert_data_watermark(uid, username):
    with DbSession() as db:
        new_upload = add_data_watermark(db=db, uid=uid, uploadBy=username)
        print(
            f"Data added successfully with UID: {new_upload.uid}, Username: {new_upload.uploadBy}"
        )


def insert_processed_data_watermark(uid):
    with DbSession() as db:
        new_upload = add_data_processed_watermark(db=db, uid=uid)
        print(f"Processed Data added successfully with UID: {new_upload.uid}")

def show_all_data_upload_table():
    with DbSession() as db:
        print_all_data(db=db)
