from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = [("admin", "Admin"), ("punong_barangay", "Punong Barangay"),
         ("staff", "Staff"), ("resident", "Resident")]
ACCOUNT_STATUS = [("pending", "Pending"), ("verified", "Verified"), ("active", "Active"),
                  ("disabled", "Disabled"), ("rejected", "Rejected"),
                  ("suspended", "Suspended"), ("archived", "Archived")]
RESIDENT_STATUS = [("PENDING", "Pending"), ("ACTIVE", "Active"),
                   ("SUSPENDED", "Suspended"), ("ARCHIVED", "Archived")]
CLASSIFICATIONS = [("Unclassified", "Unclassified"), ("Regular Resident", "Regular Resident"),
                   ("Senior Citizen", "Senior Citizen"), ("PWD", "PWD"),
                   ("Solo Parent", "Solo Parent"), ("Student", "Student")]
ID_STATUS = [("Assigned", "Assigned"), ("Ready for Issuance", "Ready for Issuance"),
             ("Issued", "Issued"), ("Released", "Released"), ("Lost", "Lost"),
             ("Replaced", "Replaced"), ("Cancelled", "Cancelled")]
ARCHIVE_STATUS = [("ACTIVE", "Active"), ("ARCHIVED", "Archived")]
PROGRAM_STATUS = [("Scheduled", "Scheduled"), ("Ongoing", "Ongoing"), ("Completed", "Completed"),
                  ("Cancelled", "Cancelled"), ("Archived", "Archived")]
TASK_STATUS = [("assigned", "Assigned"), ("acknowledged", "Acknowledged"),
               ("in_progress", "In Progress"), ("on_hold", "On Hold"),
               ("completed", "Completed"), ("cancelled", "Cancelled")]
ASSIGN_STATUS = [("PENDING", "Pending"), ("ACKNOWLEDGED", "Acknowledged"),
                 ("IN_PROGRESS", "In Progress"), ("ON_HOLD", "On Hold"),
                 ("COMPLETED", "Completed"), ("CANCELLED", "Cancelled"), ("OVERDUE", "Overdue")]
UPDATE_TYPE = [("progress", "Progress"), ("clarification_request", "Clarification Request"),
               ("clarification_response", "Clarification Response"), ("hold", "Hold"),
               ("acknowledge", "Acknowledge"), ("complete", "Complete"), ("note", "Note")]
CONVO_TYPE = [("direct", "Direct"), ("group", "Group"), ("announcement", "Announcement")]
MSG_TYPE = [("NORMAL", "Normal"), ("IMPORTANT", "Important"), ("URGENT", "Urgent"),
            ("TASK", "Task"), ("ANNOUNCEMENT", "Announcement")]
PRIORITY = [("LOW", "Low"), ("NORMAL", "Normal"), ("HIGH", "High"), ("URGENT", "Urgent")]


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLES, default="resident")
    name = models.CharField(max_length=150, blank=True)
    account_status = models.CharField(max_length=15, choices=ACCOUNT_STATUS, default="active")
    email_verified_at = models.DateTimeField(null=True, blank=True)
    google_verified = models.BooleanField(default=False)
    google_subject_id = models.CharField(max_length=100, blank=True)
    google_email = models.EmailField(blank=True)
    google_verified_at = models.DateTimeField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    profile_image = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    resident_record = models.ForeignKey("Resident", on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="linked_users")
    handler = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="handled_users")
    handler_assigned_at = models.DateTimeField(null=True, blank=True)
    handler_assigned_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                                            related_name="+")
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    archive_reason = models.TextField(blank=True)
    created_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    updated_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    old_password_hash = models.CharField(max_length=255, blank=True)  # from old BMS; force reset on first login

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.get_full_name() or self.username
        super().save(*args, **kwargs)


class Resident(models.Model):
    resident_id = models.CharField(max_length=50, unique=True)
    household_no = models.CharField(max_length=50)
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True, null=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    civil_status = models.CharField(max_length=20)
    address = models.TextField()
    contact = models.CharField(max_length=50)
    voter = models.CharField(max_length=5, default="No")
    classification = models.CharField(max_length=30, choices=CLASSIFICATIONS, default="Unclassified")
    owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="owned_residents")
    archived_at = models.DateTimeField(null=True, blank=True)
    resident_status = models.CharField(max_length=10, choices=RESIDENT_STATUS, default="ACTIVE")
    profile_image = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [models.Index(fields=["resident_id"]), models.Index(fields=["last_name", "first_name"])]

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".replace("  ", " ").strip()
    def __str__(self):
        return f"{self.resident_id} — {self.full_name}"


