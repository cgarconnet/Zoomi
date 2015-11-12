# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
import core.views as coreviews

urlpatterns = patterns('',

	url(r'^$', coreviews.LandingView.as_view()),
)