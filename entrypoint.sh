#!/bin/sh

# Exit if any command fails
set -e

# Run migrations
poetry run python manage.py migrate

# Create superuser (only if it doesn't exist)
poetry run python manage.py createsuperuser \
  --noinput \
  --username "$DJANGO_SUPERUSER_USERNAME" \
  --email "$DJANGO_SUPERUSER_EMAIL" || true

# Set password (because --noinput won't let us specify it)
poetry run python manage.py shell <<EOF
from django.contrib.auth import get_user_model;
User = get_user_model();
try:
    u = User.objects.get(username="$DJANGO_SUPERUSER_USERNAME")
    u.set_password("$DJANGO_SUPERUSER_PASSWORD")
    u.save()
    print("Superuser password updated.")
except User.DoesNotExist:
    print("Superuser does not exist, skipping password update.")
EOF

# Finally, run whatever CMD was passed (Gunicorn by default)
exec "$@"