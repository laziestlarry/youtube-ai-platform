# This file is used to import all models into the Base's metadata.
# It's crucial for tools like Alembic to detect model changes.
from app.backend.db.base_class import Base  # noqa
from app.backend.models.video import Video  # noqa
# Import other models here as they are created
# from app.backend.models.user import User  # noqa