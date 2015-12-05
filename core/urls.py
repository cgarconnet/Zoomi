# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
import core.views as coreviews
from django.contrib.auth.decorators import login_required, permission_required # to block users who are not logged is so that cannot create
# all url that we want to protect we add login_required()
# for admin securisation we add permission_required('is_staff') before (coreviews.LocationUpdateView.as_view())
# this prevent people from cheating the url


urlpatterns = patterns('',

# v1 is formerly the simple Index.html jQuery page
# this view is kept as i was well communicated to first customers
	url(r'^v1/$', coreviews.LegacyHomePageView.as_view()),

# v2.0 was a couple of tries not very well structured
# to be deleted once v3 is fully tested
	url(r'^modal/$', coreviews.ModalView.as_view()),
	url(r'^popup/$', coreviews.PopupView.as_view()),
#	url(r'^entries/$', coreviews.index, name='index'),
	url(r'^listcreate/$', coreviews.ListAppend.as_view(), name='listappend'),	
	# eg: /entries/5/
#	url(r'^entries/(?P<entry_id>\d+)/$', coreviews.detail, name='detail'),	
	url(r'^entries/(?P<pk>\d+)/$', coreviews.EntryUpdateView.as_view(), name='detail'),	
	url(r'^entriesmodal/(?P<pk>\d+)/$', coreviews.EntryModalUpdateViewv2.as_view(), name='detailmodal'),	
	url(r'^refresh_entries/(?P<pk>\d+)/$', coreviews.EntryRefreshViewv2.as_view(), name='detailrefresh'),

# Now comes the v 3.0, well better structured
	url(r'^$', login_required(coreviews.EntryListAppendView.as_view()), name='entrylist'),	
	url(r'^transferred/$', login_required(coreviews.EntryListTransferredAppendView.as_view()), name='entrylist'),	

	url(r'^entries/modal/(?P<pk>\d+)/$', login_required(coreviews.EntryModalUpdateView.as_view()), name='entrymodal'),	
	url(r'^entries/refresh/(?P<pk>\d+)/$', login_required(coreviews.EntryRefreshView.as_view()), name='entryrefresh'),
	url(r'^entries/update/(?P<pk>\d+)/$', login_required(coreviews.EntryAjaxUpdateView), name='entryupdate'),	
	url(r'^entries/index$', login_required(coreviews.index), name='index'),

	# Registering the entrance login page
	url(r'entrance/$', coreviews.entrance),

	# easy url to logout
	url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/entrance'})
		# next page coulb be our /entrance

)