import { apiClient } from "@/lib/apiClient";
import type { APIResponse } from "@/types/api";
import type { PullRequestData, RepositoryValidateResponse } from "@/types/github";

/**
 * Validate that a GitHub repository exists and is accessible.
 *
 * @param repoFullName - Repository identifier in "owner/repo" format.
 * @returns Repository validation result and metadata.
 */
export async function validateRepository(
  repoFullName: string
): Promise<RepositoryValidateResponse> {
  const response = await apiClient.post<APIResponse<RepositoryValidateResponse>>(
    "/github/validate-repository",
    { repo_full_name: repoFullName }
  );
  return response.data.data as RepositoryValidateResponse;
}

/**
 * Fetch full Pull Request metadata and changed files from GitHub.
 *
 * @param owner - Repository owner/organization.
 * @param repo - Repository name.
 * @param prNumber - Pull request number.
 * @returns Complete Pull Request data.
 */
export async function getPullRequest(
  owner: string,
  repo: string,
  prNumber: number
): Promise<PullRequestData> {
  const response = await apiClient.get<APIResponse<PullRequestData>>(
    `/github/${owner}/${repo}/pulls/${prNumber}`
  );
  return response.data.data as PullRequestData;
}
