from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


from django_filters import rest_framework as filters

from core.models import (
    Case,
    Appropriation,
    Activity,
    PaymentSchedule,
    Payment,
    Municipality,
    RelatedPerson,
    SchoolDistrict,
    Team,
    Section,
    ActivityCatalog,
    Account,
    ServiceProvider,
    ApprovalLevel,
)

from core.serializers import (
    CaseSerializer,
    AppropriationSerializer,
    ActivitySerializer,
    PaymentScheduleSerializer,
    PaymentSerializer,
    RelatedPersonSerializer,
    MunicipalitySerializer,
    SchoolDistrictSerializer,
    TeamSerializer,
    SectionSerializer,
    ActivityCatalogSerializer,
    AccountSerializer,
    UserSerializer,
    HistoricalCaseSerializer,
    ServiceProviderSerializer,
    ApprovalLevelSerializer,
)

from core.utils import get_person_info

# Working models, read/write


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def perform_create(self, serializer):
        current_user = self.request.user
        team = current_user.team
        serializer.save(case_worker=current_user, team=team)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        """
        Fetch history of HistoricalCases.
        """
        case = self.get_object()
        serializer = HistoricalCaseSerializer(case.history.all(), many=True)
        return Response(serializer.data)


class AppropriationViewSet(viewsets.ModelViewSet):
    queryset = Appropriation.objects.all()
    serializer_class = AppropriationSerializer

    filterset_fields = "__all__"


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    filterset_fields = "__all__"


class PaymentScheduleViewSet(viewsets.ModelViewSet):
    queryset = PaymentSchedule.objects.all()
    serializer_class = PaymentScheduleSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class RelatedPersonViewSet(viewsets.ModelViewSet):
    queryset = RelatedPerson.objects.all()
    serializer_class = RelatedPersonSerializer

    filterset_fields = "__all__"

    @action(detail=False, methods=["get"])
    def fetch_from_serviceplatformen(self, request):
        """
        Fetch relations for a person using the CPR from Serviceplatformen.

        Returns the data as serialized RelatedPersons data.
        """
        cpr = request.query_params.get("cpr")
        if not cpr:
            return Response(
                {"errors": _("Intet CPR nummer angivet")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cpr_data = get_person_info(cpr)

        if not cpr_data:
            return Response(
                {
                    "errors": [
                        _("Fejl i CPR eller forbindelse til Serviceplatformen")
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        relations = []
        for relation in cpr_data["relationer"]:
            relations.append(
                RelatedPerson.serviceplatformen_to_related_person(relation)
            )

        return Response(relations, status.HTTP_200_OK)


# Master data, read only.


class MunicipalityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer


class SchoolDistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolDistrict.objects.all()
    serializer_class = SchoolDistrictSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class AllowedForStepsFilter(filters.FilterSet):
    allowed_for_steps = CharInFilter(
        field_name="allowed_for_steps", lookup_expr="contains"
    )

    class Meta:
        model = Section
        fields = "__all__"


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filterset_class = AllowedForStepsFilter


class ActivityCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityCatalog.objects.all()
    serializer_class = ActivityCatalogSerializer
    filterset_fields = "__all__"


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ServiceProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer


class ApprovalLevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApprovalLevel.objects.all()
    serializer_class = ApprovalLevelSerializer
