import React, { useState } from 'react';
import { Download, X, Check } from 'lucide-react';
import { CounterfactualPair, DpdpControl } from '../types/audit';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  pairs: CounterfactualPair[];
  controls: DpdpControl[];
}

export const ExportModal: React.FC<ExportModalProps> = ({
  isOpen,
  onClose,
  pairs,
  controls,
}) => {
  const [downloadedFormat, setDownloadedFormat] = useState<'json' | 'md' | null>(null);

  if (!isOpen) return null;

  const disparityCount = pairs.filter((p) => p.verdict === 'disparity').length;
  const flaggedCount = pairs.filter((p) => p.flaggedForMitigation).length;
  const attestedCount = controls.filter((c) => c.attestedByAuditor).length;

  const triggerDownload = (format: 'json' | 'md') => {
    const timestamp = new Date().toISOString().split('T')[0];
    let content = '';
    let mime = 'application/json';
    let filename = `fairhire-audit-dossier-${timestamp}.json`;

    if (format === 'json') {
      content = JSON.stringify(
        {
          generatedAt: new Date().toISOString(),
          auditSuite: 'FairHire Audit (Dual-Domain Hiring & Lending)',
          disclaimer:
            'Guidance, not legal advice. The DPDP Rules were notified on 14 November 2025 with phased implementation. Synthetic data only.',
          summary: {
            totalMatchedPairsInspectable: pairs.length,
            disparityCases: disparityCount,
            flaggedForMitigation: flaggedCount,
            dpdpControlsAttested: `${attestedCount}/${controls.length}`,
          },
          counterfactualPairs: pairs,
          dpdpControls: controls,
        },
        null,
        2
      );
    } else {
      mime = 'text/markdown';
      filename = `fairhire-dpdp-dossier-${timestamp}.md`;
      content = [
        `# FairHire Audit — Counterfactual & DPDP Audit Dossier`,
        `Generated: ${new Date().toISOString()}`,
        `*Note: Guidance, not legal advice. The DPDP Rules were notified on 14 November 2025 with phased implementation. Synthetic data only.*`,
        ``,
        `## Executive Summary`,
        `- Counterfactual Pairs Audited: ${pairs.length}`,
        `- Outcome Flips / Disparities Detected: ${disparityCount}`,
        `- Pairs Flagged for Mitigation: ${flaggedCount}`,
        `- DPDP Act Controls Attested: ${attestedCount} of ${controls.length}`,
        ``,
        `## Counterfactual Audit Findings`,
        ...pairs.map(
          (p) =>
            `- **${p.id}** (${p.modelName} · ${p.axis}): ${p.perturbationSummary} | Factual ${p.factualScore}% (${p.factualDecision}) vs Counterfactual ${p.counterfactualScore}% (${p.counterfactualDecision}) | Status: ${p.flaggedForMitigation ? 'Flagged for Mitigation' : p.verdict}`
        ),
        ``,
        `## DPDP Act Statutory Alignment`,
        ...controls.map(
          (c) =>
            `- **${c.sectionCode} — ${c.title}**: ${c.status} (Auditor Attested: ${c.attestedByAuditor ? 'Yes' : 'Pending'})`
        ),
      ].join('\n');
    }

    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    setDownloadedFormat(format);
    window.setTimeout(() => setDownloadedFormat(null), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="relative w-full max-w-lg bg-[#0e0e0e] border border-[#262626] rounded-xl p-6 shadow-2xl">
        <div className="flex items-center justify-between border-b border-[#222222] pb-4">
          <div>
            <h3 className="text-base font-semibold text-white">
              Export Audit Dossier
            </h3>
            <p className="text-xs text-[#737373] mt-0.5">
              Download complete reproducibility package and evidence logs.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="text-[#737373] hover:text-white transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="mt-5 space-y-3">
          <div className="p-3.5 bg-[#141414] border border-[#222222] rounded-lg text-xs space-y-1">
            <div className="flex justify-between text-[#888888]">
              <span>Pairs Inspected:</span>
              <strong className="text-white font-mono">{pairs.length}</strong>
            </div>
            <div className="flex justify-between text-[#888888]">
              <span>Outcome Flips Detected:</span>
              <strong className="text-white font-mono">{disparityCount}</strong>
            </div>
            <div className="flex justify-between text-[#888888]">
              <span>DPDP Controls Attested:</span>
              <strong className="text-white font-mono">{attestedCount} / {controls.length}</strong>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 pt-2">
            <button
              type="button"
              onClick={() => triggerDownload('json')}
              className="flex items-center justify-center gap-2 p-3 bg-white text-black font-medium text-xs rounded-md hover:bg-[#e5e5e5] transition-colors"
            >
              {downloadedFormat === 'json' ? <Check className="h-3.5 w-3.5" /> : <Download className="h-3.5 w-3.5" />}
              <span>Download JSON</span>
            </button>
            <button
              type="button"
              onClick={() => triggerDownload('md')}
              className="flex items-center justify-center gap-2 p-3 bg-[#181818] border border-[#2e2e2e] text-white font-medium text-xs rounded-md hover:bg-[#222222] transition-colors"
            >
              {downloadedFormat === 'md' ? <Check className="h-3.5 w-3.5" /> : <Download className="h-3.5 w-3.5" />}
              <span>Download Markdown</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
