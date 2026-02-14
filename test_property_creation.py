import requests
import json
from datetime import datetime

# First, create an organization with a unique name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
org_resp = requests.post("http://localhost:8000/api/register", json={
    "email": f"testuser_{timestamp}@example.com",
    "password": "testpass123",
    "name": "Test User",
    "org_name": f"Test Org {timestamp}"
})
print("Register response:", org_resp.status_code)
if org_resp.status_code != 200:
    print(org_resp.text)
    exit(1)

# Now create a property with all three fields
prop_resp = requests.post("http://localhost:8000/api/properties/", json={
    "name": "Test Property",
    "type": "Apartment",
    "address": "123 Main St",
    "google_maps_url": "https://maps.example.com",
    "website_social_media": "https://instagram.com/testprop",
    "owner_id": None,
    "source": "Direct Inquiry",
    "reference_link": None,
    "notes": "Test property"
}, headers={"Authorization": f"Bearer {org_resp.json().get('access_token')}"})

print("Property creation response:", prop_resp.status_code)
response_data = prop_resp.json()
print("Response JSON:", json.dumps(response_data, indent=2))

# Check if the fields are in the response
if "website_social_media" in response_data:
    print(f"✓ website_social_media: {response_data['website_social_media']}")
else:
    print("✗ website_social_media NOT in response")

if "owner_id" in response_data:
    print(f"✓ owner_id: {response_data['owner_id']}")
else:
    print("✗ owner_id NOT in response")

if "source" in response_data:
    print(f"✓ source: {response_data['source']}")
else:
    print("✗ source NOT in response")

