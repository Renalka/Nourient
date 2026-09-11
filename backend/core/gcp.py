"""Google Cloud runtime helpers.

Cloud Run supplies Application Default Credentials (ADC) through the service
identity attached to a revision.  Local development can still opt into a
service-account file by setting ``FIREBASE_CREDENTIALS_PATH`` or
``GOOGLE_APPLICATION_CREDENTIALS``.
"""

from __future__ import annotations

import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials


def source_firebase_project_id() -> str:
    """Return the Firebase project that continues to own user data."""
    return os.environ.get("FIREBASE_PROJECT_ID", "nourient-38381")


def source_bigquery_project_id() -> str:
    """Return the project that owns Nourient's existing BigQuery datasets."""
    return os.environ.get("BQ_DATA_PROJECT_ID", "nourient")


def initialize_firebase_admin():
    """Initialise Firebase Admin once, preferring Cloud Run's ADC in production."""
    if firebase_admin._apps:
        return firebase_admin.get_app()

    options = {"projectId": source_firebase_project_id()}
    credentials_path = os.environ.get("FIREBASE_CREDENTIALS_PATH")

    # Preserve the existing local developer experience without copying the key
    # into a container image. Cloud Run never receives this ignored file.
    if not credentials_path and os.environ.get("ENVIRONMENT", "development") != "production":
        local_path = Path("firebase-adminsdk.json")
        if local_path.is_file():
            credentials_path = str(local_path)

    if credentials_path:
        return firebase_admin.initialize_app(credentials.Certificate(credentials_path), options)

    # credential=None selects Application Default Credentials, provided by the
    # Cloud Run service account in production.
    return firebase_admin.initialize_app(options=options)
