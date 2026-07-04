"use client";

import Link from "next/link";
import { format } from "date-fns";
import { Trash2, ExternalLink } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { getRiskLevelStyles } from "@/lib/utils";
import type { PullRequestHistoryItem } from "@/types/history";

interface PullRequestHistoryTableProps {
  items: PullRequestHistoryItem[];
  onDelete: (id: number) => void;
}

/**
 * Responsive table listing previously reviewed Pull Requests,
 * with links to view full detail and delete controls.
 */
export function PullRequestHistoryTable({ items, onDelete }: PullRequestHistoryTableProps) {
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
              Repository / PR
            </th>
            <th className="hidden px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500 sm:table-cell">
              Author
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
              Score
            </th>
            <th className="hidden px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500 md:table-cell">
              Risk
            </th>
            <th className="hidden px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500 lg:table-cell">
              Reviewed
            </th>
            <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-gray-500">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {items.map((item) => (
            <tr key={item.id} className="hover:bg-gray-50">
              <td className="px-4 py-3">
                <p className="text-sm font-medium text-gray-900">
                  {item.repo_owner}/{item.repo_name} #{item.pr_number}
                </p>
                <p className="max-w-xs truncate text-xs text-gray-500">{item.title}</p>
              </td>
              <td className="hidden px-4 py-3 text-sm text-gray-600 sm:table-cell">{item.author}</td>
              <td className="px-4 py-3 text-sm font-semibold text-gray-900">
                {item.latest_review_score?.toFixed(1) ?? "—"}
              </td>
              <td className="hidden px-4 py-3 md:table-cell">
                {item.latest_review_risk ? (
                  <Badge className={`border ${getRiskLevelStyles(item.latest_review_risk)}`}>
                    {item.latest_review_risk}
                  </Badge>
                ) : (
                  "—"
                )}
              </td>
              <td className="hidden px-4 py-3 text-sm text-gray-500 lg:table-cell">
                {format(new Date(item.created_at), "MMM d, yyyy")}
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center justify-end gap-3">
                  <Link
                    href={`/history/${item.id}`}
                    className="text-gray-400 hover:text-blue-600"
                    title="View details"
                  >
                    <ExternalLink className="h-4 w-4" />
                  </Link>
                  <button
                    onClick={() => onDelete(item.id)}
                    className="text-gray-400 hover:text-red-600"
                    title="Delete record"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
