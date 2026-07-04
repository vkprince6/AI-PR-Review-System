"use client";

import { PullRequestHistoryTable } from "@/components/history/PullRequestHistoryTable";
import { ErrorAlert } from "@/components/ui/ErrorAlert";
import { EmptyState } from "@/components/ui/EmptyState";
import { Pagination } from "@/components/ui/Pagination";
import { Spinner } from "@/components/ui/Spinner";
import { PageContainer } from "@/components/layout/PageContainer";
import { usePullRequestHistory } from "@/hooks/usePullRequestHistory";

/**
 * History page: paginated table of all previously reviewed Pull Requests.
 */
export default function HistoryPage() {
  const { items, page, totalPages, isLoading, error, fetchPage, removeItem } =
    usePullRequestHistory(10);

  return (
    <PageContainer>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Review History</h1>
        <p className="mt-1 text-sm text-gray-500">
          Browse all previously analyzed Pull Requests.
        </p>
      </div>

      {isLoading && (
        <div className="flex justify-center py-16">
          <Spinner size={28} />
        </div>
      )}

      {!isLoading && error && <ErrorAlert message={error} onRetry={() => fetchPage(page)} />}

      {!isLoading && !error && items.length === 0 && (
        <EmptyState
          title="No reviews yet"
          description="Analyzed Pull Requests will appear here."
        />
      )}

      {!isLoading && !error && items.length > 0 && (
        <>
          <PullRequestHistoryTable items={items} onDelete={removeItem} />
          <Pagination page={page} totalPages={totalPages} onPageChange={fetchPage} />
        </>
      )}
    </PageContainer>
  );
}
