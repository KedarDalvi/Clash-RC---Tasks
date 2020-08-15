#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Views
=====

Login, Logout to your userprofile and view, edit the settings therein.

"""

from django.views.generic import TemplateView
from django.views.generic import FormView

from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.contrib.auth import logout

from django.shortcuts import redirect

from django.conf import settings

try:
    import urlparse
except ImportError:
    # python3 compat
    import urllib.parse as urlparse

from .utils import default_redirect
from .forms import APAuthenticationForm
from .models import Profile

from social.backends.utils import load_backends


class Home(TemplateView):

    template_name = "user/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['available_backends'] = \
            load_backends(settings.AUTHENTICATION_BACKENDS)
        return context


class Login(FormView):
    """
    from: https://github.com/stefanfoulis/django-class-based-auth-views/ \
        blob/develop/class_based_auth_views/views.py

    This is a class based version of django.contrib.auth.views.login.

    Usage:
    in urls.py:
    url(r'^login/$',
      LoginView.as_view(
      form_class=MyCustomAuthFormClass,
      success_url='/my/custom/success/url/),
      name="login"),

    """
    redirect_field_name = 'next'
    form_class = APAuthenticationForm
    template_name = "user/login.html"
    success_url = "/user/"

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(Login, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in
        AuthenticationForm.is_valid()). So now we
        can check the test cookie stuff and log him in.
        """
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in
        AuthenticationForm.is_valid()). So now we
        set the test cookie again and re-render the form with errors.
        """
        self.set_test_cookie()
        return super(Login, self).form_invalid(form)

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(
                self.redirect_field_name,
                ''
            )

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(),
        but adds test cookie stuff.
        """
        self.set_test_cookie()
        return super(Login, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context['available_backends'] = \
            load_backends(settings.AUTHENTICATION_BACKENDS)
        return context


class Logout(TemplateView):
    template_name = "user/home.html"
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        logout(self.request)
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = kwargs
        redirect_field_name = self.get_redirect_field_name()
        context.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value":
            self.request.REQUEST.get(redirect_field_name),
            })
        return context

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_URL
        kwargs.setdefault(
            "redirect_field_name",
            self.get_redirect_field_name()
        )
        return default_redirect(self.request, fallback_url, **kwargs)


class RequireEmail(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(RequireEmail, self).get_context_data(**kwargs)
        context['email_required'] = True
        context['backend'] = self.session['partial_pipeline']['backend']
        context['available_backends'] = \
            load_backends(settings.AUTHENTICATION_BACKENDS)
        return context


class ProfileView(DetailView):
    model = Profile

    def get_object(self):
        if 'pk' in self.request.GET:
            user = User.objects.get(pk=self.request.GET['pk'])
            return self.model.objects.get(user=user)
        else:
            user, created = self.model.objects.get_or_create(
                user=self.request.user
            )
            if created:
                user.save()
            return user
