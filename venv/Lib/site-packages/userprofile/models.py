from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from datetime import date

GENDER_CHOICES = (
    ('u', _('undefined')),
    ('M', _('Male')),
    ('F', _('Female')),
)

LOOKFOR_CHOICES = (
    ('a', _('any')),
    ('M', _('Man')),
    ('F', _('Female')),
)


class ProfileManager(models.Manager):
    """
    .. class:: ProfileManager

    Django Manager class for :mod:`question.models.Profile` objects.

    It provides simple statistic methods.
    """

    def count(self):
        """
        .. classmethod:: count(self)

        Returns the number of all profiles in database.

        :rtype: count of all profiles.

        """
        return super(ProfileManager, self).get_queryset().count()

    def female_count(self):
        """
        .. classmethod:: female_count(self)

        Returns the number of all female profiles in database.

        :rtype: count of female profiles.
        """
        return super(ProfileManager, self).get_queryset().filter(
            gender='F'
        ).count()

    def male_count(self):
        """
        .. classmethod:: male_count(self)

        Returns the number of all male profiles in database.

        :rtype: count of male profiles.
        """
        return super(ProfileManager, self).get_queryset().filter(
            gender='M'
        ).count()

    def female_percent(self):
        """
        .. classmethod:: female_percent(self)

        Returns the percent of female profiles in database.

        :rtype: percent of female profiles.
        """
        return self.female_count() / self.count()

    def male_percent(self):
        """
        .. classmethod:: male_percent(self)

        Returns the percent of male profiles in database.

        :rtype: percent of male profiles.
        """
        return self.male_count() / self.count()

    def get_by_natural_key(self, username):
        return self.get(username=username)


class Profile(models.Model):
    """
    The actual Profile to describe a user in the context of matchmaking.
    """
    user = models.OneToOneField(User)
    """Reference to :mod:`django.contrib.auth.models.User`"""

    is_public = models.BooleanField(default=False)
    """Describes whether the profile shall be visible publically."""

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES[0][0]
    )
    """Describe the gender of the user."""

    lookfor = models.CharField(
        max_length=1,
        choices=LOOKFOR_CHOICES,
        default=LOOKFOR_CHOICES[0][0]
    )
    """Describe what gender the user is looking for."""

    dob = models.DateField(blank=True, null=True)
    """Date of Birth."""

    objects = ProfileManager()
    """Use :mod:`question.models.ProfileManager` for Profile.objects."""

    @property
    def age(self):
        """
        Calculate a users age in years.
        """
        if self.dob:
            return int((date.today() - self.dob).days / 365)
        else:
            return 0

    def __unicode__(self):
        """
        Unicode representation of self
        """
        return u'%s (%s, %s)' % (self.user.username, self.gender, self.age)

    def __str__(self):
        return self.__unicode__()

    @models.permalink
    def get_absolute_url(self):
        return ('user:profile-view', [str(self.id)])
