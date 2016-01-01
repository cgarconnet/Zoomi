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

class EntryUpdateView(UpdateView): # re-used from v2
	model = coremodels.Entry
#	model = coremodels.Event # by just changing the model here, I can have access to the right form edit template
	template_name = 'base/form.html'
	form_class = coremodels.EntryUpdateForm

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
#	fields = ['name'] # "__all__" no longer required as defined in the models

	def get_queryset(self):
		# return the Entry object for the current user and for done = not done
		return coremodels.Entry.objects.filter(Q(user=self.request.user, transfered=0) | Q(assignees=self.request.user), done=False).order_by('order')

	def form_valid(self, form):
	# this feature is used between submission of the user and sending these data to the database
		form.instance.user = self.request.user
		return super(EntryListAppendViewBS, self).form_valid(form)

class EntryListTransferredAppendView(ListAppendView):
	model = coremodels.Entry
	template_name = 'entry/transferred.html'
	context_object_name = 'entry'
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


	def get_queryset(self):
		# return the Entry object for the current user and for done = not done
		entry = coremodels.Entry.objects.get(id=self.kwargs['pk'])

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

		for index, entry_id in enumerate(entries.getlist('entry[]')):
			# save index of entry_id as it's new order value
			entry = coremodels.Entry.objects.get(id=entry_id)
			entry.order = index
# for debug			print(index)
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
    #delete change statement
    b.done = (False if b.done == 1 else True) # int(JSON_value) #10
    b.save()
    # resp=json.dumps(b)
#    return HttpResponse(resp, content_type="application/json")
	# I should now refresh the value in the DOM
    return HttpResponse(None, content_type="application/json")


# code for site authentification
# only specific here is the name of entrance page
@sitegate_view(widget_attrs={'class': 'form-control', 'placeholder': lambda f: f.label}, template='form_bootstrap3') # This also prevents logged in users from accessing our sign in/sign up page.
def entrance(request):
	return render(request, 'base/entrance.html', {'title': 'Sign in & Sign up'})