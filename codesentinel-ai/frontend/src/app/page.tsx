"use client";

import { RepositoryInput } from "@/components/dashboard/RepositoryInput";
import { AnalyzingState } from "@/components/dashboard/AnalyzingState";
import { ReviewDisplay } from "@/components/review/ReviewDisplay";
import { ErrorAlert } from "@/components/ui/ErrorAlert";
import { PageContainer } from "@/components/layout/PageContainer";
import { useReviewSubmit } from "@/hooks/useReviewSubmit";

/**
 * Dashboard page: repository input form, loading state, and
 * the resulting AI review display.
 */
export default function DashboardPage() {
  const { isLoading, error, result, submitReview, reset } = useReviewSubmit();

  return (
    <PageContainer>
      <div className="mb-6 rounded-3xl border border-slate-200 bg-white/80 p-6 shadow-[0_10px_40px_rgba(15,23,42,0.06)] backdrop-blur-sm">
        <p className="text-sm font-medium text-blue-600">CodeSentinel AI</p>
        <h1 className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">
          Review pull requests with clarity and speed.
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
          Submit a pull request to receive a focused, production-style review with risk insights, issue detection, and a quality score.
        </p>
      </div>

      <RepositoryInput onSubmit={submitReview} isLoading={isLoading} />

      <div className="mt-6">
        {isLoading && <AnalyzingState />}
        {!isLoading && error && <ErrorAlert message={error} onRetry={reset} />}
        {!isLoading && !error && result && <ReviewDisplay review={result} />}
      </div>
    </PageContainer>
  );
}
