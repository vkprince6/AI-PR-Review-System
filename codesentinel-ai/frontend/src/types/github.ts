/**
 * GitHub-related domain types, mirroring backend github_schemas.py.
 */

export interface RepositoryValidateResponse {
  is_valid: boolean;
  owner: string;
  name: string;
  default_branch?: string | null;
  is_private?: boolean | null;
  stars?: number | null;
  description?: string | null;
}

export interface ChangedFile {
  filename: string;
  status: "added" | "modified" | "removed" | "renamed";
  additions: number;
  deletions: number;
  changes: number;
  patch?: string | null;
}

export interface PullRequestData {
  pr_number: number;
  title: string;
  description?: string | null;
  author: string;
  base_branch: string;
  head_branch: string;
  additions: number;
  deletions: number;
  changed_files_count: number;
  html_url: string;
  changed_files: ChangedFile[];
}
