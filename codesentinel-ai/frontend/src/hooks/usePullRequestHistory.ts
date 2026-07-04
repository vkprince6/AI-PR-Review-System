"use client";

import { useState, useCallback, useEffect } from "react";
import { listPullRequests, deletePullRequest } from "@/services/historyService";
import { ApiError } from "@/lib/apiClient";
import type { PullRequestHistoryItem } from "@/types/history";

interface UsePullRequestHistoryState {
  items: PullRequestHistoryItem[];
  total: number;
  page: number;
  totalPages: number;
  isLoading: boolean;
  error: string | null;
}

/**
 * Hook managing paginated Pull Request history fetching and deletion.
 *
 * @param pageSize - Number of items per page.
 * @returns History state and control functions.
 */
export function usePullRequestHistory(pageSize: number = 10) {
  const [state, setState] = useState<UsePullRequestHistoryState>({
    items: [],
    total: 0,
    page: 1,
    totalPages: 0,
    isLoading: true,
    error: null,
  });

  const fetchPage = useCallback(
    async (page: number) => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));
      try {
        const response = await listPullRequests(page, pageSize);
        setState({
          items: response.items,
          total: response.total,
          page: response.page,
          totalPages: response.total_pages,
          isLoading: false,
          error: null,
        });
      } catch (err) {
        const message = err instanceof ApiError ? err.message : "Failed to load history.";
        setState((prev) => ({ ...prev, isLoading: false, error: message }));
      }
    },
    [pageSize]
  );

  const removeItem = useCallback(
    async (id: number) => {
      try {
        await deletePullRequest(id);
        await fetchPage(state.page);
      } catch (err) {
        const message = err instanceof ApiError ? err.message : "Failed to delete record.";
        setState((prev) => ({ ...prev, error: message }));
      }
    },
    [fetchPage, state.page]
  );

  useEffect(() => {
    fetchPage(1);
  }, [fetchPage]);

  return { ...state, fetchPage, removeItem };
}
