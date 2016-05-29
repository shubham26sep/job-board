"""
"""
from django.conf import settings
from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    location = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.location


class Skill(models.Model):
    name = models.CharField(_('name'), max_length=60)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """
    Store User account details.
    """

    USER_TYPE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate'),
    )

    UG_COURSE_CHOICES = (
        ('none', 'NA'),
        ('B.Tech/B.E.', 'B.Tech/B.E.'),
        ('B.Sc', 'B.Sc'),
        ('B.C.A', 'B.C.A'),
    )

    PG_COURSE_CHOICES = (
        ('none', 'NA'),
        ('M.Tech', 'M.Tech'),
        ('M.C.A', 'M.C.A'),
    )

    username = models.CharField(
        _('username'),
        max_length=75,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(_('name'), max_length=60)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active.  Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    resume = models.BooleanField(default=False)
    mobile_number = models.PositiveIntegerField(_('mobile number'), max_length=10, null=True, blank=True)
    work_experience = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    current_location = models.ForeignKey(Location, related_name="current_location", null=True, blank=True)
    corrected_location = models.ForeignKey(Location, related_name="corrected_location", null=True, blank=True)
    nearest_city = models.ForeignKey(Location, related_name="nearest_city", null=True, blank=True)
    preferred_location = models.ManyToManyField(Location, null=True, blank=True)
    ctc = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    current_designation = models.CharField(_('current designation'), max_length=100, null=True, blank=True)
    current_employer = models.CharField(_('current employer'), max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='recruiter')
    skills = models.ManyToManyField(Skill, related_name="skills", null=True, blank=True)
    ug_course = models.CharField(max_length=20, choices=UG_COURSE_CHOICES, default='none')
    ug_institute_name = models.CharField(_('ug institute name'), max_length=100, null=True, blank=True)
    ug_tier1 = models.BooleanField(default=False)
    ug_passing_year = models.PositiveSmallIntegerField(max_length=4, null=True, blank=True)
    pg_course = models.CharField(max_length=20, choices=PG_COURSE_CHOICES, default='none')
    pg_institute_name = models.CharField(_('pg institute name'), max_length=100, null=True, blank=True)
    pg_tier1 = models.BooleanField(default=False)
    pg_passing_year = models.PositiveSmallIntegerField(max_length=4, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['username',]

    def __str__(self):
        return '<{id}>: {username}'.format(
            id=self.id,
            username=self.username,
        )

    # def get_full_name(self):
    #     return self.name

    def get_short_name(self):
        return self.id



    def __str__(self):
        return self.name