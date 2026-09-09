"use client";

import React from "react";
import { motion } from "framer-motion";
import { CheckCircle2, AlertTriangle, ShieldCheck, ShieldAlert } from "lucide-react";

interface RubberStampProps {
  verdict: string;
  confidence: number;
  type: "fakenews" | "hatespeech";
}

export const RubberStamp: React.FC<RubberStampProps> = ({ verdict, confidence, type }) => {
  const isRealOrSafe =
    verdict.toLowerCase().includes("real") || verdict.toLowerCase().includes("safe");

  let stampClass = "";
  let stampTitle = "";
  let stampSub = "";
  let Icon = CheckCircle2;

  if (type === "fakenews") {
    if (isRealOrSafe) {
      stampClass = "rubber-stamp-real";
      stampTitle = "VERIFIED REAL NEWS";
      stampSub = `ACCURACY CONFIRMED · ${confidence.toFixed(1)}%`;
      Icon = CheckCircle2;
    } else {
      stampClass = "rubber-stamp-fake";
      stampTitle = "DEBUNKED: FAKE NEWS";
      stampSub = `DISINFORMATION DETECTED · ${confidence.toFixed(1)}%`;
      Icon = AlertTriangle;
    }
  } else {
    if (isRealOrSafe) {
      stampClass = "rubber-stamp-safe";
      stampTitle = "SAFE PUBLIC DISCOURSE";
      stampSub = `NO TOXICITY DETECTED · ${confidence.toFixed(1)}%`;
      Icon = ShieldCheck;
    } else {
      stampClass = "rubber-stamp-hostile";
      stampTitle = "FLAGGED: HOSTILE SPEECH";
      stampSub = `CIVIC VIOLATION · ${confidence.toFixed(1)}%`;
      Icon = ShieldAlert;
    }
  }

  return (
    <motion.div
      initial={{ scale: 2.4, opacity: 0, rotate: -22, filter: "blur(6px)" }}
      animate={{ scale: 1, opacity: 1, rotate: -6, filter: "blur(0px)" }}
      transition={{
        type: "spring",
        stiffness: 280,
        damping: 18,
        delay: 0.1,
      }}
      className={`rubber-stamp ${stampClass} relative flex flex-col items-center justify-center text-center shadow-sm select-none`}
    >
      <div className="flex items-center gap-2 mb-0.5">
        <Icon className="w-5 h-5 stroke-[2.5]" />
        <span className="text-base md:text-lg font-black tracking-wider font-headline">
          {stampTitle}
        </span>
      </div>
      <div className="text-[10px] md:text-xs font-mono-meta font-bold tracking-widest opacity-90">
        {stampSub}
      </div>

      {/* Weathered Stamp Texture Dots */}
      <div className="absolute inset-0 border border-current opacity-30 rounded-xs pointer-events-none -m-1" />
    </motion.div>
  );
};
