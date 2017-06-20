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
    {'name': 'metteur_en_scene', 'label': 'Metteur en scène'},
    {'name': 'assistant_realisateur', 'label': 'Assistant Réalisateur'},
    {'name': 'assistant_plateau', 'label': 'Assistant Plateau'},
    {'name': 'scripte', 'label': 'Scripte'},
    {'name': 'regisseur', 'label': 'Régisseur'},
    {'name': 'operateur_chef', 'label': 'Chef Opérateur'},
    {'name': 'image_operateur_assistant', 'label': 'Assistant Opérateur Image'},
    {'name': 'image_operateur_steadycam', 'label': 'Opérateur Steadycam'},
    {'name': 'photographe_plateau', 'label': 'Photographe Plateau'},
    {'name': 'son_operateur_chef', 'label': 'Chef Opérateur Son'},
    {'name': 'son_prise', 'label': 'Prise de son'},
    {'name': 'son_perchman', 'label': 'Perchman'},
    {'name': 'decor_chef', 'label': 'Chef Décorateur'},
    {'name': 'accessoiriste', 'label': 'Accessoiriste'},
    {'name': 'hmc_maquillage', 'label': 'Maquilleur'},
    {'name': 'hmc_costumier', 'label': 'Costumier'},
    {'name': 'hmc_habilleur', 'label': 'Habilleur'},
    {'name': 'hmc_coiffeur', 'label': 'Coiffeur'},
    {'name': 'post_monteur', 'label': 'Monteur'},
    {'name': 'post_monteur_son', 'label': 'Monteur Son'},
    {'name': 'post_mixeur', 'label': 'Mixeur'},
    {'name': 'post_etalonneur', 'label': 'Etalonneur'},
    {'name': 'post_direction', 'label': 'Directeur Post-Production'},
    {'name': 'cascadeur', 'label': 'Cascadeur'},
    {'name': 'catering', 'label': 'Catering'},
    {'name': 'acteur', 'label': 'Acteur'},
    {'name': 'compositeur', 'label': 'Compositeur'},
    {'name': 'interprete', 'label': 'Inteprète'},
    {'name': 'dialoguiste', 'label': 'Dialoguiste'},
]

