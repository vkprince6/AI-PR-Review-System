/**
 * Generic API response envelope.
 * Mirrors backend `APIResponse[T]` schema for consistent typing
 * across every API call in the application.
 */
export interface APIResponse<T> {
  success: boolean;
  message?: string | null;
  data?: T | null;
}

/**
 * Generic paginated list response envelope.
 * Mirrors backend `PaginatedResponse[T]` schema.
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/**
 * Structured error shape returned by the backend's global exception handler.
 */
export interface APIErrorPayload {
  success: false;
  error: string;
  details: Record<string, unknown>;
}
