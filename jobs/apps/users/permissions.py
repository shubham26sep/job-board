from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


class PermissionMixin(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PermissionMixin, self).dispatch(*args, **kwargs)


class AdminPermissionMixin(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(AdminPermissionMixin, self).dispatch(*args, **kwargs)


class RecruiterPermissionMixin(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff==False and u.user_type=='recruiter'))
    def dispatch(self, *args, **kwargs):
        return super(RecruiterPermissionMixin, self).dispatch(*args, **kwargs)