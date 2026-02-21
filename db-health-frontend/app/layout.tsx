import "./globals.css"
import { ThemeProvider } from "next-themes"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "DBPulse AI",
  description: "AI-Powered Oracle & PostgreSQL Health Check Platform",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="dark">
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
