from django.contrib import messages
from django.contrib.auth import login, authenticate, views as auth_views
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import (CustomUserCreationForm, ProfileUpdateForm,
                            CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm,
                            CustomPasswordChangeForm)
from accounts.models import Profile



class CustomSignUpView(CreateView):
    model = User
    template_name = 'accounts/registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)

        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)

    def form_valid(self, form):
        result = super().form_valid(form)
        #username = form.cleaned_data['username']
        #password = form.cleaned_data['password1']
        #user = authenticate(self.request, username=username, password=password)
        user = self.object
        if user is not None:
            login(self.request, user)
        return result



class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_detail.html'

    def get_object(self, queryset=None):
        if self.request.user.id == None:
           return None

        pk = self.request.user.pk
        self.kwargs['pk'] = pk
        profile = super().get_object(queryset)
        return profile

    def get(self, request, *args, **kwargs):
        if self.request.user.id == None:
            redirect_url = reverse_lazy('accounts:sign_in')
            return HttpResponseRedirect(redirect_url)

        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        #profile = self.object
        context = super().get_context_data(**kwargs)
        context['title_profile'] = True
        user = self.object.user
        enrolls_list = user.enrolls.all().order_by('created')
        reviews_list = user.reviews.all().order_by('created')
        context['reviews_list'] = reviews_list

        for el in enrolls_list:
            el.rate = '--'
            for rev in reviews_list:
                if el.event == rev.event:
                    el.rate = rev.rate
                    break
        context['enrolls_list'] = enrolls_list
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Данные успешно обновлены')
        return super().form_valid(form)



class CustomLoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/registration/signin.html'
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)

        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)



class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/registration/password_reset_email.txt'
    subject_template_name = 'accounts/registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    # html_email_template_name = 'accounts/registration/password_reset_email.html'

    def form_valid(self, form):
        self.request.session['reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)



class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.get('reset_email', '')

        # удалить авторизованного пользователя из сессии
        del self.request.session['_auth_user_id']

        return context



class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/registration/password_change_done.html'
    success_url = reverse_lazy('accounts:password_change_done'),

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # удалить авторизованного пользователя из сессии
        del self.request.session['_auth_user_id']
        context['user'] = None

        return context



class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')



class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'

