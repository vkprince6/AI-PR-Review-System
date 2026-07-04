interface PageContainerProps {
  children: React.ReactNode;
}

/**
 * Consistent max-width, padded, responsive page wrapper.
 */
export function PageContainer({ children }: PageContainerProps) {
  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
  );
}
