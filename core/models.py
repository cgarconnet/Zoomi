# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Avg

import os
import uuid

# Create your models here.

class Theme(models.Model):
# il appartient à un user
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100, null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.user) + ' / ' + str(self.name)

class Item(models.Model):
# il appartient à un client d'un user pour un Business
	user = models.ForeignKey(User)
	theme = models.ForeignKey(Theme)
	name = models.CharField(max_length=100, null=False, blank=False)
	description = models.TextField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.user) + ' / ' + str(self.name)
