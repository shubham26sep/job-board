from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

from jobs.apps.users.models import User
from jobs.apps.users.forms import AddUserForm, LoginForm, UpdateProfileForm, EditUserForm, CandidateFilterForm
from jobs.apps.users.permissions import PermissionMixin, AdminPermissionMixin, RecruiterPermissionMixin


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                u = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'users/login.html', {'error': 'Incorrect email or password.'})
            user = authenticate(username=u.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser == True:
                        return HttpResponseRedirect(reverse('users:user-list'))
                    else:
                        return HttpResponseRedirect(reverse('users:filter_candidates'))
                else:
                    return render(request, 'users/login.html', {'error': 'Incorrect email or password'})
            else:
                return render(request, 'users/login.html', {'error': 'Incorrect email or password.'})
    return render( request , 'users/login.html' , {'form': LoginForm} )


def logout_view(request):
    '''
    '''
    logout(request)

    return HttpResponseRedirect(reverse('users:login'))


class UserView(AdminPermissionMixin, generic.ListView):
    template_name = 'users/user-list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True).order_by('id')


class UserAdd(AdminPermissionMixin, generic.CreateView):
    model = User
    template_name = 'users/user_add.html'
    form_class = AddUserForm

    def form_valid(self, form):
        password = form.cleaned_data.pop('password')
        locations = form.cleaned_data.pop('preferred_location')
        selected_skills = form.cleaned_data.pop('skills')
        instance = form.save(commit=False)
        if password != "":
            instance.set_password(password)
        instance.username = instance.email
        instance.save()
        for loc in locations:
            instance.preferred_location.add(loc)
        for skill in selected_skills:
            instance.skills.add(skill)
        instance.save()
        return HttpResponseRedirect(reverse('users:user-list'))


class UserEdit(AdminPermissionMixin, generic.UpdateView):
    model = User
    template_name = 'users/user_edit.html'
    form_class = EditUserForm
    success_url = '/users/'


class UserDetail(PermissionMixin, generic.DetailView):
    model = User
    template_name = 'users/user-view.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(UserDetail, self).get_context_data(*args, **kwargs)
        if self.request.user.is_superuser==True:
            ctx['base_template'] = 'admin_base.html'
        else:
            ctx['base_template'] = 'recruiter_base.html'
        return ctx

class UserDelete(AdminPermissionMixin, generic.DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = '/users/'


class UpdateProfile(PermissionMixin, generic.UpdateView):
    model = User
    template_name = 'users/update-profile.html'
    form_class = UpdateProfileForm

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        ctx = super(UpdateProfile, self).get_context_data(*args, **kwargs)
        if self.request.user.is_superuser==True:
            ctx['base_template'] = 'admin_base.html'
        else:
            ctx['base_template'] = 'recruiter_base.html'
        return ctx

    def form_valid(self, form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        password = form.cleaned_data.pop('password')
        self.object = form.save(commit=False)
        if password != "":
            self.object.set_password(password)
        self.object.save()

        auth.update_session_auth_hash(self.request, self.request.user)
        if self.request.user.is_superuser == True:
            return HttpResponseRedirect(reverse('users:user-list'))
        else:
            return HttpResponseRedirect(reverse('users:filter_candidates'))


class CandidateFilter(RecruiterPermissionMixin, generic.edit.FormView):
    template_name = 'users/candidate_filter.html'
    form_class = CandidateFilterForm
    success_url = '/candidates/'

    def form_valid(self, form):
        preferred_location = form.cleaned_data.pop('preferred_location')
        work_experience = form.cleaned_data.pop('work_experience')
        skills = form.cleaned_data.pop('skills')
        self.request.session['preferred_location'] = list(preferred_location.values_list('location', flat=True))
        self.request.session['work_experience'] = work_experience
        self.request.session['skills'] = list(skills.values_list('name', flat=True))

        return HttpResponseRedirect(self.success_url)


class CandidateView(RecruiterPermissionMixin, generic.ListView):
    template_name = 'users/candidate-list.html'
    context_object_name = 'candidate_list'

    def get_queryset(self):
        queryset = User.objects.filter(user_type='candidate')
        if 'preferred_location' in self.request.session:
            locations = self.request.session['preferred_location']
            queryset = queryset.filter(preferred_location__location__in=locations).distinct()
            del locations
        if 'skills' in self.request.session:
            skills = self.request.session['skills']
            queryset = queryset.filter(skills__name__in=skills).distinct()
            del skills
        if 'work_experience' in self.request.session:
            experience = self.request.session['work_experience']
            if experience == '0-2':
                queryset = queryset.filter(work_experience__gte=0, work_experience__lte=2)
            elif experience == '2-4':
                queryset = queryset.filter(work_experience__gte=2, work_experience__lte=4)
            elif experience == '4-6':
                queryset = queryset.filter(work_experience__gte=4, work_experience__lte=6)
            elif experience == '6-8':
                queryset = queryset.filter(work_experience__gte=6, work_experience__lte=8)
            elif experience == '8-10':
                queryset = queryset.filter(work_experience__gte=8, work_experience__lte=10)
            elif experience == '10-12':
                queryset = queryset.filter(work_experience__gte=10, work_experience__lte=12)
            elif experience == '12-14':
                queryset = queryset.filter(work_experience__gte=12, work_experience__lte=14)
            elif experience == '14-16':
                queryset = queryset.filter(work_experience__gte=14, work_experience__lte=16)
            elif experience == '>16':
                queryset = queryset.filter(work_experience__gte=16)
            del experience

        return queryset