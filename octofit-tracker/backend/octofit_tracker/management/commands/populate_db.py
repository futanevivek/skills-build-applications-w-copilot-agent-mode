#
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_data

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        try:
            # Clear existing data
            User.objects.all().delete()
            Team.objects.all().delete()
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            Workout.objects.all().delete()

            # Populate users
            users = [User(**user) for user in test_data['users']]
            User.objects.bulk_create(users)

            # Refresh users from the database to ensure proper references
            users = list(User.objects.all())

            # Populate teams and assign members
            teams = []
            for i, team_data in enumerate(test_data['teams']):
                team = Team(name=team_data['name'])
                team.save()
                team.members.add(*users[i::len(test_data['teams'])])  # Distribute users across teams
                teams.append(team)

            # Populate activities
            activities = [
                Activity(**{**activity, 'user': users[i % len(users)]})
                for i, activity in enumerate(test_data['activities'])
            ]
            Activity.objects.bulk_create(activities)

            # Populate leaderboard
            leaderboard_entries = [
                Leaderboard(**{**entry, 'user': users[i % len(users)]})
                for i, entry in enumerate(test_data['leaderboard'])
            ]
            Leaderboard.objects.bulk_create(leaderboard_entries)

            # Populate workouts
            workouts = [Workout(**workout) for workout in test_data['workouts']]
            Workout.objects.bulk_create(workouts)

            self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error populating the database: {e}'))
