import { Spinner } from "@/components/ui/Spinner";

/**
 * Loading state shown while the AI review pipeline is running.
 * Communicates the multi-step nature of the process to set expectations.
 */
export function AnalyzingState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-gray-200 bg-white p-12 shadow-sm">
      <Spinner size={32} />
      <p className="mt-4 text-sm font-medium text-gray-900">Analyzing pull request...</p>
      <p className="mt-1 text-sm text-gray-500">
        Fetching diff from GitHub and running AI code review. This can take up to 30 seconds.
      </p>
    </div>
  );
}
