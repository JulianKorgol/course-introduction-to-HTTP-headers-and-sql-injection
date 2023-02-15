from django.core.management.base import BaseCommand
from tasks.models import BlogPost
from django.contrib.auth.models import User
import random


titles = ['Second Post', 'Third Post']
content = ['This is the second post', 'This is the third post']


usernames = ['SMITH', 'JOHNSON', 'WILLIAMS', 'JONES', 'BROWN', 'DAVIS', 'MILLER', 'WILSON', 'MOORE']
passwords = ['love', 'austin', 'access', 'matrix', 'secret', 'anthony', 'orange', 'jackson', 'chicken', 'peanut']


class Command(BaseCommand):
    help = 'Loads the database with data'

    def handle(self, *args, **options):
        BlogPost.objects.create(id=3, title='First Post', content='This is the first post')

        BlogPost.objects.create(id=random.randint(5, 50), title=titles[0], content=content[0])
        BlogPost.objects.create(id=random.randint(51, 95), title=titles[1], content=content[1])

        BlogPost.objects.create(id=97, title='Hidden Fourth Post', content='This is the fourth post', public=False)


        User.objects.create_user(username='test', password='siema')

        for i in range(3):
            username = random.choice(usernames)
            password = random.choice(passwords)
            usernames.remove(username)
            passwords.remove(password)
            User.objects.create_user(username=username, password=password)

        User.objects.create_user(username='congratulations', password='youfoundme')

        self.stdout.write(self.style.SUCCESS('Successfully loaded the database'))
