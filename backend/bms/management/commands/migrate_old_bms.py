"""Import data from the old BMS SQLite database (bms.sqlite3) into B.R.I.D.G.E.
Usage: python manage.py migrate_old_bms --db /path/to/bms.sqlite3
Old password hashes use a custom algorithm and are NOT portable — imported users
get an unusable password and must reset it (or set one via Django admin).
"""
import sqlite3, json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from bms.models import (User, Resident, Classification, ResidentIDSequence, ResidentIDIssuance,
    BarangayOfficial, Announcement, Program, Request, CertificateIssuance, Task,
    TaskAssignment, TaskUpdate, StaffAssignmentHistory, Conversation, Message,
    MessageRecipient, Notification, GalleryItem, ActivityLog, SystemSetting)


def dt(s):
    if not s:
        return None
    s = str(s).replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(s)
        if timezone.is_naive(d):
            d = timezone.make_aware(d)
        return d
    except Exception:
        return None


def jload(s):
    try:
        return json.loads(s or "{}")
    except Exception:
        return {}


class Command(BaseCommand):
    help = "Migrate old BMS SQLite data into B.R.I.D.G.E"

    def add_arguments(self, parser):
        parser.add_argument("--db", required=True, help="Path to old bms.sqlite3")

    def handle(self, *args, **opts):
        con = sqlite3.connect(opts["db"])
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        users, residents, requests, tasks, conversations, messages = {}, {}, {}, {}, {}, {}

        for r in cur.execute("SELECT * FROM users ORDER BY id"):
            u, _ = User.objects.get_or_create(username=r["username"], defaults={
                "name": r["name"] or r["username"], "role": r["role"] or "resident",
                "email": r["email"] or "", "account_status": r["account_status"] or "active",
                "position": r["position"] or "", "department": r["department"] or "",
                "contact_number": r["contact_number"] or "", "profile_image": r["profile_image"] or "",
                "google_subject_id": r["google_subject_id"] or "", "google_email": r["google_email"] or "",
                "google_verified": bool(r["google_verified"]),
                "date_joined": dt(r["created_at"]) or timezone.now(),
                "last_login": dt(r["last_login_at"]), "old_password_hash": r["password_hash"] or ""})
            u.set_unusable_password(); u.save(update_fields=["password"])
            users[r["id"]] = u
        self.stdout.write(f"users: {len(users)}")

        for r in cur.execute("SELECT * FROM residents ORDER BY id"):
            obj, _ = Resident.objects.get_or_create(resident_id=r["resident_id"], defaults={
                "household_no": r["household_no"], "last_name": r["last_name"],
                "first_name": r["first_name"], "middle_name": r["middle_name"] or "",
                "birth_date": r["birth_date"], "gender": r["gender"],
                "civil_status": r["civil_status"], "address": r["address"],
                "contact": r["contact"], "voter": r["voter"] or "No",
                "classification": r["classification"] or "Unclassified",
                "owner_user": users.get(r["owner_user_id"]),
                "resident_status": r["resident_status"] or "ACTIVE",
                "profile_image": r["profile_image"] or "", "archived_at": dt(r["archived_at"])})
            residents[r["id"]] = obj
        self.stdout.write(f"residents: {len(residents)}")

        for r in cur.execute("SELECT id, resident_record_id FROM users WHERE resident_record_id IS NOT NULL"):
            u = users.get(r["id"]); rr = residents.get(r["resident_record_id"])
            if u and rr: u.resident_record = rr; u.save(update_fields=["resident_record"])

        n = 0
        for r in cur.execute("SELECT * FROM classifications"):
            Classification.objects.get_or_create(resident=residents.get(r["resident_record_id"]),
                resident_id_text=r["resident_id"], full_name=r["full_name"],
                classification=r["classification"], defaults={"class_code": r["class_code"] or "",
                "class_status": r["class_status"] or "Active", "payload": jload(r["payload_json"])}); n += 1
        self.stdout.write(f"classifications: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM resident_id_sequences"):
            ResidentIDSequence.objects.get_or_create(sequence_year=r["sequence_year"], prefix=r["prefix"],
                defaults={"next_number": r["next_number"]}); n += 1
        self.stdout.write(f"id_sequences: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM resident_id_issuances"):
            ResidentIDIssuance.objects.get_or_create(issuance_number=r["issuance_number"], defaults={
                "resident": residents.get(r["resident_record_id"]), "resident_id_text": r["resident_id"],
                "status": r["status"], "issued_at": dt(r["issued_at"]), "issued_by": r["issued_by"] or "",
                "remarks": r["remarks"] or ""}); n += 1
        self.stdout.write(f"id_issuances: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM barangay_officials"):
            BarangayOfficial.objects.get_or_create(first_name=r["first_name"], last_name=r["last_name"],
                position=r["position"], defaults={"middle_name": r["middle_name"] or "", "suffix": r["suffix"] or "",
                "bio": r["bio"] or "", "contact_info": r["contact_info"] or "",
                "profile_image": r["profile_image"] or "", "display_order": r["display_order"] or 0,
                "is_visible": bool(r["is_visible"]), "status": r["status"] or "ACTIVE",
                "archived_at": dt(r["archived_at"])}); n += 1
        self.stdout.write(f"officials: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM announcements"):
            Announcement.objects.get_or_create(title=r["title"], body=r["body"], defaults={
                "category": r["category"] or "", "priority": r["priority"] or "NORMAL",
                "archived_at": dt(r["archived_at"]), "created_by": users.get(r["created_by_user_id"]),
                "payload": jload(r["payload_json"]), "created_at": dt(r["created_at"]) or timezone.now()}); n += 1
        self.stdout.write(f"announcements: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM programs"):
            Program.objects.get_or_create(event_id=r["event_id"], defaults={"title": r["title"],
                "description": r["description"] or "", "event_date": r["event_date"],
                "start_time": r["start_time"] or "", "end_time": r["end_time"] or "",
                "location": r["location"] or "", "organizer": r["organizer"] or "",
                "status": r["status"] or "Scheduled", "created_by": users.get(r["created_by_user_id"])}); n += 1
        self.stdout.write(f"programs: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM requests"):
            obj, _ = Request.objects.get_or_create(request_id=r["request_id"], defaults={
                "owner_user": users.get(r["owner_user_id"]), "resident": residents.get(r["resident_record_id"]),
                "type": r["type"], "purpose": r["purpose"] or "", "category": r["category"] or "",
                "status": r["status"] or "pending", "date_needed": r["date_needed"],
                "remarks": r["remarks"] or "", "processed_at": dt(r["processed_at"]),
                "approved_at": dt(r["approved_at"]), "approved_by": users.get(r["approved_by_user_id"]),
                "payload": jload(r["payload_json"]), "created_at": dt(r["created_at"]) or timezone.now()})
            requests[r["id"]] = obj; n += 1
        self.stdout.write(f"requests: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM certificate_issuances"):
            CertificateIssuance.objects.get_or_create(cert_no=r["cert_no"], defaults={
                "request": requests.get(r["request_record_id"]), "issued_by": users.get(r["issued_by_user_id"]),
                "payload": jload(r["payload_json"]), "created_at": dt(r["created_at"]) or timezone.now()}); n += 1
        self.stdout.write(f"certificates: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM tasks"):
            obj, _ = Task.objects.get_or_create(task_id=r["task_id"], defaults={"title": r["title"] or "",
                "task_type": r["task_type"] or "", "priority": r["priority"] or "NORMAL",
                "due_date": r["due_date"], "due_time": r["due_time"] or "", "status": r["status"] or "assigned",
                "assigned_to": users.get(r["assigned_to_user_id"]), "description": r["description"] or "",
                "created_by": users.get(r["created_by_user_id"]), "completion_date": dt(r["completion_date"]),
                "completion_notes": r["completion_notes"] or "", "related_record": r["related_record"] or "",
                "progress_percent": r["progress_percent"] or 0, "acknowledged_at": dt(r["acknowledged_at"]),
                "payload": jload(r["payload_json"]), "created_at": dt(r["created_at"]) or timezone.now()})
            tasks[r["id"]] = obj; n += 1
        self.stdout.write(f"tasks: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM task_assignments"):
            TaskAssignment.objects.get_or_create(task=tasks.get(r["task_id"]), staff=users.get(r["staff_id"]),
                defaults={"status": r["status"] or "PENDING", "assigned_at": dt(r["assigned_at"]) or timezone.now(),
                "acknowledged_at": dt(r["acknowledged_at"]), "completed_at": dt(r["completed_at"]),
                "completion_notes": r["completion_notes"] or ""}); n += 1
        self.stdout.write(f"task_assignments: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM task_updates"):
            TaskUpdate.objects.get_or_create(task=tasks.get(r["task_id"]), staff=users.get(r["staff_id"]),
                update_text=r["update_text"], defaults={"update_type": r["update_type"] or "progress",
                "progress_percent": r["progress_percent"] or 0,
                "created_at": dt(r["created_at"]) or timezone.now()}); n += 1
        self.stdout.write(f"task_updates: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM staff_assignment_history"):
            StaffAssignmentHistory.objects.get_or_create(staff=users.get(r["staff_id"]),
                changed_at=dt(r["changed_at"]) or timezone.now(), defaults={
                "previous_handler": users.get(r["previous_handler_id"]),
                "new_handler": users.get(r["new_handler_id"]), "changed_by": users.get(r["changed_by"]),
                "reason": r["reason"] or ""}); n += 1
        self.stdout.write(f"staff_history: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM conversations"):
            c, _ = Conversation.objects.get_or_create(conversation_key=r["conversation_key"], defaults={
                "title": r["title"] or "", "type": r["type"] or "direct",
                "created_by": users.get(r["created_by"]) or User.objects.first(),
                "created_at": dt(r["created_at"]) or timezone.now()})
            conversations[r["id"]] = c; n += 1
        self.stdout.write(f"conversations: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM messages"):
            m = Message.objects.create(conversation=conversations.get(r["conversation_id"]),
                sender=users.get(r["sender_id"]) or User.objects.first(),
                message_type=r["message_type"] or "NORMAL", subject=r["subject"] or "",
                body=r["body"], is_important=bool(r["is_important"]),
                task=tasks.get(r["task_id"]) if r["task_id"] else None,
                created_at=dt(r["created_at"]) or timezone.now())
            messages[r["id"]] = m; n += 1
        self.stdout.write(f"messages: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM message_recipients"):
            MessageRecipient.objects.get_or_create(message=messages.get(r["message_id"]),
                conversation=conversations.get(r["conversation_id"]), recipient=users.get(r["recipient_id"]),
                defaults={"is_read": bool(r["is_read"]), "read_at": dt(r["read_at"]),
                "is_archived": bool(r["is_archived"]), "archived_at": dt(r["archived_at"])}); n += 1
        self.stdout.write(f"message_recipients: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM notifications"):
            Notification.objects.get_or_create(user=users.get(r["user_id"]), title=r["title"],
                created_at=dt(r["created_at"]) or timezone.now(), defaults={"body": r["body"] or "",
                "notification_type": r["notification_type"] or "", "is_read": bool(r["is_read"]),
                "related_id": r["related_id"] or "", "related_type": r["related_type"] or "",
                "sender": users.get(r["sender_id"])}); n += 1
        self.stdout.write(f"notifications: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM gallery_items"):
            GalleryItem.objects.get_or_create(image_path=r["image_path"], caption=r["caption"], defaults={
                "thumbnail_path": r["thumbnail_path"] or "", "description": r["description"] or "",
                "display_order": r["display_order"] or 0, "is_visible": bool(r["is_visible"]),
                "status": r["status"] or "ACTIVE", "archived_at": dt(r["archived_at"])}); n += 1
        self.stdout.write(f"gallery: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM activity_logs"):
            ActivityLog.objects.get_or_create(event_type=r["event_type"],
                created_at=dt(r["created_at"]) or timezone.now(),
                defaults={"actor": users.get(r["actor_user_id"]), "payload": jload(r["payload_json"])}); n += 1
        self.stdout.write(f"activity_logs: {n}")

        n = 0
        for r in cur.execute("SELECT * FROM system_settings"):
            SystemSetting.objects.update_or_create(setting_key=r["setting_key"],
                defaults={"setting_value": r["setting_value"] or ""}); n += 1
        self.stdout.write(f"system_settings: {n}")

        self.stdout.write(self.style.SUCCESS("Migration complete. Copy old uploads/ -> backend/media/ for images."))
