import { Inbox } from "lucide-react";

interface EmptyStateProps {
  title: string;
  description?: string;
}

/**
 * Standardized empty-state display for lists with no data.
 */
export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-gray-300 bg-gray-50 px-6 py-14 text-center">
      <Inbox className="mb-3 h-10 w-10 text-gray-400" />
      <p className="text-sm font-medium text-gray-900">{title}</p>
      {description && <p className="mt-1 text-sm text-gray-500">{description}</p>}
    </div>
  );
}
