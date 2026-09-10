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
    <div className="w-full max-w-7xl mx-auto px-3 sm:px-4 py-6 sm:py-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
        {/* Left Column: Moderation Input Desk */}
        <div className="lg:col-span-5 bg-[#FAF8F5] border-2 border-[#CBC8B9] p-4 sm:p-6 shadow-xs rounded-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-[#CBC8B9] pb-3 mb-4">
              <span className="text-xs font-mono-meta font-bold uppercase tracking-wider text-[#353535]">
                Toxicity Intake Desk
              </span>
              <span className="text-xs font-mono-meta text-[#1E5E41] font-bold bg-[#EDE8DF] px-2 py-0.5 rounded-xs border border-[#CBC8B9] flex items-center gap-1">
                <ShieldCheck className="w-3 h-3 text-[#1E5E41]" /> Zero-Curse Filter
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
                <FileText className="w-3.5 h-3.5" /> Text Discourse
              </button>
              <button
                type="button"
                onClick={() => setMode("media")}
                className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-mono-meta font-bold uppercase rounded-xs transition-all ${
                  mode === "media" ? "bg-[#FAF8F5] text-[#131112] shadow-xs" : "text-[#353535]"
                }`}
              >
                <Mic className="w-3.5 h-3.5" /> Audio / Video File
              </button>
            </div>

            <form onSubmit={handleAnalyze} className="space-y-4">
              {mode === "text" ? (
                <div>
                  <label className="block text-xs font-headline font-bold uppercase tracking-wider mb-1 text-[#131112]">
                    Enter Social Comment or Public Statement:
                  </label>
                  <textarea
                    rows={6}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Enter social media comment, community post, or statement to evaluate hostility..."
                    className="w-full p-3 bg-[#EDE8DF]/60 border border-[#CBC8B9] rounded-xs text-sm font-headline text-[#131112] placeholder-[#737A87] focus:bg-[#FAF8F5] focus:outline-hidden focus:border-[#131112] focus:ring-1 focus:ring-[#131112] transition-all"
                  />
                </div>
              ) : (
                <div>
                  <label className="block text-xs font-headline font-bold uppercase tracking-wider mb-1 text-[#131112]">
                    Upload Media File (Whisper Automatic Transcription):
                  </label>
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    className="w-full p-6 border-2 border-dashed border-[#CBC8B9] hover:border-[#D74108] bg-[#EDE8DF]/60 hover:bg-[#FAF8F5] rounded-xs text-center cursor-pointer transition-all flex flex-col items-center justify-center"
                  >
                    <UploadCloud className="w-8 h-8 text-[#353535] mb-2" />
                    <span className="text-xs font-mono-meta font-bold text-[#131112]">
                      {mediaFile ? mediaFile.name : "Click to browse or drop Audio/Video file"}
                    </span>
                    <span className="text-[10px] font-mono-meta text-[#353535] mt-1">
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
                className="w-full min-h-[46px] px-4 py-3 bg-[#131112] hover:bg-[#D74108] text-white text-xs sm:text-sm font-mono-meta font-bold uppercase tracking-wider sm:tracking-widest rounded-xs flex items-center justify-center gap-2.5 transition-all shadow-sm cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed text-center"
              >
                {loading ? (
                  <>
                    <span className="inline-block w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin shrink-0" />
                    <span className="truncate">{mode === "media" ? "Whisper Transcribing & BERT Evaluating..." : "Analyzing Civility..."}</span>
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4 shrink-0" />
                    <span>{mode === "media" ? "Transcribe & Assess Hostility" : "Inspect Content & Log Verdict"}</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Quick-Load Samples */}
          <div className="mt-6 pt-4 border-t border-[#CBC8B9]">
            <div className="text-[11px] font-mono-meta font-bold uppercase tracking-wider text-[#353535] mb-2 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-[#D74108]" /> Academic Benchmark Samples:
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => loadSample("safe")}
                className="text-[11px] font-mono-meta px-2.5 py-1 bg-[#EDE8DF] hover:bg-[#DFD9CE] text-[#1E5E41] rounded-xs border border-[#CBC8B9] transition-all font-semibold"
              >
                ✔ Safe / Respectful Discourse
              </button>
              <button
                type="button"
                onClick={() => loadSample("hostile")}
                className="text-[11px] font-mono-meta px-2.5 py-1 bg-[#EDE8DF] hover:bg-[#DFD9CE] text-[#D74108] rounded-xs border border-[#CBC8B9] transition-all font-semibold"
              >
                ⛔ Targeted Hostility Claim
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Moderation Verdict Card */}
        <div className="lg:col-span-7 bg-[#FAF8F5] border-2 border-[#131112] p-4 sm:p-6 md:p-8 shadow-xs rounded-xs flex flex-col justify-between relative overflow-hidden">
          {result ? (
            <div>
              {/* Card Broadsheet Header */}
              <div className="border-b-2 border-[#131112] pb-2 flex items-center justify-between text-xs font-mono-meta text-[#353535]">
                <span>COMMUNITY SAFETY & HOSTILITY OBSERVATION</span>
                <span className="flex items-center gap-1 text-[#131112] font-bold">
                  <Zap className="w-3 h-3 text-[#D74108] shrink-0" /> {result.inference_time_ms}ms
                </span>
              </div>

              {/* Title & Metadata */}
              <div className="mt-3 sm:mt-4 mb-4 sm:mb-6">
                <h2 className="text-xl sm:text-2xl md:text-3xl font-headline font-bold text-[#131112] leading-tight">
                  Toxicity & Civility Assessment
                </h2>
                <div className="mt-1 text-xs font-mono-meta text-[#353535]">
                  Engine: {result.model_used || "Fine-Tuned BERT (78.08% F1)"} · Input Medium: {result.input_type.toUpperCase()}
                </div>
              </div>

              {/* Centerpiece: Rubber Stamp & Confidence Meter */}
              <div className="p-4 sm:p-6 bg-[#EDE8DF] border border-[#CBC8B9] rounded-xs my-4 sm:my-6 flex flex-col sm:flex-row items-center justify-center sm:justify-around gap-6">
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
                        stroke="#CBC8B9"
                        strokeWidth="8"
                        fill="transparent"
                      />
                      <circle
                        cx="48"
                        cy="48"
                        r="38"
                        stroke={result.verdict.toLowerCase().includes("safe") ? "#1E5E41" : "#D74108"}
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
                    {result.verdict.toLowerCase().includes("safe") ? "Safe For Publication" : "Violates Civility Standards"}
                  </div>
                </div>
              </div>

              {/* Whisper Speech Transcript Box (If Audio/Video) */}
              {result.transcribed_text && (
                <div className="mt-4 mb-3">
                  <div className="text-xs font-mono-meta font-bold uppercase tracking-wider text-[#131112] mb-1 flex items-center gap-1.5">
                    <Volume2 className="w-3.5 h-3.5 text-[#D74108]" /> OpenAI Whisper Spoken Transcript:
                  </div>
                  <div className="p-3 bg-[#FAF8F5] border-l-4 border-[#131112] text-xs font-mono-meta text-[#131112] leading-relaxed shadow-xs">
                    "{result.transcribed_text}"
                  </div>
                </div>
              )}

              {/* Text Preview */}
              {result.preview_text && !result.transcribed_text && (
                <div className="mt-4">
                  <div className="text-xs font-mono-meta font-bold uppercase tracking-wider text-[#353535] mb-1">
                    Evaluated Discourse Snippet:
                  </div>
                  <div className="p-3 bg-[#FAF8F5] border-l-4 border-[#353535] text-xs font-headline italic text-[#131112] leading-relaxed shadow-xs">
                    "{result.preview_text}"
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full min-h-[350px] flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-[#CBC8B9] rounded-xs bg-[#FAF8F5]">
              <div className="w-16 h-16 rounded-full bg-[#EDE8DF] flex items-center justify-center text-[#353535] mb-3">
                <Mic className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-headline font-bold text-[#131112]">
                Moderation Intake Awaiting Input
              </h3>
              <p className="mt-1 max-w-sm text-xs font-headline italic text-[#353535]">
                Submit public discourse text or upload an audio/video file to extract speech
                via OpenAI Whisper and detect toxicity.
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
