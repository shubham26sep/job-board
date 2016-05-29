from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.login_view, name='login'), 
	url(r'^accounts/login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^users/$',views.UserView.as_view(), name='user-list'),
	url(r'^users/new/$',views.UserAdd.as_view(), name='users_add'),
	url(r'^users/(?P<pk>\d+)/$',views.UserDetail.as_view(), name='user_detail'),
	url(r'^users/(?P<pk>\d+)/edit/$',views.UserEdit.as_view(), name='user_edit'),
	url(r'^users/(?P<pk>\d+)/delete/$',views.UserDelete.as_view(), name='user_delete'),
	url(r'^filter-candidates/$',views.CandidateFilter.as_view(), name='filter_candidates'),
	url(r'^candidates/$',views.CandidateView.as_view(), name='candidate-list'),
	url(r'^export-candidate-data/$', views.export_candidate_data, name='export_candidate_data'),
	url(r'^profile/$',views.UpdateProfile.as_view(), name='update-profile'),

]