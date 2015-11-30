# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, QueryDict
from django.template import RequestContext
from django.contrib import messages

from django.template.loader import render_to_string #for the modal edit

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


from django.shortcuts import render
from django.views.generic.base import TemplateView # to import html templates
from django.views.generic.list import ListView # to list my object from database
from django.views.generic.detail import DetailView # to show details of my selected object from database
from django.views.generic.edit import CreateView, UpdateView # to enable the edit form (create and then edit)

import core.models as coremodels # we import our models
from core.models import ListAppendView
	
# Create your views here.
# v1 views
class LegacyHomePageView(TemplateView):
		template_name = "v1/index.html"


# v2 views (to be deleted once v3 is fully tested)
class EntryRefreshViewv2(DetailView):
	model = coremodels.Entry
	template_name = "v2/modal/entry.html"
	context_object_name = 'entry'


class ModalView(ListView):
	model = coremodels.Entry
	template_name = "v2/modal/list.html"

	def get_queryset(self):
		# return the review object for the current user and the current location
		return coremodels.Entry.objects.filter(user=self.request.user).order_by('order')

class PopupView(TemplateView):
		template_name = "v2/modal/modal.html"

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

	return render_to_response('v2/entry/index.html', context, context_instance=RequestContext(request))

def detail(request, entry_id):
	try:
		entry = coremodels.Entry.objects.get(pk=entry_id)
	except Entry.DoesNotExist:
		raise Http404
	return render_to_response('v2/entry/detail.html', {'entry': entry})

class EntryUpdateView(UpdateView):
	model = coremodels.Entry
#	model = coremodels.Event # by just changing the model here, I can have access to the right form edit template
	template_name = 'v2/base/form.html'
	# # fields ="__all__" this is when we want all fields, but in this case, we don't want the user nor the Location Id
	fields = ['name','duedate','assignees'] # the fields on the edit page


class EntryModalUpdateViewv2(UpdateView):
	model = coremodels.Entry
#	form_class = ItemForm
	template_name = 'v2/modal/form.html'
	fields = ['name','duedate','assignees'] # the fields on the edit page
	context_object_name = 'entry'

	def dispatch(self, *args, **kwargs):
		self.item_id = kwargs['pk']
		return super(EntryModalUpdateViewv2, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		form.save()
# 		item = coremodels.Entry.objects.get(id=self.item_id)
#		return render_to_response('modal/')
		return HttpResponse('') # we could return something here
# #		return HttpResponse(render_to_string('modal/edit_success.html', {'item': item}))

class ListAppend(ListAppendView):
	model = coremodels.Entry
	template_name = 'v2/entry/listcreate.html'
#	fields = ['name'] # "__all__" no longer required as defined in the models

	def get_queryset(self):
		# return the review object for the current user and the current location
		return coremodels.Entry.objects.filter(user=self.request.user).order_by('order')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		return super(ListAppend, self).form_valid(form)


# v3 views
class EntryListAppendView(ListAppendView):
	model = coremodels.Entry
	template_name = 'entry/list.html'
#	fields = ['name'] # "__all__" no longer required as defined in the models

	def get_queryset(self):
		# return the review object for the current user and the current location
		return coremodels.Entry.objects.filter(user=self.request.user).order_by('order')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		return super(EntryListAppendView, self).form_valid(form)


class EntryModalUpdateView(UpdateView):
	model = coremodels.Entry
#	form_class = ItemForm
	template_name = 'entry/modal.html' #I will have to customize the fields to make it more simple rather than the current generic form template
	fields = ['name','duedate','assignees'] # the fields on the edit page
	context_object_name = 'entry'

	def dispatch(self, *args, **kwargs):
		self.item_id = kwargs['pk']
		return super(EntryModalUpdateView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		form.save()
# 		item = coremodels.Entry.objects.get(id=self.item_id)
#		return render_to_response('modal/')
		return HttpResponse('') # we could return something here
# #		return HttpResponse(render_to_string('modal/edit_success.html', {'item': item}))

class EntryRefreshView(DetailView):
	model = coremodels.Entry
	template_name = "entry/details.html"
	context_object_name = 'objects'

@csrf_exempt
def EntryAjaxUpdateView(request, pk):
	# source: http://stackoverflow.com/questions/25135155/how-to-change-model-variable-by-onclick-function-used-in-template-asynchronously?answertab=active#tab-top
#    JSON_field=request.POST.get("field")
    JSON_value=request.POST.get("value")
    b=coremodels.Entry.objects.get(id=pk) #str(value))
    #delete change statement
    b.done = (1 if b.done == 0 else 0) # int(JSON_value) #10
    b.save()
    # resp=json.dumps(b)
#    return HttpResponse(resp, content_type="application/json")
	# I should now refresh the value in the DOM
    return HttpResponse(None, content_type="application/json")

