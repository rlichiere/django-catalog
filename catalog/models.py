from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


# producteur/scenariste/realisateur/assistant_realisateur/scripte/regisseur/
# image_operateur_chef/image_operateur_assistant/image_operateur_steadycam/photographe_plateau
# son_operateur_chef/son_perchman/
# decor_chef/decor_accessoiriste
# hmc_maquilleur/hmc_costumier/hmc_habilleur/hmc_coiffeur
# post_monteur/post_monteur_son/post_mixeur/post_etalonneur/post_direction
# cascadeur
class Capacity(models.Model):
    name = models.CharField(max_length=200, unique=True)
    label = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.label


class Participant(models.Model):
    user = models.OneToOneField(User)
    capacities = models.ManyToManyField(Capacity)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    label = models.CharField(max_length=200)
    creator = models.ForeignKey(User)
    created = models.DateField(null=True)
    status = models.CharField(max_length=50, default='active')    # active, archive

    def __unicode__(self):
        return self.label


class Participation(models.Model):
    project = models.ForeignKey(Project)
    capacity = models.ForeignKey(Capacity)
    participant = models.ForeignKey(Participant)
    owner_validation = models.BooleanField(default=False)
    participant_validation = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s - %s (o:%s, p:%s' % (self.project, self.capacity, self.participant,
                                             self.owner_validation, self.participant_validation)


# decor/accessoire/costume
class ObjectCategory(models.Model):
    label = models.CharField(max_length=200)
    creator = models.ForeignKey(User)

    def __unicode__(self):
        return '%s' % self.label


class Object(models.Model):
    label = models.CharField(max_length=200)
    category = models.ForeignKey(ObjectCategory)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return '%s' % self.label
