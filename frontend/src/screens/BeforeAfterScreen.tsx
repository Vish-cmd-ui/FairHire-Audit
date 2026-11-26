import React, { useMemo, useState } from 'react';
import { MITIGATION_STRATEGIES } from '../data/auditData';

interface BeforeAfterScreenProps {
  flaggedCount: number;
}

export const BeforeAfterScreen: React.FC<BeforeAfterScreenProps> = ({
  flaggedCount,
}) => {
  const [strategyId, setStrategyId] = useState(MITIGATION_STRATEGIES[0].id);

  const strategy = useMemo(
    () =>
      MITIGATION_STRATEGIES.find((s) => s.id === strategyId) ??
      MITIGATION_STRATEGIES[0],
    [strategyId]
  );

  return (
    <div className="mx-auto max-w-[1240px] px-6 pt-10 pb-16">
      {/* Title */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-[#222222] pb-8">
        <div>
          <div className="text-xs font-mono text-[#737373] uppercase tracking-wider mb-2">
            03 / Mitigation Interventions
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Before vs. After Remediation Impact
          </h1>
          <p className="mt-2 text-sm text-[#888888] max-w-xl">
            Evaluating algorithmic fixes: Blind Pre-processors (stripping demographic tokens) and Guarded Prompt constraints.
          </p>
        </div>

        {/* Strategy Selector */}
        <div className="flex flex-wrap items-center gap-2">
          {MITIGATION_STRATEGIES.map((strat) => (
            <button
              key={strat.id}
              type="button"
              onClick={() => setStrategyId(strat.id)}
              className={`rounded px-3.5 py-1.5 text-xs font-medium transition-colors ${
                strategyId === strat.id
                  ? 'bg-white text-black'
                  : 'bg-[#141414] text-[#888888] border border-[#262626] hover:text-white'
              }`}
            >
              {strat.label.split('(')[0].trim()}
            </button>
          ))}
        </div>
      </div>

      {/* Primary Comparison Overview */}
      <div className="mt-8 glass-pane p-6">
        <div className="max-w-2xl mb-6">
          <h2 className="text-xl font-semibold text-white">
            {strategy.label}
          </h2>
          <p className="mt-1 text-xs text-[#888888] leading-relaxed">
            {strategy.mechanism}
          </p>
        </div>

        {/* 3 Core Metric Deliberations */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Flip Rate Delta */}
          <div className="bg-[#121212] border border-[#222222] rounded-lg p-5">
            <div className="text-[11px] font-mono text-[#737373] uppercase tracking-wider mb-2">
              Counterfactual Flip Rate
            </div>
            <div className="flex items-baseline gap-3">
              <span className="text-2xl font-bold font-mono text-[#737373] line-through">
                {strategy.baseFlipRateBefore.toFixed(1)}%
              </span>
              <span className="text-3xl font-bold font-mono text-white">
                {strategy.baseFlipRateAfter.toFixed(1)}%
              </span>
            </div>
            <div className="mt-2 text-xs text-[#888888]">
              Reduction in outcome inversions across identical profiles.
            </div>
          </div>

          {/* Demographic Parity */}
          <div className="bg-[#121212] border border-[#222222] rounded-lg p-5">
            <div className="text-[11px] font-mono text-[#737373] uppercase tracking-wider mb-2">
              Demographic Parity Ratio
            </div>
            <div className="flex items-baseline gap-3">
              <span className="text-2xl font-bold font-mono text-[#737373] line-through">
                {strategy.parityBefore.toFixed(2)}
              </span>
              <span className="text-3xl font-bold font-mono text-white">
                {strategy.parityAfter.toFixed(2)}
              </span>
            </div>
            <div className="mt-2 text-xs text-[#888888]">
              Equalized selection rates across protected groups.
            </div>
          </div>

          {/* False Rejection Disparity */}
          <div className="bg-[#121212] border border-[#222222] rounded-lg p-5">
            <div className="text-[11px] font-mono text-[#737373] uppercase tracking-wider mb-2">
              False Rejection (FRR) Gap
            </div>
            <div className="flex items-baseline gap-3">
              <span className="text-2xl font-bold font-mono text-[#737373] line-through">
                {strategy.fnrGapBefore.toFixed(0)}%
              </span>
              <span className="text-3xl font-bold font-mono text-white">
                {strategy.fnrGapAfter.toFixed(1)}%
              </span>
            </div>
            <div className="mt-2 text-xs text-[#888888]">
              Disparity in credit rejection for qualified applicants.
            </div>
          </div>
        </div>
      </div>

      {/* Feature Weight Shifts Table */}
      <div className="mt-8 glass-pane p-6">
        <h3 className="text-sm font-semibold text-white mb-4">
          Proxy Feature Neutralization Shifts
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead>
              <tr className="border-b border-[#222222] text-[#737373] font-mono uppercase text-[10px]">
                <th className="pb-3 font-normal">Proxy Feature</th>
                <th className="pb-3 font-normal">Protected Axis</th>
                <th className="pb-3 font-normal">Weight (Before)</th>
                <th className="pb-3 font-normal">Weight (After)</th>
                <th className="pb-3 font-normal text-right">Residual Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1c1c1c]">
              {strategy.featureShifts.map((shift, i) => (
                <tr key={i}>
                  <td className="py-3 font-medium text-white font-mono">
                    {shift.feature}
                  </td>
                  <td className="py-3 text-[#a3a3a3]">
                    {shift.proxyFor}
                  </td>
                  <td className="py-3 text-[#737373] font-mono">
                    {shift.weightBefore.toFixed(1)} pts
                  </td>
                  <td className="py-3 text-white font-mono font-medium">
                    {shift.weightAfter.toFixed(1)} pts
                  </td>
                  <td className="py-3 text-right">
                    <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-[#1a1a1a] text-white border border-[#333333]">
                      {shift.residualStatus}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
