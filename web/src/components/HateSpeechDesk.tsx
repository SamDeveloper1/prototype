"use client";

import React, { useState, useRef } from "react";
import { predictHateSpeech, predictHateSpeechMedia } from "@/lib/api";
import { HateSpeechResponse } from "@/types/api";
import { RubberStamp } from "./RubberStamp";
import { Mic, FileText, UploadCloud, Send, Sparkles, AlertCircle, ChevronDown, ChevronUp, Code2, Zap, Volume2, ShieldCheck } from "lucide-react";

export const HateSpeechDesk: React.FC = () => {
  const [mode, setMode] = useState<"text" | "media">("text");
  const [inputText, setInputText] = useState("");
  const [mediaFile, setMediaFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<HateSpeechResponse | null>(null);
  const [showJson, setShowJson] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Quick Test Samples for Examiners
  const loadSample = (type: "safe" | "hostile") => {
    setError(null);
    setMode("text");
    if (type === "safe") {
      setInputText(
        "Have a wonderful day everyone! Wishing all students the very best of luck with their final year engineering project presentations."
      );
    } else {
      setInputText(
        "These migrants and outsiders are ruining our culture and heritage. They must be kicked out of the country immediately without mercy."
      );
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setMediaFile(file);
      setError(null);
    }
  };

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (mode === "text") {
      if (!inputText || inputText.trim().length < 3) {
        setError("Please enter at least 3 characters to analyze discourse toxicity.");
        return;
      }
      setLoading(true);
      try {
        const data = await predictHateSpeech({ text: inputText });
        setResult(data);
      } catch (err: any) {
        setError(err.message || "An unexpected error occurred during analysis.");
      } finally {
        setLoading(false);
      }
    } else {
      if (!mediaFile) {
        setError("Please select an audio (.mp3, .wav) or video (.mp4, .mov) file to transcribe and analyze.");
        return;
      }
      setLoading(true);
      try {
        const data = await predictHateSpeechMedia(mediaFile);
        setResult(data);
      } catch (err: any) {
        setError(err.message || "An error occurred during audio/video transcription.");
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Moderation Input Desk */}
        <div className="lg:col-span-5 bg-[#FFFFFF] border-2 border-[#E2DBD0] p-6 shadow-sm rounded-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-[#EBE5DA] pb-3 mb-4">
              <span className="text-xs font-mono-meta font-bold uppercase tracking-wider text-[#6B7280]">
                Toxicity Intake Desk
              </span>
              <span className="text-xs font-mono-meta text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-xs border border-emerald-200 flex items-center gap-1">
                <ShieldCheck className="w-3 h-3" /> Zero-Curse Filter
              </span>
            </div>

            {/* Input Mode Selector */}
            <div className="flex rounded-xs bg-[#F3EFE6] p-1 mb-4 border border-[#DDD5C7]">
              <button
                type="button"
                onClick={() => setMode("text")}
                className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-mono-meta font-bold uppercase rounded-xs transition-all ${
                  mode === "text" ? "bg-[#FFFFFF] text-[#1C1E21] shadow-xs" : "text-[#71717A]"
                }`}
              >
                <FileText className="w-3.5 h-3.5" /> Text Discourse
              </button>
              <button
                type="button"
                onClick={() => setMode("media")}
                className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-mono-meta font-bold uppercase rounded-xs transition-all ${
                  mode === "media" ? "bg-[#FFFFFF] text-[#1C1E21] shadow-xs" : "text-[#71717A]"
                }`}
              >
                <Mic className="w-3.5 h-3.5" /> Audio / Video File
              </button>
            </div>

            <form onSubmit={handleAnalyze} className="space-y-4">
              {mode === "text" ? (
                <div>
                  <label className="block text-xs font-headline font-bold uppercase tracking-wider mb-1 text-[#374151]">
                    Enter Social Comment or Public Statement:
                  </label>
                  <textarea
                    rows={6}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Enter social media comment, community post, or statement to evaluate hostility..."
                    className="w-full p-3 bg-[#FAF8F5] border border-[#DDD5C7] rounded-xs text-sm font-headline text-[#1C1E21] placeholder-[#9CA3AF] focus:bg-[#FFFFFF] focus:outline-hidden focus:border-[#1C1E21] focus:ring-1 focus:ring-[#1C1E21] transition-all"
                  />
                </div>
              ) : (
                <div>
                  <label className="block text-xs font-headline font-bold uppercase tracking-wider mb-1 text-[#374151]">
                    Upload Media File (Whisper Automatic Transcription):
                  </label>
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    className="w-full p-6 border-2 border-dashed border-[#DDD5C7] hover:border-[#1C1E21] bg-[#FAF8F5] rounded-xs text-center cursor-pointer transition-all flex flex-col items-center justify-center"
                  >
                    <UploadCloud className="w-8 h-8 text-[#9CA3AF] mb-2" />
                    <span className="text-xs font-mono-meta font-bold text-[#1C1E21]">
                      {mediaFile ? mediaFile.name : "Click to browse or drop Audio/Video file"}
                    </span>
                    <span className="text-[10px] font-mono-meta text-[#6B7280] mt-1">
                      {mediaFile
                        ? `${(mediaFile.size / (1024 * 1024)).toFixed(2)} MB · Ready for Whisper`
                        : "Supports: .mp3, .wav, .m4a, .mp4, .mov, .mkv (Max 50MB)"}
                    </span>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="audio/*,video/*"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                  </div>
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
                className="w-full py-3 bg-[#1C1E21] hover:bg-[#000000] text-[#FAF8F5] text-xs font-mono-meta font-bold uppercase tracking-widest rounded-xs flex items-center justify-center gap-2 transition-all shadow-sm cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <span className="inline-block w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                    <span>{mode === "media" ? "Whisper Transcribing & BERT Evaluating..." : "Analyzing Civility..."}</span>
                  </>
                ) : (
                  <>
                    <Send className="w-3.5 h-3.5" />
                    <span>{mode === "media" ? "Transcribe & Assess Hostility" : "Inspect Content & Log Verdict"}</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Quick-Load Samples */}
          <div className="mt-6 pt-4 border-t border-[#EBE5DA]">
            <div className="text-[11px] font-mono-meta font-bold uppercase tracking-wider text-[#6B7280] mb-2 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-amber-500" /> Academic Benchmark Samples:
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => loadSample("safe")}
                className="text-[11px] font-mono-meta px-2.5 py-1 bg-[#F3EFE6] hover:bg-[#EAE4D7] text-[#0F766E] rounded-xs border border-[#DDD5C7] transition-all"
              >
                ✔ Safe / Respectful Discourse
              </button>
              <button
                type="button"
                onClick={() => loadSample("hostile")}
                className="text-[11px] font-mono-meta px-2.5 py-1 bg-[#F3EFE6] hover:bg-[#EAE4D7] text-[#B91C1C] rounded-xs border border-[#DDD5C7] transition-all"
              >
                ⛔ Targeted Hostility Claim
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Moderation Verdict Card */}
        <div className="lg:col-span-7 bg-[#FFFFFF] border-2 border-[#1C1E21] p-6 md:p-8 shadow-md rounded-xs flex flex-col justify-between relative overflow-hidden">
          {result ? (
            <div>
              {/* Card Broadsheet Header */}
              <div className="border-b-2 border-[#1C1E21] pb-2 flex items-center justify-between text-xs font-mono-meta text-[#6B7280]">
                <span>COMMUNITY SAFETY & HOSTILITY OBSERVATION</span>
                <span className="flex items-center gap-1 text-[#1C1E21] font-bold">
                  <Zap className="w-3 h-3 text-amber-500" /> {result.inference_time_ms}ms
                </span>
              </div>

              {/* Title & Metadata */}
              <div className="mt-4 mb-6">
                <h2 className="text-2xl md:text-3xl font-headline font-bold text-[#1C1E21] leading-tight">
                  Toxicity & Civility Assessment
                </h2>
                <div className="mt-1 text-xs font-mono-meta text-[#6B7280]">
                  Engine: {result.model_used || "Fine-Tuned BERT (78.08% F1)"} · Input Medium: {result.input_type.toUpperCase()}
                </div>
              </div>

              {/* Centerpiece: Rubber Stamp & Confidence Meter */}
              <div className="p-6 bg-[#FAF8F5] border border-[#DDD5C7] rounded-xs my-6 flex flex-col md:flex-row items-center justify-around gap-6">
                {/* Physics Animated Rubber Stamp */}
                <RubberStamp
                  verdict={result.verdict}
                  confidence={result.confidence_score}
                  type="hatespeech"
                />

                {/* Circular / Radial Confidence Meter */}
                <div className="flex flex-col items-center justify-center">
                  <div className="relative w-24 h-24 flex items-center justify-center">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle
                        cx="48"
                        cy="48"
                        r="38"
                        stroke="#E5E0D8"
                        strokeWidth="8"
                        fill="transparent"
                      />
                      <circle
                        cx="48"
                        cy="48"
                        r="38"
                        stroke={result.verdict.includes("Safe") ? "#0D9488" : "#B91C1C"}
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
                      <span className="text-xl font-headline font-bold text-[#1C1E21]">
                        {result.confidence_score.toFixed(0)}%
                      </span>
                      <span className="text-[9px] font-mono-meta text-[#6B7280]">
                        CONFIDENCE
                      </span>
                    </div>
                  </div>
                  <div className="mt-1 text-[11px] font-mono-meta font-bold text-[#4B5563]">
                    {result.verdict.includes("Safe") ? "Safe For Publication" : "Violates Civility Standards"}
                  </div>
                </div>
              </div>

              {/* Whisper Speech Transcript Box (If Audio/Video) */}
              {result.transcribed_text && (
                <div className="mt-4 mb-3">
                  <div className="text-xs font-mono-meta font-bold uppercase tracking-wider text-blue-800 mb-1 flex items-center gap-1.5">
                    <Volume2 className="w-3.5 h-3.5" /> OpenAI Whisper Spoken Transcript:
                  </div>
                  <div className="p-3 bg-blue-50/60 border-l-2 border-blue-600 text-xs font-mono-meta text-[#1E3A8A] leading-relaxed">
                    "{result.transcribed_text}"
                  </div>
                </div>
              )}

              {/* Text Preview */}
              {result.preview_text && !result.transcribed_text && (
                <div className="mt-4">
                  <div className="text-xs font-mono-meta font-bold uppercase tracking-wider text-[#6B7280] mb-1">
                    Evaluated Discourse Snippet:
                  </div>
                  <div className="p-3 bg-[#FDFCFA] border-l-2 border-[#1C1E21] text-xs font-headline italic text-[#374151] leading-relaxed">
                    "{result.preview_text}"
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full min-h-[350px] flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-[#DDD5C7] rounded-xs">
              <div className="w-16 h-16 rounded-full bg-[#F3EFE6] flex items-center justify-center text-[#9CA3AF] mb-3">
                <Mic className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-headline font-bold text-[#1C1E21]">
                Moderation Intake Awaiting Input
              </h3>
              <p className="mt-1 max-w-sm text-xs font-headline italic text-[#6B7280]">
                Submit public discourse text or upload an audio/video file to extract speech
                via OpenAI Whisper and detect toxicity.
              </p>
            </div>
          )}

          {/* Expandable "Inspect Raw API JSON" Drawer */}
          {result && (
            <div className="mt-6 pt-4 border-t border-[#EBE5DA]">
              <button
                type="button"
                onClick={() => setShowJson(!showJson)}
                className="flex items-center gap-2 text-xs font-mono-meta text-[#6B7280] hover:text-[#1C1E21] transition-colors"
              >
                <Code2 className="w-4 h-4 text-blue-600" />
                <span className="font-semibold">
                  {showJson ? "Hide API Raw Log" : "Inspect Raw API JSON (FastAPI Output)"}
                </span>
                {showJson ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>

              {showJson && (
                <pre className="mt-3 p-3 bg-[#1C1E21] text-emerald-400 font-mono-meta text-[11px] rounded-xs overflow-x-auto max-h-48 border border-black shadow-inner">
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
