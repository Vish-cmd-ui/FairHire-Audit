import React, { useState } from 'react';
import {
  ArrowRight,
  TrendingDown,
  CheckCircle,
  AlertTriangle,
} from 'lucide-react';
import { EXECUTIVE_TIMEFRAMES } from '../data/auditData';
import { ProtectedAxis, ScreenPath, TransitionKind } from '../types/audit';

interface ExecutiveResultsScreenProps {
  onNavigate: (path: ScreenPath, transition: TransitionKind) => void;
  flaggedCount: number;
}

type TimeframeKey = keyof typeof EXECUTIVE_TIMEFRAMES;

const TIMEFRAMES: { id: TimeframeKey; label: string }[] = [
  { id: 'q4-2026', label: 'Baseline Audit' },
  { id: 'projected', label: 'Post-Mitigation' },
];

export const ExecutiveResultsScreen: React.FC<ExecutiveResultsScreenProps> = ({
  onNavigate,
  flaggedCount,
}) => {
  const [timeframe, setTimeframe] = useState<TimeframeKey>('q4-2026');
  const snapshot = EXECUTIVE_TIMEFRAMES[timeframe];

  return (
    <div className="mx-auto max-w-[1240px] px-6 pt-10 pb-16">
      {/* Editorial Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-[#222222] pb-8">
        <div>
          <div className="text-xs font-mono text-[#737373] uppercase tracking-wider mb-2">
            02 / Executive Summary
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Algorithmic Fairness Risk Posture
          </h1>
          <p className="mt-2 text-sm text-[#888888] max-w-xl">
            Portfolio-wide metrics on outcome flips, demographic parity ratios, and compliance exposure across production models.
          </p>
        </div>

        {/* Minimalist Switcher */}
        <div className="flex items-center gap-2">
          {TIMEFRAMES.map((tf) => (
            <button
              key={tf.id}
              type="button"
              onClick={() => setTimeframe(tf.id)}
              className={`rounded px-3.5 py-1.5 text-xs font-medium transition-colors ${
                timeframe === tf.id
                  ? 'bg-white text-black'
                  : 'bg-[#141414] text-[#888888] border border-[#262626] hover:text-white'
              }`}
            >
              {tf.label}
            </button>
          ))}
        </div>
      </div>

      {/* 4 Primary Metric Cards */}
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Flip Rate */}
        <div className="glass-pane p-6">
          <div className="text-xs font-mono text-[#737373] uppercase tracking-wider">
            Counterfactual Flip Rate
          </div>
          <div className="mt-3 text-3xl font-bold font-mono text-white">
            {snapshot.flipRate.toFixed(1)}%
          </div>
          <p className="mt-2 text-xs text-[#737373] leading-relaxed">
            Decisions inverted solely upon swapping protected demographic attributes.
          </p>
        </div>

        {/* Demographic Parity */}
        <div className="glass-pane p-6">
          <div className="text-xs font-mono text-[#737373] uppercase tracking-wider">
            Demographic Parity Ratio
          </div>
          <div className="mt-3 text-3xl font-bold font-mono text-white">
            {snapshot.demographicParity.toFixed(2)}
          </div>
          <p className="mt-2 text-xs text-[#737373] leading-relaxed">
            Adverse impact threshold: ≥ 0.80. Parity target: 1.00.
          </p>
        </div>

        {/* False Rejection Disparity */}
        <div className="glass-pane p-6">
          <div className="text-xs font-mono text-[#737373] uppercase tracking-wider">
            FRR Disparity Gap
          </div>
          <div className="mt-3 text-3xl font-bold font-mono text-white">
            {(snapshot.equalizedOddsGap * 100).toFixed(0)}%
          </div>
          <p className="mt-2 text-xs text-[#737373] leading-relaxed">
            Difference in false rejection rates between metro and rural credit applicants.
          </p>
        </div>

        {/* Evaluated Cases */}
        <div className="glass-pane p-6">
          <div className="text-xs font-mono text-[#737373] uppercase tracking-wider">
            Pairs Evaluated
          </div>
          <div className="mt-3 text-3xl font-bold font-mono text-white">
            {snapshot.pairsEvaluated}
          </div>
          <p className="mt-2 text-xs text-[#737373] leading-relaxed">
            Synthetic counterfactual test pairs evaluated across hiring and lending.
          </p>
        </div>
      </div>

      {/* Risk Axis Breakdown */}
      <div className="mt-8 glass-pane p-6">
        <h3 className="text-sm font-semibold text-white mb-4">
          Risk Disparity Breakdown by Protected Axis
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead>
              <tr className="border-b border-[#222222] text-[#737373] font-mono uppercase text-[10px]">
                <th className="pb-3 font-normal">Protected Axis</th>
                <th className="pb-3 font-normal">Pairs Tested</th>
                <th className="pb-3 font-normal">Mean Score Gap</th>
                <th className="pb-3 font-normal">Parity Ratio</th>
                <th className="pb-3 font-normal text-right">Audit Severity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1c1c1c]">
              {snapshot.axes.map((axis, i) => (
                <tr key={i}>
                  <td className="py-3 font-medium text-white">
                    {axis.axis}
                  </td>
                  <td className="py-3 text-[#a3a3a3] font-mono">
                    {axis.pairsTested}
                  </td>
                  <td className="py-3 text-[#a3a3a3] font-mono">
                    {axis.meanScoreDelta > 0 ? `${axis.meanScoreDelta.toFixed(1)} pts` : '0.0 pts'}
                  </td>
                  <td className="py-3 text-[#a3a3a3] font-mono">
                    {axis.demographicParityRatio.toFixed(2)}
                  </td>
                  <td className="py-3 text-right">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${
                      axis.severity === 'critical'
                        ? 'bg-white text-black font-semibold'
                        : axis.severity === 'elevated'
                        ? 'bg-[#262626] text-white'
                        : 'text-[#737373]'
                    }`}>
                      {axis.severity === 'critical' ? 'High Risk' : axis.severity === 'elevated' ? 'Medium Risk' : 'Nominal'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Models under test */}
      <div className="mt-8 glass-pane p-6">
        <h3 className="text-sm font-semibold text-white mb-4">
          Audited Production Decision Systems
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {snapshot.models.map((mod) => (
            <div key={mod.id} className="bg-[#121212] border border-[#222222] rounded-lg p-5">
              <div className="flex items-center justify-between text-xs text-[#737373] font-mono mb-2">
                <span>{mod.domain}</span>
                <span className={mod.status === 'Verified' ? 'text-white' : 'text-[#a3a3a3]'}>
                  {mod.status}
                </span>
              </div>
              <h4 className="text-base font-semibold text-white">
                {mod.name}
              </h4>
              <p className="mt-1 text-xs text-[#888888]">
                Owner: {mod.owner}
              </p>
              <div className="mt-4 pt-3 border-t border-[#1c1c1c] flex items-center justify-between text-xs">
                <span className="text-[#737373]">Pairs Audited: <strong className="text-white font-mono">{mod.pairsAudited}</strong></span>
                <span className="text-[#737373]">Parity: <strong className="text-white font-mono">{mod.parityRatio.toFixed(2)}</strong></span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
