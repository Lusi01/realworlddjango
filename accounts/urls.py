from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views
from .forms import CustomPasswordChangeForm

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', views.CustomSignUpView.as_view(), name='sign_up'),
    path('sign-in/', views.CustomLoginView.as_view(), name='sign_in'),

    # побеспокоиться о безопасности - чтобы пользователь мог открыть только свой профайл -
    # следов-но надо удалить pk из URL-адреса
    #path('profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Password reset
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<str:uidb64>/<str:token>', views.CustomPasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # Password change
    path('password-change/',
         PasswordChangeView.as_view(
             template_name='accounts/registration/password_change.html',
             form_class=CustomPasswordChangeForm,
             success_url=reverse_lazy('accounts:password_change_done')
         ),
         name='password_change'),
#    path('password-change/',  views.CustomPasswordChangeView.as_view(), name='password_change'),

    # path('password-change-done/',
    #      PasswordChangeDoneView.as_view(
    #          template_name='accounts/registration/password_change_done.html'
    #      ),
    #      name='password_change_done'),
    path('password-change-done/',  views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

]