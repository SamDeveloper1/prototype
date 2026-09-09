"use client";

import React, { useEffect, useState } from "react";
import { checkBackendHealth } from "@/lib/api";
import { Radio, Newspaper, Cpu, Clock } from "lucide-react";

export const Masthead: React.FC = () => {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [currentDate, setCurrentDate] = useState<string>("");

  useEffect(() => {
    // Format real-time broadsheet date
    const now = new Date();
    setCurrentDate(
      now.toLocaleDateString("en-IN", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    );

    // Check backend health
    checkBackendHealth()
      .then(() => setIsHealthy(true))
      .catch(() => setIsHealthy(false));
  }, []);

  return (
    <header className="w-full border-b-2 border-[#E2DBD0] bg-[#FAF8F5]/80 backdrop-blur-xs sticky top-0 z-50">
      {/* Top Metadata Bar */}
      <div className="max-w-7xl mx-auto px-4 py-1.5 flex flex-wrap items-center justify-between text-xs font-mono-meta text-[#6B7280] border-b border-[#EBE5DA]">
        <div className="flex items-center gap-4">
          <span className="font-semibold text-[#1C1E21] flex items-center gap-1.5">
            <Newspaper className="w-3.5 h-3.5" /> THE DIGITAL BROADSHEET
          </span>
          <span className="hidden md:inline">|</span>
          <span className="hidden md:inline">VOL. XXIV · NO. 142</span>
          <span className="hidden md:inline">|</span>
          <span className="hidden sm:inline">NATIONAL RESEARCH EDITION</span>
        </div>

        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3 text-[#8B949E]" />
            {currentDate || "Wednesday, September 9, 2026"}
          </span>
          <span>|</span>
          {/* Backend Health Status Pill */}
          <div className="flex items-center gap-1.5">
            <span
              className={`inline-block w-2 h-2 rounded-full ${
                isHealthy === true
                  ? "bg-emerald-500 animate-pulse"
                  : isHealthy === false
                  ? "bg-rose-500"
                  : "bg-amber-400"
              }`}
            />
            <span className="font-bold text-[11px]">
              {isHealthy === true
                ? "API ONLINE (PORT 8000)"
                : isHealthy === false
                ? "BACKEND OFFLINE"
                : "CONNECTING..."}
            </span>
          </div>
        </div>
      </div>

      {/* Primary Newspaper Masthead Title */}
      <div className="max-w-7xl mx-auto px-4 py-4 md:py-6 text-center">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-headline font-bold tracking-tight text-[#1C1E21] uppercase">
          The Veritas Chronicle
        </h1>
        <p className="mt-1 text-xs md:text-sm font-headline italic tracking-wide text-[#555A64]">
          Independent Automated Disinformation Verification & Multimodal Toxicity Observatory
        </p>

        {/* Double Border Rule */}
        <div className="mt-4 pt-1.5 border-t border-b-2 border-[#1C1E21] flex items-center justify-between text-[11px] font-mono-meta text-[#4B5563] uppercase tracking-wider">
          <div className="hidden sm:flex items-center gap-2">
            <Cpu className="w-3.5 h-3.5 text-blue-700" />
            <span>Engines: BERT Fine-Tuned (97.02% F1) · OpenAI Whisper</span>
          </div>
          <div className="mx-auto sm:mx-0 font-bold text-[#1C1E21]">
            Price: Open Source · Final Year Research Thesis Prototype
          </div>
          <div className="hidden sm:flex items-center gap-1.5">
            <Radio className="w-3 h-3 text-emerald-600" />
            <span>Zero-Curse Filter Active</span>
          </div>
        </div>
      </div>
    </header>
  );
};
