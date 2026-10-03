from rest_framework import serializers
from .models import (User, Resident, Classification, ResidentIDSequence, ResidentIDIssuance,
    BarangayOfficial, Announcement, Program, Request, CertificateIssuance, Task,
    TaskAssignment, TaskUpdate, StaffAssignmentHistory, Conversation, Message,
    MessageRecipient, Notification, GalleryItem, ActivityLog, SystemSetting)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","name","role","email","account_status","position","department",
                  "contact_number","profile_image","resident_record","is_active","date_joined"]
        read_only_fields = ["id","date_joined"]

class ResidentSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model = Resident
        fields = "__all__"

class ClassificationSerializer(serializers.ModelSerializer):
    class Meta: model = Classification; fields = "__all__"
class ResidentIDSequenceSerializer(serializers.ModelSerializer):
    class Meta: model = ResidentIDSequence; fields = "__all__"
class ResidentIDIssuanceSerializer(serializers.ModelSerializer):
    class Meta: model = ResidentIDIssuance; fields = "__all__"
class BarangayOfficialSerializer(serializers.ModelSerializer):
    class Meta: model = BarangayOfficial; fields = "__all__"
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta: model = Announcement; fields = "__all__"
class ProgramSerializer(serializers.ModelSerializer):
    class Meta: model = Program; fields = "__all__"
class RequestSerializer(serializers.ModelSerializer):
    class Meta: model = Request; fields = "__all__"
class CertificateIssuanceSerializer(serializers.ModelSerializer):
    class Meta: model = CertificateIssuance; fields = "__all__"
class TaskSerializer(serializers.ModelSerializer):
    class Meta: model = Task; fields = "__all__"
class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta: model = TaskAssignment; fields = "__all__"
class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta: model = TaskUpdate; fields = "__all__"
class StaffAssignmentHistorySerializer(serializers.ModelSerializer):
    class Meta: model = StaffAssignmentHistory; fields = "__all__"
class ConversationSerializer(serializers.ModelSerializer):
    class Meta: model = Conversation; fields = "__all__"
class MessageSerializer(serializers.ModelSerializer):
    class Meta: model = Message; fields = "__all__"
class MessageRecipientSerializer(serializers.ModelSerializer):
    class Meta: model = MessageRecipient; fields = "__all__"
class NotificationSerializer(serializers.ModelSerializer):
    class Meta: model = Notification; fields = "__all__"
class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta: model = GalleryItem; fields = "__all__"
class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta: model = ActivityLog; fields = "__all__"
class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta: model = SystemSetting; fields = "__all__"
