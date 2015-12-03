# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
import core.views as coreviews

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
	url(r'^$', coreviews.EntryListAppendView.as_view(), name='entrylist'),	
	url(r'^entries/modal/(?P<pk>\d+)/$', coreviews.EntryModalUpdateView.as_view(), name='entrymodal'),	
	url(r'^entries/refresh/(?P<pk>\d+)/$', coreviews.EntryRefreshView.as_view(), name='entryrefresh'),
	url(r'^entries/update/(?P<pk>\d+)/$', coreviews.EntryAjaxUpdateView, name='entryupdate'),	
	url(r'^entries/index$', coreviews.index, name='index'),
	url(r'^entries/editpage/(?P<pk>\d+)/$', coreviews.EntryEditView.as_view(), name='entryedit'),

)