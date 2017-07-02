# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import *
from datetime import datetime

from catalog.core import config

static_password = config.DEFAULT_USER_PASSWORD

capacities = [
    {'name': 'producteur', 'label': 'Producteur'},
    {'name': 'scenariste', 'label': 'Scénariste'},
    {'name': 'realisateur', 'label': 'Réalisateur'},
    {'name': 'assistant_realisateur', 'label': 'Assistant Réalisateur'},
    {'name': 'scripte', 'label': 'Scripte'},
    {'name': 'regisseur', 'label': 'Régisseur'},
    {'name': 'image_operateur_chef', 'label': 'Chef Opérateur'},
    {'name': 'image_operateur_assistant', 'label': 'Assistant Opérateur Image'},
    {'name': 'image_operateur_steadycam', 'label': 'Opérateur Steadycam'},
    {'name': 'photographe_plateau', 'label': 'Photographe Plateau'},
    {'name': 'son_operateur_chef', 'label': 'Chef Opérateur Son'},
    {'name': 'son_perchman', 'label': 'Perchman'},
    {'name': 'decor_chef', 'label': 'Chef Décorateur'},
    {'name': 'decor_accessoiriste', 'label': 'Accessoiriste'},
    {'name': 'hmc_maquilleur', 'label': 'Maquilleur'},
    {'name': 'hmc_costumier', 'label': 'Costumier'},
    {'name': 'hmc_habilleur', 'label': 'Habilleur'},
    {'name': 'hmc_coiffeur', 'label': 'Coiffeur'},
    {'name': 'post_monteur', 'label': 'Monteur'},
    {'name': 'post_monteur_son', 'label': 'Monteur Son'},
    {'name': 'post_mixeur', 'label': 'Mixeur'},
    {'name': 'post_etalonneur', 'label': 'Etalonneur'},
    {'name': 'post_direction', 'label': 'Directeur Post-Production'},
    {'name': 'cascadeur', 'label': 'Cascadeur'},
]

participants = [
]

projects = [
]

participations = [
]

''' objects data'''
locations = [
]

accessory_categories = [
]

images = [
]


''' objects '''

decors = [
]

actors = [
]

accessories = [
]


class Command(BaseCommand):
    help = 'populate_db'
    transaction = dict()

    def handle(self, *args, **kwargs):

        try:
            self.transaction['capacities'] = list()
            self.transaction['participants'] = list()
            self.transaction['projects'] = list()
            self.transaction['participations'] = list()
            self.transaction['locations'] = list()
            self.transaction['accessory_categories'] = list()
            self.transaction['images'] = list()
            self.transaction['decors'] = list()
            self.transaction['actors'] = list()
            self.transaction['accessories'] = list()

            print('\nCAPACITIES')
            for capacity in capacities:
                if Capacity.objects.filter(name=capacity['name']).count() == 0:
                    cap = Capacity(name=capacity['name'], label=capacity['label'])
                    cap.save()
                    self.transaction['capacities'].append(cap)
                    print('capacity: %s' % cap.name)

            print('\nPARTICIPANTS')
            for participant in participants:
                if User.objects.filter(email=participant['email']).count() == 0:
                    user = User(email=participant['email'], username=participant['login'], password=static_password,
                                first_name=participant['first_name'], last_name=participant['last_name'])
                    user.save()
                    self.transaction['participants'].append(user)

                    part = Participant(user=user)
                    part.save()
                    for part_cap in participant['capacities']:
                        print('user:%s cap %s found : %s' % (user, part_cap, Capacity.objects.get(name=part_cap)))
                        part.capacities.add(Capacity.objects.get(name=part_cap))
                    print('user:%s capacities = %s' % (user, part.capacities.all()))

            print('\nPROJECTS')
            for project in projects:
                if Project.objects.filter(name=project['name']).count() == 0:
                    creator = User.objects.get(username=project['creator'])
                    proj = Project(name=project['name'], label=project['label'],
                                   creator=creator, status=project['status'], created=datetime.now())
                    proj.save()
                    self.transaction['projects'].append(proj)
                    print('project: %s' % proj.name)

            print('\nPARTICIPATIONS')
            for participation in participations:
                project = Project.objects.get(name=participation['project'])
                participant = Participant.objects.get(user__username=participation['participant'])
                capacity = Capacity.objects.get(name=participation['capacity'])
                part = Participation(project=project, participant=participant, capacity=capacity,
                                     owner_validation=participation['o_val'],
                                     participant_validation=participation['p_val'])
                part.save()
                self.transaction['participations'].append(part)
                print('participation: from [%s] on [%s] as [%s]'
                      % (part.participant.user.username, project.name, part.capacity.name))

            print('\nLOCATIONS')
            for loc in locations:
                country = self.get_value_or_none(loc, 'country')
                city = self.get_value_or_none(loc, 'city')
                postal_code = self.get_value_or_none(loc, 'postal_code')
                gps_lon = self.get_value_or_none(loc, 'gps_lon')
                gps_lat = self.get_value_or_none(loc, 'gps_lat')
                location = Location(label=loc['label'], country=country, city=city, postal_code=postal_code,
                                    gps_lat=gps_lat, gps_lon=gps_lon)
                location.save()
                self.transaction['locations'].append(location)
                print('location: %s' % location.label)

            print('\nACCESSORY_CATEGORIES')
            for acc_cat in accessory_categories:
                accessory_category = AccessoryCategory(label=acc_cat['label'])
                accessory_category.save()
                self.transaction['accessory_categories'].append(accessory_category)
                print('accessory_category: %s' % accessory_category.label)

            print('\nIMAGES')
            for obj in images:
                image = Image(label=obj['label'], storage=obj['storage'], path=obj['path'])
                image.save()
                self.transaction['images'].append(image)
                print('image: %s' % image.label)

            print('\nDECORS')
            for obj in decors:
                owner = Participant.objects.get(user__username=obj['owner'])
                decor = Decor(type='Decor', label=obj['label'], owner=owner)
                decor.save()
                self.transaction['decors'].append(decor)
                print('decor: %s' % decor.label)

            print('\nACTORS')
            for obj in actors:
                owner = Participant.objects.get(user__username=obj['owner'])
                actor = Actor(type='Actor', label=owner.user.get_full_name(), owner=owner, created=datetime.now())
                actor.save()
                self.transaction['actors'].append(actor)
                print('actor: %s' % actor.owner)

            print('\nACCESSORIES')
            for obj in accessories:
                owner = Participant.objects.get(user__username=obj['owner'])
                accessory = Accessory(type='Accessory', label=obj['label'], owner=owner)
                accessory.save()
                self.transaction['accessories'].append(accessory)
                print('accessory: %s' % accessory.label)

        except Exception as e:
            print('command error : %s' % e)
            self.rollback()
        return None

    def rollback(self):
        for participant in self.transaction['participants']:
            participant.delete()
        for capacity in self.transaction['capacities']:
            capacity.delete()
        print('rollback done.')

    def get_value_or_none(self, tab, key):
        if key in tab:
            return tab[key]
        else:
            return None