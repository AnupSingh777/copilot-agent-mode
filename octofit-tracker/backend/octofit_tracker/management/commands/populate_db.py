from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='marvel')
        dc = Team.objects.create(name='dc')

        # Users
        users = [
            User(email='tony@stark.com', name='Tony Stark', team='marvel'),
            User(email='steve@rogers.com', name='Steve Rogers', team='marvel'),
            User(email='bruce@wayne.com', name='Bruce Wayne', team='dc'),
            User(email='clark@kent.com', name='Clark Kent', team='dc'),
        ]
        User.objects.bulk_create(users)

        # Activities
        Activity.objects.create(user='Tony Stark', activity_type='run', duration=30, date='2025-12-01')
        Activity.objects.create(user='Steve Rogers', activity_type='swim', duration=45, date='2025-12-02')
        Activity.objects.create(user='Bruce Wayne', activity_type='cycle', duration=60, date='2025-12-03')
        Activity.objects.create(user='Clark Kent', activity_type='fly', duration=120, date='2025-12-04')

        # Leaderboard
        Leaderboard.objects.create(user='Tony Stark', score=150)
        Leaderboard.objects.create(user='Steve Rogers', score=200)
        Leaderboard.objects.create(user='Bruce Wayne', score=180)
        Leaderboard.objects.create(user='Clark Kent', score=220)

        # Workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='easy')
        Workout.objects.create(name='Sprints', description='Run 100m sprints', difficulty='medium')
        Workout.objects.create(name='Deadlift', description='Deadlift 100kg', difficulty='hard')

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { unique: true })')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
