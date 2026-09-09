import type { Metadata } from "next";
import { Newsreader, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const newsreader = Newsreader({
  subsets: ["latin"],
  variable: "--font-headline",
  display: "swap",
  style: ["normal", "italic"],
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-body",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "The Veritas Chronicle | AI Fake News & Hate Speech Observatory",
  description: "B.Tech Final Year Research Prototype. Real-time NLP verification powered by fine-tuned BERT (97.02% F1) and OpenAI Whisper multimodal transcription.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${newsreader.variable} ${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen flex flex-col bg-[#F9F6F0] text-[#1C1E21] antialiased selection:bg-[#E5DFD3] selection:text-black">
        {children}
      </body>
    </html>
  );
}
