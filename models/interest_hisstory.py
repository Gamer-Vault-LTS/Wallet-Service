from services.db_service import db
import uuid
from datetime import datetime

class Interest(db.Model):
    __tablename__ = 'interest_history'

    interest_id = db.Column(db.String(50),nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    interest_generated = db.Column(db.Numeric(10, 2), default=0.00)
    annual_interest = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)