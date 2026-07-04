/**
 * AI Review-related domain types, mirroring backend review_schemas.py.
 */

export type IssueSeverity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";

export type IssueCategory =
  | "BUG"
  | "SECURITY"
  | "PERFORMANCE"
  | "STYLE"
  | "BEST_PRACTICE"
  | "MAINTAINABILITY";

export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface ReviewIssue {
  file_path: string;
  line_number?: number | null;
  severity: IssueSeverity;
  category: IssueCategory;
  description: string;
  suggestion: string;
}

export interface ReviewResult {
  summary: string;
  overall_score: number;
  risk_level: RiskLevel;
  issues: ReviewIssue[];
  strengths: string[];
}

export interface ReviewResponse {
  id: number;
  repo_full_name: string;
  pr_number: number;
  pr_title: string;
  review: ReviewResult;
  model_used: string;
  created_at: string;
}

export interface ReviewRequest {
  repo_owner: string;
  repo_name: string;
  pr_number: number;
}
