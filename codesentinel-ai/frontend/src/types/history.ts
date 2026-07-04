/**
 * History-related domain types, mirroring backend history_schemas.py.
 */

export interface PullRequestHistoryItem {
  id: number;
  repo_owner: string;
  repo_name: string;
  pr_number: number;
  title: string;
  author: string;
  additions: number;
  deletions: number;
  changed_files_count: number;
  html_url: string;
  created_at: string;
  latest_review_score?: number | null;
  latest_review_risk?: string | null;
}

export interface ReviewHistoryItem {
  id: number;
  pull_request_id: number;
  repo_full_name: string;
  pr_number: number;
  pr_title: string;
  overall_score: number;
  risk_level: string;
  model_used: string;
  created_at: string;
}