class Classification(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="classifications")
    resident_id_text = models.CharField(max_length=50)
    full_name = models.CharField(max_length=150)
    classification = models.CharField(max_length=30, choices=CLASSIFICATIONS)
    class_code = models.CharField(max_length=30, blank=True, null=True)
    class_status = models.CharField(max_length=20, default="Active")
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResidentIDSequence(models.Model):
    sequence_year = models.IntegerField()
    prefix = models.CharField(max_length=20)
    next_number = models.IntegerField(default=1)
    class Meta:
        unique_together = ("sequence_year", "prefix")


class ResidentIDIssuance(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="id_issuances")
    resident_id_text = models.CharField(max_length=50)
    issuance_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=ID_STATUS, default="Assigned")
    issued_at = models.DateTimeField(null=True, blank=True)
    issued_by = models.CharField(max_length=150, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BarangayOfficial(models.Model):
    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=80)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=ARCHIVE_STATUS, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    def __str__(self): return f"{self.first_name} {self.last_name} — {self.position}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY, default="NORMAL", null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="announcements")
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["-created_at"]


class Program(models.Model):
    event_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    start_time = models.CharField(max_length=20, blank=True, null=True)
    end_time = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    organizer = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=15, choices=PROGRAM_STATUS, default="Scheduled")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="programs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["-event_date"]


class Request(models.Model):
    REQ_STATUS = [("pending", "Pending"), ("processing", "Processing"), ("approved", "Approved"),
                  ("completed", "Completed"), ("rejected", "Rejected"), ("cancelled", "Cancelled")]
    request_id = models.CharField(max_length=50, unique=True)
    owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="requests")
    resident = models.ForeignKey(Resident, on_delete=models.SET_NULL, null=True, blank=True, related_name="requests")
    type = models.CharField(max_length=100)
    purpose = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, choices=REQ_STATUS, default="pending")
    date_needed = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_requests")
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CertificateIssuance(models.Model):
    cert_no = models.CharField(max_length=50, unique=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="certificates")
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="issued_certs")
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    task_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    task_type = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY, default="NORMAL", null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default="assigned")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks_assigned")
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks_created")
    completion_date = models.DateTimeField(null=True, blank=True)
    completion_notes = models.TextField(blank=True, null=True)
    related_record = models.CharField(max_length=100, blank=True, null=True)
    progress_percent = models.IntegerField(default=0)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments")
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_assignments")
    status = models.CharField(max_length=15, choices=ASSIGN_STATUS, default="PENDING")
    assigned_at = models.DateTimeField()
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completion_notes = models.TextField(blank=True, null=True)
    class Meta: unique_together = ("task", "staff")


class TaskUpdate(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="updates")
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_updates")
    update_type = models.CharField(max_length=25, choices=UPDATE_TYPE, default="progress")
    update_text = models.TextField()
    progress_percent = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class StaffAssignmentHistory(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignment_history")
    previous_handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    new_handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    changed_at = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)


class Conversation(models.Model):
    conversation_key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=15, choices=CONVO_TYPE, default="direct")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    message_type = models.CharField(max_length=15, choices=MSG_TYPE, default="NORMAL")
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField()
    is_important = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MessageRecipient(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="recipients")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_recipients")
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    notification_type = models.CharField(max_length=50, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    related_id = models.CharField(max_length=50, blank=True, null=True)
    related_type = models.CharField(max_length=50, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]


class GalleryItem(models.Model):
    image_path = models.CharField(max_length=255)
    thumbnail_path = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=ARCHIVE_STATUS, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, blank=True)


class ActivityLog(models.Model):
    event_type = models.CharField(max_length=100)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="activity_logs")
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]


class SystemSetting(models.Model):
    setting_key = models.CharField(max_length=100, primary_key=True)
    setting_value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.setting_key
