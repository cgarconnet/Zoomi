# coding: utf8
from __future__ import unicode_literals # pour l'encoding facon Python 3
from django.db import models
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Avg

import os
import uuid

# Create your models here.


# Create your models here.
class Entry(models.Model):

	name = models.CharField(max_length=50)
	data = models.CharField(max_length=200, blank=True)
	order = models.IntegerField(default=0)

	class Meta:
		ordering = ['order']
		verbose_name_plural = "entries"

	def __str__(self):
		return str(self.name)

# <!--         <a href="{% url 'core.views.detail' entry.id %}">{{ entry }}</a>  -->
#         <a href="{% url entry.update_entry_url entry.id %}">{{ entry }}</a>

	def update_entry_url(self):
		# return "location/"+str(self.id)+"/detail" # not the best way to do it
		# instead use the core.urlresolvers
		return reverse (viewname="detail", args=[self.id])

	def get_absolute_url(self):
		# return "location/"+str(self.id)+"/detail" # not the best way to do it
		# instead use the core.urlresolvers
		return reverse (viewname="index") #, args=[self.id])


class EntryForm(ModelForm):
	class Meta:
		model = Entry
		fields = '__all__'

class Theme(models.Model):
# il appartient à un user
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100, null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user) + ' / ' + str(self.name)

class Item(models.Model):
# il appartient à un client d'un user pour un Business
	user = models.ForeignKey(User)
	theme = models.ForeignKey(Theme)
	name = models.CharField(max_length=100, null=False, blank=False)
	description = models.TextField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user) + ' / ' + str(self.name)
