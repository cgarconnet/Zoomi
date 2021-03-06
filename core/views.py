# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, QueryDict
from django.template import RequestContext
from django.contrib import messages

from django.template.loader import render_to_string #for the modal edit
from django.db.models import Q # used to select OR conditions in Filters

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.forms.models import model_to_dict # for the UserProfile view

from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView # to import html templates
from django.views.generic.list import ListView # to list my object from database
from django.views.generic.detail import DetailView # to show details of my selected object from database
from django.views.generic.edit import CreateView, UpdateView # to enable the edit form (create and then edit)

from sitegate.decorators import redirect_signedin, sitegate_view # for sitegate and authenficiation

import core.models as coremodels # we import our models
from core.models import ListAppendView, ListCommentView, ListThemeView

#import datetime
from django.utils import timezone
from datetime import timedelta

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


def detail(request, entry_id):
	try:
		entry = coremodels.Entry.objects.get(pk=entry_id)
	except Entry.DoesNotExist:
		raise Http404
	return render_to_response('v2/entry/detail.html', {'entry': entry})


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


# ----- v3 views -----

class ReleasesPageView(TemplateView):
		template_name = "base/releases.html"

class home(TemplateView):
	template_name = "base/theme.html"


class HelpPageView(TemplateView):
		template_name = "base/help.html"

class UserDetailView(UpdateView):
#	model = coremodels.User
	template_name = 'base/form.html'
	fields = ['first_name','last_name','email'] # the fields on the edit page

	def get_context_data(self, **kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)
		context['form_title'] = "Update of your profile - step 1/2"
		return context

	def get_object(self):
		return get_object_or_404(coremodels.User, pk=self.request.user.id)

class UserProfileView(UpdateView):
#	model = coremodels.User
	template_name = 'base/form.html'
	fields = ['company'] # the fields on the edit page

	def get_context_data(self, **kwargs):
		context = super(UserProfileView, self).get_context_data(**kwargs)
		context['form_title'] = "Update of your profile - step 2/2"
		return context

	def get_object(self):
		return get_object_or_404(coremodels.UserProfile, user=self.request.user.id)
#		return get_object_or_404(coremodels.UserProfile, pk=self.request.user.id)


	# def get_context_data(request, self): #, **kwargs):
	# 	context = super(UserDetailView, self.request.user)
	# 	context['user_attr_map'] = model_to_dict(self.object)
	# 	context['userprofile_attr_map'] = model_to_dict(self.object.UserProfile)
	# 	return context


# View behind this entry http://127.0.0.1:8000/themes/3/entries/
class ThemeListEntriesView(ListAppendView):
	model = coremodels.Entry
	template_name = 'entry/listBS.html'
	context_object_name = 'entry'
	hide_sortable = 'hide_entry' # this is a CSS to hide the move item

#	fields = ['name'] # "__all__" no longer required as defined in the models

	def get_queryset(self):
		# return the Entry object for the current user and for done = not done
		return coremodels.Entry.objects.filter(user=self.request.user, transfered=0, theme=self.kwargs['pk']).order_by('created_at')

	# def get_context_data(self, **kwargs):
	# 	# the reverse as form_valid. Modify data between extract from DB -> page
	# 	context = super(ThemeListEntriesView, self).get_context_data(**kwargs)
	# 	# we prefill the them based on page we have, but he can change it
	# 	theme = coremodels.Theme.objects.get(id=self.kwargs['pk'])
	# 	return context

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		# form.instance.theme = coremodels.Theme.objects.get(id=self.kwargs['pk']) - no longer used because now we have the them field
		return super(ThemeListEntriesView, self).form_valid(form)

class EntryUpdateView(UpdateView): # re-used from v2
	model = coremodels.Entry
