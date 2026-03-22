import { useState } from "react";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const checkFact = async () => {
    if (!text.trim()) {
      setError("Please enter a claim to check");
      return;
    }
    
    setLoading(true);
    setError(null);
    setResult(null); // Clear previous result

    try {
      const url = `http://127.0.0.1:8000/check?text=${encodeURIComponent(text)}`;
      console.log("📡 Sending request to:", url);
      
      const res = await fetch(url, { method: "POST" });
      const data = await res.json();
      
      console.log("✅ FULL RESPONSE RECEIVED:", data);
      console.log("   - input:", data.input);
      console.log("   - result:", data.result);
      console.log("   - confidence:", data.confidence);
      
      setResult(data);
    } catch (err) {
      console.error("❌ FETCH ERROR:", err.message);
      setError("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      checkFact();
    }
  };

  const getVerdictInfo = () => {
    console.log("=== getVerdictInfo called ===");
    console.log("result:", result);
    console.log("result.result:", result?.result);
    
    if (!result || result.result === undefined || result.result === null) {
      console.log("No result or empty result");
      return {
        label: "? WAITING",
        bgColor: "#6b7a8d",
        textColor: "#cbd5e1",
        message: "Enter a claim"
      };
    }

    const rawVerdict = result.result;
    const verdict = String(rawVerdict).toLowerCase().trim();
    
    console.log("Raw verdict:", rawVerdict);
    console.log("Processed verdict:", verdict);
    console.log("Type:", typeof verdict);

    if (verdict === "true") {
      console.log("MATCH: TRUE");
      return {
        label: "✓ TRUE",
        bgColor: "#10b981",
        textColor: "#86efac",
        message: "This claim matches verified facts."
      };
    } else if (verdict === "false") {
      console.log("MATCH: FALSE");
      return {
        label: "✗ FALSE",
        bgColor: "#ef4444",
        textColor: "#fca5a5",
        message: "This claim contradicts verified facts."
      };
    } else if (verdict === "suspicious") {
      console.log("MATCH: SUSPICIOUS");
      return {
        label: "⚠ SUSPICIOUS",
        bgColor: "#f59e0b",
        textColor: "#fcd34d",
        message: "This claim is partially similar but may contain errors."
      };
    } else if (verdict === "unknown") {
      console.log("MATCH: UNKNOWN");
      return {
        label: "? UNKNOWN",
        bgColor: "#6b7a8d",
        textColor: "#cbd5e1",
        message: "Unable to determine. Confidence too low."
      };
    }

    console.log("NO MATCH - showing fallback");
    return {
      label: `? ${verdict.toUpperCase()}`,
      bgColor: "#8b5cf6",
      textColor: "#f3e8ff",
      message: `Result: ${verdict}`
    };
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #020617, #0f172a)",
      color: "white",
      padding: "40px",
      fontFamily: "sans-serif"
    }}>

      {/* NAVBAR */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        marginBottom: "50px",
        alignItems: "center"
      }}>
        <h2 style={{ color: "#00f5d4", fontSize: "28px", margin: 0 }}>🔍 VeriNews AI</h2>
        <a 
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            background: "#00f5d4",
            color: "black",
            padding: "10px 20px",
            borderRadius: "8px",
            border: "none",
            textDecoration: "none",
            fontWeight: "bold",
            cursor: "pointer"
          }}>
          API Docs →
        </a>
      </div>

      {/* HERO */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "50px",
        alignItems: "flex-start"
      }}>

        {/* LEFT SECTION */}
        <div>
          <h1 style={{ 
            fontSize: "56px", 
            fontWeight: "bold", 
            lineHeight: "1.2", 
            marginBottom: "20px",
            marginTop: 0
          }}>
            Detect Fake News <br />
            with <span style={{ color: "#00f5d4" }}>AI Precision</span> <br />
            In Real Time.
          </h1>

          <p style={{ 
            color: "#94a3b8", 
            marginTop: "20px", 
            fontSize: "16px", 
            lineHeight: "1.6" 
          }}>
            AI-powered fact checking using semantic similarity and Sentence Transformers. Get instant verdicts with confidence scores.
          </p>

          <textarea
            placeholder="Enter a news claim to analyze..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyPress={handleKeyPress}
            style={{
              width: "100%",
              marginTop: "25px",
              padding: "14px",
              borderRadius: "8px",
              background: "#1e293b",
              color: "white",
              border: "1px solid #334155",
              fontSize: "14px",
              fontFamily: "inherit",
              minHeight: "120px",
              resize: "vertical",
              boxSizing: "border-box"
            }}
          />

          <div style={{ display: "flex", gap: "12px", marginTop: "14px" }}>
            <button
              onClick={checkFact}
              disabled={loading}
              style={{
                flex: 1,
                background: loading ? "#666" : "#00f5d4",
                color: "black",
                padding: "12px 20px",
                borderRadius: "8px",
                border: "none",
                fontWeight: "bold",
                fontSize: "16px",
                cursor: loading ? "not-allowed" : "pointer",
                transition: "all 0.2s"
              }}
            >
              {loading ? "⏳ Analyzing..." : "Analyze Claim"}
            </button>
            <button
              onClick={() => {
                setText("");
                setResult(null);
                setError(null);
              }}
              style={{
                padding: "12px 20px",
                background: "#334155",
                color: "white",
                border: "none",
                borderRadius: "8px",
                fontWeight: "bold",
                cursor: "pointer",
                transition: "all 0.2s"
              }}
            >
              Clear
            </button>
          </div>

          {error && (
            <p style={{ color: "#ff6b6b", marginTop: "14px", fontSize: "14px" }}>
              ❌ {error}
            </p>
          )}
        </div>

        {/* RIGHT SECTION - LIVE ANALYSIS CARD */}
        <div style={{
          background: "#1e293b",
          padding: "28px",
          borderRadius: "12px",
          border: "1px solid #334155",
          minHeight: "400px",
          display: "flex",
          flexDirection: "column",
          justifyContent: result ? "flex-start" : "center",
          alignItems: result ? "stretch" : "center"
        }}>
          <h3 style={{ 
            color: "#94a3b8", 
            fontSize: "13px", 
            margin: "0 0 20px 0", 
            textTransform: "uppercase",
            letterSpacing: "0.1em"
          }}>
            🔎 Live Analysis
          </h3>

          {result ? (() => {
            const info = getVerdictInfo();
            console.log("RENDERING VERDICT:", info);
            return (
            <div style={{ width: "100%" }}>
              {/* Input Display */}
              <div style={{
                background: "#0f172a",
                padding: "14px",
                borderRadius: "8px",
                marginBottom: "20px",
                fontSize: "13px",
                color: "#cbd5e1",
                lineHeight: "1.6",
                maxHeight: "100px",
                overflow: "auto",
                borderLeft: "3px solid #00f5d4"
              }}>
                <p style={{ margin: 0 }}>"{result.input}"</p>
              </div>

              {/* Verdict Badge + Confidence - BULLETPROOF VERSION */}
              <div style={{
                display: "flex",
                gap: "14px",
                marginBottom: "20px",
                alignItems: "center",
                justifyContent: "space-between"
              }}>
                {/* BADGE */}
                <div style={{
                  backgroundColor: info.bgColor || "#6b7a8d",
                  padding: "12px 20px",
                  borderRadius: "8px",
                  fontWeight: "bold",
                  fontSize: "15px",
                  textTransform: "uppercase",
                  letterSpacing: "0.1em",
                  color: "white",
                  minWidth: "150px",
                  textAlign: "center",
                  border: "2px solid " + (info.bgColor || "#6b7a8d"),
                  boxShadow: `0 0 10px ${info.bgColor || "#6b7a8d"}80`
                }}>
                  {info.label || "? UNKNOWN"}
                </div>

                {/* CONFIDENCE */}
                <div style={{ textAlign: "right" }}>
                  <p style={{ fontSize: "12px", color: "#94a3b8", margin: "0 0 4px 0" }}>
                    Confidence
                  </p>
                  <p style={{ fontSize: "24px", fontWeight: "bold", margin: 0, color: info.bgColor || "#6b7a8d" }}>
                    {(result.confidence * 100).toFixed(0)}%
                  </p>
                </div>
              </div>

              {/* Progress Bar */}
              <div style={{ marginBottom: "20px" }}>
                <div style={{ fontSize: "12px", color: "#64748b", marginBottom: "8px" }}>
                  Confidence Score: {(result.confidence * 100).toFixed(2)}%
                </div>
                <div style={{
                  width: "100%",
                  height: "8px",
                  background: "#334155",
                  borderRadius: "10px",
                  overflow: "hidden",
                  border: "1px solid #475569"
                }}>
                  <div style={{
                    width: `${result.confidence * 100}%`,
                    height: "8px",
                    backgroundColor: info.bgColor || "#6b7a8d",
                    borderRadius: "10px",
                    transition: "width 0.6s ease"
                  }}></div>
                </div>
              </div>

              {/* Message */}
              <div style={{
                background: "#0f172a",
                padding: "14px",
                borderRadius: "8px",
                fontSize: "13px",
                lineHeight: "1.6",
                color: info.textColor || "#cbd5e1"
              }}>
                <p style={{ margin: 0 }}>
                  {info.message || "Verdict received"}
                </p>
              </div>
            </div>
            );
          })() : (
            <div style={{ textAlign: "center" }}>
              <p style={{ fontSize: "16px", color: "#64748b" }}>
                Enter a claim and click "Analyze" to see results
              </p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}