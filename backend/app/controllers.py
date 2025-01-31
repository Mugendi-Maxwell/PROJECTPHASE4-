from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_cors import CORS
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.models import House, Apartment, Tenant, Complaint, Payment, Landlord
from app.utils import engine
import contextlib
import bcrypt
import jwt
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
CORS(app)
api = Api(app)

# Secret key for JWT encoding
SECRET_KEY = 'your_secret_key'

# Database session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

# Helper function to manage session
@contextlib.contextmanager
def get_session():
    db = db_session()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        db.close()

# Helper function to serialize SQLAlchemy objects
def serialize(model, exclude_fields=None):
    exclude_fields = exclude_fields or []
    return {column.name: str(getattr(model, column.name)) for column in model.__table__.columns if column.name not in exclude_fields}


class HouseResource(Resource):
    def get(self, house_id=None):
        with get_session() as db:
            if house_id:
                house = db.query(House).filter(House.id == house_id).first()
                if house:
                    return make_response(jsonify(serialize(house)), 200)
                else:
                    return make_response(jsonify({"message": "House not found"}), 404)
            else:
                query = db.query(House)
                address = request.args.get('address')
                rent_price = request.args.get('rent_price')

                if address:
                    query = query.filter(House.address.ilike(f"%{address}%"))
                if rent_price:
                    query = query.filter(House.rent_price <= float(rent_price))

                houses = query.all()

                if houses:
                    return make_response(jsonify([serialize(house) for house in houses]), 200)
                else:
                    return make_response(jsonify({"message": "No houses found"}), 404)


class ApartmentResource(Resource):
    def get(self):
        with get_session() as db:
            apartments = db.query(Apartment).all()
            return make_response(jsonify([serialize(apartment) for apartment in apartments]), 200)

    def post(self):
        data = request.get_json()
        if not data or 'house_id' not in data or 'apartment_number' not in data or 'rooms' not in data:
            return make_response(jsonify({"error": "Missing required fields: house_id, apartment_number, rooms"}), 400)

        with get_session() as db:
            try:
                new_apartment = Apartment(
                    house_id=data['house_id'],
                    apartment_number=data['apartment_number'],
                    rooms=data['rooms'],
                    status=data.get('status', 'available')
                )
                db.add(new_apartment)
                db.commit()
                db.refresh(new_apartment)
                return make_response(jsonify(serialize(new_apartment)), 201)
            except SQLAlchemyError as e:
                return make_response(jsonify({"error": str(e)}), 400)


class TenantMoveInResource(Resource):
    def post(self):
        # Get the data from the request body
        data = request.get_json()
        house_id = data.get('house_id')
        tenant_name = data.get('name')
        tenant_contact = data.get('contact')

        # Validate input
        if not house_id or not tenant_name or not tenant_contact:
            return make_response(jsonify({"error": "Missing required fields: house_id, name, contact"}), 400)

        with get_session() as db:
            try:
                # Fetch the house details based on the house_id
                house = db.query(House).filter(House.id == house_id).first()
                if not house:
                    return make_response(jsonify({"error": "House not found"}), 404)

                # Find an available apartment in the specified house
                apartment = db.query(Apartment).filter(Apartment.house_id == house_id, Apartment.status == 'available').first()
                if not apartment:
                    return make_response(jsonify({"error": "No available apartments in this house"}), 404)

                # Create a new tenant
                new_tenant = Tenant(
                    name=tenant_name,
                    contact=tenant_contact,
                    apartment_id=apartment.id
                )
                db.add(new_tenant)
                apartment.status = 'occupied'  # Mark the apartment as occupied
                db.commit()
                db.refresh(new_tenant)

                # Record the rent payment
                rent_payment = Payment(
                    amount=house.rent_price,
                    date=datetime.utcnow(),
                    tenant_id=new_tenant.id
                )
                db.add(rent_payment)
                db.commit()

                # Respond with success and tenant details
                return make_response(jsonify({
                    "message": "Tenant moved in and rent paid successfully",
                    "tenant": {
                        "name": new_tenant.name,
                        "contact": new_tenant.contact,
                        "apartment_id": new_tenant.apartment_id,
                        "house_id": house.id
                    }
                }), 201)

            except SQLAlchemyError as e:
                db.rollback()
                return make_response(jsonify({"error": str(e)}), 500)