#	model = coremodels.Event # by just changing the model here, I can have access to the right form edit template
	template_name = 'base/form.html'
	form_class = coremodels.EntryUpdateForm

	def get_queryset(self):
		base_qs = super(EntryUpdateView, self).get_queryset()
		return base_qs.filter(Q(user=self.request.user) | Q(assignees=self.request.user))

	def get_form_kwargs(self):
		kwargs = super(EntryUpdateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		if not(self.object.transfered) and form.instance.transfered: #if this entry is transfered for the first time, then we change the order to appear at the top
			form.instance.order = -1
		return super(EntryUpdateView, self).form_valid(form)

	# # fields ="__all__" this is when we want all fields, but in this case, we don't want the user nor the Location Id
#	fields = ['name','duedate','transfered','assignees','impediment','section','theme'] # the fields on the edit page

class EntryListAppendView(ListAppendView):
	model = coremodels.Entry
	template_name = 'entry/list.html'
	context_object_name = 'entry'
#	fields = ['name'] # "__all__" no longer required as defined in the models

	def get_queryset(self):
		# return the Entry object for the current user and for done = not done
		return coremodels.Entry.objects.filter(Q(user=self.request.user, transfered=0) | Q(assignees=self.request.user), done=False).order_by('order')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		return super(EntryListAppendView, self).form_valid(form)

# same as above but using Bootstrap
class EntryListAppendViewBS(ListAppendView):
	model = coremodels.Entry
	template_name = 'entry/listBS.html'
	context_object_name = 'entry'
	hide_sortable = ""
	hide_assignees = 'hide_entry'

#	fields = ['name'] # "__all__" no longer required as defined in the models

	def get_queryset(self):
		# return the Entry object for the current user and for done = not done
		return coremodels.Entry.objects.filter(Q(user=self.request.user, transfered=0) | Q(assignees=self.request.user), done=False).order_by('order')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
#		print(form['section_name'].value())
		if form['section_name'].value():
			form.instance.order = coremodels.Entry.objects.get(id=form['section_name'].value()).order+1 # we use the free value x001
		return super(EntryListAppendViewBS, self).form_valid(form)

class EntryListTransferredAppendView(ListAppendView):
	model = coremodels.Entry
	# template_name = 'entry/transferred.html'
	# context_object_name = 'entry'

	template_name = 'entry/listBS.html'
	context_object_name = 'entry'
	hide_sortable = 'hide_entry' # this is a CSS to hide the move item
	hide_sender = 'hide_entry'

#	fields = ['name'] # "__all__" no longer required as defined in the models

	def get_queryset(self):
		# return the Entry object for the current user and for done = not done
		return coremodels.Entry.objects.filter(user=self.request.user, transfered=1, done=False).order_by('order')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		return super(EntryListTransferredAppendView, self).form_valid(form)


class ThemeListAppendView(ListThemeView):
	model = coremodels.Theme
	template_name = 'theme/list.html'
	context_object_name = 'theme'


	def get_queryset(self):
		# return the Entry object for the current user and for done = not done
		return coremodels.Theme.objects.filter(user=self.request.user).order_by('created_at')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		return super(ThemeListAppendView, self).form_valid(form)

class CommentListAppendView(ListCommentView):
	model = coremodels.Comment
	template_name = 'comment/list.html'
	context_object_name = 'comment'

	def get_context_data(self, **kwargs):
		# the reverse as form_valid. Modify data between extract from DB -> page
		context = super(CommentListAppendView, self).get_context_data(**kwargs)

		entry = coremodels.Entry.objects.filter(Q(user=self.request.user) | Q(assignees=self.request.user), id=self.kwargs['pk'])
		print(entry.count())

		context['nb_entry'] = entry.count()


		# location = coremodels.Location.objects.get(id=self.kwargs['pk'])

		# if self.request.user.is_authenticated():
		# 	user_reviews = coremodels.Review.objects.filter(location=location, user=self.request.user)
		# 	if user_reviews.count() > 0:
		# 		context['user_review'] = user_reviews[0]
		# 	else:
		# 		context['user_review'] = None
		return context

	def get_queryset(self):
		# return the Entry object for the current user and for done = not done
#		entry = coremodels.Entry.objects.get(id=self.kwargs['pk'])
		entry = coremodels.Entry.objects.filter(Q(user=self.request.user) | Q(assignees=self.request.user), id=self.kwargs['pk'])
#		print(entry.count())
		self.nb_entry = '666'
		if entry:
			entry = entry[0]
#			print('coucou')

# Q(user=self.request.user, transfered=0) | Q(assignees=self.request.user)
		return coremodels.Comment.objects.filter(entry=entry).order_by('-created_at')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		form.instance.entry = coremodels.Entry.objects.get(id=self.kwargs['pk'])
		return super(CommentListAppendView, self).form_valid(form)


class EntryModalUpdateView(UpdateView):
	model = coremodels.Entry
	form_class = coremodels.EntryUpdateForm
	template_name = 'entry/modal.html' #I will have to customize the fields to make it more simple rather than the current generic form template
#	fields = ['name','duedate','impediment','transfered','assignees', 'section'] # the fields on the edit page
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
#	template_name = "entry/detailsformatted.html" no longer this one with BS - Bootstrap style
	template_name = "entry/detailsBS.html"
	context_object_name = 'objects'

@csrf_exempt
def index(request):

	if request.method == 'POST':

		# request.POST['content'] is a query string like 'entry[]=3&entry[]=2&entry[]=1'
		# convert to a QueryDict so we can do things with it
		entries = QueryDict(request.POST['content'])
		section_index = 0 # first section is set to 1000
		section_count = 0 # first entry in a section
		for index, entry_id in enumerate(entries.getlist('entry[]')):
			# save index of entry_id as it's new order value
			entry = coremodels.Entry.objects.get(id=entry_id)
			if entry.section:
				section_index = section_index + 1000 # we change the counter
				section_count = 0 # the short number is defined to 2 as when moving one item to the top
				# we need an empty slot it will be X001 X being the thousand for the entry

				# so after saving this order to make a section_count increase
				entry.order = section_index + section_count
				section_count = section_count + 1

			else:
				section_count = section_count + 1
				entry.order = section_index + section_count

#			entry.order = index
#			entry.order = section_index + section_count
# for debug			print(entry.order)
			entry.save()

    # split our entries arbitrarily, so we can have two lists on the page...

	context = coremodels.Entry.objects.order_by('order')

#	entry_list1 = coremodels.Entry.objects.order_by('order')[:20]
#	entry_list2 = coremodels.Entry.objects.order_by('order')[20:]
#	context = {'entry_list1': entry_list1, 'entry_list2': entry_list2}

	return HttpResponse('')

@csrf_exempt
def EntryAjaxUpdateView(request, pk):
	# source: http://stackoverflow.com/questions/25135155/how-to-change-model-variable-by-onclick-function-used-in-template-asynchronously?answertab=active#tab-top
#    JSON_field=request.POST.get("field")
	JSON_value=request.POST.get("value")
	b=coremodels.Entry.objects.get(id=pk) #str(value))
	b.done = (False if b.done == 1 else True) # int(JSON_value) #10
	b.completed_on = timezone.now() #datetime.datetime.now()
	b.save()

	if b.recurrence_days: # if this entry is recurrent, then we clone it
		b.pk = None
		b.duedate = b.duedate + timedelta(days=b.recurrence_days)
		b.done = False
		b.save()
	return HttpResponse(None, content_type="application/json")


# code for site authentification
# only specific here is the name of entrance page
@sitegate_view(widget_attrs={'class': 'form-control', 'placeholder': lambda f: f.label}, template='form_bootstrap3') # This also prevents logged in users from accessing our sign in/sign up page.
def entrance(request):
	return render(request, 'base/entrance.html', {'title': 'Sign in & Sign up'})
