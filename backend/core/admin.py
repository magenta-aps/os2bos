# Copyright (C) 2019 Magenta ApS, http://magenta.dk.
# Contact: info@magenta.dk.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Customize django-admin interface."""


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.html import escape, mark_safe, format_html_join
from django.urls import reverse
from django import forms

from django_audit_fields.admin import ModelAdminAuditFieldsMixin

from core.models import (
    Municipality,
    PaymentSchedule,
    Payment,
    Case,
    Appropriation,
    Activity,
    RelatedPerson,
    SchoolDistrict,
    Section,
    ActivityDetails,
    Account,
    ServiceProvider,
    PaymentMethodDetails,
    Team,
    ApprovalLevel,
    SectionInfo,
    EffortStep,
    TargetGroup,
    Effort,
    Rate,
)

for klass in (
    PaymentMethodDetails,
    Team,
    SectionInfo,
    Rate,
):
    admin.site.register(klass, admin.ModelAdmin)


User = get_user_model()


class ClassificationInline(admin.TabularInline):
    """TabularInline for Classification inlines."""

    def has_view_permission(self, request, obj=None):
        """Override has_view_permission for InlineModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()

    def has_add_permission(self, request):
        """Override has_add_permission for InlineModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()

    def has_change_permission(self, request, obj=None):
        """Override has_change_permission for InlineModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()

    def has_delete_permission(self, request, obj=None):
        """Override has_delete_permission for InlineModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()


class ClassificationAdmin(admin.ModelAdmin):
    """ModelAdmin for Classification models."""

    def has_view_permission(self, request, obj=None):
        """Override has_view_permission for ModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()

    def has_add_permission(self, request):
        """Override has_add_permission for ModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()

    def has_change_permission(self, request, obj=None):
        """Override has_change_permission for ModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()

    def has_delete_permission(self, request, obj=None):
        """Override has_delete_permission for ModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()

    def has_module_permission(self, request):
        """Override has_model_permission for ModelAdmin."""
        user = request.user
        return user.is_authenticated and user.is_workflow_engine_or_admin()


@admin.register(Case)
class CaseAdmin(ModelAdminAuditFieldsMixin, admin.ModelAdmin):
    """ModelAdmin for Case."""

    pass


@admin.register(Appropriation)
class AppropriationAdmin(ModelAdminAuditFieldsMixin, admin.ModelAdmin):
    """ModelAdmin for Appropriation."""

    pass


@admin.register(Activity)
class ActivityAdmin(ModelAdminAuditFieldsMixin, admin.ModelAdmin):
    """ModelAdmin for Activity."""

    readonly_fields = ("account_number",)

    def account_number(self, obj):
        """Get account number."""
        return obj.account_number

    account_number.short_description = _("kontonummer")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Dislay read only fields on payment."""

    readonly_fields = ("payment_id", "account_string", "account_string_new")
    search_fields = ("payment_schedule__payment_id",)

    list_display = (
        "id",
        "payment_id",
        "account_string",
        "date",
        "paid",
        "paid_date",
        "payment_schedule_str",
    )
    list_filter = (
        "paid",
        "payment_schedule__fictive",
        "date",
        "paid_date",
        "payment_method",
        "recipient_type",
    )

    def payment_schedule_str(self, obj):
        """Get related payment schedule link."""
        link = reverse(
            "admin:core_paymentschedule_change", args=[obj.payment_schedule.id]
        )
        return mark_safe(
            f'<a href="{link}">{escape(obj.payment_schedule.__str__())}</a>'
        )

    def payment_id(self, obj):
        """Get payment ID from payment plan."""
        return obj.payment_schedule.payment_id

    def account_string(self, obj):
        """Get account string."""
        return obj.account_string

    def account_string_new(self, obj):
        """Get new account string."""
        return obj.account_string_new

    payment_id.short_description = _("betalings-ID")
    account_string.short_description = _("kontostreng")
    account_string_new.short_description = _("ny kontostreng")
    payment_schedule_str.short_description = _("betalingsplan")


class TargetGroupForm(forms.ModelForm):
    """Form for TargetGroup to set required_fields_for_case."""

    def __init__(self, *args, **kwargs):
        """__init__ for TargetGroupForm.

        Set initial value for required_fields_for_case.
        """
        super(TargetGroupForm, self).__init__(*args, **kwargs)
        # Set initial value as a list
        self.initial[
            "required_fields_for_case"
        ] = self.instance.required_fields_for_case

    def required_fields_for_case_choices():
        """Define the choices for the required_fields_for_case field."""
        excluded_fields = ["revision"]

        choices = [
            (field.name, field.verbose_name)
            for field in Case._meta.get_fields()
            if field.null
            and hasattr(field, "verbose_name")
            and field.name not in excluded_fields
        ]
        return choices

    required_fields_for_case = forms.MultipleChoiceField(
        choices=required_fields_for_case_choices(),
        label=_("Påkrævede felter på sag"),
        required=False,
    )


@admin.register(TargetGroup)
class TargetGroupAdmin(ClassificationAdmin):
    """ModelAdmin for TargetGroup with custom ModelForm."""

    fields = ("name", "required_fields_for_case", "active")
    list_display = (
        "name",
        "active",
    )
    form = TargetGroupForm


@admin.register(Effort)
class EffortAdmin(ClassificationAdmin):
    """ModelAdmin for Effort."""

    filter_horizontal = ("allowed_for_target_groups",)

    list_display = (
        "name",
        "active",
    )


@admin.register(PaymentSchedule)
class PaymentScheduleAdmin(admin.ModelAdmin):
    """Display read only fields on payment schedule."""

    readonly_fields = ("payment_id", "account_string", "account_string_new")
    search_fields = ("payment_id",)
    list_display = (
        "id",
        "payment_id",
        "recipient_type",
        "recipient_id",
        "recipient_name",
        "payment_frequency",
        "payment_method",
        "payment_type",
        "payment_amount",
        "account_string",
        "fictive",
    )
    list_filter = (
        "payment_method",
        "payment_type",
        "payment_frequency",
        "fictive",
    )

    def account_string(self, obj):
        """Get account string."""
        return obj.account_string

    def account_string_new(self, obj):
        """Get new account string."""
        return obj.account_string_new

    account_string.short_description = _("kontostreng")
    account_string_new.short_description = _("ny kontostreng")


@admin.register(Account)
class AccountAdmin(ClassificationAdmin):
    """Display account number (konteringsnummer) as read only field."""

    readonly_fields = ("number",)
    list_display = (
        "main_account_number",
        "active",
    )

    def number(self, obj):
        """Get account number."""
        return obj.number

    number.short_description = _("konteringsnummer")


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Add team to user admin interface."""

    fieldsets = (
        ("Organisation", {"fields": ("team",)}),
    ) + BaseUserAdmin.fieldsets