participants = [
    {'email': 'l.cerare@kino-a.com', 'login': 'luk', 'first_name': 'Luk', 'last_name': 'CERARE',
     'capacities': ['producteur', 'realisateur', 'scenariste', 'post_monteur']},

    {'email': 'c.palkou@kino-a.com', 'login': 'karole', 'first_name': 'Karole', 'last_name': 'PALKOU',
     'capacities': ['acteur']},

    {'email': 'f.jiron@kino-a.com', 'login': 'frederik', 'first_name': 'Frédérik', 'last_name': 'JIRON',
     'capacities': ['acteur']},

    {'email': 'm.brunette@kino-a.com', 'login': 'macari', 'first_name': 'Macari', 'last_name': 'BRUNETTE',
     'capacities': ['acteur']},

    {'email': 'a.hadilaye@kino-a.com', 'login': 'a.h-l', 'first_name': 'Alecsandr', 'last_name': 'HADI-LAYE',
     'capacities': ['acteur']},

    {'email': 'c.chenaideur@kino-a.com', 'login': 'klovisse', 'first_name': 'Klovisse', 'last_name': 'CHENAIDEUR',
     'capacities': ['compositeur', 'interprete']},

    {'email': 'm.lionnant@kino-a.com', 'login': 'matth', 'first_name': 'Matth', 'last_name': 'LIONNANT',
     'capacities': ['dialoguiste']},

    {'email': 'l.vairan@kino-a.com', 'login': 'loique', 'first_name': 'Loïque', 'last_name': 'VAIRANT',
     'capacities': ['dialoguiste']},

    {'email': 'm.bas@kino-a.com', 'login': 'matisse', 'first_name': 'Matisse', 'last_name': 'BAS',
     'capacities': ['son_prise']},

    {'email': 'cemoi@aim.com', 'login': 'pandareum', 'first_name': 'Rémy', 'last_name': 'CEMOI',
     'capacities': ['realisateur', 'scenariste', 'dialoguiste']},

    {'email': 'dajuju@gmail.com', 'login': 'dajuju', 'first_name': 'Julian', 'last_name': 'FAVIAI',
     'capacities': ['realisateur', 'scenariste', 'dialoguiste', 'regisseur', 'accessoiriste']},

    {'email': 'dodo@gmail.com', 'login': 'dodo', 'first_name': 'Dordine', 'last_name': 'FLAMAND',
     'capacities': ['realisateur', 'scenariste', 'dialoguiste', 'operateur_chef', 'post_monteur']},

    {'email': 'kamina@team-camina.org', 'login': 'kamina', 'first_name': 'Team', 'last_name': 'KAMINA',
     'capacities': ['producteur']},

    {'email': 'greg@gmail.com', 'login': 'greg', 'first_name': 'Grégorie', 'last_name': 'GRONEZ',
     'capacities': ['acteur']},

    {'email': 'a.toussez@gmail.com', 'login': 'aubepine', 'first_name': 'Aubépine', 'last_name': 'TOUSSEZ',
     'capacities': ['acteur']},

    {'email': 'g.plurare@gmail.com', 'login': 'guillaume', 'first_name': 'Guillaume', 'last_name': 'PLURARE',
     'capacities': ['acteur']},

    {'email': 's.bonette@gmail.com', 'login': 'sebastien', 'first_name': 'Sébastian', 'last_name': 'BONNETTE',
     'capacities': ['acteur']},

    {'email': 'm.gomette@gmail.com', 'login': 'mathieu', 'first_name': 'Tathieu', 'last_name': 'GOMETTE',
     'capacities': []},

    {'email': 'd.trucmuche@gmail.com', 'login': 'david', 'first_name': 'Flavid', 'last_name': 'TRUCMUCHE',
     'capacities': []},

    {'email': 'makesheup@gmail.com', 'login': 'makesheup', 'first_name': 'Make She Up', 'last_name': '(July Ravanello)',
     'capacities': []},

    {'email': 'lanana@gmail.com', 'login': 'lanana', 'first_name': 'Lanana', 'last_name': ' ',
     'capacities': []},
]

projects = [
    {'name': 'captive',      'label': 'Captive',      'creator': 'luk',       'status': 'archive'},
    {'name': 'paulette',     'label': 'Paulette',     'creator': 'luk',       'status': 'archive'},
    {'name': 'glitch',       'label': 'Glitch',       'creator': 'kamina',    'status': 'archive'},
    {'name': 'valse',        'label': 'Valse',        'creator': 'kamina',    'status': 'archive'},
    {'name': 'room_service', 'label': 'Room Service', 'creator': 'kamina',    'status': 'archive'},
    {'name': 'star_truc',    'label': 'Star Truc',    'creator': 'pandareum', 'status': 'active'},
]

