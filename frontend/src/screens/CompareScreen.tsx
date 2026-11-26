import React, { useMemo, useState } from 'react';
import {
  AlertCircle,
  CheckCircle2,
  Filter,
  Search,
  Sliders,
  ShieldCheck,
  ChevronRight,
} from 'lucide-react';
import {
  AuditDomain,
  CounterfactualPair,
  PairVerdict,
} from '../types/audit';

interface CompareScreenProps {
  pairs: CounterfactualPair[];
  selectedPairId: string;
  onSelectPair: (id: string) => void;
  onToggleFlag: (id: string) => void;
  onToggleException: (id: string) => void;
}

const DOMAINS: ('All' | AuditDomain)[] = [
  'All',
  'Talent Screening',
  'Credit Underwriting',
];

export const CompareScreen: React.FC<CompareScreenProps> = ({
  pairs,
  selectedPairId,
  onSelectPair,
  onToggleFlag,
  onToggleException,
}) => {
  const [domainFilter, setDomainFilter] = useState<'All' | AuditDomain>('All');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredPairs = useMemo(() => {
    return pairs.filter((pair) => {
      if (domainFilter !== 'All' && pair.domain !== domainFilter) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        return (
          pair.id.toLowerCase().includes(q) ||
          pair.modelName.toLowerCase().includes(q) ||
          pair.axis.toLowerCase().includes(q) ||
          pair.perturbationSummary.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [pairs, domainFilter, searchQuery]);

  const activePair = useMemo(() => {
    return (
      filteredPairs.find((p) => p.id === selectedPairId) ??
      pairs.find((p) => p.id === selectedPairId) ??
      filteredPairs[0] ??
      pairs[0]
    );
  }, [filteredPairs, pairs, selectedPairId]);

  const scoreGap = activePair
    ? Math.abs(activePair.factualScore - activePair.counterfactualScore)
    : 0;

  return (
    <div className="mx-auto max-w-[1240px] px-6 pt-10 pb-16">
      {/* Title & Description */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-[#222222] pb-8">
        <div>
          <div className="text-xs font-mono text-[#737373] uppercase tracking-wider mb-2">
            01 / Matched-Pair Audit
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Counterfactual Disparity Inspector
          </h1>
          <p className="mt-2 text-sm text-[#888888] max-w-xl">
            Audit automated decisions across identical profiles differing solely by protected attributes (gender, location, or college tier).
          </p>
        </div>

        {/* Filter buttons */}
        <div className="flex items-center gap-2">
          {DOMAINS.map((dom) => (
            <button
              key={dom}
              type="button"
              onClick={() => setDomainFilter(dom)}
              className={`rounded px-3 py-1.5 text-xs font-medium transition-colors ${
                domainFilter === dom
                  ? 'bg-white text-black'
                  : 'bg-[#141414] text-[#888888] border border-[#262626] hover:text-white'
              }`}
            >
              {dom === 'All' ? 'All Domains' : dom}
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid: Pair List (Left) + Detail View (Right) */}
      <div className="mt-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Compact Pair Selector */}
        <div className="lg:col-span-4 flex flex-col gap-3">
          <div className="relative mb-2">
            <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-[#525252]" />
            <input
              type="text"
              placeholder="Search pair or attribute..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[#0d0d0d] border border-[#222222] rounded-md pl-9 pr-3 py-2 text-xs text-white placeholder-[#525252] focus:outline-none focus:border-white"
            />
          </div>

          <div className="flex flex-col gap-2 max-h-[620px] overflow-y-auto pr-1">
            {filteredPairs.map((pair) => {
              const isSelected = pair.id === activePair?.id;
              const isDisparity = pair.verdict === 'disparity';
              const gap = Math.abs(pair.factualScore - pair.counterfactualScore);

              return (
                <button
                  key={pair.id}
                  type="button"
                  onClick={() => onSelectPair(pair.id)}
                  className={`text-left p-3.5 rounded-lg border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#181818] border-white text-white'
                      : 'bg-[#0d0d0d] border-[#222222] text-[#888888] hover:border-[#333333] hover:text-[#cccccc]'
                  }`}
                >
                  <div className="flex items-center justify-between text-[11px] font-mono text-[#737373] mb-1.5">
                    <span>{pair.id} · {pair.axis}</span>
                    <span className={isDisparity ? 'text-white font-medium' : 'text-[#737373]'}>
                      {isDisparity ? 'Flip Disparity' : gap > 0 ? `${gap}pt Drift` : 'Invariant'}
                    </span>
                  </div>
                  <div className="text-xs font-medium text-white line-clamp-1">
                    {pair.perturbationSummary}
                  </div>
                  <div className="mt-2 flex items-center justify-between text-[11px] text-[#737373]">
                    <span>Factual: <strong className="text-[#a3a3a3]">{pair.factualScore}</strong></span>
                    <span>Counterfactual: <strong className="text-[#a3a3a3]">{pair.counterfactualScore}</strong></span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Clean Pair Inspection Deck */}
        {activePair && (
          <div className="lg:col-span-8 flex flex-col gap-6">
            {/* Pair Hero Card */}
            <div className="glass-pane p-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#222222] pb-5">
                <div>
                  <div className="flex items-center gap-2 text-xs font-mono text-[#737373]">
                    <span>{activePair.domain}</span>
                    <span>·</span>
                    <span>{activePair.modelName}</span>
                  </div>
                  <h2 className="text-xl font-semibold text-white mt-1">
                    {activePair.perturbationSummary}
                  </h2>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => onToggleFlag(activePair.id)}
                    className={`px-3 py-1.5 text-xs font-medium rounded border transition-colors ${
                      activePair.flaggedForMitigation
                        ? 'bg-white text-black border-white'
                        : 'bg-[#141414] text-[#888888] border-[#262626] hover:text-white'
                    }`}
                  >
                    {activePair.flaggedForMitigation ? 'Flagged for Fix' : 'Flag for Fix'}
                  </button>
                </div>
              </div>

              {/* Side by side comparison cards */}
              <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Factual Twin */}
                <div className="bg-[#121212] border border-[#222222] rounded-lg p-5">
                  <div className="text-[11px] font-mono text-[#737373] uppercase tracking-wider mb-2">
                    Baseline Profile (A)
                  </div>
                  <div className="flex items-baseline justify-between mb-4">
                    <span className="text-3xl font-bold font-mono text-white">
                      {activePair.factualScore}
                      <span className="text-xs text-[#737373] font-normal"> / 100</span>
                    </span>
                    <span className="px-2 py-0.5 rounded text-xs font-medium bg-[#1a1a1a] text-white border border-[#333333]">
                      {activePair.factualDecision}
                    </span>
                  </div>
                  <p className="text-xs text-[#888888] leading-relaxed">
                    Evaluated under standard criteria prior to protected attribute perturbation.
                  </p>
                </div>

                {/* Counterfactual Twin */}
                <div className="bg-[#121212] border border-[#222222] rounded-lg p-5">
                  <div className="text-[11px] font-mono text-[#737373] uppercase tracking-wider mb-2">
                    Counterfactual Twin (B)
                  </div>
                  <div className="flex items-baseline justify-between mb-4">
                    <span className="text-3xl font-bold font-mono text-white">
                      {activePair.counterfactualScore}
                      <span className="text-xs text-[#737373] font-normal"> / 100</span>
                    </span>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium border ${
                      activePair.factualDecision !== activePair.counterfactualDecision
                        ? 'bg-white text-black border-white font-semibold'
                        : 'bg-[#1a1a1a] text-white border-[#333333]'
                    }`}>
                      {activePair.counterfactualDecision}
                    </span>
                  </div>
                  <p className="text-xs text-[#888888] leading-relaxed">
                    Identical credentials with <strong className="text-white">{activePair.axis}</strong> perturbed.
                  </p>
                </div>
              </div>

              {/* Score gap callout */}
              <div className="mt-4 p-3.5 bg-[#141414] border border-[#222222] rounded-md flex items-center justify-between text-xs">
                <span className="text-[#888888]">
                  Score Gap Delta: <strong className="text-white">{scoreGap.toFixed(1)} points</strong>
                </span>
                <span className="font-mono text-[#737373] text-[11px]">
                  Governed under: {activePair.dpdpClause}
                </span>
              </div>
            </div>

            {/* Attributes Table */}
            <div className="glass-pane p-6">
              <h3 className="text-sm font-semibold text-white mb-4">
                Verified Credentials & Invariant Fields
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead>
                    <tr className="border-b border-[#222222] text-[#737373] font-mono uppercase text-[10px]">
                      <th className="pb-3 font-normal">Credential / Feature</th>
                      <th className="pb-3 font-normal">Profile A</th>
                      <th className="pb-3 font-normal">Profile B</th>
                      <th className="pb-3 font-normal text-right">Delta / Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1c1c1c]">
                    {activePair.attributes.map((attr, idx) => (
                      <tr key={idx} className={attr.isPerturbed ? 'bg-white/[0.02]' : ''}>
                        <td className="py-3 font-medium text-white">
                          {attr.label}
                        </td>
                        <td className="py-3 text-[#a3a3a3]">
                          {attr.factualValue}
                        </td>
                        <td className="py-3 text-[#a3a3a3]">
                          {attr.counterfactualValue}
                        </td>
                        <td className="py-3 text-right font-mono">
                          {attr.isPerturbed ? (
                            <span className="text-white font-medium underline underline-offset-4 decoration-[#525252]">
                              Perturbed ({attr.shapShift > 0 ? `+${attr.shapShift}` : attr.shapShift} pts)
                            </span>
                          ) : (
                            <span className="text-[#525252]">100% Identical</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Rationale explanation */}
              <div className="mt-5 pt-4 border-t border-[#1c1c1c] text-xs text-[#888888] leading-relaxed">
                <strong className="text-white">Audit Finding: </strong>
                {activePair.narrativeSummary}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
