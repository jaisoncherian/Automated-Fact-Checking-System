import React, { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

const VERDICT_COLORS = {
  "true": { background: "#e8f5e9", color: "#2e7d32", label: "✓ True" },
  "fake": { background: "#ffebee", color: "#c62828", label: "✗ Fake" },
  "suspicious": { background: "#fff8e1", color: "#e65100", label: "⚠ Suspicious" },
  "unknown": { background: "#f3f4f6", color: "#555555", label: "? Unknown" }
}

export default function FactChecker() {
  const [text, setText] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleCheck() {
    setLoading(true)
    setError("")
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/check-multilingual`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      })

      if (!response.ok) {
        throw new Error("Server error. Is the API running?")
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || "An error occurred")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ color: "#333", marginBottom: "10px" }}>Vernacular Fact Checker</h1>
      <p style={{ color: "#666", marginBottom: "20px" }}>
        Enter text in any language — Malayalam, Hindi, Tamil, English...
      </p>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type or paste your claim here..."
        style={{
          width: "100%",
          minHeight: "120px",
          padding: "12px",
          fontSize: "14px",
          border: "1px solid #ddd",
          borderRadius: "4px",
          boxSizing: "border-box",
          fontFamily: "Arial, sans-serif",
          resize: "vertical"
        }}
      />

      <button
        onClick={handleCheck}
        disabled={loading || !text.trim()}
        style={{
          marginTop: "15px",
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: loading || !text.trim() ? "#ccc" : "#2196F3",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: loading || !text.trim() ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Checking..." : "Check Facts"}
      </button>

      {error && (
        <div style={{ color: "red", marginTop: "15px", padding: "10px", backgroundColor: "#ffe0e0", borderRadius: "4px" }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: "30px", backgroundColor: "#f9f9f9", padding: "20px", borderRadius: "4px", border: "1px solid #eee" }}>
          <h2 style={{ color: "#333", marginTop: "0" }}>Results</h2>

          <p style={{ color: "#666", marginBottom: "5px" }}>
            <strong>Language detected:</strong> {result.language_name} ({result.detected_language})
          </p>

          {result.detected_language !== "en" && (
            <p style={{ color: "#666", marginBottom: "5px" }}>
              <strong>Translation to English:</strong> {result.english_translation}
            </p>
          )}

          <p style={{ color: "#666", marginBottom: "20px" }}>
            <strong>Claims found:</strong> {result.claims_found}
          </p>

          {result.results && result.results.length > 0 ? (
            <div>
              {result.results.map((item, index) => {
                const verdictStyle = VERDICT_COLORS[item.verdict] || VERDICT_COLORS["unknown"]
                return (
                  <div key={index} style={{
                    marginBottom: "15px",
                    padding: "15px",
                    backgroundColor: "white",
                    border: "1px solid #ddd",
                    borderRadius: "4px"
                  }}>
                    <p style={{ fontStyle: "italic", color: "#555", marginTop: "0", marginBottom: "10px", fontSize: "14px" }}>
                      {item.claim}
                    </p>

                    <div style={{
                      display: "inline-block",
                      padding: "6px 12px",
                      backgroundColor: verdictStyle.background,
                      color: verdictStyle.color,
                      borderRadius: "20px",
                      fontSize: "14px",
                      fontWeight: "bold",
                      marginBottom: "10px"
                    }}>
                      {verdictStyle.label}
                    </div>

                    <p style={{ color: "#333", marginTop: "10px", marginBottom: "5px" }}>
                      {item.explanation}
                    </p>

                    <p style={{ color: "#888", fontSize: "13px", marginTop: "5px" }}>
                      Confidence: {(item.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                )
              })}
            </div>
          ) : (
            <p style={{ color: "#999" }}>No claims extracted from the text.</p>
          )}
        </div>
      )}
    </div>
  )
}
