import { CheckCircle2 } from "lucide-react";
import { ScoreGauge } from "@/components/review/ScoreGauge";
import { RiskBadge } from "@/components/review/RiskBadge";
import { IssueCard } from "@/components/review/IssueCard";
import { EmptyState } from "@/components/ui/EmptyState";
import type { ReviewResponse } from "@/types/review";

interface ReviewDisplayProps {
  review: ReviewResponse;
}

/**
 * Full display of an AI-generated Pull Request review: summary,
 * score, risk level, identified issues, and strengths.
 */
export function ReviewDisplay({ review }: ReviewDisplayProps) {
  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm text-gray-500">{review.repo_full_name} · PR #{review.pr_number}</p>
            <h2 className="mt-1 text-xl font-bold text-gray-900">{review.pr_title}</h2>
            <div className="mt-3 flex items-center gap-2">
              <RiskBadge riskLevel={review.review.risk_level} />
              <span className="text-xs text-gray-400">Model: {review.model_used}</span>
            </div>
          </div>
          <ScoreGauge score={review.review.overall_score} />
        </div>
        <p className="mt-5 border-t border-gray-100 pt-4 text-sm leading-relaxed text-gray-700">
          {review.review.summary}
        </p>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h3 className="text-base font-semibold text-gray-900">
          Issues Found ({review.review.issues.length})
        </h3>
        <div className="mt-4 space-y-3">
          {review.review.issues.length === 0 ? (
            <EmptyState
              title="No issues found"
              description="The AI reviewer did not flag any concerns in this diff."
            />
          ) : (
            review.review.issues.map((issue, idx) => <IssueCard key={idx} issue={issue} />)
          )}
        </div>
      </div>

      {review.review.strengths.length > 0 && (
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="text-base font-semibold text-gray-900">Strengths</h3>
          <ul className="mt-4 space-y-2">
            {review.review.strengths.map((strength, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                <CheckCircle2 className="mt-0.5 h-4 w-4 flex-shrink-0 text-green-600" />
                {strength}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
