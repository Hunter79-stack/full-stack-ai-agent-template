"""Services layer - business logic.

Services orchestrate business operations, using repositories for data access
and raising domain exceptions for error handling.
"""
{%- set services = [] %}
{%- if cookiecutter.use_jwt or cookiecutter.enable_webhooks or cookiecutter.enable_rag %}
# ruff: noqa: I001, RUF022 - Imports structured for Jinja2 template conditionals
{%- endif %}
{%- if cookiecutter.use_jwt %}
{%- set _ = services.append("UserService") %}

from app.services.user import UserService
{%- endif %}
{%- if cookiecutter.enable_session_management and cookiecutter.use_jwt %}
{%- set _ = services.append("SessionService") %}

from app.services.session import SessionService
{%- endif %}
{%- if cookiecutter.use_database %}
{%- set _ = services.append("ConversationService") %}

from app.services.conversation import ConversationService
{%- endif %}
{%- if cookiecutter.enable_webhooks and cookiecutter.use_database %}
{%- set _ = services.append("WebhookService") %}

from app.services.webhook import WebhookService
{%- endif %}
{%- if cookiecutter.enable_rag and (cookiecutter.use_postgresql or cookiecutter.use_sqlite) %}
{%- set _ = services.append("RAGDocumentService") %}

from app.services.rag_document import RAGDocumentService
{%- set _ = services.append("RAGSyncService") %}

from app.services.rag_sync import RAGSyncService
{%- set _ = services.append("SyncSourceService") %}

from app.services.sync_source import SyncSourceService
{%- endif %}
{%- if cookiecutter.use_jwt and (cookiecutter.use_postgresql or cookiecutter.use_sqlite) %}
{%- set _ = services.append("FileUploadService") %}

from app.services.file_upload import FileUploadService
{%- endif %}
{%- if services %}

__all__ = {{ services }}
{%- endif %}
