from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import ProbForm,SignUpForm
from .models import Problems,Volunteers,VUser
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required


from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout,login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from time import sleep
# Create your views here.

# class PermissionRequiredMixin(AccessMixin):
#     """
#     Mixin to require a specific permission for a view.
#     """
#     permission_required = 'app.view_problem'  # Define the permission_required attribute in subclasses

#     def dispatch(self, request, *args, **kwargs):
#         # Check if permission_required is set
#         if self.permission_required is None:
#             raise ImproperlyConfigured(
#                 "{0} is missing the permission_required attribute.".format(
#                     self.__class__.__name__
#                 )
#             )

#         # Fetch the user object based on kwargs
#         user = request.user

#         # Check if the user has the required permission
#         if not request.user.has_perm(self.permission_required) or request.user != user:
#             raise PermissionDenied

#         return super().dispatch(request, *args, **kwargs)


def home(request):
    return render(request,'app/home.html')

class Problem(LoginRequiredMixin,CreateView):
    template_name='app/problem_form.html'
    form_class=ProbForm
    model=Problems
    success_url='index'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class List(LoginRequiredMixin,ListView):
    template_name='app/index.html'
    model=Problems
    context_object_name='problems'

    def get_queryset(self) -> QuerySet[Any]:
        problems=Problems.objects.filter(user=self.request.user)
        return problems
        

class DetailProblem(LoginRequiredMixin,DetailView):
    template_name='app/view_solution.html'
    context_object_name='problem'
    model=Problems
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        prob=Problems.objects.get(id=self.kwargs.get('pk'))
        if prob.user.id == self.request.user.id:
            return super().get_context_data(**kwargs)
        else:
            raise PermissionDenied

class VolIndex(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    template_name='app/vol_index.html'
    model=Problems
    context_object_name='users'
    permission_required=('app.view_problems', 'app.view_volunteers') #you can give any number of permissions
    def get_queryset(self) -> QuerySet[Any]:
        volunteer=Volunteers.objects.get(vol_id=self.request.user.id)
        users=VUser.objects.filter(vol=volunteer)
        return users

@login_required
@permission_required('app.view_problems', raise_exception=True)
def list_problems(request,pk):
    user=User.objects.get(id=pk)
    curr_user=User.objects.get(id=request.user.id)
    curr_vol=Volunteers.objects.get(vol_id=curr_user.id)
    curr_vol_users=VUser.objects.filter(vol=curr_vol)
    for u in curr_vol_users:
        if u.user.id == user.id:
            problems=Problems.objects.filter(user=user)
            return render(request,'app/view_user_problems.html',{'user':user,'problems':problems})
    raise PermissionDenied

    
class Solution_Volunteer(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    template_name='app/vol_solution.html'
    model=Problems
    fields=('solution','resolved')
    context_object_name='problem'
    success_url='../../../index'
    permission_required=('app.view_problems',)
    def get_success_url(self) -> str:
        success_url='../../../viewuser/'+str(self.kwargs.get('uid'))
        return success_url
    def get_queryset(self) -> QuerySet[Any]:
        if self.request.method=='GET':
            querySet=super().get_queryset()
            querySet.user_id=self.kwargs.get('uid')
            return querySet

        return super().get_queryset()
    

class Login_User(LoginView):
    template_name='app/user_login.html'

    def get_success_url(self) -> str:
        return reverse_lazy('index')
    
    
class Login_Volunteer(LoginView):
    template_name='app/vol_login.html'

    def get_success_url(self) -> str:
        if self.request.user.groups.filter(name='Volunteers').exists():
            return reverse_lazy('volindex')
        else:
            # logout_view=Logout_User.as_view()
            logout(self.request)
            raise PermissionDenied
    
class Logout_User(LogoutView):
    next_page = reverse_lazy('home')

class Delete(DeleteView):
    model=Problems
    template_name='app/delete_prob.html'
    success_url='../index'

class SignUpView(CreateView):
    form_class=SignUpForm
    template_name='app/signup.html'
    success_url='index'

    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().get(request,*args,*kwargs)
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if form.is_valid():
            user=form.save()
            login(self.request,user)
            volunteer=form.cleaned_data['volunteer']
            vuser=VUser(vol=volunteer,user=self.request.user)
            vuser.save()
            logout(self.request)
        return super().form_valid(form)
    


    
    