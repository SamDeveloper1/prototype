"use client";

import React, { useState } from "react";
import { predictFakeNews } from "@/lib/api";
import { FakeNewsResponse } from "@/types/api";
import { RubberStamp } from "./RubberStamp";
import { Globe, FileText, Send, Sparkles, AlertCircle, ChevronDown, ChevronUp, Code2, Zap } from "lucide-react";
import confetti from "canvas-confetti";

export const FakeNewsDesk: React.FC = () => {
  const [mode, setMode] = useState<"text" | "url">("text");
  const [inputText, setInputText] = useState("");
  const [inputUrl, setInputUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<FakeNewsResponse | null>(null);
  const [showJson, setShowJson] = useState(false);

  // Quick Test Samples for Examiners
  const loadSample = (type: "real_text" | "fake_text" | "real_url") => {
    setError(null);
    if (type === "real_text") {
      setMode("text");
      setInputText(
        "The Reserve Bank of India has announced a 50 basis point repo rate hike in today's monetary policy committee meeting, citing inflation targets."
      );
    } else if (type === "fake_text") {
      setMode("text");
      setInputText(
        "BREAKING: Government announces direct 1 lakh rupee grant to all engineering college students who forward this message to 10 friends immediately."
      );
    } else {
      setMode("url");
      setInputUrl(
        "https://indianexpress.com/article/cities/ahmedabad/vadodara-narendra-pm-modi-inertia-swipe-upa-era-dedicated-freight-corridor-10868440/?ref=hometop_hp"
      );
    }
  };

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    const payload = mode === "text" ? { text: inputText } : { url: inputUrl };
    if (mode === "text" && (!inputText || inputText.trim().length < 5)) {
      setError("Please enter at least a complete sentence (5+ characters) to verify.");
      return;
    }
    if (mode === "url" && (!inputUrl || !inputUrl.startsWith("http"))) {
      setError("Please provide a valid web article URL starting with http:// or https://");
      return;
    }

    setLoading(true);
    try {
      const data = await predictFakeNews(payload);
      setResult(data);
      if (data.verdict === "Real News") {
        confetti({ particleCount: 35, spread: 60, origin: { y: 0.7 } });
      }
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred during prediction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-3 sm:px-4 py-6 sm:py-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
        {/* Left Column: Input Desk */}
        <div className="lg:col-span-5 bg-[#FAF8F5] border-2 border-[#CBC8B9] p-4 sm:p-6 shadow-xs rounded-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-[#CBC8B9] pb-3 mb-4">
              <span className="text-xs font-mono-meta font-bold uppercase tracking-wider text-[#353535]">
                Dispatch Submission Box
              </span>
              <span className="text-xs font-mono-meta text-[#D74108] font-bold bg-[#EDE8DF] px-2 py-0.5 rounded-xs border border-[#CBC8B9]">
                Model: BERT (97.02% F1)
              </span>
            </div>

            {/* Input Mode Selector */}
            <div className="flex rounded-xs bg-[#EAE4D9] p-1 mb-4 border border-[#CBC8B9]">
              <button
                type="button"
                onClick={() => setMode("text")}
                className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-mono-meta font-bold uppercase rounded-xs transition-all ${
                  mode === "text" ? "bg-[#FAF8F5] text-[#131112] shadow-xs" : "text-[#353535]"
                }`}
              >
                <FileText className="w-3.5 h-3.5" /> Plain Text Claim
              </button>
              <button
                type="button"
                onClick={() => setMode("url")}
                className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-mono-meta font-bold uppercase rounded-xs transition-all ${
                  mode === "url" ? "bg-[#FAF8F5] text-[#131112] shadow-xs" : "text-[#353535]"
                }`}
              >
                <Globe className="w-3.5 h-3.5" /> Web Article URL
              </button>
            </div>

            <form onSubmit={handleAnalyze} className="space-y-4">
              {mode === "text" ? (
                <div>
                  <label className="block text-xs font-headline font-bold uppercase tracking-wider mb-1 text-[#131112]">
                    Enter News Headline or Full Article Text:
                  </label>
                  <textarea
                    rows={6}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Paste news claim, social media rumor, or press statement here..."
                    className="w-full p-3 bg-[#EDE8DF]/60 border border-[#CBC8B9] rounded-xs text-sm font-headline text-[#131112] placeholder-[#737A87] focus:bg-[#FAF8F5] focus:outline-hidden focus:border-[#131112] focus:ring-1 focus:ring-[#131112] transition-all"
                  />
                </div>
              ) : (
                <div>
                  <label className="block text-xs font-headline font-bold uppercase tracking-wider mb-1 text-[#131112]">
                    Enter Article URL to Live Scrape:
                  </label>
                  <input
                    type="url"
                    value={inputUrl}
                    onChange={(e) => setInputUrl(e.target.value)}
                    placeholder="https://indianexpress.com/article/..."
                    className="w-full p-3 bg-[#EDE8DF]/60 border border-[#CBC8B9] rounded-xs text-sm font-mono-meta text-[#131112] placeholder-[#737A87] focus:bg-[#FAF8F5] focus:outline-hidden focus:border-[#131112] focus:ring-1 focus:ring-[#131112] transition-all"
                  />
                  <p className="mt-1.5 text-[11px] font-mono-meta text-[#353535]">
                    Supports Indian Express, PIB Releases, The Hindu, NDTV, Alt News, etc.
                  </p>
                </div>
              )}

              {error && (
                <div className="flex items-start gap-2 p-3 bg-red-50 border border-red-200 text-red-700 text-xs font-mono-meta rounded-xs">
                  <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full min-h-[46px] px-4 py-3 bg-[#131112] hover:bg-[#D74108] text-white text-xs sm:text-sm font-mono-meta font-bold uppercase tracking-wider sm:tracking-widest rounded-xs flex items-center justify-center gap-2.5 transition-all shadow-sm cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed text-center"
              >
                {loading ? (
                  <>
                    <span className="inline-block w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin shrink-0" />
                    <span className="truncate">Executing BERT Inference...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4 shrink-0" />
                    <span>Verify Claim & Print Edition</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Quick-Load Samples */}
          <div className="mt-6 pt-4 border-t border-[#CBC8B9]">
            <div className="text-[11px] font-mono-meta font-bold uppercase tracking-wider text-[#353535] mb-2 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-[#D74108]" /> One-Click Examiner Benchmarks:
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => loadSample("real_text")}
                className="text-[11px] font-mono-meta px-2.5 py-1 bg-[#EDE8DF] hover:bg-[#DFD9CE] text-[#131112] rounded-xs border border-[#CBC8B9] transition-all font-semibold"
              >
                ✓ Real News Text
              </button>
              <button
                type="button"
                onClick={() => loadSample("fake_text")}
                className="text-[11px] font-mono-meta px-2.5 py-1 bg-[#EDE8DF] hover:bg-[#DFD9CE] text-[#D74108] rounded-xs border border-[#CBC8B9] transition-all font-semibold"
              >
                ⚠ Viral Fake Claim
              </button>
              <button
                type="button"
                onClick={() => loadSample("real_url")}
                className="text-[11px] font-mono-meta px-2.5 py-1 bg-[#EDE8DF] hover:bg-[#DFD9CE] text-[#1E5E41] rounded-xs border border-[#CBC8B9] transition-all font-semibold"
              >
                📰 Live Express URL
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Front Page Result Card */}
        <div className="lg:col-span-7 bg-[#FAF8F5] border-2 border-[#131112] p-4 sm:p-6 md:p-8 shadow-xs rounded-xs flex flex-col justify-between relative overflow-hidden">
          {result ? (
            <div>
              {/* Card Broadsheet Header */}
              <div className="border-b-2 border-[#131112] pb-2 flex items-center justify-between text-xs font-mono-meta text-[#353535]">
                <span>SPECIAL FORENSIC REPORT</span>
                <span className="flex items-center gap-1 text-[#131112] font-bold">
                  <Zap className="w-3 h-3 text-[#D74108] shrink-0" /> {result.inference_time_ms}ms
                </span>
              </div>

              {/* Headline */}
              <div className="mt-3 sm:mt-4 mb-4 sm:mb-6">
                <h2 className="text-xl sm:text-2xl md:text-3xl font-headline font-bold text-[#131112] leading-tight">
                  {result.headline_analyzed || "Disinformation Assessment Summary"}
                </h2>
                <div className="mt-1 text-xs font-mono-meta text-[#353535]">
                  Analyzed via {result.model_used || "Fine-Tuned BERT Transformer"} · Input: {result.input_type.toUpperCase()}
                </div>
              </div>

              {/* Centerpiece: Rubber Stamp & Confidence Meter */}
              <div className="p-4 sm:p-6 bg-[#EDE8DF] border border-[#CBC8B9] rounded-xs my-4 sm:my-6 flex flex-col sm:flex-row items-center justify-center sm:justify-around gap-6">
                {/* Physics Animated Rubber Stamp */}
                <RubberStamp
                  verdict={result.verdict}
                  confidence={result.confidence_score}
                  type="fakenews"
                />

                {/* Circular / Radial Confidence Meter */}
                <div className="flex flex-col items-center justify-center">
                  <div className="relative w-24 h-24 flex items-center justify-center">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle
                        cx="48"
                        cy="48"
                        r="38"
                        stroke="#CBC8B9"
                        strokeWidth="8"
                        fill="transparent"
                      />
                      <circle
                        cx="48"
                        cy="48"
                        r="38"
                        stroke={result.verdict === "Real News" ? "#1E5E41" : "#D74108"}
                        strokeWidth="8"
                        strokeDasharray={2 * Math.PI * 38}
                        strokeDashoffset={
                          2 * Math.PI * 38 * (1 - result.confidence_score / 100)
                        }
                        strokeLinecap="round"
                        fill="transparent"
                        className="transition-all duration-1000 ease-out"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center justify-center text-center">
                      <span className="text-xl font-headline font-bold text-[#131112]">
                        {result.confidence_score.toFixed(0)}%
                      </span>
                      <span className="text-[9px] font-mono-meta text-[#353535]">
                        CONFIDENCE
                      </span>
                    </div>
                  </div>
                  <div className="mt-1 text-[11px] font-mono-meta font-bold text-[#353535]">
                    {result.confidence_score >= 80
                      ? "High Statistical Certainty"
                      : "Moderate Significance"}
                  </div>
                </div>
              </div>

              {/* Scraped Article Preview / Context */}
              {result.preview_text && (
                <div className="mt-4">
                  <div className="text-xs font-mono-meta font-bold uppercase tracking-wider text-[#353535] mb-1">
                    Scraped Article Lead Excerpt:
                  </div>
                  <div className="p-3 bg-[#EDE8DF]/50 border-l-2 border-[#131112] text-xs font-headline italic text-[#353535] leading-relaxed">
                    "{result.preview_text}"
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full min-h-[350px] flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-[#CBC8B9] rounded-xs bg-[#FAF8F5]">
              <div className="w-16 h-16 rounded-full bg-[#EDE8DF] flex items-center justify-center text-[#353535] mb-3">
                <FileText className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-headline font-bold text-[#131112]">
                Front Page Verification Awaiting Input
              </h3>
              <p className="mt-1 max-w-sm text-xs font-headline italic text-[#353535]">
                Submit a raw news story or paste a live URL from the left panel to execute
                BERT forensic classification.
              </p>
            </div>
          )}

          {/* Expandable "Inspect Raw API JSON" Drawer */}
          {result && (
            <div className="mt-6 pt-4 border-t border-[#CBC8B9]">
              <button
                type="button"
                onClick={() => setShowJson(!showJson)}
                className="flex items-center gap-2 text-xs font-mono-meta text-[#353535] hover:text-[#131112] transition-colors"
              >
                <Code2 className="w-4 h-4 text-[#D74108]" />
                <span className="font-semibold">
                  {showJson ? "Hide API Raw Log" : "Inspect Raw API JSON (FastAPI Output)"}
                </span>
                {showJson ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>

              {showJson && (
                <pre className="mt-3 p-3 bg-[#131112] text-emerald-400 font-mono-meta text-[11px] rounded-xs overflow-x-auto max-h-48 border border-black shadow-inner">
                  {JSON.stringify(result, null, 2)}
                </pre>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
