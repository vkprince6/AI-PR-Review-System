import { apiClient } from "@/lib/apiClient";
import type { APIResponse } from "@/types/api";
import type { ReviewRequest, ReviewResponse } from "@/types/review";

/**
 * Trigger an AI-powered code review for a given Pull Request.
 *
 * @param request - Repository owner, name, and PR number to review.
 * @returns The structured AI review result.
 */
export async function analyzePullRequest(request: ReviewRequest): Promise<ReviewResponse> {
  const response = await apiClient.post<APIResponse<ReviewResponse>>(
    "/review/analyze",
    request
  );
  return response.data.data as ReviewResponse;
}

/**
 * Retrieve a previously generated review by its ID.
 *
 * @param reviewId - Primary key of the review record.
 * @returns The stored review result.
 */
export async function getReview(reviewId: number): Promise<ReviewResponse> {
  const response = await apiClient.get<APIResponse<ReviewResponse>>(`/review/${reviewId}`);
  return response.data.data as ReviewResponse;
}
