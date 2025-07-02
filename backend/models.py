from sqlalchemy import Column, Integer, String, JSON
from database import Base

class UserInfo(Base):
    __tablename__ = "user_info"

    id                  = Column(Integer, primary_key=True, index=True)
    age_group           = Column(String, nullable=False)
    gender              = Column(String, nullable=False)
    english_proficiency = Column(Integer, nullable=False)
    current_role        = Column(String, nullable=False)

class EmailAssessment(Base):
    __tablename__ = "email_assessment"

    id                 = Column(Integer, primary_key=True, index=True)
    email_number       = Column(Integer, nullable=False)
    authenticity_score = Column(Integer, nullable=False)
    reasons            = Column(JSON,    nullable=False)
    remarks            = Column(String)