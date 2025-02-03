from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS  # Import CORS
from app.utils import engine, Base  # Assuming engine and Base are correctly defined in utils.py
from datetime import datetime, timedelta

# Create the tables in the database (use Alembic for production)
Base.metadata.create_all(bind=engine)

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

app.config['SECRET_KEY'] = 'your-secret-key-here'

# Define the API routes and resources.
# Note: Make sure that the resource names (e.g., 'TenantResource' and 'RentStatusResource')
# are defined in your controllers.
api_router = [
    ('/signup/landlord', 'LandlordSignUpResource'),
    ('/login/landlord', 'LandlordLoginResource'),
    ('/houses', 'HouseResource'),
    ('/signup/tenant', 'TenantSignUpResource'),
    ('/login/tenant', 'TenantLoginResource'),
    ('/tenants', 'TenantResource'),            # New resource for fetching tenants
    ('/tenants/move-in', 'TenantMoveInResource'),
    ('/tenants/move-out', 'TenantMoveOutResource'),
    ('/rent-payment', 'RentPaymentResource'),
    ('/complaints', 'ComplaintResource'),
    ('/complaints/status', 'ComplaintStatusUpdateResource'),
    ('/rent-status', 'RentStatusResource')       # New resource for fetching rent status
]

# Dynamically import resources and add them to the API
for route, resource_name in api_router:
    try:
        # Import resource from app.controllers dynamically
        resource_module = __import__(f'app.controllers', fromlist=[resource_name])
        resource_class = getattr(resource_module, resource_name)
        api.add_resource(resource_class, route)
    except (ImportError, AttributeError) as e:
        print(f"Error importing {resource_name}: {e}")

# Default route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the House Management API!"})

# Run the application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
