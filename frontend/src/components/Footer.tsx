import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import { ScreenPath, TransitionKind } from '../types/audit';

interface FooterProps {
  activeScreen: ScreenPath;
  onNavigate: (path: ScreenPath, transition: TransitionKind) => void;
}

export const Footer: React.FC<FooterProps> = ({ activeScreen, onNavigate }) => {
  const handleDpdpClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    onNavigate('dpdp-compliance', 'push');
  };

  return (
    <footer className="mt-20 border-t border-[#1a1a1a] bg-[#000000]">
      <div className="mx-auto flex max-w-[1240px] flex-col items-start justify-between gap-4 px-6 py-8 text-xs text-[#737373] sm:flex-row sm:items-center">
        <div className="flex flex-col gap-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-medium text-white">FairHire Audit</span>
            <span>·</span>
            <span>Dual-Domain Bias, Hallucination & Privacy Governance (Hiring & Lending)</span>
          </div>
          <p className="text-[11px] text-[#525252]">
            Guidance, not legal advice. The DPDP Rules were notified on 14 November 2025 with phased implementation. Synthetic data only.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <a
            href="#dpdp-compliance"
            onClick={handleDpdpClick}
            className={`inline-flex items-center gap-1 font-medium transition-colors ${
              activeScreen === 'dpdp-compliance'
                ? 'text-white'
                : 'text-[#888888] hover:text-white'
            }`}
          >
            <span>DPDP Alignment</span>
            <ArrowUpRight className="h-3 w-3" />
          </a>
        </div>
      </div>
    </footer>
  );
};
