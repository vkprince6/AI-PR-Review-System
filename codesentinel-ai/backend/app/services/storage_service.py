"""
Per-user review history storage.

Stores review history in a JSON file per storage key so review data is
isolated by user/session instead of being mixed into a shared database.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.core.logger import logger


class StorageService:
    """Persist and retrieve review history for a single storage key."""

    def __init__(self, storage_key: Optional[str] = None) -> None:
        self.storage_key = (storage_key or "default").strip() or "default"
        self.storage_dir = Path(settings.history_storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.storage_dir / f"{self._safe_filename(self.storage_key)}.json"

    @staticmethod
    def _safe_filename(value: str) -> str:
        digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
        return digest

    def _load_records(self) -> List[Dict[str, Any]]:
        if not self.file_path.exists():
            return []

        try:
            content = self.file_path.read_text(encoding="utf-8")
            payload = json.loads(content)
            if isinstance(payload, list):
                return payload
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to read history storage file | file={file} | error={error}", file=str(self.file_path), error=str(exc))

        return []

    def _write_records(self, records: List[Dict[str, Any]]) -> None:
        self.file_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    def save_review(
        self,
        review_id: int,
        request: Any,
        pr_data: Any,
        review_result: Any,
        model_used: str,
    ) -> Dict[str, Any]:
        """Append a new review record for the active storage key."""
        record = {
            "id": review_id,
            "repo_owner": request.repo_owner,
            "repo_name": request.repo_name,
            "pr_number": pr_data.pr_number,
            "pr_title": pr_data.title,
            "author": pr_data.author,
            "additions": pr_data.additions,
            "deletions": pr_data.deletions,
            "changed_files_count": pr_data.changed_files_count,
            "html_url": pr_data.html_url,
            "summary": review_result.summary,
            "overall_score": review_result.overall_score,
            "risk_level": review_result.risk_level.value,
            "issues": [issue.model_dump(mode="json") for issue in review_result.issues],
            "strengths": review_result.strengths,
            "model_used": model_used,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        records = self._load_records()
        records.append(record)
        self._write_records(records)
        return record

    def list_pull_requests(self) -> List[Dict[str, Any]]:
        """Return API-friendly pull-request history items derived from stored records."""
        items = []
        for record in self._load_records():
            items.append(
                {
                    "id": record["id"],
                    "repo_owner": record["repo_owner"],
                    "repo_name": record["repo_name"],
                    "pr_number": record["pr_number"],
                    "pr_title": record["pr_title"],
                    "title": record["pr_title"],
                    "author": record["author"],
                    "additions": record["additions"],
                    "deletions": record["deletions"],
                    "changed_files_count": record["changed_files_count"],
                    "html_url": record["html_url"],
                    "created_at": record["created_at"],
                    "latest_review_score": record["overall_score"],
                    "latest_review_risk": record["risk_level"],
                }
            )
        return items

    def get_pull_request_detail(self, pull_request_id: int) -> Optional[Dict[str, Any]]:
        records = self._load_records()
        for record in records:
            if record["id"] == pull_request_id:
                return record
        return None

    def delete_pull_request(self, pull_request_id: int) -> bool:
        records = self._load_records()
        updated = [record for record in records if record["id"] != pull_request_id]
        if len(updated) == len(records):
            return False
        self._write_records(updated)
        return True

    def list_reviews(self) -> List[Dict[str, Any]]:
        records = self._load_records()
        items = []
        for record in records:
            items.append(
                {
                    "id": record["id"],
                    "pull_request_id": record["id"],
                    "repo_full_name": f"{record['repo_owner']}/{record['repo_name']}",
                    "pr_number": record["pr_number"],
                    "pr_title": record["pr_title"],
                    "overall_score": record["overall_score"],
                    "risk_level": record["risk_level"],
                    "model_used": record["model_used"],
                    "created_at": record["created_at"],
                }
            )
        return items

    def get_review(self, review_id: int) -> Optional[Dict[str, Any]]:
        records = self._load_records()
        for record in records:
            if record["id"] == review_id:
                return record
        return None

    def delete_review(self, review_id: int) -> bool:
        records = self._load_records()
        updated = [record for record in records if record["id"] != review_id]
        if len(updated) == len(records):
            return False
        self._write_records(updated)
        return True
