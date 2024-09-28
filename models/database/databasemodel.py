from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Logs(db.Model):
    __tablename__ = 'logs'

    logs_id = db.Column(UUID, primary_key=True, server_default=db.text("uuid_generate_v4()"))
    computer = db.Column(db.String(255), nullable=False)
    user = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)


