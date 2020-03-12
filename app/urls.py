
# author : Hao, Nik

from django.conf.urls import url
from django.urls import path
from app import views


urlpatterns = [
	path('', views.index, name='index'),
	path('404', views.handler404, name='404'),
	path('500', views.handler500, name='500'),
	path('redirect', views.redirect, name='redirect'),
	path('studentview', views.studentview,name='studentview'),
	path('hint', views.hint, name="hint"),
	path('update_request',views.update_request,name="update_request"),
	path('reset_question',views.reset_question,name="reset_question"),
	path('faq',views.faq, name="faq"),
	path('contact',views.contact, name="contact"),
	path('game_master_page',views.game_master_page, name="game_master_page"),
	path('create_route',views.create_route,name="create_route"),
	path('add_question',views.add_question,name="add_question"),
	path('create_game',views.create_game, name="create_game"),
	path('set_map_false',views.set_map_false, name="set_map_false"),
	path('login_page', views.login_page, name="login_page"),
	path('login_view', views.login_view, name="login_view"),
	path('logout', views.logout_view, name="logout_view"),
	path('delete_question',views.delete_question, name="delete_question"),
	path('edit',views.edit,name="edit"),
	path('add_question_existing',views.add_question_existing,name="add_question_existing"),
	path('delete_route',views.delete_route,name="delete_route"),
	path('locations', views.locations, name="locations"),
	path('signUp_page', views.signUp_page, name="signUp_page"),
	path('manage_account',views.manage_account, name="manage_account")
]
