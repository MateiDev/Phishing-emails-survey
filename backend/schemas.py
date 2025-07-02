from pydantic import BaseModel, Field
from typing import List, Optional

class _Config:
    model_config = {"from_attributes": True}

class UserInfoBase(BaseModel):
    age_group: str
    gender: str
    english_proficiency: int = Field(ge=1, le=10)
    current_role: str

class UserInfoCreate(UserInfoBase):
    pass

class UserInfo(UserInfoBase, _Config):
    id: int

class EmailAssessmentBase(BaseModel):
    email_number: int
    authenticity_score: int = Field(ge=1, le=10)
    reasons: List[str]
    remarks: Optional[str] = None

class EmailAssessmentCreate(EmailAssessmentBase):
    pass

class EmailAssessment(EmailAssessmentBase, _Config):
    id: int