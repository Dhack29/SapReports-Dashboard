import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'warranty_dipek';")
    res = cursor.fetchall()

with open('c:/Users/Dipek/Desktop/CRIS/SapReports/schema.txt', 'w') as f:
    for col in res:
        f.write(f"{col[0]} ({col[1]})\n")
