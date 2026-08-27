import type { Metadata } from "next";
import Link from "next/link";
import { Fraunces, Figtree } from "next/font/google";
import "./globals.css";

const display = Fraunces({ variable: "--font-display", subsets: ["latin"] });
const body = Figtree({ variable: "--font-body", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "QuietDesk — overnight front office for independent shops",
  description:
    "A Strands Graph that works the night inbox for a closed shop, then wakes the owner only for irreversible binds.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable}`}>
      <body>
        <header className="wrap site-header">
          <Link href="/" className="brand">
            Quiet<span>Desk</span>
          </Link>
          <nav className="nav">
            <Link href="/how">How it binds</Link>
            <Link href="/ops">Night board</Link>
            <Link href="/how#architecture">Architecture</Link>
          </nav>
        </header>
        <main>{children}</main>
        <footer className="wrap site-footer">
          <span>QuietDesk · Agents for Humans · Professional Agents</span>
          <span>Strands Graph. Python policy. Owner binds.</span>
        </footer>
      </body>
    </html>
  );
}
