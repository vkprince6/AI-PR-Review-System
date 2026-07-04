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
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-[0_10px_40px_rgba(15,23,42,0.06)] sm:p-8">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-2xl">
            <p className="text-sm font-medium text-slate-500">
              {review.repo_full_name} · PR #{review.pr_number}
            </p>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">
              {review.pr_title}
            </h2>
            <div className="mt-4 flex flex-wrap items-center gap-2">
              <RiskBadge riskLevel={review.review.risk_level} />
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-500">
                Model: {review.model_used}
              </span>
            </div>
          </div>
          <ScoreGauge score={review.review.overall_score} />
        </div>
        <p className="mt-6 rounded-2xl border border-slate-100 bg-slate-50/70 p-4 text-sm leading-7 text-slate-700">
          {review.review.summary}
        </p>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-[0_10px_40px_rgba(15,23,42,0.06)] sm:p-8">
        <h3 className="text-base font-semibold text-slate-900">
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
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-[0_10px_40px_rgba(15,23,42,0.06)] sm:p-8">
          <h3 className="text-base font-semibold text-slate-900">Strengths</h3>
          <ul className="mt-4 space-y-2">
            {review.review.strengths.map((strength, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-slate-700">
                <CheckCircle2 className="mt-0.5 h-4 w-4 flex-shrink-0 text-emerald-600" />
                {strength}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
