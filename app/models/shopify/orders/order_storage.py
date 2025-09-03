from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os
import json

# Create base class for SQLAlchemy models
Base = declarative_base()

class StoredOrder(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    shopify_order_id = Column(String(100), unique=True, nullable=False)
    order_name = Column(String(50))
    order_data = Column(Text, nullable=False)  # Store the complete order data as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert the order to a dictionary with parsed JSON data"""
        return {
            "id": self.id,
            "shopify_order_id": self.shopify_order_id,
            "order_name": self.order_name,
            "order_data": json.loads(self.order_data),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# Database setup
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'orders.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)