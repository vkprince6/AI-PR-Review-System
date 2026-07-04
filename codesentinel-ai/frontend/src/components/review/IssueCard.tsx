import { Badge } from "@/components/ui/Badge";
import { getSeverityStyles } from "@/lib/utils";
import type { ReviewIssue } from "@/types/review";
import { FileCode2 } from "lucide-react";

interface IssueCardProps {
  issue: ReviewIssue;
}

/**
 * Displays a single identified code review issue with severity,
 * category, file location, description, and suggested fix.
 */
export function IssueCard({ issue }: IssueCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 p-4">
      <div className="flex flex-wrap items-center gap-2">
        <Badge className={getSeverityStyles(issue.severity)}>{issue.severity}</Badge>
        <Badge className="bg-gray-100 text-gray-700">{issue.category}</Badge>
        <span className="flex items-center gap-1 text-xs text-gray-500">
          <FileCode2 className="h-3.5 w-3.5" />
          {issue.file_path}
          {issue.line_number ? `:${issue.line_number}` : ""}
        </span>
      </div>
      <p className="mt-2 text-sm text-gray-800">{issue.description}</p>
      <div className="mt-2 rounded-md bg-blue-50 px-3 py-2">
        <p className="text-xs font-medium text-blue-700">Suggestion</p>
        <p className="mt-0.5 text-sm text-blue-900">{issue.suggestion}</p>
      </div>
    </div>
  );
}
