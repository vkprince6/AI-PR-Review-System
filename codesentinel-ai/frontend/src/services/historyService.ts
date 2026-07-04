import { apiClient } from "@/lib/apiClient";
import type { APIResponse, PaginatedResponse } from "@/types/api";
import type { PullRequestHistoryItem, ReviewHistoryItem } from "@/types/history";
import type { ReviewResponse } from "@/types/review";

/**
 * List reviewed Pull Requests with pagination.
 *
 * @param page - 1-indexed page number.
 * @param pageSize - Number of items per page.
 * @returns Paginated Pull Request history.
 */
export async function listPullRequests(
  page: number = 1,
  pageSize: number = 10
): Promise<PaginatedResponse<PullRequestHistoryItem>> {
  const response = await apiClient.get<APIResponse<PaginatedResponse<PullRequestHistoryItem>>>(
    "/history/pull-requests",
    { params: { page, page_size: pageSize } }
  );
  return response.data.data as PaginatedResponse<PullRequestHistoryItem>;
}

/**
 * Fetch a single Pull Request's latest review detail.
 *
 * @param pullRequestId - Primary key of the Pull Request.
 * @returns The PR's latest review, structured.
 */
export async function getPullRequestDetail(pullRequestId: number): Promise<ReviewResponse> {
  const response = await apiClient.get<APIResponse<ReviewResponse>>(
    `/history/pull-requests/${pullRequestId}`
  );
  return response.data.data as ReviewResponse;
}

/**
 * Delete a Pull Request and all its associated reviews.
 *
 * @param pullRequestId - Primary key of the Pull Request to delete.
 */
export async function deletePullRequest(pullRequestId: number): Promise<void> {
  await apiClient.delete(`/history/pull-requests/${pullRequestId}`);
}

/**
 * List all AI reviews with pagination.
 *
 * @param page - 1-indexed page number.
 * @param pageSize - Number of items per page.
 * @returns Paginated review history.
 */
export async function listReviews(
  page: number = 1,
  pageSize: number = 10
): Promise<PaginatedResponse<ReviewHistoryItem>> {
  const response = await apiClient.get<APIResponse<PaginatedResponse<ReviewHistoryItem>>>(
    "/history/reviews",
    { params: { page, page_size: pageSize } }
  );
  return response.data.data as PaginatedResponse<ReviewHistoryItem>;
}

/**
 * Delete a single review record.
 *
 * @param reviewId - Primary key of the Review to delete.
 */
export async function deleteReview(reviewId: number): Promise<void> {
  await apiClient.delete(`/history/reviews/${reviewId}`);
}
