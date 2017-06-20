# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import *


class Command(BaseCommand):
    help = 'clean_db'
    transaction = dict()

    def handle(self, *args, **kwargs):

        try:
            for participation in Participation.objects.all():
                participation.delete()
            for project in Project.objects.all():
                project.delete()
            for participant in Participant.objects.all():
                participant.delete()
            for user in User.objects.all():
                if user.username != 'admin':
                    user.delete()
            for capacity in Capacity.objects.all():
                capacity.delete()

        except Exception as e:
            print('command error : %s' % e)
        return None
