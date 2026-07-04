import axios, { AxiosError, AxiosInstance } from "axios";
import type { APIErrorPayload } from "@/types/api";

/**
 * Normalized application-level error thrown by the API client.
 * Wraps backend error payloads into a consistent shape for UI consumption.
 */
export class ApiError extends Error {
  public readonly statusCode: number;
  public readonly details: Record<string, unknown>;

  constructor(message: string, statusCode: number, details: Record<string, unknown> = {}) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
    this.details = details;
  }
}

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

/**
 * Configured Axios instance for all backend communication.
 * Centralizes base URL, headers, and response error normalization.
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<APIErrorPayload>) => {
    const responseData = error.response?.data;
    const message = responseData?.error ?? error.message ?? "An unexpected error occurred.";
    const statusCode = error.response?.status ?? 500;
    const details = responseData?.details ?? {};
    return Promise.reject(new ApiError(message, statusCode, details));
  }
);
