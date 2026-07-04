"use client";

import { useState, FormEvent } from "react";
import { Search, Sparkles } from "lucide-react";
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

  function handleSampleSubmit() {
    setValidationError(null);
    setRepoFullName("octocat/Hello-World");
    setPrNumber("1");
    onSubmit("octocat", "Hello-World", 1);
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-[0_10px_40px_rgba(15,23,42,0.06)] sm:p-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-medium text-blue-600">Instant AI review</p>
          <h2 className="mt-1 text-xl font-semibold text-slate-900">Review a Pull Request</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            Enter a public GitHub repository and pull request number to receive a concise, production-ready review.
          </p>
        </div>
        <div className="rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700">
          Fast • Reliable • Actionable
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mt-6 flex flex-col gap-4 lg:flex-row lg:items-end">
        <div className="flex-1">
          <label htmlFor="repo" className="block text-sm font-medium text-slate-700">
            Repository
          </label>
          <input
            id="repo"
            type="text"
            placeholder="facebook/react"
            value={repoFullName}
            onChange={(e) => setRepoFullName(e.target.value)}
            disabled={isLoading}
            className="mt-2 block w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm shadow-sm outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100"
          />
        </div>

        <div className="w-full lg:w-40">
          <label htmlFor="pr-number" className="block text-sm font-medium text-slate-700">
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
            className="mt-2 block w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2.5 text-sm shadow-sm outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="flex items-center justify-center gap-2 rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isLoading ? <Spinner size={16} className="text-white" /> : <Search className="h-4 w-4" />}
          {isLoading ? "Analyzing..." : "Analyze PR"}
        </button>
      </form>

      <div className="mt-4 flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={handleSampleSubmit}
          disabled={isLoading}
          className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-3 py-1.5 text-sm font-medium text-blue-700 transition hover:bg-blue-100 disabled:cursor-not-allowed disabled:opacity-70"
        >
          <Sparkles className="h-4 w-4" />
          Try sample PR
        </button>
        <span className="text-sm text-slate-500">Example: octocat/Hello-World • PR #1</span>
      </div>

      {validationError && <p className="mt-3 text-sm font-medium text-rose-600">{validationError}</p>}
    </div>
  );
}
