# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import *


class Command(BaseCommand):
    help = 'clean_db'
    transaction = dict()

    def handle(self, *args, **kwargs):

        try:
            # main base data
            self.delete_items(Participation.objects.all())
            self.delete_items(Project.objects.all())
            self.delete_items(Capacity.objects.all())

            # objects : base data
            self.delete_items(Decor.objects.all())
            self.delete_items(Actor.objects.all())
            self.delete_items(Accessory.objects.all())

            # objects : root data
            self.delete_items(Location.objects.all())
            self.delete_items(Image.objects.all())
            # self.delete_items(Object.objects.all())
            self.delete_items(AccessoryCategory.objects.all())

            # main root data
            self.delete_items(Participant.objects.all())
            self.delete_items(User.objects.all(), 'admin')

        except Exception as e:
            print('command error : %s' % e)
        return None

    def delete_items(self, items, except_key=None):
        for item in items:
            if except_key is not None:
                if item.username == except_key:
                    continue
            item.delete()