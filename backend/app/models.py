from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .utils import Base  # Ensure this points to your Base definition

class Landlord(Base):
    __tablename__ = 'landlords'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    
    # Relationship to House model (one-to-many)
    houses = relationship('House', back_populates='landlord')

class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    house_id = Column(Integer, ForeignKey('houses.id'), nullable=True)
    
    # Relationships to Payment and Complaint models
    payments = relationship('Payment', back_populates='tenant')
    complaints = relationship('Complaint', back_populates='tenant')
    
    # Optional back-populated relationship to House
    house = relationship('House', back_populates='tenants')

class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(200), nullable=False)
    num_apartments = Column(Integer, nullable=False)
    rent_price = Column(Float, nullable=False)
    landlord_id = Column(Integer, ForeignKey('landlords.id'), nullable=False)
    vacant_apartments = Column(Integer, nullable=False)
    
    # Relationships to Landlord and Tenant models
    landlord = relationship('Landlord', back_populates='houses')
    tenants = relationship('Tenant', back_populates='house')

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    
    # Back-populate relationship to Tenant
    tenant = relationship('Tenant', back_populates='payments')

class Complaint(Base):
    __tablename__ = 'complaints'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(500), nullable=False)
    status = Column(String(50), default='Pending')
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    
    # Back-populate relationship to Tenant
    tenant = relationship('Tenant', back_populates='complaints')
