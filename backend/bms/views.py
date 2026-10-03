from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import (User, Resident, Classification, ResidentIDSequence, ResidentIDIssuance,
    BarangayOfficial, Announcement, Program, Request, CertificateIssuance, Task,
    TaskAssignment, TaskUpdate, StaffAssignmentHistory, Conversation, Message,
    MessageRecipient, Notification, GalleryItem, ActivityLog, SystemSetting)
from .serializers import (UserSerializer, ResidentSerializer, ClassificationSerializer,
    ResidentIDSequenceSerializer, ResidentIDIssuanceSerializer, BarangayOfficialSerializer,
    AnnouncementSerializer, ProgramSerializer, RequestSerializer, CertificateIssuanceSerializer,
    TaskSerializer, TaskAssignmentSerializer, TaskUpdateSerializer, StaffAssignmentHistorySerializer,
    ConversationSerializer, MessageSerializer, MessageRecipientSerializer, NotificationSerializer,
    GalleryItemSerializer, ActivityLogSerializer, SystemSettingSerializer)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all(); serializer_class = UserSerializer
    search_fields = ["username","name","email","position","department"]
    filterset_fields = ["role","account_status","is_active"]

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all(); serializer_class = ResidentSerializer
    search_fields = ["resident_id","last_name","first_name","household_no","contact","address"]
    filterset_fields = ["classification","gender","civil_status","voter","resident_status"]

class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all(); serializer_class = ClassificationSerializer
class ResidentIDSequenceViewSet(viewsets.ModelViewSet):
    queryset = ResidentIDSequence.objects.all(); serializer_class = ResidentIDSequenceSerializer
class ResidentIDIssuanceViewSet(viewsets.ModelViewSet):
    queryset = ResidentIDIssuance.objects.all(); serializer_class = ResidentIDIssuanceSerializer
    filterset_fields = ["status","resident"]
class BarangayOfficialViewSet(viewsets.ModelViewSet):
    queryset = BarangayOfficial.objects.all(); serializer_class = BarangayOfficialSerializer
    filterset_fields = ["status","is_visible","position"]
class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all(); serializer_class = AnnouncementSerializer
    filterset_fields = ["category","priority"]
class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all(); serializer_class = ProgramSerializer
    filterset_fields = ["status"]
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all(); serializer_class = RequestSerializer
    search_fields = ["request_id","type","purpose"]
    filterset_fields = ["status","type","resident","owner_user"]
class CertificateIssuanceViewSet(viewsets.ModelViewSet):
    queryset = CertificateIssuance.objects.all(); serializer_class = CertificateIssuanceSerializer
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all(); serializer_class = TaskSerializer
    filterset_fields = ["status","priority","assigned_to","created_by"]
class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all(); serializer_class = TaskAssignmentSerializer
class TaskUpdateViewSet(viewsets.ModelViewSet):
    queryset = TaskUpdate.objects.all(); serializer_class = TaskUpdateSerializer
class StaffAssignmentHistoryViewSet(viewsets.ModelViewSet):
    queryset = StaffAssignmentHistory.objects.all(); serializer_class = StaffAssignmentHistorySerializer
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all(); serializer_class = ConversationSerializer
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all(); serializer_class = MessageSerializer
class MessageRecipientViewSet(viewsets.ModelViewSet):
    queryset = MessageRecipient.objects.all(); serializer_class = MessageRecipientSerializer
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all(); serializer_class = NotificationSerializer
    filterset_fields = ["is_read","user"]
class GalleryItemViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all(); serializer_class = GalleryItemSerializer
    filterset_fields = ["status","is_visible"]
class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all(); serializer_class = ActivityLogSerializer
class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset = SystemSetting.objects.all(); serializer_class = SystemSettingSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def public_site(request):
    """Aggregated payload for the public landing page (old BMS welcome hero + CMS)."""
    settings = {s.setting_key: s.setting_value for s in SystemSetting.objects.all()}
    return Response({
        "settings": settings,
        "officials": BarangayOfficialSerializer(
            BarangayOfficial.objects.filter(status="ACTIVE", is_visible=True).order_by("display_order"), many=True).data,
        "announcements": AnnouncementSerializer(
            Announcement.objects.filter(archived_at__isnull=True).order_by("-created_at")[:6], many=True).data,
        "programs": ProgramSerializer(
            Program.objects.filter(status__in=["Scheduled","Ongoing"]).order_by("event_date")[:6], many=True).data,
        "gallery": GalleryItemSerializer(
            GalleryItem.objects.filter(status="ACTIVE", is_visible=True).order_by("display_order")[:12], many=True).data,
    })

@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard_stats(request):
    return Response({
        "residents": Resident.objects.filter(resident_status="ACTIVE").count(),
        "households": Resident.objects.values("household_no").distinct().count(),
        "pending_requests": Request.objects.filter(status__in=["pending","processing"]).count(),
        "open_tasks": Task.objects.exclude(status__in=["completed","cancelled"]).count(),
        "unread_notifications": Notification.objects.filter(is_read=False).count(),
        "officials": BarangayOfficial.objects.filter(status="ACTIVE").count(),
        "programs_ongoing": Program.objects.filter(status="Ongoing").count(),
        "activity_logs": ActivityLog.objects.count(),
    })
