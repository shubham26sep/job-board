from django import forms
from django.core.exceptions import ValidationError

from jobs.apps.users.models import User


class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class UpdateProfileForm(forms.ModelForm):
    """
    """
    password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name' , 'email' , 'password' , 'confirm_password']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data.pop('confirm_password')
        if password != confirm_password:
            raise ValidationError("password does not match.")

        return confirm_password


class AddUserForm(forms.ModelForm):
    """
    """
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile_number', 'password', 'confirm_password', 'user_type', 'work_experience',
        'resume', 'current_location', 'corrected_location', 'nearest_city', 'preferred_location',
        'ctc', 'current_designation', 'current_employer', 'skills', 'ug_course', 'ug_institute_name',
        'ug_tier1', 'ug_passing_year', 'pg_course', 'pg_institute_name', 'pg_tier1', 'pg_passing_year']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data.pop('confirm_password')
        if password != confirm_password:
            raise ValidationError("password does not match.")

        return confirm_password


class EditUserForm(AddUserForm):
    """
    """
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields.pop('confirm_password')


class CandidateFilterForm(forms.ModelForm):
    """
    """
    WORK_EXPERIENCE_CHOICES = (
        ('0-2', '0-2'),
        ('2-4', '2-4'),
        ('4-6', '4-6'),
        ('6-8', '6-8'),
        ('8-10', '8-10'),
        ('10-12', '10-12'),
        ('12-14', '12-14'),
        ('14-16', '14-16'),
        ('>16', '>16'),
    )
    work_experience = forms.ChoiceField(choices = WORK_EXPERIENCE_CHOICES, widget=forms.Select(), required=True)
    class Meta:
        model = User
        fields = ['preferred_location', 'skills']
    