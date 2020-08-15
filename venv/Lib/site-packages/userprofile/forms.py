#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Django-Forms to be used for userprofile
"""

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import PrependedText


class APAuthenticationForm(AuthenticationForm):
    """
    APAuthenticationForm subclasses AuthenticationFiorm from Django
    for *A*ngry*P*lanet
    It includes crispy form helpers, to integrate with bootstrap
    """
    def __init__(self, *args, **kwargs):
        super(APAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_class = 'well'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('user:login')
        self.helper.layout = Layout(
            PrependedText('username', '@', placeholder="username"),
            PrependedText('password', '*', placeholder="password"),
            Submit('submit', _('Login')),
        )
