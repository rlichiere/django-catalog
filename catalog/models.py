from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Capacity(models.Model):
    name = models.CharField(max_length=200, unique=True)
    label = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Capacities'

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label


class Participant(models.Model):
    user = models.OneToOneField(User)
    capacities = models.ManyToManyField(Capacity)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    label = models.CharField(max_length=200)
    creator = models.ForeignKey(User)
    created = models.DateField(null=True)
    status = models.CharField(max_length=50, default='active')    # active, archive

    def __unicode__(self):
        return self.label

    def __str__(self):
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

    def __str__(self):
        return '%s - %s - %s (o:%s, p:%s' % (self.project, self.capacity, self.participant,
                                             self.owner_validation, self.participant_validation)


''' Objects data '''


class Location(models.Model):
    label = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=True)
    postal_code = models.IntegerField(null=True)
    country = models.CharField(max_length=200, null=True)
    gps_lat = models.CharField(max_length=200, null=True)
    gps_lon = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return '%s' % self.label

    def __str__(self):
        return '%s' % self.label


class AccessoryCategory(models.Model):
    label = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s' % self.label

    def __str__(self):
        return '%s' % self.label

    class Meta:
        verbose_name_plural = 'Accessory Categories'


class Image(models.Model):
    label = models.CharField(max_length=10)
    storage = models.CharField(max_length=10, null=True)
    path = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return '%s' % self.label

    def __str__(self):
        return '%s' % self.label


''' Objects models '''


class Object(models.Model):
    label = models.CharField(max_length=200)
    owner = models.ForeignKey(Participant)
    created = models.DateField(null=True)
    location = models.ForeignKey(Location, null=True)
    photos = models.ManyToManyField(Image)
    type = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.label

    def __str__(self):
        return '%s' % self.label


class Decor(Object):
    type = 'Decor'

    def __unicode__(self):
        return '%s' % self.label

    def __str__(self):
        return '%s' % self.label


class Actor(Object):
    type = 'Actor'

    def __unicode__(self):
        return '%s' % self.label

    def __str__(self):
        return '%s' % self.label


class Accessory(Object):
    category = models.ManyToManyField(AccessoryCategory)
    type = 'Accessory'

    def __unicode__(self):
        return '%s' % self.label

    def __str__(self):
        return '%s' % self.label

    class Meta:
        verbose_name_plural = 'Accessories'
