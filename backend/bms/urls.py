from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, ResidentViewSet, ClassificationViewSet, ResidentIDSequenceViewSet,
    ResidentIDIssuanceViewSet, BarangayOfficialViewSet, AnnouncementViewSet, ProgramViewSet,
    RequestViewSet, CertificateIssuanceViewSet, TaskViewSet, TaskAssignmentViewSet, TaskUpdateViewSet,
    StaffAssignmentHistoryViewSet, ConversationViewSet, MessageViewSet, MessageRecipientViewSet,
    NotificationViewSet, GalleryItemViewSet, ActivityLogViewSet, SystemSettingViewSet,
    public_site, dashboard_stats)
from django.urls import path

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("residents", ResidentViewSet)
router.register("classifications", ClassificationViewSet)
router.register("id-sequences", ResidentIDSequenceViewSet)
router.register("id-issuances", ResidentIDIssuanceViewSet)
router.register("officials", BarangayOfficialViewSet)
router.register("announcements", AnnouncementViewSet)
router.register("programs", ProgramViewSet)
router.register("requests", RequestViewSet)
router.register("certificates", CertificateIssuanceViewSet)
router.register("tasks", TaskViewSet)
router.register("task-assignments", TaskAssignmentViewSet)
router.register("task-updates", TaskUpdateViewSet)
router.register("staff-history", StaffAssignmentHistoryViewSet)
router.register("conversations", ConversationViewSet)
router.register("messages", MessageViewSet)
router.register("message-recipients", MessageRecipientViewSet)
router.register("notifications", NotificationViewSet)
router.register("gallery", GalleryItemViewSet)
router.register("activity-logs", ActivityLogViewSet)
router.register("settings", SystemSettingViewSet)

urlpatterns = [
    path("public-site/", public_site, name="public-site"),
    path("dashboard-stats/", dashboard_stats, name="dashboard-stats"),
] + router.urls
