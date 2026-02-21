import ThemeToggle from "@/components/ThemeToggle"
import Link from "next/link"

export default function Home() {
  return (
    <main className="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors duration-300">

      {/* Navbar */}
      <div className="flex justify-between items-center px-10 py-6 max-w-7xl mx-auto">
        <h1 className="text-2xl font-semibold tracking-tight">
          DBPulse AI
        </h1>
        <ThemeToggle />
      </div>

      {/* Hero */}
      <section className="text-center px-6 pt-24 pb-20 max-w-4xl mx-auto">
        <h2 className="text-5xl md:text-6xl font-bold leading-tight tracking-tight mb-6">
          Intelligent Database  
          <span className="block text-gray-400 dark:text-gray-500">
            Health Analysis Platform
          </span>
        </h2>

        <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto mb-10">
          Upload Oracle AWR or PostgreSQL logs and receive
          a structured health score with actionable insights.
          No login required.
        </p>

        <div className="flex justify-center gap-4">
          <Link href="/oracle">
            <button className="px-6 py-3 bg-black text-white dark:bg-white dark:text-black rounded-xl hover:opacity-80 transition">
              Analyze Oracle
            </button>
          </Link>

          <Link href="/postgres">
            <button className="px-6 py-3 border border-gray-300 dark:border-gray-700 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition">
              Analyze PostgreSQL
            </button>
          </Link>
        </div>
      </section>

      {/* Feature Section */}
      <section className="border-t border-gray-200 dark:border-gray-800 py-20 px-6">
        <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-10 text-center">

          <div>
            <h3 className="text-xl font-semibold mb-3">
              AI-Powered Scoring
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              Automated analysis of wait events,
              CPU, memory, and performance patterns.
            </p>
          </div>

          <div>
            <h3 className="text-xl font-semibold mb-3">
              Secure File Processing
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              Files are processed temporarily and
              not permanently stored.
            </p>
          </div>

          <div>
            <h3 className="text-xl font-semibold mb-3">
              Actionable Recommendations
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              Practical guidance tailored for
              Oracle & PostgreSQL DBAs.
            </p>
          </div>

        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-800 py-8 text-center text-gray-400 dark:text-gray-500 text-sm">
        © {new Date().getFullYear()} DBPulse AI — Built for Database Engineers
      </footer>

    </main>
  )
}
