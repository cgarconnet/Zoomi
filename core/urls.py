# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
import core.views as coreviews

urlpatterns = patterns('',

	url(r'^$', coreviews.LandingView.as_view()),
	url(r'^modal/$', coreviews.ModalView.as_view()),
	url(r'^popup/$', coreviews.PopupView.as_view()),
	url(r'^entries/$', coreviews.index, name='index'),
	url(r'^listcreate/$', coreviews.ListAppend.as_view(), name='listappend'),	
	# eg: /entries/5/
#	url(r'^entries/(?P<entry_id>\d+)/$', coreviews.detail, name='detail'),	
	url(r'^entries/(?P<pk>\d+)/$', coreviews.EntryUpdateView.as_view(), name='detail'),	


)