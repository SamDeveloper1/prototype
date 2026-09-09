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
    <nav className="w-full max-w-7xl mx-auto px-4 mt-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2 bg-[#EFE9DF] p-1.5 rounded-sm border border-[#DDD5C7]">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              className={`flex items-start gap-3 p-3 text-left transition-all rounded-xs relative ${
                isActive
                  ? "bg-[#FFFFFF] text-[#1C1E21] shadow-sm border border-[#D5CCC0]"
                  : "text-[#606770] hover:bg-[#F5F1E9] hover:text-[#1C1E21]"
              }`}
            >
              <div
                className={`p-2 rounded-xs ${
                  isActive ? "bg-[#1C1E21] text-[#FAF8F5]" : "bg-[#DDD5C7] text-[#555A64]"
                }`}
              >
                <Icon className="w-5 h-5" />
              </div>
              <div>
                <div className="text-xs md:text-sm font-bold font-headline tracking-wide uppercase">
                  {tab.label}
                </div>
                <div className="text-[11px] font-mono-meta text-[#737A87]">
                  {tab.subtitle}
                </div>
              </div>

              {isActive && (
                <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-8 h-1 bg-[#1C1E21] rounded-full hidden md:block" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};
