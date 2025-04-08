import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
import django

# Simplified script to test Django initialization
print("Initializing Django...")
try:
    django.setup()
    print("Django initialized successfully.")
except Exception as e:
    print("Error during Django initialization:", e)

from octofit_tracker.models import User
from bson import ObjectId

# Test inserting a single user using Django ORM
print("Inserting a single user using Django ORM...")
user = User(_id=ObjectId(), username='testuser', email='testuser@example.com', password='testpassword')
user.save()
print(f"Inserted User: {user.username}, Email: {user.email}")

# Verify the user was inserted
retrieved_user = User.objects.filter(email='testuser@example.com').first()
print("Retrieved User:", retrieved_user)

# Clean up
if retrieved_user:
    retrieved_user.delete()
