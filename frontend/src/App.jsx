import { useEffect, useState } from "react";
import { api } from "./services/api";

import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend
} from "recharts";


export default function App() {
  const [mode, setMode] = useState("upload");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const [transcript, setTranscript] = useState("");
  const [emotion, setEmotion] = useState(null);
  const [confidence, setConfidence] = useState(null);

  const [theme, setTheme] = useState("dark");

  const [timeline, setTimeline] = useState([]);


  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  async function handleAnalyze() {
    if (!file) return alert("Please select an audio file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setTranscript("");
      setEmotion(null);
      setConfidence(null);

      const res = await api.post("/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setTimeline(res.data.emotion_timeline || []);
      setTranscript(res.data.transcript);
      setEmotion(res.data.emotion.top_emotion);
      setConfidence(res.data.confidence);
    } catch (err) {
      console.error(err);
      alert("Analysis failed. Check backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen p-6 max-w-[1400px] mx-auto">
      {/* HEADER */}
      <header className="mb-8 flex items-center justify-between">
        <div>
          <h1
            className="text-4xl font-semibold"
            style={{ fontFamily: "Clash Display" }}
          >
            Emotion Voice AI
          </h1>
          <p className="text-[var(--text-dim)] mt-1">
            Signal-level analysis of human speech.
          </p>
        </div>

        {/* THEME TOGGLE */}
        <button
          onClick={() => setTheme(theme === "light" ? "dark" : "light")}
          className="btn-secondary px-4 py-2"
        >
          {theme === "light" ? "Dark Mode" : "Light Mode"}
        </button>
      </header>

      {/* MODE SWITCH */}
      <div className="flex gap-3 mb-6">
        <button
          onClick={() => setMode("upload")}
          className={`px-4 py-2 ${
            mode === "upload" ? "btn-primary" : "btn-secondary"
          }`}
        >
          Upload Audio
        </button>
        <button
          onClick={() => setMode("live")}
          className={`px-4 py-2 ${
            mode === "live" ? "btn-primary" : "btn-secondary"
          }`}
        >
          Live Mic (V2)
        </button>
      </div>

      {/* MAIN GRID */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* INPUT */}
        <div className="panel p-5">
          <h2 className="text-lg mb-4">Input</h2>

          <div className="space-y-4">
            <input
              id="audio-upload"
              type="file"
              accept="audio/*"
              className="hidden"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <label htmlFor="audio-upload" className="upload-box block">
              {file ? (
                <div>Selected: {file.name}</div>
              ) : (
                <div className="text-[var(--text-dim)]">
                  Click to select an audio file
                </div>
              )}
            </label>

            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full py-2 btn-primary disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </div>
        </div>

        {/* TRANSCRIPT */}
        <div className="md:col-span-2 panel p-5">
          <h2 className="text-lg mb-4">Transcript</h2>

          <div className="h-[320px] overflow-auto p-4 rounded text-sm leading-relaxed">
            {transcript ? (
              transcript
            ) : (
              <div className="empty-state">
                {loading
                  ? "Processing audio…"
                  : "No transcript yet. Upload an audio file to begin."}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* RESULTS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        {/* EMOTION */}
        <div className="panel p-5">
          <h2 className="text-lg mb-2">Emotion</h2>
          {emotion ? (
            <div className="text-xl">
              {emotion.label} ({(emotion.score * 100).toFixed(1)}%)
            </div>
          ) : (
            <div className="empty-state">
              {loading ? "Analyzing emotion…" : "No result yet"}
            </div>
          )}
        </div>

        {/* CONFIDENCE */}
        <div className="panel p-5">
          <h2 className="text-lg mb-2">Confidence</h2>
          {confidence ? (
            <div>
              <div className="text-2xl mb-2">{confidence.score}%</div>
              <div className="h-2 rounded bg-black/10 dark:bg-white/10 overflow-hidden">
                <div
                  className="h-full"
                  style={{
                    width: `${confidence.score}%`,
                    background: "var(--accent)",
                  }}
                />
              </div>
              <div className="text-sm text-[var(--text-dim)] mt-2">
                Level: {confidence.level}
              </div>
            </div>
          ) : (
            <div className="empty-state">
              {loading ? "Computing confidence…" : "No result yet"}
            </div>
          )}
        </div>

        {/* TIMELINE */}
        <div className="panel p-5">
          <h2 className="text-lg mb-2">Emotion Timeline</h2>

          {timeline.length > 0 ? (
            <div style={{ width: "100%", height: 250 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={timeline}>
                  <XAxis dataKey="time" tickFormatter={(v) => `${v}s`} />
                  <YAxis domain={[0, 1]} />
                  <Tooltip />
                  <Legend />

                  <Line type="monotone" dataKey="calm" stroke="#3b82f6" dot={false} />
                  <Line type="monotone" dataKey="happy" stroke="#22c55e" dot={false} />
                  <Line type="monotone" dataKey="angry" stroke="#ef4444" dot={false} />
                  <Line type="monotone" dataKey="sad" stroke="#6366f1" dot={false} />
                  <Line type="monotone" dataKey="fear" stroke="#f59e0b" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="empty-state">
              No timeline data yet
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