class ComplaintResource(Resource):
    def post(self):
        data = request.get_json()
        tenant_id = data.get('tenant_id')
        description = data.get('description')

        if not tenant_id or not description:
            return make_response(jsonify({"error": "Missing required fields: tenant_id, description"}), 400)

        with get_session() as db:
            try:
                complaint = Complaint(
                    tenant_id=tenant_id,
                    description=description,
                    status='pending'
                )
                db.add(complaint)
                db.commit()
                db.refresh(complaint)
                return make_response(jsonify({"message": "Complaint submitted successfully", "complaint": serialize(complaint)}), 201)
            except SQLAlchemyError as e:
                db.rollback()
                return make_response(jsonify({"error": str(e)}), 500)


class TenantMoveOutResource(Resource):
    def delete(self, tenant_id):
        with get_session() as db:
            try:
                tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
                if not tenant:
                    return make_response(jsonify({"error": "Tenant not found"}), 404)

                apartment = db.query(Apartment).filter(Apartment.id == tenant.apartment_id).first()
                if apartment:
                    apartment.status = 'available'
                    db.commit()

                db.delete(tenant)
                db.commit()

                return make_response(jsonify({"message": "Tenant moved out successfully"}), 200)
            except SQLAlchemyError as e:
                db.rollback()
                return make_response(jsonify({"error": str(e)}), 500)


class HouseUpdateApartmentsResource(Resource):
    def put(self, house_id):
        data = request.get_json()
        num_apartments = data.get('num_apartments')

        if not num_apartments:
            return make_response(jsonify({"error": "Missing required field: num_apartments"}), 400)

        with get_session() as db:
            try:
                house = db.query(House).filter(House.id == house_id).first()
                if not house:
                    return make_response(jsonify({"error": "House not found"}), 404)

                house.num_apartments = num_apartments
                db.commit()

                return make_response(jsonify({"message": "Number of apartments updated successfully", "house": serialize(house)}), 200)
            except SQLAlchemyError as e:
                db.rollback()
                return make_response(jsonify({"error": str(e)}), 500)


class LandlordSignUpResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        contact = data.get('contact')
        password = data.get('password')

        if not name or not contact or not password:
            return make_response(jsonify({'message': 'Username, contact, and password are required'}), 400)

        with get_session() as db:
            try:
                existing_landlord = db.query(Landlord).filter(Landlord.username == name).first()
                if existing_landlord:
                    return make_response(jsonify({'message': 'Landlord with this username already exists'}), 400)

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                new_landlord = Landlord(username=name, contact=contact, password=hashed_password.decode('utf-8'))
                db.add(new_landlord)
                db.commit()
                db.refresh(new_landlord)
                return make_response(jsonify({'message': 'Landlord signed up successfully', 'name': new_landlord.username}), 201)
            except SQLAlchemyError as e:
                db.rollback()
                return make_response(jsonify({'error': str(e)}), 500)


class LandlordLoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'password' not in data:
            return make_response(jsonify({'message': 'Username and password are required'}), 400)

        name = data.get('name')
        password = data.get('password')

        with get_session() as db:
            landlord = db.query(Landlord).filter(Landlord.username == name).first()
            if not landlord:
                return make_response(jsonify({'message': 'Landlord not found'}), 404)

            if not bcrypt.checkpw(password.encode('utf-8'), landlord.password.encode('utf-8')):
                return make_response(jsonify({'message': 'Invalid credentials'}), 400)

            token = jwt.encode(
                {'id': landlord.id, 'exp': datetime.utcnow() + timedelta(days=1)},
                SECRET_KEY,
                algorithm="HS256"
            )

            return make_response(jsonify({'message': 'Login successful', 'token': token}), 200)


router = [
    (HouseResource, "/houses/<int:house_id>"),
    (ApartmentResource, "/apartments"),
    (LandlordSignUpResource, "/signup/landlord"),
    (LandlordLoginResource, "/login/landlord"),
    (TenantMoveInResource, "/tenants/move-in"),
    (ComplaintResource, "/complaints"),
    (TenantMoveOutResource, "/tenants/move-out/<int:tenant_id>"),
    (HouseUpdateApartmentsResource, "/houses/update-apartments/<int:house_id>"),
]

for resource_class, route in router:
    api.add_resource(resource_class, route)
