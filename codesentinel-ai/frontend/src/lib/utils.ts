import { clsx, type ClassValue } from "clsx";

/**
 * Merge conditional class names into a single string.
 *
 * @param inputs - Class values to conditionally combine.
 * @returns A merged className string.
 */
export function cn(...inputs: ClassValue[]): string {
  return clsx(inputs);
}

/**
 * Map a risk level to a Tailwind color token for badges/borders.
 *
 * @param riskLevel - The risk level string (LOW/MEDIUM/HIGH/CRITICAL).
 * @returns Tailwind class names for background, text, and border.
 */
export function getRiskLevelStyles(riskLevel: string): string {
  switch (riskLevel.toUpperCase()) {
    case "LOW":
      return "bg-green-50 text-green-700 border-green-200";
    case "MEDIUM":
      return "bg-yellow-50 text-yellow-700 border-yellow-200";
    case "HIGH":
      return "bg-orange-50 text-orange-700 border-orange-200";
    case "CRITICAL":
      return "bg-red-50 text-red-700 border-red-200";
    default:
      return "bg-gray-50 text-gray-700 border-gray-200";
  }
}

/**
 * Map an issue severity to a Tailwind color token for badges.
 *
 * @param severity - The issue severity string.
 * @returns Tailwind class names for background and text.
 */
export function getSeverityStyles(severity: string): string {
  switch (severity.toUpperCase()) {
    case "CRITICAL":
      return "bg-red-100 text-red-800";
    case "HIGH":
      return "bg-orange-100 text-orange-800";
    case "MEDIUM":
      return "bg-yellow-100 text-yellow-800";
    case "LOW":
      return "bg-blue-100 text-blue-800";
    case "INFO":
      return "bg-gray-100 text-gray-700";
    default:
      return "bg-gray-100 text-gray-700";
  }
}

/**
 * Parse a "owner/repo" full name string into its components.
 *
 * @param fullName - Repository identifier in "owner/repo" format.
 * @returns A tuple of [owner, repo], or null if invalid.
 */
export function parseRepoFullName(fullName: string): [string, string] | null {
  const trimmed = fullName.trim();
  const parts = trimmed.split("/");
  if (parts.length !== 2 || !parts[0] || !parts[1]) {
    return null;
  }
  return [parts[0], parts[1]];
}
