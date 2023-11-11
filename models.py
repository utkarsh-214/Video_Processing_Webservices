from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class AudioExtractionData(Base):
    __tablename__ = "upload_data_audio"
    uid = Column(String(50), primary_key=True, default=str(uuid.uuid4()), unique=True)
    uploaded_by = Column(String(500))
    filename = Column(String(500))
    uploadTime = Column(DateTime, default=func.current_timestamp())

class UploadData(Base):
    __tablename__ = "upload_data"
    uid = Column(String(50), primary_key=True, unique=True)
    uploadBy = Column(String(500))
    uploadTime = Column(DateTime, default=func.current_timestamp())


class ProcessedData(Base):
    __tablename__ = "processed_data"
    uid = Column(String(50), primary_key=True, unique=True)
    ProceesedTime = Column(DateTime, default=func.current_timestamp())
