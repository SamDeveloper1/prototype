"use client";

import React from "react";
import { ShieldCheck, Cpu, Award } from "lucide-react";

interface MastheadProps {
  title?: string;
  subtitle?: string;
}

export const Masthead: React.FC<MastheadProps> = ({
  title = "TruthGuard AI",
  subtitle = "Automated News Verification & Multimodal Toxicity Detection System",
}) => {
  return (
    <header className="w-full border-b-2 border-[#CBC8B9] bg-[#EDE8DF] sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:py-6 text-center">
        {/* Main Title: Ibarra Real Nova Editorial Font */}
        <div className="flex items-center justify-center">
          <h1 className="text-4xl sm:text-6xl md:text-7xl font-headline font-bold tracking-normal text-[#131112]">
            {title}
          </h1>
        </div>

        {/* Subtitle in Dark Grey */}
        <p className="mt-1 text-xs sm:text-sm font-headline italic tracking-wide text-[#353535] max-w-2xl mx-auto px-2">
          {subtitle}
        </p>

        {/* Paperio Minimalist Strip with Grenadier Accent */}
        <div className="mt-3 sm:mt-4 pt-2 border-t border-b-2 border-[#131112] flex flex-wrap items-center justify-center gap-x-6 gap-y-1.5 text-[11px] font-mono-meta text-[#353535] uppercase tracking-wider">
          <div className="flex items-center gap-1.5 text-[#131112] font-semibold">
            <Award className="w-3.5 h-3.5 text-[#D74108] shrink-0" />
            <span>Final Year B.Tech Project</span>
          </div>

          <span className="hidden sm:inline text-[#CBC8B9]">·</span>

          <div className="flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-[#353535] shrink-0" />
            <span>BERT (97.02% F1) & OpenAI Whisper</span>
          </div>

          <span className="hidden sm:inline text-[#CBC8B9]">·</span>

          <div className="flex items-center gap-1.5 text-[#1E5E41] font-semibold">
            <ShieldCheck className="w-3.5 h-3.5 text-[#1E5E41] shrink-0" />
            <span>Zero-Curse Filter Active</span>
          </div>
        </div>
      </div>
    </header>
  );
};
