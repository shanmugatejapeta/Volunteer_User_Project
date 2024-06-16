from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('prob',views.Problem.as_view(),name='prob'),
    path('index',views.List.as_view(),name='index'),
    path('index/<int:pk>',views.DetailProblem.as_view(),name='buttonSolution'),
    path('vol/index',views.VolIndex.as_view(),name='volindex'),
    path('vol/index/<int:uid>/<int:pk>',views.Solution_Volunteer.as_view(),name='solution'),
    path('login',views.Login_User.as_view(),name='userlogin'),
    path('loginvol',views.Login_Volunteer.as_view(),name='vollogin'),
    path('logout',views.Logout_User.as_view(),name='logout'),
    path('delete/<int:pk>',views.Delete.as_view(),name='deleteProb'),
    path('viewuser/<int:pk>',views.list_problems,name='prob_of_user'),
    path('signup',views.SignUpView.as_view(),name='signup'),
    
]