import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bridge_core.settings")

import django
django.setup()

from django.core.management import call_command

try:
    print("📥 Starting data import...")
    call_command("loaddata", "data_export.json", verbosity=2)
    print("✅ Data import completed successfully!")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)