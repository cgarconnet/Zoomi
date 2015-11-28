# coding: utf8
from django.db import models
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Avg

from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

import os
import uuid


# Create your models here.
class Entry(models.Model):

	user = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	data = models.CharField(max_length=200, blank=True)
	order = models.IntegerField(default=1000)
	duedate = models.DateTimeField(null=True, blank=True)
	done = models.IntegerField(default=0) # 0 = to do / 1 = completed
	impediment = models.IntegerField(default=0) # 0 = No / 1 = Yes
	assignees = models.ManyToManyField(User, related_name='assignees',blank=True)	

	created_at = models.DateTimeField(auto_now_add=True)

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
		return reverse (viewname="listappend") #, args=[self.id]) 3 before index, now listappend because after adding we want to load again that page


class EntryCreateForm(ModelForm):

	class Meta:
		model = Entry
		fields = ['name','duedate'] # the form on the homepage


	def __init__(self, *args, **kwargs): # current_business, as parameter (cf Creeam)
#		self.request = kwargs.pop('request', None)
#		current_user = kwargs.pop('user')
#		current_business = kwargs['pk']
		super(EntryCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = "What do you need to do today?"
		#self.fields['customer'].queryset = 
#		self.fields['customer'].queryset = coremodels.Customer.objects.filter(user=current_user,business=current_business)
#		self.fields['customer'].queryset = coremodels.Customer.objects.filter(user=current_user)
#		self.fields['business'].queryset = coremodels.Business.objects.filter(user=current_user)

class EntryForm(ModelForm): # Seams not required
	class Meta:
		model = Entry
#		fields = '__all__'  Define exclude instead
		exclude = ['user']

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

class ListAppendView(MultipleObjectMixin,MultipleObjectTemplateResponseMixin,ModelFormMixin,ProcessFormView):
	""" A View that displays a list of objects and a form to create a new object.
	The View processes this form. """
	template_name_suffix = '_append'
	form_class = EntryCreateForm
	allow_empty = True

	def get(self, request, *args, **kwargs):
		self.object_list = self.get_queryset()
		allow_empty = self.get_allow_empty()
		if not allow_empty and len(self.object_list) == 0:
			raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
							% {'class_name': self.__class__.__name__})
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = self.get_context_data(object_list=self.object_list, form=form)
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		self.object = None
		return super(ListAppendView, self).post(request, *args, **kwargs)

	def form_invalid(self, form):
		self.object_list = self.get_queryset()
		return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))

