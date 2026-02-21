"use client"

import { useState } from "react"
import Link from "next/link"

export default function OraclePage() {
  const [awrFile, setAwrFile] = useState<File | null>(null)
  const [topFile, setTopFile] = useState<File | null>(null)
  const [score, setScore] = useState<number | null>(null)
  const [issues, setIssues] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    if (!awrFile) {
      alert("Please upload an AWR report first.")
      return
    }

    setLoading(true)
    setScore(null)
    setIssues([])

    const formData = new FormData()
    formData.append("file", awrFile)

    try {
      const response = await fetch("http://localhost:8000/analyze/oracle", {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      setScore(data.score)
      setIssues(data.issues || [])

    } catch (error) {
      console.error("Backend error:", error)
      alert("Failed to connect to backend.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors duration-300">

      <div className="max-w-4xl mx-auto px-6 py-12">

        <Link href="/" className="text-sm text-gray-500 dark:text-gray-400 hover:underline">
          ← Back to Home
        </Link>

        <h1 className="text-4xl font-bold mt-6 mb-4">
          Oracle Health Analysis
        </h1>

        <p className="text-gray-500 dark:text-gray-400 mb-10">
          Upload your AWR report and optional server TOP output.
        </p>

        {/* AWR Upload */}
        <label className="block border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-xl p-10 text-center mb-6 cursor-pointer hover:border-black dark:hover:border-white transition">
          <input
            type="file"
            className="hidden"
            accept=".html,.txt"
            onChange={(e) => {
              if (e.target.files) {
                setAwrFile(e.target.files[0])
              }
            }}
          />

          {awrFile ? (
            <p className="font-medium">
              Selected: {awrFile.name}
            </p>
          ) : (
            <p className="text-gray-500 dark:text-gray-400">
              Click to upload AWR report (.html / .txt)
            </p>
          )}
        </label>

        {/* TOP Upload */}
        <label className="block border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-xl p-10 text-center mb-8 cursor-pointer hover:border-black dark:hover:border-white transition">
          <input
            type="file"
            className="hidden"
            accept=".txt"
            onChange={(e) => {
              if (e.target.files) {
                setTopFile(e.target.files[0])
              }
            }}
          />

          {topFile ? (
            <p className="font-medium">
              Selected: {topFile.name}
            </p>
          ) : (
            <p className="text-gray-500 dark:text-gray-400">
              Optional: Upload TOP command output (.txt)
            </p>
          )}
        </label>

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="px-6 py-3 bg-black text-white dark:bg-white dark:text-black rounded-xl hover:opacity-80 transition disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Run Health Check"}
        </button>

        {/* Result Section */}
        {score !== null && (
          <div className="mt-12 p-8 border border-gray-200 dark:border-gray-800 rounded-xl">
            <h2 className="text-2xl font-semibold mb-4">
              Health Score
            </h2>

            <div className="text-6xl font-bold mb-6">
              {score}%
            </div>

            {issues.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Detected Issues:</h3>
                <ul className="list-disc list-inside text-gray-500 dark:text-gray-400">
                  {issues.map((issue, index) => (
                    <li key={index}>{issue}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

      </div>
    </main>
  )
}
