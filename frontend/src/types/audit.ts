export type ScreenPath =
  | 'compare'
  | 'executive-results'
  | 'before-after'
  | 'dpdp-compliance';

export type TransitionKind = 'none' | 'push' | 'push_back';

export type AuditDomain =
  | 'Credit Underwriting'
  | 'Talent Screening'
  | 'Health Triage';

export type ProtectedAxis =
  | 'Gender'
  | 'Region & Pin Code'
  | 'Age Cohort'
  | 'Surname Proxy';

export type PairVerdict = 'disparity' | 'drift' | 'invariant';

export interface ProfileAttribute {
  label: string;
  factualValue: string;
  counterfactualValue: string;
  isPerturbed: boolean;
  isProtected?: boolean;
  shapShift: number; // contribution delta in percentage points
}

export interface CounterfactualPair {
  id: string;
  domain: AuditDomain;
  modelName: string;
  axis: ProtectedAxis;
  perturbationSummary: string;
  factualDecision: string;
  counterfactualDecision: string;
  factualScore: number; // 0-100 probability / score
  counterfactualScore: number;
  threshold: number;
  verdict: PairVerdict;
  dpdpClause: string;
  flaggedForMitigation: boolean;
  exceptionApproved: boolean;
  proxyLeakageFeature: string;
  attributes: ProfileAttribute[];
  narrativeSummary: string;
}

export interface AxisRiskSummary {
  axis: ProtectedAxis;
  pairsTested: number;
  flipRate: number; // percentage
  meanScoreDelta: number; // points
  demographicParityRatio: number; // 0.00 - 1.00
  severity: 'critical' | 'elevated' | 'nominal';
  primaryProxy: string;
}

export interface ModelPortfolioItem {
  id: string;
  name: string;
  domain: AuditDomain;
  owner: string;
  pairsAudited: number;
  flipRate: number;
  parityRatio: number;
  equalizedOddsGap: number;
  exposureAmount: string;
  status: 'Action Required' | 'Monitoring' | 'Verified';
}

export interface MitigationStrategy {
  id: 'orthogonal' | 'reweigh' | 'threshold' | 'combined';
  label: string;
  shortDescription: string;
  mechanism: string;
  baseFlipRateBefore: number;
  baseFlipRateAfter: number;
  parityBefore: number;
  parityAfter: number;
  aucBefore: number;
  aucAfter: number;
  fnrGapBefore: number;
  fnrGapAfter: number;
  featureShifts: {
    feature: string;
    proxyFor: ProtectedAxis;
    weightBefore: number;
    weightAfter: number;
    residualStatus: 'Eliminated' | 'Contained' | 'Monitoring';
  }[];
}

export interface DpdpControl {
  id: string;
  sectionCode: string;
  title: string;
  obligation: string;
  linkedModels: string[];
  evidenceSummary: string;
  counterfactualMetric: string;
  owner: string;
  lastAudited: string;
  status: 'Verified' | 'Remediation Active' | 'Action Required';
  attestedByAuditor: boolean;
  adverseRecourseTemplate: string;
}
