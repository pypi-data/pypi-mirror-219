from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from djangoldp.models import Model
from djangoldp_community.models import Community, CommunityMember
from djangoldp_tzcld.permissions import TzcldCommunityProfilePermissions

#############################
# Extend user model
#############################


class TzcldTerritoryDepartment(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Department')
        verbose_name_plural = _("TZCLD Departments")
        anonymous_perms = ['view']
        container_path = "tzcld-departments/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:departments"

class TzcldTerritoryRegion(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Région')
        verbose_name_plural = _("TZCLD Régions")
        anonymous_perms = ['view']
        container_path = "tzcld-regions/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:regions"

class TzcldProfilesMembership(Model):
    name = models.CharField(max_length=255, blank=False, null=True, default='')


    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Memebership type')
        verbose_name_plural = _("TZCLD Memebership types")
        anonymous_perms = ['view']
        authenticated_perms = ['view']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-profile-membership/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:profileMembership"

# DjangoLDP User Extension

class TzcldProfile(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tzcld_profile")
    #description = models.CharField(max_length=255, blank=True, null=True, default='')
    #postal_code = models.CharField(max_length=255, blank=True, null=True, default='')
    #address = models.CharField(max_length=255, blank=True, null=True, default='')
    #phone = models.CharField(max_length=255, blank=True, null=True, default='')
    #position = models.CharField(max_length=255, blank=True, null=True, default='')
    last_contribution_year = models.CharField(max_length=255, blank=True, null=True, default='')
    regions = models.ManyToManyField(TzcldTerritoryRegion, related_name='profile_regions', blank=True)
    departments = models.ManyToManyField(TzcldTerritoryDepartment, related_name='profile_department', blank=True)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        try:
            return '{} ({})'.format(self.user.get_full_name(), self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD User Profile')
        verbose_name_plural = _("TZCLD Users Profiles")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['inherit', 'change']
        ordering = ['user']
        #serializer_fields = ['@id', 'description', 'regions', 'postal_code', 'address', 'events', 'phone', 'orgs', 'position', 'membership', 'last_contribution_year', 'jobs']
        serializer_fields = ['@id', 'last_contribution_year', 'jobs', 'regions', 'departments', 'is_member']
        rdf_type = "tzcld:profile"
        auto_author = 'user'
        depth = 1
        nested_fields = ['jobs']

class TzcldProfileJob(Model):
    position = models.CharField(max_length=255, blank=True, null=True, default='')
    organisation = models.CharField(max_length=255, blank=True, null=True, default='')
    address = models.CharField(max_length=255, blank=True, null=True, default='')
    postal_code = models.CharField(max_length=255, blank=True, null=True, default='')
    city = models.CharField(max_length=255, blank=True, null=True, default='')
    department = models.ForeignKey(TzcldTerritoryDepartment, on_delete=models.DO_NOTHING,related_name='job_department', blank=True, null=True)
    #address_public = models.BooleanField(default=False)
    profile = models.ForeignKey(TzcldProfile, on_delete=models.CASCADE,related_name='jobs', blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True, default='')
    
    phone = models.CharField(max_length=255, blank=True, null=True, default='')
    phone_public = models.BooleanField(default=False)
    mobile_phone = models.CharField(max_length=255, blank=True, null=True, default='')
    mobile_phone_public = models.BooleanField(default=False)
    email = models.CharField(max_length=255, blank=True, null=True, default='')
    email_public = models.BooleanField(default=False)

    def __str__(self):
        try:
            return '{} ({})'.format(self.position, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD User profile job')
        verbose_name_plural = _("TZCLD Users profiles jobs")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'view', 'add', 'change']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-profile-job/"
        serializer_fields = ['@id', 'position', 'organisation', 'address', 'postal_code', 'city', 'department','profile', 'link','phone' ,'phone_public' ,'mobile_phone' ,'mobile_phone_public' ,'email' ,'email_public' ]
        nested_fields = []
        rdf_type = "tzcld:profileJob"

#############################
# Old models version
#############################
"""

class TzcldProfileEvent(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    tzcldprofile = models.ManyToManyField(TzcldProfile, related_name='events', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Event')
        verbose_name_plural = _("TZCLD Events")
        anonymous_perms = ['view']
        container_path = "tzcld-events/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:event"


class TzcldProfileOrganisation(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    tzcldprofile = models.ManyToManyField(TzcldProfile, related_name='orgs', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Organisation or Territory')
        verbose_name_plural = _("TZCLD Organisations or Territories")
        anonymous_perms = ['view']
        container_path = "tzcld-orgs/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:org"


class TzcldProfileRegion(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    tzcldprofile = models.ManyToManyField(TzcldProfile, related_name='regions', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Region or departement')
        verbose_name_plural = _("TZCLD Regions or departements")
        anonymous_perms = ['view']
        container_path = "tzcld-regions/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:regions"
"""

#############################
# DjangoLDP Community Extension
#############################

class TzcldTerritoriesStepState(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory step state')
        verbose_name_plural = _("TZCLD Territories step states")
        anonymous_perms = ['view']
        container_path = "tzcld-territories-step-states/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryStepState"

class TzcldTerritoriesKind(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Kind')
        verbose_name_plural = _("TZCLD Territories Kind")
        anonymous_perms = ['view']
        container_path = "tzcld-kinds/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryKind"

class TzcldTerritoriesOriginMobilization(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Origin Mobilization')
        verbose_name_plural = _("TZCLD Origins Mobilization")
        anonymous_perms = ['view']
        container_path = "tzcld-origins-mobilization/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryOriginMobilization"


class TzcldTerritoriesTrainingCourse(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Training Course')
        verbose_name_plural = _("TZCLD Training Courses")
        anonymous_perms = ['view']
        container_path = "tzcld-training-courses/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryTrainingCourse"

class TzcldTerritoriesTeamTrainingCourse(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Team Training Course')
        verbose_name_plural = _("TZCLD Team Training Courses")
        anonymous_perms = ['view']
        container_path = "tzcld-team-training-courses/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryTeamTrainingCourse"

class TzcldTerritoriesTrainingPromotoion(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Training Promotoion')
        verbose_name_plural = _("TZCLD Training Promotoions")
        anonymous_perms = ['view']
        container_path = "tzcld-training-promotoions/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryTrainingPromotoion"

class TzcldTerritoriesTeamTrainingPromotoion(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Team Training Promotoion')
        verbose_name_plural = _("TZCLD Team Training Promotoions")
        anonymous_perms = ['view']
        container_path = "tzcld-team-training-promotoions/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryTeamTrainingPromotoion"

class TzcldTerritoriesTrainingProfile(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Training Profile')
        verbose_name_plural = _("TZCLD Training Profiles")
        anonymous_perms = ['view']
        container_path = "tzcld-training-profiles/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryTrainingProfile"


class TzcldCommunity(Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='tzcld_profile', null=True, blank=True)
    kind = models.ForeignKey(TzcldTerritoriesKind, on_delete=models.DO_NOTHING,related_name='kind', blank=True, null=True)
    step_state = models.ForeignKey(TzcldTerritoriesStepState, on_delete=models.DO_NOTHING,related_name='step_state', blank=False, null=True)
    regions = models.ManyToManyField(TzcldTerritoryRegion, related_name='community_regions', blank=True)
    departments = models.ManyToManyField(TzcldTerritoryDepartment, related_name='community_departments', blank=True)
    membership = models.ForeignKey(TzcldProfilesMembership, on_delete=models.DO_NOTHING,related_name='membership', blank=False, null=True)
    membership_organisation_name = models.CharField(max_length=254, blank=True, null=True, default='')
    visible = models.BooleanField(default=True)
    """
    features = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_mail_1 = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_mail_2 = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_mail_3 = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_last_name = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_first_name = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_job = models.CharField(max_length=255, blank=True, null=True, default='')
    membership = models.BooleanField(default=False)
    last_contribution_year = models.CharField(max_length=255, blank=True, null=True, default='')
    """

    def __str__(self):
        try:
            return '{} ({})'.format(self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Profile')
        verbose_name_plural = _("TZCLD Territories Profiles")
        permission_classes = [TzcldCommunityProfilePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        ordering = ['community']
        container_path = "tzcld-communities/"
        #serializer_fields = ['@id', 'contact_first_name', 'contact_last_name', 'contact_job', 'kind', 'features', 'region', 'contact_mail_1', 'contact_mail_2', 'contact_mail_3', 'membership', 'last_contribution_year']
        serializer_fields = ['@id', 'community', 'kind', 'step_state', 'kind', 'departments', 'regions', 'locations', 'tzcld_community_contacts', 'membership', 'membership_organisation_name', 'visible']
        rdf_type = "tzcld:communityProfile"
        depth = 0

class TzcldCommunityIdentity(Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='tzcld_profile_identity', null=True, blank=True)
    deputy = models.CharField(max_length=254, blank=True, null=True, default='')
    circonscription = models.CharField(max_length=254, blank=True, null=True, default='')
    origin_mobilization = models.ForeignKey(TzcldTerritoriesOriginMobilization, on_delete=models.DO_NOTHING,related_name='territory_origin_mobilization', blank=True, null=True)
    application_date =  models.DateField(verbose_name="Estimated application date")
    signatory_structure = models.CharField(max_length=254, blank=True, null=True, default='')
    birth_date =  models.DateField(verbose_name="Project birth date")
    last_contribution_date =  models.DateField(verbose_name="Last contribution date")

    def __str__(self):
        try:
            return '{} ({})'.format(self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Identity')
        verbose_name_plural = _("TZCLD Territories Identities")
        permission_classes = [TzcldCommunityProfilePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        container_path = "tzcld-communities-identity/"
        serializer_fields = ['@id', 'community', 'deputy', 'circonscription', 'origin_mobilization', 'application_date', 'signatory_structure', 'birth_date', 'last_contribution_date']
        rdf_type = "tzcld:communityIdentity"
        depth = 0


class TzcldTerritoryLocation(Model):
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    address = models.CharField(max_length=255, blank=True, null=True, default='')
    postal_code = models.CharField(max_length=255, blank=True, null=True, default='')
    city = models.CharField(max_length=255, blank=True, null=True, default='')
    #department = models.ForeignKey(TzcldTerritoryDepartment, on_delete=models.DO_NOTHING,related_name='location_department', blank=True, null=True)
    #link = models.CharField(max_length=255, blank=True, null=True, default='')
    #twitter_link = models.CharField(max_length=255, blank=True, null=True, default='')
    #linkedin_link = models.CharField(max_length=255, blank=True, null=True, default='')
    community = models.ForeignKey(TzcldCommunity, on_delete=models.CASCADE,related_name='locations', blank=True, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory location')
        verbose_name_plural = _("TZCLD Territories locations")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'view', 'add', 'change']
        superuser_perms = ['inherit', 'view', 'add', 'change']
        container_path = "tzcld-territories-location/"
        #serializer_fields = ['@id', 'name', 'address', 'postal_code', 'city', 'department', 'link', 'twitter_link', 'linkedin_link', 'phones', 'emails', 'community']
        serializer_fields = ['@id', 'name', 'address', 'postal_code', 'city', 'phones', 'emails', 'community']
        nested_fields = []
        rdf_type = "tzcld:territoryLocation"

class TzcldTerritoryProjectTeamMemeber(Model):
    firstname = models.CharField(max_length=255, blank=True, null=True, default='')
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    etp = models.CharField(max_length=255, blank=True, null=True, default='')
    position_funding = models.CharField(max_length=255, blank=True, null=True, default='')
    community_identity = models.ForeignKey(TzcldCommunityIdentity, on_delete=models.CASCADE,related_name='territories_project_team_memebers', blank=True, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.community_identity.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Project Team Memeber')
        verbose_name_plural = _("TZCLD Territories Project Team Memebers")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'view', 'add', 'change']
        superuser_perms = ['inherit', 'view', 'add', 'change']
        container_path = "tzcld-territories-project-team-memeber/"
        serializer_fields = ['@id', 'firstname', 'name', 'etp', 'position_funding', 'community_identity']
        nested_fields = ['community_identity']
        rdf_type = "tzcld:territoryProjectTeamMemeber"

class TzcldTerritoryTraining(Model):
    training_course = models.ForeignKey(TzcldTerritoriesTrainingCourse, on_delete=models.DO_NOTHING,related_name='territory_training_course', blank=True, null=True)
    training_promotoion = models.ForeignKey(TzcldTerritoriesTrainingPromotoion, on_delete=models.DO_NOTHING,related_name='territory_training_promotion', blank=True, null=True)
    training_person = models.CharField(max_length=255, blank=True, null=True, default='')
    training_profile = models.ForeignKey(TzcldTerritoriesTrainingProfile, on_delete=models.DO_NOTHING,related_name='territory_training_profile', blank=True, null=True)
    community_identity = models.ForeignKey(TzcldCommunityIdentity, on_delete=models.CASCADE,related_name='territories_trainings', blank=True, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.community_identity.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Training')
        verbose_name_plural = _("TZCLD Territories Trainings")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'view', 'add', 'change']
        superuser_perms = ['inherit', 'view', 'add', 'change']
        container_path = "tzcld-territories-training/"
        serializer_fields = ['@id', 'training_course', 'training_promotoion', 'training_person', 'training_profile', 'community_identity']
        nested_fields = ['community_identity']
        rdf_type = "tzcld:territoryTraining"

class TzcldTerritoryTeamTraining(Model):
    training_course = models.ForeignKey(TzcldTerritoriesTrainingCourse, on_delete=models.DO_NOTHING,related_name='territory_team_training_course', blank=True, null=True)
    training_promotoion = models.ForeignKey(TzcldTerritoriesTrainingPromotoion, on_delete=models.DO_NOTHING,related_name='territory_team_training_promotion', blank=True, null=True)
    training_person = models.CharField(max_length=255, blank=True, null=True, default='')
    community_identity = models.ForeignKey(TzcldCommunityIdentity, on_delete=models.CASCADE,related_name='territories_team_trainings', blank=True, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.community_identity.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Team Training')
        verbose_name_plural = _("TZCLD Territories Team Trainings")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'view', 'add', 'change']
        superuser_perms = ['inherit', 'view', 'add', 'change']
        container_path = "tzcld-territories-team-training/"
        serializer_fields = ['@id', 'training_course', 'training_promotoion', 'training_person', 'training_profile', 'community_identity']
        nested_fields = ['community_identity']
        rdf_type = "tzcld:territoryTeamTraining"


class TzcldCommunityDeliberation(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory deliberation')
        verbose_name_plural = _("TZCLD Territories deliberations")
        anonymous_perms = ['view']
        container_path = "tzcld-communities-deliberations/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:communityDeliberation"

class TzcldOtherCommunityDeliberation(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Other Territory deliberation')
        verbose_name_plural = _("TZCLD Other Community deliberations")
        anonymous_perms = ['view']
        container_path = "tzcld-others-communities-deliberations/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:otherCommunityDeliberation"


class TzcldCouncilDepartmentDeliberation(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Council department deliberation')
        verbose_name_plural = _("TZCLD Council department deliberations")
        anonymous_perms = ['view']
        container_path = "tzcld-councils-departments-deliberations/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:councilDepartmentDeliberation"

class TzcldCommunityEvaluationPointPart(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    title = models.CharField(max_length=254, blank=True, null=True, default='')
    subtitle = models.CharField(max_length=254, blank=True, null=True, default='')
    order = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Evaluation Point Part')
        verbose_name_plural = _("TZCLD Territories Evaluation Point Parts")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        container_path = "tzcld-evaluation-point-parts/"
        serializer_fields = ['@id', 'name', 'title', 'subtitle', 'order', 'part_points']
        ordering = ['order']
        nested_fields = []
        rdf_type = "tzcld:evaluationPointPart"
        depth = 0

class TzcldCommunityEvaluationPoint(Model):

    TYPE_FALSE = 'checkboxe'
    TYPE_DELIBERATION = 'tzcld-communities-deliberations'
    TYPE_OTHER_DELIBERATION = 'tzcld-others-communities-deliberations'
    TYPE_CONCILS_DELIBERATION = 'tzcld-councils-departments-deliberations'
    TYPE_OF_FIELD_CHOICES = [
        (TYPE_FALSE, 'Checkboxe'),
        (TYPE_DELIBERATION, 'TZCLD Territory deliberation'),
        (TYPE_OTHER_DELIBERATION, 'TZCLD Other Territory deliberation'),
        (TYPE_CONCILS_DELIBERATION, 'TZCLD Council department deliberation'),
    ]

    name = models.CharField(max_length=1024, blank=True, null=True, default='')
    order = models.IntegerField(blank=True, null=True, default=1)
    part = models.ForeignKey(TzcldCommunityEvaluationPointPart, on_delete=models.DO_NOTHING,related_name='part_points', blank=True, null=True)
    points = models.IntegerField(blank=True, null=True, default=0)
    fieldType = models.CharField(
        max_length=25,
        choices=TYPE_OF_FIELD_CHOICES,
        default=TYPE_FALSE,
    )

    def __str__(self):
        try:
            return '{} ({})'.format(self.id, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Evaluation Point')
        verbose_name_plural = _("TZCLD Territories Evaluation Points")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        ordering = ['order']
        container_path = "tzcld-communities-evaluation-points/"
        serializer_fields = ['@id', 'name', 'order', 'part', 'points']
        rdf_type = "tzcld:communityEvaluationPoint"
        depth = 0


class TzcldCommunityEvaluationPointAnswer(Model):

    answer = answer = models.BooleanField(default=False)
    answer_option = models.CharField(max_length=1024, blank=True, null=True, default='')
    comment = models.TextField(blank=True, null=True)
    evaluation_point = models.ForeignKey(TzcldCommunityEvaluationPoint, on_delete=models.DO_NOTHING,related_name='evaluation_point_answer', blank=False, null=True)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING,related_name='community_answer', blank=False, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.id, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Evaluation Point Answer')
        verbose_name_plural = _("TZCLD Territories Evaluation Point answers")
        permission_classes = [TzcldCommunityProfilePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        container_path = "tzcld-communities-evaluation-point-answers/"
        serializer_fields = ['@id', 'answer', 'answer_option', 'comment', 'evaluation_point', 'community']
        rdf_type = "tzcld:communityEvaluationPointAnswer"
        depth = 0
		
		
#############################
# Shared models for user and community
#############################

class TzcldContactPhone(Model):
    phone = models.CharField(max_length=255, blank=True, null=True, default='')
    phone_type = models.CharField(max_length=255, blank=True, null=True, default='')
    phone_public = models.BooleanField(default=False)
    job = models.ForeignKey(TzcldProfileJob, on_delete=models.CASCADE, related_name='phones', blank=True, null=True)
    location = models.ForeignKey(TzcldTerritoryLocation, on_delete=models.CASCADE, related_name='phones', blank=True, null=True)


    def __str__(self):
        try:
            return '{} ({})'.format(self.position, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Phone')
        verbose_name_plural = _("TZCLD Phones")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-contact-phone/"
        serializer_fields = ['@id', 'phone', 'phone_type', 'phone_public', 'job', 'location']
        nested_fields = []
        rdf_type = "tzcld:phone"

class TzcldContactEmail(Model):
    email = models.CharField(max_length=255, blank=True, null=True, default='')
    email_type = models.CharField(max_length=255, blank=True, null=True, default='')
    email_public = models.BooleanField(default=False)
    job = models.ForeignKey(TzcldProfileJob, on_delete=models.CASCADE,related_name='emails', blank=True, null=True)
    location = models.ForeignKey(TzcldTerritoryLocation, on_delete=models.CASCADE,related_name='emails', blank=True, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.position, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Email')
        verbose_name_plural = _("TZCLD Emails")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-contact-email/"
        serializer_fields = ['@id', 'email', 'email_type', 'email_public', 'job', 'location']
        nested_fields = []
        rdf_type = "tzcld:email"


class TzcldContactMember(Model):
    member = models.OneToOneField(CommunityMember, on_delete=models.CASCADE, related_name="tzcld_contact_member")
    tzcldCommunity = models.ForeignKey(TzcldCommunity, on_delete=models.CASCADE, related_name='tzcld_community_contacts', null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Contact Member')
        verbose_name_plural = _("TZCLD Territories Contact Members")
        anonymous_perms = ['view']
        authenticated_perms = ['view']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-contact-member/"
        serializer_fields = ['@id', 'member', 'is_primary']
        nested_fields = []
        rdf_type = "tzcld:contactMember"



class TzcldSharedNote(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    longdesc = models.TextField(blank=True, null=True)
    tzcldCommunity = models.ForeignKey(TzcldCommunity, on_delete=models.CASCADE, related_name='tzcld_community_shared_notes', null=True, blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.id, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Shared Note')
        verbose_name_plural = _("TZCLD Shared Notes")
        anonymous_perms = ['view']
        authenticated_perms = ['view']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-shared-note/"
        serializer_fields = ['@id', 'user', 'longdesc', 'tzcldCommunity']
        nested_fields = []
        rdf_type = "tzcld:sharedNote"

class TzcldSharedNoteComment(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    comment = models.TextField(blank=True, null=True)
    tzcldSharedNote = models.ForeignKey(TzcldSharedNote, on_delete=models.CASCADE, related_name='tzcld_shared_note_comments', null=True, blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.id, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Shared Note Comment')
        verbose_name_plural = _("TZCLD Shared Notes Comments")
        anonymous_perms = ['view']
        authenticated_perms = ['view']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-shared-note-comment/"
        serializer_fields = ['@id', 'user', 'comment', 'tzcldSharedNote']
        nested_fields = []
        rdf_type = "tzcld:sharedNoteComment"

class TzcldTerritoryRequest(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,verbose_name="Interlocuteur")
    date =  models.DateField(verbose_name="Date")
    contactType = models.CharField(max_length=1024, blank=True, null=True, default='',verbose_name="Type of contact")
    subject = models.CharField(max_length=1024, blank=True, null=True, default='',verbose_name="Sujet/Demande")
    comment = models.CharField(max_length=1024, blank=True, null=True, default='',verbose_name="Comments")
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING,related_name='community_requests', blank=False, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.id, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Request')
        verbose_name_plural = _("TZCLD Territories Requests")
        anonymous_perms = ['view']
        authenticated_perms = ['view']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-territory-request/"
        serializer_fields = ['@id', 'user', 'date', 'contactType', 'subject', 'comment', 'community']
        nested_fields = []
        rdf_type = "tzcld:territoryRequest"


class TzcldFollowedTrainingB (Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Followed Training B')
        verbose_name_plural = _("TZCLD Followed Trainings B")
        anonymous_perms = ['view']
        container_path = "tzcld-followed-training-b/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:followed-training-b"

class TzcldFollowedTrainingD (Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Followed Training D')
        verbose_name_plural = _("TZCLD Followed Trainings D")
        anonymous_perms = ['view']
        container_path = "tzcld-followed-training-d/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:followed-training-d"


class TzcldTerritorySynthesisFollowed(Model):
    
    context = models.TextField(blank=True, null=True, verbose_name="Context")
    strongPoints = models.TextField(blank=True, null=True, verbose_name="Strong Points")
    questions = models.TextField(blank=True, null=True, verbose_name="Questions")
    needs = models.TextField(blank=True, null=True, verbose_name="Needs, Actions")
    targetdate =  models.DateField(verbose_name="Target date")
    followedTrainingB = models.ForeignKey(TzcldFollowedTrainingB, on_delete=models.DO_NOTHING,related_name='territory_followed_training_b', blank=True, null=True)
    followedTrainingBNumber = models.CharField(max_length=1024, blank=True, null=True, default='',verbose_name="Type of contact")
    followedTrainingD = models.ForeignKey(TzcldFollowedTrainingD, on_delete=models.DO_NOTHING,related_name='territory_followed_training_b', blank=True, null=True)
    followedTrainingDNumber = models.CharField(max_length=1024, blank=True, null=True, default='',verbose_name="Type of contact")
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING,related_name='community_synthesis_followed', blank=False, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.id, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Synthesis Followed')
        verbose_name_plural = _("TZCLD Territories Synthesis Followed")
        anonymous_perms = ['view']
        authenticated_perms = ['view']
        superuser_perms = ['inherit', 'change']
        container_path = "tzcld-territory-synthesis followed/"
        serializer_fields = ['@id', 'context', 'strongPoints', 'questions', 'needs', 'targetdate', 'followedTrainingB', 'followedTrainingBNumber', 'followedTrainingD', 'followedTrainingDNumber', 'community']
        nested_fields = []
        rdf_type = "tzcld:territorySynthesisFollowed"


class TzcldCommunityFollowedPointPart(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    title = models.CharField(max_length=254, blank=True, null=True, default='')
    order = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Followed Point Part')
        verbose_name_plural = _("TZCLD Territories Followed Point Parts")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        container_path = "tzcld-followed-point-parts/"
        serializer_fields = ['@id', 'name', 'title', 'order', 'followed_part_points']
        ordering = ['order']
        nested_fields = []
        rdf_type = "tzcld:followedPointPart"
        depth = 0

class TzcldCommunityFollowedPoint(Model):

    TYPE_TEXT = 'text'
    TYPE_TEXTAREA = 'textarea'
    TYPE_OF_FIELD_CHOICES = [
        (TYPE_TEXT, 'Text'),
        (TYPE_TEXTAREA, 'Textearea'),
    ]

    name = models.CharField(max_length=1024, blank=True, null=True, default='')
    order = models.IntegerField(blank=True, null=True, default=1)
    part = models.ForeignKey(TzcldCommunityFollowedPointPart, on_delete=models.DO_NOTHING,related_name='followed_part_points', blank=True, null=True)
    fieldType = models.CharField(
        max_length=25,
        choices=TYPE_OF_FIELD_CHOICES,
        default=TYPE_TEXTAREA,
    )
    helpComment = models.TextField(blank=True, null=True, verbose_name="Questions to ask")

    def __str__(self):
        try:
            return '{} ({})'.format(self.id, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Followed Point')
        verbose_name_plural = _("TZCLD Territories Followed Points")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        ordering = ['order']
        container_path = "tzcld-communities-followed-points/"
        serializer_fields = ['@id', 'name', 'order', 'part', 'fieldType', 'helpComment']
        rdf_type = "tzcld:communityFollowedPoint"
        depth = 0


class TzcldCommunityFollowedPointAnswer(Model):

    answer = answer = models.BooleanField(default=False)
    followed_point = models.ForeignKey(TzcldCommunityFollowedPoint, on_delete=models.DO_NOTHING,related_name='followed_point_answer', blank=False, null=True)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING,related_name='community_followed_answer', blank=False, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.id, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Followed Point Answer')
        verbose_name_plural = _("TZCLD Territories Followed Point answers")
        permission_classes = [TzcldCommunityProfilePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        container_path = "tzcld-communities-followed-point-answers/"
        serializer_fields = ['@id', 'answer', 'followed_point','community']
        rdf_type = "tzcld:communityFollowedPointAnswer"
        depth = 0


#############################
# DjangoLDP Community Extension
#############################



# Create tzcld user profile, job instance and contact email/phone when user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_tzcld_profile(sender, instance, created, **kwargs):
    if not Model.is_external(instance) and created:
        tzcld_profile = TzcldProfile.objects.create(user=instance)
        profile_job = TzcldProfileJob.objects.create(profile=tzcld_profile)
        TzcldContactEmail.objects.create(job=profile_job)
        TzcldContactPhone.objects.create(job=profile_job)

        # add the user to the first (tzcld) community
        community = Community.objects.order_by('id').first()
        if community:
            community.members.create(user=instance)

# Create tzcld community profile, job instance and contact email/phone when community is created
@receiver(post_save, sender=Community)
def create_tzcld_community(instance, created, **kwargs):
    if not Model.is_external(instance) and created:
        tzCommunity = TzcldCommunity.objects.create(community=instance)
        territory_location = TzcldTerritoryLocation.objects.create(name="Adresse à renseigner", community=tzCommunity)
        TzcldContactEmail.objects.create(email="brad@example.com", location=territory_location)
        TzcldContactPhone.objects.create(phone="0606060606", location=territory_location)

