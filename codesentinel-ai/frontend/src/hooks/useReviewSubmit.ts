"use client";

import { useState, useCallback } from "react";
import { analyzePullRequest } from "@/services/reviewService";
import { ApiError } from "@/lib/apiClient";
import { getOrCreateStorageKey } from "@/lib/storage";
import type { ReviewResponse } from "@/types/review";

interface UseReviewSubmitState {
  isLoading: boolean;
  error: string | null;
  result: ReviewResponse | null;
}

interface ReviewSubmissionOptions {
  storageKey?: string;
  githubToken?: string;
  groqApiKey?: string;
}

/**
 * Hook encapsulating the AI review submission workflow: loading,
 * error, and result state management for the review form.
 *
 * @returns Submission state and a submit handler.
 */
export function useReviewSubmit() {
  const [state, setState] = useState<UseReviewSubmitState>({
    isLoading: false,
    error: null,
    result: null,
  });

  const submitReview = useCallback(
    async (
      repoOwner: string,
      repoName: string,
      prNumber: number,
      options: ReviewSubmissionOptions = {}
    ) => {
      setState({ isLoading: true, error: null, result: null });
      try {
        const storageKey = options.storageKey || getOrCreateStorageKey();
        const result = await analyzePullRequest({
          repo_owner: repoOwner,
          repo_name: repoName,
          pr_number: prNumber,
          storage_key: storageKey,
          github_token: options.githubToken,
          groq_api_key: options.groqApiKey,
        });
        setState({ isLoading: false, error: null, result });
      } catch (err) {
        const message = err instanceof ApiError ? err.message : "Failed to analyze pull request.";
        setState({ isLoading: false, error: message, result: null });
      }
    },
    []
  );

  const reset = useCallback(() => {
    setState({ isLoading: false, error: null, result: null });
  }, []);

  return { ...state, submitReview, reset };
}
