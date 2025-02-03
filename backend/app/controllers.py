from flask import request, Response, make_response
from flask_restful import Resource
from app.models import Landlord, Tenant, House, Payment, Complaint
from app.utils import SessionLocal
from datetime import datetime, timedelta
import bcrypt
import jwt
import json
import traceback

# ---------------------------
# Landlord Authentication and House Management
# ---------------------------
class LandlordSignUpResource(Resource):
    def post(self):
        data = request.get_json()
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return Response(
                '{"message": "Missing required fields"}',
                status=400,
                mimetype='application/json'
            )

        session = SessionLocal()
        existing_landlord = session.query(Landlord).filter_by(email=data['email']).first()
        if existing_landlord:
            session.close()
            return Response(
                '{"message": "Email already exists"}',
                status=400,
                mimetype='application/json'
            )

        # Hash the password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        new_landlord = Landlord(
            name=data['name'],
            email=data['email'],
            password=hashed_password.decode('utf-8')
        )
        try:
            with SessionLocal() as session:
                session.add(new_landlord)
                session.commit()
                return Response(
                    '{"message": "Landlord created successfully"}',
                    status=201,
                    mimetype='application/json'
                )
        except Exception as e:
            session.rollback()
            return Response(
                '{"message": "Error creating landlord", "error": "' + str(e) + '"}',
                status=500,
                mimetype='application/json'
            )
        finally:
            session.close()

class LandlordLoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return Response(
                '{"message": "Email and password are required"}',
                status=400,
                mimetype='application/json'
            )
        session = SessionLocal()
        try:
            landlord = session.query(Landlord).filter_by(email=data['email']).first()
            if not landlord or not bcrypt.checkpw(data['password'].encode('utf-8'), landlord.password.encode('utf-8')):
                return Response(
                    '{"message": "Invalid credentials"}',
                    status=401,
                    mimetype='application/json'
                )
            token = self.generate_token(landlord.id)
            response_data = json.dumps({
                "message": "Login successful",
                "token": token,
                "landlord_id": landlord.id
            })
            return Response(response_data, status=200, mimetype='application/json')
        finally:
            session.close()

    def generate_token(self, landlord_id):
        expiration = datetime.utcnow() + timedelta(days=7)
        token = jwt.encode({'landlord_id': landlord_id, 'exp': expiration},
                           'your-secret-key-here',
                           algorithm='HS256')
        return token

# ---------------------------
# House Management Resource
# ---------------------------
class HouseResource(Resource):
    def get(self):
        session = SessionLocal()
        landlord_id = request.args.get('landlord_id')
        address = request.args.get('address')
        rent_price = request.args.get('rent_price')
        try:
            query = session.query(House)
            # Filter by landlord_id if provided
            if landlord_id:
                query = query.filter(House.landlord_id == landlord_id)
            # Additional tenant filters: address and rent price
            if address:
                query = query.filter(House.address.ilike(f"%{address}%"))
            if rent_price:
                query = query.filter(House.rent_price <= float(rent_price))
            houses = query.all()
            house_list = [
                {
                    "id": house.id,
                    "address": house.address,
                    "num_apartments": house.num_apartments,
                    "rent_price": house.rent_price,
                    "landlord_id": house.landlord_id,
                    "vacant_apartments": house.vacant_apartments
                }
                for house in houses
            ]
            response_data = json.dumps({"houses": house_list})
            return Response(response_data, status=200, mimetype="application/json")
        except Exception as e:
            return Response(
                json.dumps({"message": "Error fetching houses", "error": str(e)}),
                status=500,
                mimetype="application/json"
            )
        finally:
            session.close()

    def post(self):
        data = request.get_json()
        # Validate required fields (include landlord_id!)
        if not data.get('address') or not data.get('num_apartments') or not data.get('rent_price') or not data.get('landlord_id'):
            return Response(
                '{"message": "Missing required house data"}',
                status=400,
                mimetype='application/json'
            )
        new_house = House(
            address=data['address'],
            num_apartments=data['num_apartments'],
            rent_price=data['rent_price'],
            vacant_apartments=data['num_apartments'],
            landlord_id=data['landlord_id']
        )
        session = SessionLocal()
        try:
            session.add(new_house)
            session.commit()
            return Response(
                '{"message": "House added successfully"}',
                status=201,
                mimetype='application/json'
            )
        except Exception as e:
            session.rollback()
            print(f"Error adding house: {e}")
            print("Traceback:", traceback.format_exc())
            return Response(
                json.dumps({"message": "Error adding house", "error": str(e)}),
                status=500,
                mimetype="application/json"
            )
        finally:
            session.close()

