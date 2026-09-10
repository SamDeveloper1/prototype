"use client";

import React, { useState } from "react";
import { Masthead } from "@/components/Masthead";
import { EditorialNav, DeskTab } from "@/components/EditorialNav";
import { FakeNewsDesk } from "@/components/FakeNewsDesk";
import { HateSpeechDesk } from "@/components/HateSpeechDesk";
import { ModelObservatory } from "@/components/ModelObservatory";
import { BookOpen, ShieldCheck } from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<DeskTab>("fakenews");

  return (
    <div className="min-h-screen flex flex-col justify-between">
      <div>
        {/* Newspaper Broadsheet Masthead */}
        <Masthead />

        {/* Editorial Desk Navigation */}
        <EditorialNav activeTab={activeTab} onSelectTab={setActiveTab} />

        {/* Active Desk Display */}
        <main className="transition-all duration-300">
          {activeTab === "fakenews" && <FakeNewsDesk />}
          {activeTab === "hatespeech" && <HateSpeechDesk />}
          {activeTab === "observatory" && <ModelObservatory />}
        </main>
      </div>

      {/* Broadsheet Footer */}
      <footer className="w-full border-t-2 border-[#CBC8B9] bg-[#FAF8F5] py-6 sm:py-8 mt-12 text-xs font-mono-meta text-[#353535]">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left">
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-x-3 gap-y-1">
            <span className="font-bold text-[#131112] font-headline text-base sm:text-lg">
              TruthGuard AI
            </span>
            <span className="hidden sm:inline text-[#CBC8B9]">·</span>
            <span className="text-[11px] sm:text-xs text-[#353535]">
              Final Year B.Tech Research Prototype (2026)
            </span>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
            <span className="flex items-center gap-1.5 text-[#1E5E41] font-semibold text-[11px] sm:text-xs">
              <ShieldCheck className="w-4 h-4 text-[#1E5E41] shrink-0" /> Zero-Curse Examiner Safe
            </span>
            <span className="hidden sm:inline text-[#CBC8B9]">·</span>
            <span className="flex items-center gap-1.5 text-[#D74108] font-semibold text-[11px] sm:text-xs">
              <BookOpen className="w-4 h-4 text-[#D74108] shrink-0" /> 20,000 Indian Corpus
            </span>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 mt-4 pt-3 border-t border-[#CBC8B9] text-[11px] text-[#353535] text-center">
          FastAPI Backend · Next.js 14 · Fine-Tuned BERT (97.02% F1) · OpenAI Whisper Multimodal
        </div>
      </footer>
    </div>
  );
}
