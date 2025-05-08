from services.db_service import db
import uuid
from datetime import datetime

class Interest(db.Model):
    __tablename__ = 'interest_history'

    id = db.Column(db.String(50), primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    interest_generated = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    annual_interest = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
