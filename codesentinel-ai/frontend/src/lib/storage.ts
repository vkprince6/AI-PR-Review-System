const STORAGE_KEY_NAME = "codesentinel-storage-key";

export function getOrCreateStorageKey(): string {
  if (typeof window === "undefined") {
    return "default";
  }

  const existing = window.localStorage.getItem(STORAGE_KEY_NAME);
  if (existing) {
    return existing;
  }

  const generated =
    typeof crypto !== "undefined" && typeof crypto.randomUUID === "function"
      ? `user-${crypto.randomUUID()}`
      : `user-${Math.random().toString(36).slice(2, 10)}`;

  window.localStorage.setItem(STORAGE_KEY_NAME, generated);
  return generated;
}

export function setStorageKey(storageKey: string): void {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(STORAGE_KEY_NAME, storageKey);
}