# ---------------------------
# Tenant Authentication and Actions
# ---------------------------
class TenantSignUpResource(Resource):
    def post(self):
        data = request.get_json()
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return Response(
                '{"message": "Missing required fields"}',
                status=400,
                mimetype='application/json'
            )
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        new_tenant = Tenant(
            name=data['name'],
            email=data['email'],
            password=hashed_password.decode('utf-8')
        )
        session = SessionLocal()
        try:
            session.add(new_tenant)
            session.commit()
            return Response(
                '{"message": "Tenant created successfully"}',
                status=201,
                mimetype='application/json'
            )
        except Exception as e:
            session.rollback()
            return Response(
                json.dumps({"message": "Error creating tenant", "error": str(e)}),
                status=500,
                mimetype="application/json"
            )
        finally:
            session.close()

class TenantLoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return Response(
                '{"message": "Email and password are required"}',
                status=400,
                mimetype='application/json'
            )
        session = SessionLocal()
        try:
            tenant = session.query(Tenant).filter_by(email=data['email']).first()
            if not tenant or not bcrypt.checkpw(data['password'].encode('utf-8'), tenant.password.encode('utf-8')):
                return Response(
                    '{"message": "Invalid credentials"}',
                    status=401,
                    mimetype='application/json'
                )
            token = self.generate_token(tenant.id)
            return Response(
                json.dumps({"message": "Login successful", "token": token}),
                status=200,
                mimetype='application/json'
            )
        finally:
            session.close()

    def generate_token(self, tenant_id):
        expiration = datetime.utcnow() + timedelta(days=7)
        token = jwt.encode({'tenant_id': tenant_id, 'exp': expiration}, 'your-secret-key-here', algorithm='HS256')
        return token