participations = [
    {'project': 'captive', 'capacity': 'producteur',  'participant': 'luk'},
    {'project': 'captive', 'capacity': 'scenariste',  'participant': 'luk'},
    {'project': 'captive', 'capacity': 'realisateur', 'participant': 'luk'},
    {'project': 'captive', 'capacity': 'acteur',      'participant': 'karole'},
    {'project': 'captive', 'capacity': 'acteur',      'participant': 'frederik'},

    {'project': 'paulette', 'capacity': 'producteur',  'participant': 'luk'},
    {'project': 'paulette', 'capacity': 'scenariste',  'participant': 'luk'},
    {'project': 'paulette', 'capacity': 'realisateur', 'participant': 'luk'},
    {'project': 'paulette', 'capacity': 'dialoguiste', 'participant': 'matth'},
    {'project': 'paulette', 'capacity': 'son_prise',   'participant': 'matisse'},
    {'project': 'paulette', 'capacity': 'acteur',      'participant': 'macari'},
    {'project': 'paulette', 'capacity': 'acteur',      'participant': 'a.h-l'},
    {'project': 'paulette', 'capacity': 'acteur',      'participant': 'karole'},
    {'project': 'paulette', 'capacity': 'acteur',      'participant': 'frederik'},

    {'project': 'glitch', 'capacity': 'producteur',        'participant': 'kamina'},
    {'project': 'glitch', 'capacity': 'scenariste',        'participant': 'sebastien'},
    {'project': 'glitch', 'capacity': 'metteur_en_scene',  'participant': 'pandareum'},
    {'project': 'glitch', 'capacity': 'post_monteur',      'participant': 'dodo'},
    {'project': 'glitch', 'capacity': 'regisseur',         'participant': 'dajuju'},
    {'project': 'glitch', 'capacity': 'assistant_plateau', 'participant': 'mathieu'},
    {'project': 'glitch', 'capacity': 'assistant_plateau', 'participant': 'guillaume'},
    {'project': 'glitch', 'capacity': 'assistant_plateau', 'participant': 'david'},
    {'project': 'glitch', 'capacity': 'hmc_maquillage',    'participant': 'makesheup'},
    {'project': 'glitch', 'capacity': 'hmc_maquillage',    'participant': 'dajuju'},
    {'project': 'glitch', 'capacity': 'catering',          'participant': 'lanana'},

    {'project': 'valse', 'capacity': 'producteur', 'participant': 'kamina'},
    {'project': 'valse', 'capacity': 'scenariste', 'participant': 'pandareum'},
    {'project': 'valse', 'capacity': 'scenariste', 'participant': 'dajuju'},
    {'project': 'valse', 'capacity': 'scenariste', 'participant': 'dodo'},
    {'project': 'valse', 'capacity': 'scenariste', 'participant': 'guillaume'},
    {'project': 'valse', 'capacity': 'realisateur', 'participant': 'pandareum'},
    {'project': 'valse', 'capacity': 'realisateur', 'participant': 'dajuju'},
    {'project': 'valse', 'capacity': 'realisateur', 'participant': 'dodo'},
    {'project': 'valse', 'capacity': 'realisateur', 'participant': 'guillaume'},

    {'project': 'room_service', 'capacity': 'producteur', 'participant': 'kamina'},
    {'project': 'room_service', 'capacity': 'scenariste', 'participant': 'pandareum'},
    {'project': 'room_service', 'capacity': 'scenariste', 'participant': 'dajuju'},
    {'project': 'room_service', 'capacity': 'scenariste', 'participant': 'dodo'},
    {'project': 'room_service', 'capacity': 'scenariste', 'participant': 'guillaume'},
    {'project': 'room_service', 'capacity': 'realisateur', 'participant': 'pandareum'},
    {'project': 'room_service', 'capacity': 'realisateur', 'participant': 'dajuju'},
    {'project': 'room_service', 'capacity': 'realisateur', 'participant': 'dodo'},
    {'project': 'room_service', 'capacity': 'realisateur', 'participant': 'guillaume'},

    {'project': 'star_truc', 'capacity': 'scenariste',       'participant': 'pandareum'},
    {'project': 'star_truc', 'capacity': 'scenariste',       'participant': 'dodo'},
    {'project': 'star_truc', 'capacity': 'scenariste',       'participant': 'dajuju'},
    {'project': 'star_truc', 'capacity': 'scenariste',       'participant': 'guillaume'},
    {'project': 'star_truc', 'capacity': 'dialoguiste',      'participant': 'pandareum'},
    {'project': 'star_truc', 'capacity': 'dialoguiste',      'participant': 'guillaume'},
    {'project': 'star_truc', 'capacity': 'metteur_en_scene', 'participant': 'pandareum'},
    {'project': 'star_truc', 'capacity': 'accessoiriste',    'participant': 'dajuju'},
]


class Command(BaseCommand):
    help = 'populate_db_adv'
    transaction = dict()

    def handle(self, *args, **kwargs):

        try:
            self.transaction['capacities'] = list()
            self.transaction['participants'] = list()
            self.transaction['projects'] = list()

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
                if 'o_val' in participation:
                    owner_validation = participation['o_val']
                else:
                    owner_validation = True
                if 'p_val' in participation:
                    part_validation = participation['p_val']
                else:
                    part_validation = True
                part = Participation(project=project, participant=participant, capacity=capacity,
                                     owner_validation=owner_validation, participant_validation=part_validation)
                part.save()
                self.transaction['projects'].append(part)
                print('participation: from [%s] on [%s] as [%s]'
                      % (part.participant.user.username, proj.name, part.capacity.name))

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
