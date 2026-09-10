"use client";

import React from "react";
import { Newspaper, ShieldAlert, BarChart3 } from "lucide-react";

export type DeskTab = "fakenews" | "hatespeech" | "observatory";

interface EditorialNavProps {
  activeTab: DeskTab;
  onSelectTab: (tab: DeskTab) => void;
}

export const EditorialNav: React.FC<EditorialNavProps> = ({ activeTab, onSelectTab }) => {
  const tabs = [
    {
      id: "fakenews" as DeskTab,
      label: "Desk 1: Fake News Verification",
      subtitle: "URL Web Scraping & Text Claims",
      icon: Newspaper,
    },
    {
      id: "hatespeech" as DeskTab,
      label: "Desk 2: Hate Speech & Multimodal Lab",
      subtitle: "Text, Audio & Video Analysis",
      icon: ShieldAlert,
    },
    {
      id: "observatory" as DeskTab,
      label: "Desk 3: Model Observatory",
      subtitle: "SVM vs BiLSTM vs BERT (97.02%)",
      icon: BarChart3,
    },
  ];

  return (
    <nav className="w-full max-w-7xl mx-auto px-3 sm:px-4 mt-4 sm:mt-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2 bg-[#DFD9CE] p-1.5 rounded-sm border border-[#CBC8B9]">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              className={`flex items-start gap-2.5 sm:gap-3 p-2.5 sm:p-3 text-left transition-all rounded-xs relative cursor-pointer ${
                isActive
                  ? "bg-[#FAF8F5] text-[#131112] shadow-xs border border-[#CBC8B9]"
                  : "text-[#353535] hover:bg-[#EAE4D9] hover:text-[#131112]"
              }`}
            >
              <div
                className={`p-2 rounded-xs shrink-0 ${
                  isActive ? "bg-[#D74108] text-white" : "bg-[#CBC8B9] text-[#353535]"
                }`}
              >
                <Icon className="w-4 h-4 sm:w-5 sm:h-5 shrink-0" />
              </div>
              <div>
                <div className="text-xs md:text-sm font-bold font-headline tracking-wide uppercase">
                  {tab.label}
                </div>
                <div className="text-[11px] font-mono-meta text-[#6B7280]">
                  {tab.subtitle}
                </div>
              </div>

              {isActive && (
                <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-8 h-1 bg-[#D74108] rounded-full hidden md:block" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};
