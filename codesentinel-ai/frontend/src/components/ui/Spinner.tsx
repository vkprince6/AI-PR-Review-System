import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface SpinnerProps {
  size?: number;
  className?: string;
}

/**
 * Reusable animated loading spinner.
 */
export function Spinner({ size = 20, className }: SpinnerProps) {
  return <Loader2 size={size} className={cn("animate-spin text-blue-600", className)} />;
}
