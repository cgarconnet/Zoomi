# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
import core.views as coreviews
from django.contrib.auth.decorators import login_required, permission_required # to block users who are not logged is so that cannot create
# all url that we want to protect we add login_required()
# for admin securisation we add permission_required('is_staff') before (coreviews.LocationUpdateView.as_view())
# this prevent people from cheating the url
import django.contrib.auth.views as authviews

urlpatterns = [

# v1 is formerly the simple Index.html jQuery page
# this view is kept as i was well communicated to first customers
	url(r'^v1/$', coreviews.LegacyHomePageView.as_view()),

# v2.0 was a couple of tries not very well structured
# to be deleted once v3 is fully tested
#	url(r'^modal/$', coreviews.ModalView.as_view()),
#	url(r'^popup/$', coreviews.PopupView.as_view()),
#	url(r'^entries/$', coreviews.index, name='index'),
#	url(r'^listcreate/$', coreviews.ListAppend.as_view(), name='listappend'),	
	# eg: /entries/5/
#	url(r'^entries/(?P<entry_id>\d+)/$', coreviews.detail, name='detail'),	
#	url(r'^entries/(?P<pk>\d+)/$', coreviews.EntryUpdateView.as_view(), name='detail'),	
#	url(r'^entriesmodal/(?P<pk>\d+)/$', coreviews.EntryModalUpdateViewv2.as_view(), name='detailmodal'),	
#	url(r'^refresh_entries/(?P<pk>\d+)/$', coreviews.EntryRefreshViewv2.as_view(), name='detailrefresh'),

# Now comes the v 3.0, well better structured
#	url(r'^v2/$', login_required(coreviews.EntryListAppendView.as_view()), name='entrylist'),	
	url(r'^$', login_required(coreviews.EntryListAppendViewBS.as_view()), name='entrylistBS'), # Bootstrap test
	url(r'^releases/$', coreviews.ReleasesPageView.as_view()),
	url(r'^help/$', coreviews.HelpPageView.as_view()),

	url(r'^transferred/$', login_required(coreviews.EntryListTransferredAppendView.as_view()), name='transflist'),	

	url(r'^entries/modal/(?P<pk>\d+)/$', login_required(coreviews.EntryModalUpdateView.as_view()), name='entrymodal'),	
	url(r'^entries/refresh/(?P<pk>\d+)/$', login_required(coreviews.EntryRefreshView.as_view()), name='entryrefresh'),
	url(r'^entries/update/(?P<pk>\d+)/$', login_required(coreviews.EntryAjaxUpdateView), name='entryupdate'),	
	url(r'^entries/index$', login_required(coreviews.index), name='index'),
	url(r'^entries/(?P<pk>\d+)/$', login_required(coreviews.EntryUpdateView.as_view()), name='detail'),	

	# to show the comments on an entry
	url(r'^entries/(?P<pk>\d+)/comment/$', login_required(coreviews.CommentListAppendView.as_view()), name='commentlist'),	

	# to show the theme
	url(r'^themes/$', login_required(coreviews.ThemeListAppendView.as_view()), name='themelist'),	
	url(r'^themes/(?P<pk>\d+)/entries/$', login_required(coreviews.ThemeListEntriesView.as_view()), name='themedetails'),	


	# to show the user profile
	url(r'^user/details/$', login_required(coreviews.UserDetailView.as_view()), name='userdetails'),
	url(r'^user/profile/$', login_required(coreviews.UserProfileView.as_view()), name='userprofile'),

	# Registering the entrance login page
	url(r'^entrance/$', coreviews.entrance),

	# easy url to logout
	url(r'^logout/$', authviews.logout,{'next_page': '/entrance/'}),
		# next page coulb be our /entrance

]