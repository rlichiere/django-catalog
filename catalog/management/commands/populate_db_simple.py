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
    {'email': 'a@a.a', 'login': 'a', 'first_name': 'Fa', 'last_name': 'LA', 'capacities': ['producteur']},
    {'email': 'b@b.b', 'login': 'b', 'first_name': 'Fb', 'last_name': 'LB', 'capacities': ['scenariste']},
    {'email': 'c@c.c', 'login': 'c', 'first_name': 'Fc', 'last_name': 'LC', 'capacities': ['realisateur']},
    {'email': 'd@d.d', 'login': 'd', 'first_name': 'Fd', 'last_name': 'LD', 'capacities': ['cascadeur']},
]

projects = [
    {'name': 'projet_0', 'label': 'Projet 0', 'creator': 'a', 'status': 'archive'},
    {'name': 'projet_1', 'label': 'Projet 1', 'creator': 'a', 'status': 'active'},
    {'name': 'projet_2', 'label': 'Projet 2', 'creator': 'b', 'status': 'active'},
    {'name': 'projet_3', 'label': 'Projet 3', 'creator': 'c', 'status': 'active'},
]

participations = [
    {'project': 'projet_1', 'participant': 'a', 'capacity': 'producteur', 'o_val': True, 'p_val': True},
    {'project': 'projet_1', 'participant': 'b', 'capacity': 'scenariste', 'o_val': True, 'p_val': True},
    {'project': 'projet_1', 'participant': 'c', 'capacity': 'realisateur', 'o_val': True, 'p_val': True},
    {'project': 'projet_2', 'participant': 'a', 'capacity': 'producteur', 'o_val': True, 'p_val': True},
    {'project': 'projet_2', 'participant': 'a', 'capacity': 'scenariste', 'o_val': True, 'p_val': True},
    {'project': 'projet_2', 'participant': 'a', 'capacity': 'realisateur', 'o_val': True, 'p_val': True},
    {'project': 'projet_2', 'participant': 'b', 'capacity': 'scenariste', 'o_val': True, 'p_val': True},
    {'project': 'projet_2', 'participant': 'b', 'capacity': 'realisateur', 'o_val': True, 'p_val': True},
    {'project': 'projet_2', 'participant': 'c', 'capacity': 'scenariste', 'o_val': True, 'p_val': True},

    {'project': 'projet_1', 'participant': 'd', 'capacity': 'cascadeur', 'o_val': False, 'p_val': True},
    {'project': 'projet_2', 'participant': 'd', 'capacity': 'cascadeur', 'o_val': False, 'p_val': True},
    {'project': 'projet_3', 'participant': 'd', 'capacity': 'cascadeur', 'o_val': True, 'p_val': False},
]


class Command(BaseCommand):
    help = 'populate_db'
    transaction = dict()

    def handle(self, *args, **kwargs):

        try:
            self.transaction['capacities'] = list()
            self.transaction['participants'] = list()
            self.transaction['projects'] = list()

            for capacity in capacities:
                if Capacity.objects.filter(name=capacity['name']).count() == 0:
                    cap = Capacity(name=capacity['name'], label=capacity['label'])
                    cap.save()
                    self.transaction['capacities'].append(cap)

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
                    # part.save()

            for project in projects:
                if Project.objects.filter(name=project['name']).count() == 0:
                    creator = User.objects.get(username=project['creator'])
                    proj = Project(name=project['name'], label=project['label'],
                                   creator=creator, status=project['status'], created=datetime.now())
                    proj.save()
                    self.transaction['projects'].append(proj)
            #
            for participation in participations:
                project = Project.objects.get(name=participation['project'])
                participant = Participant.objects.get(user__username=participation['participant'])
                capacity = Capacity.objects.get(name=participation['capacity'])
                part = Participation(project=project, participant=participant, capacity=capacity,
                                     owner_validation=participation['o_val'],
                                     participant_validation=participation['p_val'])
                part.save()
                self.transaction['projects'].append(part)

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
