from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User, Resident, Classification, ResidentIDSequence, ResidentIDIssuance,
    BarangayOfficial, Announcement, Program, Request, CertificateIssuance, Task,
    TaskAssignment, TaskUpdate, StaffAssignmentHistory, Conversation, Message,
    MessageRecipient, Notification, GalleryItem, ActivityLog, SystemSetting)

@admin.register(User)
class BMSUserAdmin(UserAdmin):
    list_display = ("username","name","role","account_status","email","is_active")
    list_filter = ("role","account_status","is_active")
    search_fields = ("username","name","email")
    fieldsets = UserAdmin.fieldsets + (
        ("B.R.I.D.G.E Profile", {"fields": ("role","name","account_status","position","department",
            "contact_number","profile_image","resident_record","handler","google_subject_id","google_email")}),
    )

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ("resident_id","last_name","first_name","household_no","classification","resident_status","voter")
    list_filter = ("classification","gender","civil_status","voter","resident_status")
    search_fields = ("resident_id","last_name","first_name","household_no","contact")

admin.site.register(Classification)
admin.site.register(ResidentIDSequence)
admin.site.register(ResidentIDIssuance)
admin.site.register(BarangayOfficial)
admin.site.register(Announcement)
admin.site.register(Program)
admin.site.register(Request)
admin.site.register(CertificateIssuance)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(TaskUpdate)
admin.site.register(StaffAssignmentHistory)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(MessageRecipient)
admin.site.register(Notification)
admin.site.register(GalleryItem)
admin.site.register(ActivityLog)
admin.site.register(SystemSetting)
