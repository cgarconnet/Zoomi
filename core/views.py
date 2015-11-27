# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, QueryDict
from django.template import RequestContext
from django.contrib import messages

# Create your views here.


from django.shortcuts import render
from django.views.generic.base import TemplateView # to import html templates
from django.views.generic.list import ListView # to list my object from database
from django.views.generic.detail import DetailView # to show details of my selected object from database
from django.views.generic.edit import CreateView, UpdateView # to enable the edit form (create and then edit)

import core.models as coremodels # we import our models
from core.models import ListAppendView
	
# Create your views here.

class LandingView(TemplateView):
		template_name = "index.html"


def index(request):

	if request.method == 'POST':

		# request.POST['content'] is a query string like 'entry[]=3&entry[]=2&entry[]=1'
		# convert to a QueryDict so we can do things with it
		entries = QueryDict(request.POST['content'])

		for index, entry_id in enumerate(entries.getlist('entry[]')):
			# save index of entry_id as it's new order value
			entry = coremodels.Entry.objects.get(id=entry_id)
			entry.order = index
			print(index)
			entry.save()

    # split our entries arbitrarily, so we can have two lists on the page...
	entry_list1 = coremodels.Entry.objects.order_by('order')[:20]
	entry_list2 = coremodels.Entry.objects.order_by('order')[20:]

	context = {'entry_list1': entry_list1, 'entry_list2': entry_list2}

	return render_to_response('entry/index.html', context, context_instance=RequestContext(request))

def detail(request, entry_id):
	try:
		entry = coremodels.Entry.objects.get(pk=entry_id)
	except Entry.DoesNotExist:
		raise Http404
	return render_to_response('entry/detail.html', {'entry': entry})

class EntryUpdateView(UpdateView):
	model = coremodels.Entry
#	model = coremodels.Event # by just changing the model here, I can have access to the right form edit template
	template_name = 'base/form.html'
	# # fields ="__all__" this is when we want all fields, but in this case, we don't want the user nor the Location Id
	fields = ['name','duedate','assignees'] # the fields on the edit page

class ListAppend(ListAppendView):
	model = coremodels.Entry
	template_name = 'entry/listcreate.html'
#	fields = ['name'] # "__all__" no longer required as defined in the models

	def get_queryset(self):
		# return the review object for the current user and the current location
		return coremodels.Entry.objects.filter(user=self.request.user).order_by('order')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		return super(ListAppend, self).form_valid(form)