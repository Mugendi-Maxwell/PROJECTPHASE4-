from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .utils import Base

# House Model
class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    rent_price = Column(Float)
    num_apartments = Column(Integer)
    apartments = relationship("Apartment", back_populates="house")

# Apartment Model
class Apartment(Base):
    __tablename__ = "apartments"
    id = Column(Integer, primary_key=True, index=True)
    house_id = Column(Integer, ForeignKey("houses.id"))
    apartment_number = Column(String, unique=True, index=True)
    status = Column(String, default="available")
    house = relationship("House", back_populates="apartments")
    tenants = relationship("Tenant", back_populates="apartment")

# Tenant Model
class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact = Column(String)
    apartment_id = Column(Integer, ForeignKey("apartments.id"))
    apartment = relationship("Apartment", back_populates="tenants")
    complaints = relationship("Complaint", back_populates="tenant")
    payments = relationship("Payment", back_populates="tenant")
    password = Column(String)  

# Complaint Model
class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String, default="pending")
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant", back_populates="complaints")

# Payment Model
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    date = Column(String)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant", back_populates="payments")

# Landlord Model
class Landlord(Base):
    __tablename__ = "landlords"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)  # Unique constraint to prevent duplicates
    contact = Column(Integer, nullable=False)  # Ensure contact is always provided
    password = Column(String, nullable=False)  # Ensure password is always provided

