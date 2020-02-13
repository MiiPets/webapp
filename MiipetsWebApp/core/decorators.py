from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from core.models import User, MiiSitter
from django.shortcuts import redirect

def miiowner_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='core-login'):
    '''
    Decorator for views that checks that the logged in user is a miiowner,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_owner,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def miisitter_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='core-login'):
    '''
    Decorator for views that checks that the logged in user is a sitter,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_sitter,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def validation_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='core-login'):
    '''
    Decorator for views that checks that the logged in user is a sitter
    that has been vetted by the miipets team. If not, will redirect them
    to page saying they are not vetted yet.
    '''
    def wrap(request, *args, **kwargs):
        sitter = MiiSitter.objects.get(user=request.user)
        if sitter.validated:
            return function(request, *args, **kwargs)
        else:
            return redirect('sitter-still-vetting')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def merchant_id_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='core-login'):
    '''
    Decorator for views that checks that the logged in user is a sitter
    that has been vetted by the miipets team. If not, will redirect them
    to page saying they are not vetted yet.
    '''
    def wrap(request, *args, **kwargs):
        sitter = MiiSitter.objects.get(user=request.user)
        if sitter.merchant_id:
            return function(request, *args, **kwargs)
        else:
            return redirect('sitter-edit-profile')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def sitter_id_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='core-login'):
    '''
    Decorator for views that checks that the logged in user is a sitter
    that has been vetted by the miipets team. If not, will redirect them
    to page saying they are not vetted yet.
    '''
    def wrap(request, *args, **kwargs):
        sitter = MiiSitter.objects.get(user=request.user)
        if sitter.id_number:
            return function(request, *args, **kwargs)
        else:
            return redirect('sitter-edit-profile')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
