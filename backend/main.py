from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS  # Import CORS
from app.utils import engine, Base
from app.models import House, Tenant, Complaint, Payment, Landlord  # Import models to trigger table creation
from app.controllers import (
    HouseResource,
    ApartmentResource,  # Include the apartment resource here
    TenantMoveInResource,
    ComplaintResource,
    TenantMoveOutResource,
    HouseUpdateApartmentsResource,
    LandlordSignUpResource,
    LandlordLoginResource
)
import bcrypt  # Import bcrypt for password hashing
import jwt  # Import JWT for authentication (if using token-based auth)
from datetime import datetime, timedelta

# Create the tables in the database (use Alembic for production)
Base.metadata.create_all(bind=engine)

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Enable CORS for all routes
CORS(app)

# Secret key for JWT encoding (make sure to keep it safe in production)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Define the API routes and resources
api_router = [
    (HouseResource, '/houses'),
    (ApartmentResource, '/apartments'),
    (TenantMoveInResource, '/tenants/move-in'),
    (TenantMoveOutResource, '/tenants/move-out/<int:tenant_id>'),
    (HouseUpdateApartmentsResource, '/houses/update-apartments/<int:house_id>'),
    (ComplaintResource, '/complaints'),
    (LandlordSignUpResource, '/signup/landlord'),
    (LandlordLoginResource, '/login/landlord')
]

# Add resources to API
for resource_class, route in api_router:
    api.add_resource(resource_class, route)

# Default route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the House Management API!"})  # ✅ Correct

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