class TenantMoveInResource(Resource):
    def post(self):
        data = request.get_json()
        if not data.get('tenant_id') or not data.get('house_id'):
            return Response(
                '{"message": "tenant_id and house_id are required"}',
                status=400,
                mimetype='application/json'
            )
        session = SessionLocal()
        try:
            tenant = session.query(Tenant).get(data['tenant_id'])
            if not tenant:
                return Response(
                    '{"message": "Tenant not found"}',
                    status=404,
                    mimetype='application/json'
                )
            if tenant.house_id:
                return Response(
                    '{"message": "Tenant already rented an apartment"}',
                    status=400,
                    mimetype='application/json'
                )
            house = session.query(House).get(data['house_id'])
            if not house or house.vacant_apartments <= 0:
                return Response(
                    '{"message": "No vacant apartments available"}',
                    status=400,
                    mimetype='application/json'
                )
            tenant.house_id = house.id
            house.vacant_apartments -= 1
            if house.vacant_apartments == 0 and not hasattr(house, 'is_full'):
                house.is_full = True
            session.commit()
            return Response(
                '{"message": "Tenant moved in successfully"}',
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            session.rollback()
            return Response(
                json.dumps({"message": "Error moving in tenant", "error": str(e)}),
                status=500,
                mimetype="application/json"
            )
        finally:
            session.close()

class TenantMoveOutResource(Resource):
    def post(self):
        data = request.get_json()
        session = SessionLocal()
        try:
            tenant = session.query(Tenant).get(data['tenant_id'])
            if not tenant or not tenant.house_id:
                return Response(
                    '{"message": "Tenant not assigned to a house"}',
                    status=400,
                    mimetype='application/json'
                )
            last_payment = session.query(Payment).filter_by(tenant_id=tenant.id).order_by(Payment.date.desc()).first()
            if not last_payment:
                return Response(
                    '{"message": "Tenant has not paid rent"}',
                    status=400,
                    mimetype='application/json'
                )
            house = session.query(House).get(tenant.house_id)
            house.vacant_apartments += 1
            tenant.house_id = None
            if house.vacant_apartments > 0 and hasattr(house, 'is_full'):
                house.is_full = False
            session.commit()
            return Response(
                '{"message": "Tenant moved out successfully"}',
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            session.rollback()
            return Response(
                json.dumps({"message": "Error moving out tenant", "error": str(e)}),
                status=500,
                mimetype="application/json"
            )
        finally:
            session.close()

class RentPaymentResource(Resource):
    def post(self):
        data = request.get_json()
        session = SessionLocal()
        try:
            tenant = session.query(Tenant).get(data['tenant_id'])
            if not tenant or not tenant.house_id:
                return Response(
                    '{"message": "Tenant not assigned to a house"}',
                    status=400,
                    mimetype='application/json'
                )
            current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            existing_payment = session.query(Payment).filter(
                Payment.tenant_id == tenant.id,
                Payment.date >= current_month
            ).first()
            if existing_payment:
                return Response(
                    '{"message": "Rent already paid for this month"}',
                    status=400,
                    mimetype='application/json'
                )
            new_payment = Payment(amount=data['amount'], tenant_id=tenant.id)
            session.add(new_payment)
            session.commit()
            return Response(
                '{"message": "Rent payment recorded successfully"}',
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            session.rollback()
            return Response(
                json.dumps({"message": "Error recording rent payment", "error": str(e)}),
                status=500,
                mimetype="application/json"
            )
        finally:
            session.close()

class ComplaintResource(Resource):
    def get(self):
        session = SessionLocal()
        house_id = request.args.get('house_id')
        try:
            if house_id:
                # Join Complaint and Tenant so that only complaints for tenants in this house are returned
                complaints = session.query(Complaint).join(Tenant, Complaint.tenant_id == Tenant.id).filter(Tenant.house_id == house_id).all()
            else:
                complaints = session.query(Complaint).all()
            complaint_list = [
                {
                    "id": complaint.id,
                    "description": complaint.description,
                    "status": complaint.status,
                    "tenant_id": complaint.tenant_id
                }
                for complaint in complaints
            ]
            response_data = json.dumps({"complaints": complaint_list})
            return Response(response_data, status=200, mimetype="application/json")
        except Exception as e:
            session.rollback()
            return Response(json.dumps({"message": "Error fetching complaints", "error": str(e)}), status=500, mimetype="application/json")
        finally:
            session.close()

    def post(self):
        data = request.get_json()
        if not data.get('tenant_id') or not data.get('complaint'):
            return Response('{"message": "Missing required fields"}', status=400, mimetype='application/json')
        session = SessionLocal()
        try:
            tenant = session.query(Tenant).get(data['tenant_id'])
            if not tenant:
                return Response('{"message": "Tenant not found"}', status=404, mimetype='application/json')
            new_complaint = Complaint(tenant_id=data['tenant_id'], description=data['complaint'])
            session.add(new_complaint)
            session.commit()
            return Response('{"message": "Complaint submitted successfully"}', status=201, mimetype='application/json')
        except Exception as e:
            session.rollback()
            return Response(json.dumps({"message": "Error submitting complaint", "error": str(e)}), status=500, mimetype="application/json")
        finally:
            session.close()

class ComplaintStatusUpdateResource(Resource):
    def post(self):
        data = request.get_json()
        if not data.get('complaint_id') or not data.get('status'):
            return Response('{"message": "Missing required fields"}', status=400, mimetype='application/json')
        session = SessionLocal()
        try:
            complaint = session.query(Complaint).get(data['complaint_id'])
            if not complaint:
                return Response('{"message": "Complaint not found"}', status=404, mimetype='application/json')
            complaint.status = data['status']
            session.commit()
            return Response('{"message": "Complaint status updated successfully"}', status=200, mimetype='application/json')
        except Exception as e:
            session.rollback()
            return Response(json.dumps({"message": "Error updating complaint status", "error": str(e)}), status=500, mimetype="application/json")
        finally:
            session.close()

class TenantResource(Resource):
    def get(self):
        session = SessionLocal()
        house_id = request.args.get('house_id')
        try:
            if house_id:
                # Query tenants based on house_id
                tenants = session.query(Tenant).filter(Tenant.house_id == house_id).all()
            else:
                # If no house_id provided, fetch all tenants
                tenants = session.query(Tenant).all()

            tenant_list = [
                {
                    "id": tenant.id,
                    "name": tenant.name,
                    "email": tenant.email,
                    "house_id": tenant.house_id
                }
                for tenant in tenants
            ]
            response_data = json.dumps({"tenants": tenant_list})
            return Response(response_data, status=200, mimetype="application/json")
        except Exception as e:
            session.rollback()
            return Response(
                json.dumps({"message": "Error fetching tenants", "error": str(e)}),
                status=500,
                mimetype="application/json"
            )
        finally:
            session.close()

class RentStatusResource(Resource):
    def get(self):
        session = SessionLocal()
        house_id = request.args.get('house_id')  # Optional: filter by house
        payment_status = request.args.get('payment_status')  # Optional: filter by payment status (paid/unpaid)

        try:
            # Query all tenants with their payments
            query = session.query(Tenant).join(Payment, Tenant.id == Payment.tenant_id, isouter=True)

            # Filter by house_id if provided
            if house_id:
                query = query.filter(Tenant.house_id == house_id)

            # Filter tenants by payment_status if provided
            if payment_status:
                if payment_status.lower() == 'paid':
                    # Filter tenants who have at least one payment
                    query = query.filter(Payment.tenant_id.isnot(None))
                elif payment_status.lower() == 'unpaid':
                    # Filter tenants who have no payments
                    query = query.filter(Payment.tenant_id.is_(None))

            tenants = query.all()

            tenant_list = []
            for tenant in tenants:
                # Check if a payment exists for the tenant
                payment = session.query(Payment).filter(Payment.tenant_id == tenant.id).first()

                # If a payment exists, tenant is marked as 'paid', else 'unpaid'
                payment_status = "paid" if payment else "unpaid"

                tenant_list.append({
                    "id": tenant.id,
                    "name": tenant.name,
                    "email": tenant.email,
                    "house_id": tenant.house_id,
                    "payment_status": payment_status
                })

            response_data = json.dumps({"tenants": tenant_list})
            return Response(response_data, status=200, mimetype="application/json")
        
        except Exception as e:
            session.rollback()
            return Response(
                json.dumps({"message": "Error fetching rent status", "error": str(e)}),
                status=500,
                mimetype="application/json"
            )
        finally:
            session.close()

