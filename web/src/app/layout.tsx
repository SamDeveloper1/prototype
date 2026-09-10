import type { Metadata } from "next";
import { Ibarra_Real_Nova, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const ibarraRealNova = Ibarra_Real_Nova({
  subsets: ["latin"],
  variable: "--font-headline",
  display: "swap",
  weight: ["400", "500", "600", "700"],
  style: ["normal", "italic"],
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-body",
  display: "swap",
  weight: ["300", "400", "500", "600", "700"],
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "TruthGuard AI | Fake News & Multimodal Hate Speech Observatory",
  description: "B.Tech Final Year Research Prototype. Real-time NLP verification powered by fine-tuned BERT (97.02% F1) and OpenAI Whisper multimodal transcription.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${ibarraRealNova.variable} ${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen flex flex-col bg-[#EDE8DF] text-[#131112] antialiased selection:bg-[#D74108] selection:text-white">
        {children}
      </body>
    </html>
  );
}
