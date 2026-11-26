import React, { useMemo, useState } from 'react';
import {
  CheckCircle2,
  Clock,
  AlertTriangle,
  Copy,
  Check,
} from 'lucide-react';
import { DpdpControl } from '../types/audit';

interface DpdpComplianceScreenProps {
  controls: DpdpControl[];
  onToggleAttestation: (id: string) => void;
}

export const DpdpComplianceScreen: React.FC<DpdpComplianceScreenProps> = ({
  controls,
  onToggleAttestation,
}) => {
  const [selectedControlId, setSelectedControlId] = useState(controls[0]?.id ?? '');
  const [copiedRecourse, setCopiedRecourse] = useState(false);

  const activeControl = useMemo(() => {
    return (
      controls.find((c) => c.id === selectedControlId) ??
      controls[0]
    );
  }, [controls, selectedControlId]);

  const handleCopyRecourse = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedRecourse(true);
      window.setTimeout(() => setCopiedRecourse(false), 1800);
    } catch {
      setCopiedRecourse(true);
      window.setTimeout(() => setCopiedRecourse(false), 1800);
    }
  };

  return (
    <div className="mx-auto max-w-[1240px] px-6 pt-10 pb-16">
      {/* Title */}
      <div className="border-b border-[#222222] pb-8">
        <div className="text-xs font-mono text-[#737373] uppercase tracking-wider mb-2">
          04 / Statutory Alignment
        </div>
        <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
          Digital Personal Data Protection (DPDP) Controls
        </h1>
        <p className="mt-2 text-sm text-[#888888] max-w-2xl">
          Evaluating model pipeline conformance against India's DPDP Act (2023) principles: data minimisation, accuracy, purpose bounding, and adverse outcome recourse.
        </p>
      </div>

      {/* Main Grid: Control List + Control Detail */}
      <div className="mt-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Control List */}
        <div className="lg:col-span-5 flex flex-col gap-2.5">
          {controls.map((ctrl) => {
            const isSelected = ctrl.id === activeControl?.id;

            return (
              <button
                key={ctrl.id}
                type="button"
                onClick={() => setSelectedControlId(ctrl.id)}
                className={`text-left p-4 rounded-lg border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-[#181818] border-white text-white'
                    : 'bg-[#0d0d0d] border-[#222222] text-[#888888] hover:border-[#333333] hover:text-[#cccccc]'
                }`}
              >
                <div className="flex items-center justify-between text-[11px] font-mono text-[#737373] mb-1.5">
                  <span>{ctrl.sectionCode}</span>
                  <span className={ctrl.status === 'Verified' ? 'text-white' : 'text-[#737373]'}>
                    {ctrl.status}
                  </span>
                </div>
                <div className="text-xs font-medium text-white">
                  {ctrl.title}
                </div>
                <div className="mt-2 text-[11px] text-[#737373] line-clamp-1">
                  Metric: {ctrl.counterfactualMetric}
                </div>
              </button>
            );
          })}
        </div>

        {/* Right Column: Active Control Card */}
        {activeControl && (
          <div className="lg:col-span-7 flex flex-col gap-6">
            <div className="glass-pane p-6">
              <div className="flex items-start justify-between gap-4 border-b border-[#222222] pb-5">
                <div>
                  <div className="text-xs font-mono text-[#737373] mb-1">
                    {activeControl.sectionCode} · Owner: {activeControl.owner}
                  </div>
                  <h2 className="text-xl font-semibold text-white">
                    {activeControl.title}
                  </h2>
                </div>

                <button
                  type="button"
                  onClick={() => onToggleAttestation(activeControl.id)}
                  className={`px-3 py-1.5 text-xs font-medium rounded border transition-colors ${
                    activeControl.attestedByAuditor
                      ? 'bg-white text-black border-white'
                      : 'bg-[#141414] text-[#888888] border-[#262626] hover:text-white'
                  }`}
                >
                  {activeControl.attestedByAuditor ? 'Attested' : 'Attest Control'}
                </button>
              </div>

              {/* Obligation */}
              <div className="mt-5">
                <div className="text-[11px] font-mono text-[#737373] uppercase tracking-wider mb-1.5">
                  Statutory Obligation
                </div>
                <p className="text-xs text-[#a3a3a3] leading-relaxed">
                  {activeControl.obligation}
                </p>
              </div>

              {/* Technical Evidence */}
              <div className="mt-5 pt-4 border-t border-[#1c1c1c]">
                <div className="text-[11px] font-mono text-[#737373] uppercase tracking-wider mb-1.5">
                  Technical Audit Evidence
                </div>
                <p className="text-xs text-white leading-relaxed">
                  {activeControl.evidenceSummary}
                </p>
              </div>

              {/* Metric Card */}
              <div className="mt-5 p-4 bg-[#121212] border border-[#222222] rounded-md flex items-center justify-between text-xs">
                <span className="text-[#888888]">Audit Benchmark:</span>
                <span className="font-mono text-white font-medium">
                  {activeControl.counterfactualMetric}
                </span>
              </div>

              {/* Adverse Recourse Notice */}
              <div className="mt-5 pt-4 border-t border-[#1c1c1c]">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-mono text-[#737373] uppercase tracking-wider">
                    Statutory Grievance & Adverse Recourse Notice Template
                  </span>
                  <button
                    type="button"
                    onClick={() => handleCopyRecourse(activeControl.adverseRecourseTemplate)}
                    className="inline-flex items-center gap-1 text-[11px] text-[#888888] hover:text-white"
                  >
                    {copiedRecourse ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                    <span>{copiedRecourse ? 'Copied' : 'Copy'}</span>
                  </button>
                </div>
                <div className="p-3 bg-[#0a0a0a] border border-[#1f1f1f] rounded text-xs text-[#a3a3a3] font-mono leading-relaxed">
                  "{activeControl.adverseRecourseTemplate}"
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
