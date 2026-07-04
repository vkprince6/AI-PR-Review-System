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
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Submit a Pull Request for instant AI-powered code review.
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