@admin.register(ActivityDetails)
class ActivityDetailsAdmin(ClassificationAdmin):
    """Widgets: Filter_horizontal for many to many links, add search field."""

    filter_horizontal = (
        "main_activity_for",
        "supplementary_activity_for",
        "service_providers",
        "main_activities",
    )
    search_fields = ("activity_id", "name")
    list_display = (
        "name",
        "activity_id",
        "active",
    )


class MainActivityDetailsInline(ClassificationInline):
    """MainActivityDetailsInline for SectionAdmin."""

    model = ActivityDetails.main_activity_for.through
    extra = 0
    verbose_name = _("Tilladt hovedydelse")
    verbose_name_plural = _("Tilladte hovedydelser")
    ordering = ("activity_details__name",)


class SupplementaryActivityDetailsInline(ClassificationInline):
    """SupplementaryActivityDetailsInline for SectionAdmin."""

    model = ActivityDetails.supplementary_activity_for.through
    extra = 0
    verbose_name = _("Tilladt følgeudgift")
    verbose_name_plural = _("Tilladte følgeudgifter")
    ordering = ("activitydetails__name",)


@admin.register(Section)
class SectionAdmin(ClassificationAdmin):
    """Add search field."""

    search_fields = ("paragraph", "text")

    list_display = (
        "paragraph",
        "text",
        "list_main_activity_for",
        "list_supplementary_activity_for",
        "active",
    )
    filter_horizontal = ("allowed_for_target_groups", "allowed_for_steps")

    inlines = (
        MainActivityDetailsInline,
        SupplementaryActivityDetailsInline,
    )

    def list_main_activity_for(self, obj):
        """HTML list of main activities for Django admin purposes."""
        return format_html_join(
            "\n",
            '<div><a href="{}">{}</a></div>',
            (
                (reverse("admin:core_activitydetails_change", args=[x.id]), x,)
                for x in obj.main_activities.all()
            ),
        )

    def list_supplementary_activity_for(self, obj):
        """HTML list of supplementary activities for Django admin purposes."""
        return format_html_join(
            "\n",
            '<div><a href="{}">{}</a></div>',
            (
                [
                    (
                        reverse(
                            "admin:core_activitydetails_change", args=[x.id]
                        ),
                        x,
                    )
                    for x in obj.supplementary_activities.all()
                ]
            ),
        )

    list_main_activity_for.short_description = _("Tilladte hovedydelser")
    list_supplementary_activity_for.short_description = _(
        "Tilladte følgeudgifter"
    )


@admin.register(ServiceProvider)
class ServiceProviderAdmin(ClassificationAdmin):
    """Add search fields."""

    search_fields = ("name", "cvr_number")

    list_display = (
        "name",
        "active",
    )


@admin.register(RelatedPerson)
class RelatedPersonAdmin(ModelAdminAuditFieldsMixin, admin.ModelAdmin):
    """ModelAdmin for RelatedPerson."""

    pass


@admin.register(Municipality)
class MunicipalityAdmin(ClassificationAdmin):
    """ModelAdmin for Municipality."""

    search_fields = ("name",)
    list_display = (
        "name",
        "active",
    )


@admin.register(ApprovalLevel)
class ApprovalLevelAdmin(ClassificationAdmin):
    """ModelAdmin for ApprovalLevel."""

    list_display = (
        "name",
        "active",
    )


class SectionInline(ClassificationInline):
    """SectionInline for EffortStepAdmin."""

    model = EffortStep.sections.through
    extra = 0
    verbose_name = _("Trin tilladt for paragraf")
    verbose_name_plural = _("Trin tilladt for paragraffer")


@admin.register(EffortStep)
class EffortStepAdmin(ClassificationAdmin):
    """ModelAdmin for EffortStep."""

    search_fields = (
        "name",
        "number",
    )
    list_display = (
        "name",
        "list_sections",
        "active",
    )

    inlines = (SectionInline,)

    def list_sections(self, obj):
        """HTML list of sections for Django admin purposes."""
        return format_html_join(
            "\n",
            '<div><a href="{}">{} - {}</a></div>',
            (
                (
                    reverse("admin:core_section_change", args=[x.id]),
                    x.paragraph,
                    x.text,
                )
                for x in obj.sections.all()
            ),
        )

    list_sections.short_description = _("Tilladte paragraffer")


@admin.register(SchoolDistrict)
class SchoolDistrictAdmin(ClassificationAdmin):
    """ModelAdmin for SchoolDistrict."""

    list_display = (
        "name",
        "active",
    )
