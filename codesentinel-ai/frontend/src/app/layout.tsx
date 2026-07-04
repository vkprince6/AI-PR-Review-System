import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Navbar } from "@/components/layout/Navbar";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CodeSentinel AI",
  description: "Enterprise AI Pull Request Review Assistant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(59,130,246,0.08),_transparent_35%),linear-gradient(180deg,_#f8fafc_0%,_#f1f5f9_100%)] text-slate-900`}>
        <div className="flex min-h-screen flex-col">
          <Navbar />
          {children}
          <footer className="mt-auto border-t border-slate-200 bg-white/80 backdrop-blur-sm">
            <div className="mx-auto flex max-w-6xl items-center justify-center px-4 py-4 text-sm text-slate-500 sm:px-6 lg:px-8">
              Project created by VEERAKUMAR C B
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
