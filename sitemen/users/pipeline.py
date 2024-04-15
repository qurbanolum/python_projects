from django.contrib.auth.models import Group


def new_users_handler(user, *args, **kwargs):
    group = Group.objects.filter(name='social')
    if len(group):
        user.groups.add(group[0])