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
      <footer className="w-full border-t-2 border-[#E2DBD0] bg-[#FAF8F5] py-8 mt-12 text-center text-xs font-mono-meta text-[#6B7280]">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-[#1C1E21] font-headline text-sm">
              THE VERITAS CHRONICLE
            </span>
            <span>·</span>
            <span>Final Year B.Tech Academic Thesis Project (2026)</span>
          </div>

          <div className="flex items-center gap-6">
            <span className="flex items-center gap-1.5 text-emerald-700 font-semibold">
              <ShieldCheck className="w-4 h-4" /> Zero-Curse Examiner Safe
            </span>
            <span>·</span>
            <span className="flex items-center gap-1.5 text-blue-700 font-semibold">
              <BookOpen className="w-4 h-4" /> 20,000 Indian Samples
            </span>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-[#EBE5DA] text-[11px] text-[#9CA3AF]">
          Powered by Next.js 14, Tailwind CSS, FastAPI, Fine-Tuned BERT Transformers & OpenAI Whisper.
        </div>
      </footer>
    </div>
  );
}
