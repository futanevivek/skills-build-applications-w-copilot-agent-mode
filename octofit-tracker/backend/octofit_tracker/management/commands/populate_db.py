from django.core.management.base import BaseCommand
from pymongo import MongoClient
from bson import ObjectId
from octofit_tracker.test_data import test_users, test_teams, test_activities, test_leaderboard, test_workouts

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert users
        print("Inserting users...")
        for user in test_users:
            user["_id"] = ObjectId()
            db.users.insert_one(user)
            print(f"Inserted User: {user['username']}, Email: {user['email']}")

        # Insert teams
        print("Inserting teams...")
        for team in test_teams:
            team["_id"] = ObjectId()
            db.teams.insert_one(team)
            print(f"Inserted Team: {team['name']}")

        # Insert activities
        print("Inserting activities...")
        for activity in test_activities:
            user = db.users.find_one({"username": activity["username"]})
            if user:
                activity["_id"] = ObjectId()
                activity["user_id"] = user["_id"]
                del activity["username"]
                db.activities.insert_one(activity)
                print(f"Inserted Activity: {activity['activity_type']}, User: {user['username']}")

        # Insert leaderboard entries
        print("Inserting leaderboard entries...")
        for entry in test_leaderboard:
            user = db.users.find_one({"username": entry["username"]})
            if user:
                entry["_id"] = ObjectId()
                entry["user_id"] = user["_id"]
                del entry["username"]
                db.leaderboard.insert_one(entry)
                print(f"Inserted Leaderboard Entry: User: {user['username']}, Score: {entry['score']}")

        # Insert workouts
        print("Inserting workouts...")
        for workout in test_workouts:
            workout["_id"] = ObjectId()
            db.workouts.insert_one(workout)
            print(f"Inserted Workout: {workout['name']}, Description: {workout['description']}")

        print("Successfully populated the database with test data.")
