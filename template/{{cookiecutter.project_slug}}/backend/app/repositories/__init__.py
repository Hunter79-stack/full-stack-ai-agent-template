"""Repository layer for database operations."""
{%- if cookiecutter.use_postgresql or cookiecutter.use_sqlite or cookiecutter.use_jwt or cookiecutter.enable_webhooks %}
# ruff: noqa: I001, RUF022 - Imports structured for Jinja2 template conditionals
{%- endif %}
{%- if cookiecutter.use_jwt %}

from app.repositories import user as user_repo
{%- endif %}
{%- if cookiecutter.enable_session_management and cookiecutter.use_jwt %}

from app.repositories import session as session_repo
{%- endif %}
{%- if cookiecutter.use_database %}

from app.repositories import conversation as conversation_repo
{%- endif %}
{%- if cookiecutter.enable_webhooks and cookiecutter.use_database %}

from app.repositories import webhook as webhook_repo
{%- endif %}
{%- if cookiecutter.enable_rag and (cookiecutter.use_postgresql or cookiecutter.use_sqlite) %}

from app.repositories import rag_document as rag_document_repo
from app.repositories import sync_log as sync_log_repo
from app.repositories import sync_source as sync_source_repo
{%- endif %}
{%- if cookiecutter.use_jwt %}

from app.repositories import chat_file as chat_file_repo
{%- endif %}

__all__ = [
{%- if cookiecutter.use_jwt %}
    "user_repo",
{%- endif %}
{%- if cookiecutter.enable_session_management and cookiecutter.use_jwt %}
    "session_repo",
{%- endif %}
{%- if cookiecutter.use_database %}
    "conversation_repo",
{%- endif %}
{%- if cookiecutter.enable_webhooks and cookiecutter.use_database %}
    "webhook_repo",
{%- endif %}
{%- if cookiecutter.enable_rag and (cookiecutter.use_postgresql or cookiecutter.use_sqlite) %}
    "rag_document_repo",
    "sync_log_repo",
    "sync_source_repo",
{%- endif %}
{%- if cookiecutter.use_jwt %}
    "chat_file_repo",
{%- endif %}
]
