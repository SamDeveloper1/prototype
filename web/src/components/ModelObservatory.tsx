"use client";

import React, { useState } from "react";
import { Award, CheckCircle2, TrendingUp, Cpu, Database, BookOpen, Layers } from "lucide-react";

export const ModelObservatory: React.FC = () => {
  const [activeTask, setActiveTask] = useState<"fakenews" | "hatespeech">("fakenews");

  const fakeNewsModels = [
    {
      name: "BERT (bert-base-uncased)",
      type: "Transformer Deep Learning",
      accuracy: "97.10%",
      f1: "97.02%",
      precision: "97.20%",
      recall: "96.84%",
      isBest: true,
      badge: "★ Best Model (Deployed)",
    },
    {
      name: "Bi-Directional LSTM (BiLSTM)",
      type: "Recurrent Deep Learning",
      accuracy: "94.40%",
      f1: "94.35%",
      precision: "95.12%",
      recall: "93.60%",
      isBest: false,
      badge: "DL Baseline",
    },
    {
      name: "Linear SVM (Calibrated)",
      type: "Classical N-Gram TF-IDF",
      accuracy: "92.90%",
      f1: "93.00%",
      precision: "91.65%",
      recall: "94.40%",
      isBest: false,
      badge: "ML Baseline",
    },
    {
      name: "Logistic Regression",
      type: "Linear Classical ML",
      accuracy: "92.60%",
      f1: "92.83%",
      precision: "90.04%",
      recall: "95.80%",
      isBest: false,
      badge: "Fast ML",
    },
    {
      name: "Random Forest Classifier",
      type: "Ensemble Trees",
      accuracy: "92.50%",
      f1: "92.64%",
      precision: "90.94%",
      recall: "94.40%",
      isBest: false,
      badge: "Tree Ensemble",
    },
  ];

  const hateSpeechModels = [
    {
      name: "BERT (bert-base-uncased)",
      type: "Transformer Deep Learning",
      accuracy: "78.40%",
      f1: "78.08%",
      precision: "77.92%",
      recall: "78.24%",
      isBest: true,
      badge: "★ Best Model (Deployed)",
    },
    {
      name: "Multinomial Naive Bayes",
      type: "Probabilistic ML",
      accuracy: "70.40%",
      f1: "72.59%",
      precision: "67.59%",
      recall: "78.40%",
      isBest: false,
      badge: "Baseline ML",
    },
    {
      name: "Linear SVM",
      type: "Maximum Margin Linear",
      accuracy: "72.00%",
      f1: "72.39%",
      precision: "71.40%",
      recall: "73.40%",
      isBest: false,
      badge: "Solid ML",
    },
    {
      name: "Logistic Regression",
      type: "Calibrated Probabilistic",
      accuracy: "71.60%",
      f1: "71.49%",
      precision: "71.77%",
      recall: "71.20%",
      isBest: false,
      badge: "Fast Baseline",
    },
    {
      name: "Bi-Directional LSTM (BiLSTM)",
      type: "Recurrent Deep Learning",
      accuracy: "72.30%",
      f1: "68.49%",
      precision: "79.42%",
      recall: "60.20%",
      isBest: false,
      badge: "High Precision DL",
    },
  ];

  const currentModels = activeTask === "fakenews" ? fakeNewsModels : hateSpeechModels;

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-8">
      {/* Header Banner */}
      <div className="bg-[#FFFFFF] border-2 border-[#1C1E21] p-6 md:p-8 shadow-sm rounded-xs mb-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#EBE5DA] pb-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-mono-meta font-bold uppercase tracking-wider text-blue-700 mb-1">
              <Award className="w-4 h-4" /> Academic Experimental Observatory
            </div>
            <h2 className="text-3xl font-headline font-bold text-[#1C1E21]">
              Comparative Benchmark Suite & Empirical Findings
            </h2>
            <p className="mt-1 text-xs md:text-sm font-headline italic text-[#555A64]">
              Rigorous empirical evaluation across 20,000 balanced Indian samples (10,000 Fake News + 10,000 Hate Speech).
            </p>
          </div>

          {/* Task Switcher Pill */}
          <div className="flex rounded-xs bg-[#F3EFE6] p-1 border border-[#DDD5C7] shrink-0">
            <button
              onClick={() => setActiveTask("fakenews")}
              className={`px-4 py-2 text-xs font-mono-meta font-bold uppercase rounded-xs transition-all ${
                activeTask === "fakenews"
                  ? "bg-[#1C1E21] text-[#FAF8F5] shadow-xs"
                  : "text-[#6B7280] hover:text-[#1C1E21]"
              }`}
            >
              Task 1: Fake News (10k)
            </button>
            <button
              onClick={() => setActiveTask("hatespeech")}
              className={`px-4 py-2 text-xs font-mono-meta font-bold uppercase rounded-xs transition-all ${
                activeTask === "hatespeech"
                  ? "bg-[#1C1E21] text-[#FAF8F5] shadow-xs"
                  : "text-[#6B7280] hover:text-[#1C1E21]"
              }`}
            >
              Task 2: Hate Speech (10k)
            </button>
          </div>
        </div>

        {/* Highlight Metrics Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
          <div className="p-4 bg-[#FAF8F5] border border-[#DDD5C7] rounded-xs">
            <div className="flex items-center gap-1.5 text-xs font-mono-meta text-[#6B7280]">
              <Database className="w-3.5 h-3.5 text-blue-600" /> CORPUS SIZE
            </div>
            <div className="mt-2 text-2xl font-headline font-bold text-[#1C1E21]">
              10,000 Rows
            </div>
            <div className="text-[11px] font-mono-meta text-[#4B5563]">
              80/10/10 Stratified Split
            </div>
          </div>

          <div className="p-4 bg-[#FAF8F5] border border-[#DDD5C7] rounded-xs">
            <div className="flex items-center gap-1.5 text-xs font-mono-meta text-[#6B7280]">
              <TrendingUp className="w-3.5 h-3.5 text-emerald-600" /> SOTA F1-SCORE
            </div>
            <div className="mt-2 text-2xl font-headline font-bold text-[#047857]">
              {activeTask === "fakenews" ? "97.02% F1" : "78.08% F1"}
            </div>
            <div className="text-[11px] font-mono-meta text-[#4B5563]">
              Fine-Tuned BERT Architecture
            </div>
          </div>

          <div className="p-4 bg-[#FAF8F5] border border-[#DDD5C7] rounded-xs">
            <div className="flex items-center gap-1.5 text-xs font-mono-meta text-[#6B7280]">
              <Cpu className="w-3.5 h-3.5 text-amber-600" /> INFERENCE LATENCY
            </div>
            <div className="mt-2 text-2xl font-headline font-bold text-[#1C1E21]">
              ~320 ms
            </div>
            <div className="text-[11px] font-mono-meta text-[#4B5563]">
              Apple Silicon Metal GPU (MPS)
            </div>
          </div>

          <div className="p-4 bg-[#FAF8F5] border border-[#DDD5C7] rounded-xs">
            <div className="flex items-center gap-1.5 text-xs font-mono-meta text-[#6B7280]">
              <Layers className="w-3.5 h-3.5 text-purple-600" /> MULTIMODAL SPEECH
            </div>
            <div className="mt-2 text-2xl font-headline font-bold text-[#1C1E21]">
              Whisper Base
            </div>
            <div className="text-[11px] font-mono-meta text-[#4B5563]">
              16kHz Mono ffmpeg Audio Track
            </div>
          </div>
        </div>

        {/* Benchmark Table */}
        <div className="mt-8 overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b-2 border-[#1C1E21] text-[11px] font-mono-meta font-bold uppercase tracking-wider text-[#1C1E21] bg-[#FAF8F5]">
                <th className="py-3 px-4">Architecture</th>
                <th className="py-3 px-4">Model Class</th>
                <th className="py-3 px-4">Accuracy</th>
                <th className="py-3 px-4">F1-Score</th>
                <th className="py-3 px-4">Precision</th>
                <th className="py-3 px-4">Recall</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#EBE5DA] text-xs font-mono-meta">
              {currentModels.map((model, idx) => (
                <tr
                  key={idx}
                  className={`transition-colors ${
                    model.isBest
                      ? "bg-emerald-50/50 font-bold text-[#1C1E21]"
                      : "hover:bg-[#FAF8F5] text-[#4B5563]"
                  }`}
                >
                  <td className="py-3.5 px-4 font-headline text-sm font-bold text-[#1C1E21]">
                    {model.name}
                  </td>
                  <td className="py-3.5 px-4 text-[#6B7280]">{model.type}</td>
                  <td className="py-3.5 px-4">{model.accuracy}</td>
                  <td className="py-3.5 px-4 text-[#047857]">{model.f1}</td>
                  <td className="py-3.5 px-4">{model.precision}</td>
                  <td className="py-3.5 px-4">{model.recall}</td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded-xs text-[10px] uppercase font-bold tracking-wider ${
                        model.isBest
                          ? "bg-[#047857] text-white"
                          : "bg-[#E5E0D8] text-[#555A64]"
                      }`}
                    >
                      {model.badge}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Academic Synthesis Notes for Viva Defense */}
        <div className="mt-8 p-5 bg-[#FAF8F5] border-l-4 border-blue-600 rounded-xs">
          <div className="flex items-center gap-2 text-xs font-mono-meta font-bold uppercase tracking-wider text-blue-900 mb-2">
            <BookOpen className="w-4 h-4 text-blue-700" /> Defense Summary for Final Year Viva Examiners:
          </div>
          <ul className="space-y-1.5 text-xs font-headline italic text-[#374151] leading-relaxed list-disc list-inside">
            <li>
              <strong>Contextual Advantage</strong>: BERT achieved a <strong>+5.7% F1 increase</strong> over Linear SVM on Hate Speech detection because hostile discourse in the Indian socio-political context relies heavily on subtle subtext and targeted group references that word-count TF-IDF cannot capture.
            </li>
            <li>
              <strong>Zero-Curse Filter Rigor</strong>: The 10,000-sample hate speech corpus was strictly filtered to eliminate street profanity and vulgar slurs, ensuring the model identifies genuine semantic hostility rather than keyword-matching swear words.
            </li>
            <li>
              <strong>Multimodal Decoupling</strong>: Decoupling speech-to-text via OpenAI Whisper (base) and NLP classification via BERT enables plug-and-play support for raw text, web links, recorded audio, and video formats.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
