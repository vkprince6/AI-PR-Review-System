"use client";

import { useState, FormEvent } from "react";
import { Search } from "lucide-react";
import { Spinner } from "@/components/ui/Spinner";
import { parseRepoFullName } from "@/lib/utils";

interface RepositoryInputProps {
  onSubmit: (repoOwner: string, repoName: string, prNumber: number) => void;
  isLoading: boolean;
}

/**
 * Form allowing the user to specify a GitHub repository and PR number
 * to trigger an AI review.
 */
export function RepositoryInput({ onSubmit, isLoading }: RepositoryInputProps) {
  const [repoFullName, setRepoFullName] = useState("");
  const [prNumber, setPrNumber] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setValidationError(null);

    const parsed = parseRepoFullName(repoFullName);
    if (!parsed) {
      setValidationError("Enter a repository in 'owner/repo' format, e.g. facebook/react.");
      return;
    }

    const prNum = parseInt(prNumber, 10);
    if (isNaN(prNum) || prNum <= 0) {
      setValidationError("Enter a valid, positive Pull Request number.");
      return;
    }

    const [owner, name] = parsed;
    onSubmit(owner, name, prNum);
  }

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-900">Review a Pull Request</h2>
      <p className="mt-1 text-sm text-gray-500">
        Enter a public GitHub repository and Pull Request number to run an AI-powered review.
      </p>

      <form onSubmit={handleSubmit} className="mt-5 flex flex-col gap-4 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label htmlFor="repo" className="block text-sm font-medium text-gray-700">
            Repository
          </label>
          <input
            id="repo"
            type="text"
            placeholder="facebook/react"
            value={repoFullName}
            onChange={(e) => setRepoFullName(e.target.value)}
            disabled={isLoading}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50"
          />
        </div>

        <div className="w-full sm:w-40">
          <label htmlFor="pr-number" className="block text-sm font-medium text-gray-700">
            PR Number
          </label>
          <input
            id="pr-number"
            type="number"
            min={1}
            placeholder="1234"
            value={prNumber}
            onChange={(e) => setPrNumber(e.target.value)}
            disabled={isLoading}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="flex items-center justify-center gap-2 rounded-md bg-blue-600 px-5 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
        >
          {isLoading ? <Spinner size={16} className="text-white" /> : <Search className="h-4 w-4" />}
          {isLoading ? "Analyzing..." : "Analyze PR"}
        </button>
      </form>

      {validationError && <p className="mt-3 text-sm text-red-600">{validationError}</p>}
    </div>
  );
}
