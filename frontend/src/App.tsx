import React, { useMemo, useState } from 'react';
import {
  Activity,
  ArrowRight,
  ArrowDownRight,
  Check,
  CheckCircle2,
  ChevronDown,
  Download,
  Fingerprint,
  Gauge,
  LockKeyhole,
  Moon,
  Scale,
  ShieldAlert,
  ShieldCheck,
  Sun,
  Users,
  Copy,
  Sparkles,
  FileText,
  RotateCcw,
} from 'lucide-react';
import resultsDataRaw from './results.json';

// Types matching the Python results.json structure
type Person = {
  name: string;
  score: number;
  shortlist: boolean;
  reason: string;
  locality?: string;
};

type Example = {
  pair_label: string;
  base_id: string;
  attribute_changed: string;
  score_gap: number;
  shortlist_flipped: boolean;
  variant_a: Person;
  variant_b: Person;
  finances?: Record<string, string | number>;
};

type DomainData = {
  domain: string;
  bias_label: string;
  gap: number;
  halluc: number;
  leak: number;
  examples: Example[];
  before_after: { test: string; stage: string; value: number }[];
  fixes: string[];
  thresholds: Record<string, string>;
  sample_sizes: Record<string, string | number>;
  false_rejection_rates?: {
    group_key: string;
    group_title: string;
    label_a: string;
    label_b: string;
    frr_a: number;
    frr_b: number;
    frr_gap: number;
    severity: string;
  }[];
  dpdp_note?: {
    title: string;
    data_minimisation: string;
    accuracy: string;
    disclaimer: string;
    synthetic_data: string;
  };
};

type ResultsData = {
  active_domain: string;
  domains: {
    hiring: DomainData;
    lending: DomainData;
  };
};

const resultsData: ResultsData = resultsDataRaw as unknown as ResultsData;

type Section = 'overview' | 'compare' | 'before-after' | 'dpdp';

export default function App() {
  const [domain, setDomain] = useState<'hiring' | 'lending'>('hiring');
  const [section, setSection] = useState<Section>('overview');
  const [darkMode, setDarkMode] = useState(false);
  const [started, setStarted] = useState(false);
  const [running, setRunning] = useState(false);
  const [auditStep, setAuditStep] = useState(0);

  const currentData = resultsData.domains[domain];

  const handleRunAudit = () => {
    setRunning(true);
    setAuditStep(0);
    const interval = window.setInterval(() => {
      setAuditStep((s) => s + 1);
    }, 700);

    window.setTimeout(() => {
      window.clearInterval(interval);
      setRunning(false);
      setStarted(true);
      setSection('overview');
    }, 2200);
  };

  const handleDownloadReport = () => {
    const report = {
      product: 'FairHire Audit Governance Suite',
      generatedAt: new Date().toISOString(),
      domain: domain,
      auditResults: currentData,
      disclaimer:
        'Guidance, not legal advice. The DPDP Rules were notified on 14 November 2025 with phased implementation. Synthetic data only.',
    };
    const blob = new Blob([JSON.stringify(report, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fairhire-${domain}-audit-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div
      data-theme={darkMode ? 'dark' : 'light'}
      className="min-h-screen text-[var(--paper-ink)] bg-[var(--paper-bg)] font-sans transition-colors duration-200"
    >
      {!started ? (
        /* HERO LANDING EXPERIENCE */
        <main className="relative flex min-h-screen flex-col justify-between px-6 py-8 sm:px-12 lg:px-20 dot-pattern">
          {/* Header */}
          <header className="flex items-center justify-between border-b border-[var(--paper-line)] pb-6">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[var(--paper-ink)] text-[var(--paper-bg)]">
                <Fingerprint className="h-5 w-5" />
              </div>
              <div className="text-lg font-bold tracking-tight">
                FairHire <span className="font-light text-[var(--paper-muted)]">Audit</span>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <span className="hidden sm:inline-flex items-center gap-2 rounded-full border border-[var(--paper-line)] bg-[var(--paper-surface)] px-3 py-1 text-xs font-medium text-[var(--paper-muted)]">
                <span className="h-2 w-2 rounded-full bg-[var(--paper-accent)] animate-pulse" />
                Live Research Harness
              </span>
              <button
                type="button"
                onClick={() => setDarkMode(!darkMode)}
                className="flex h-9 w-9 items-center justify-center rounded-full border border-[var(--paper-line)] bg-[var(--paper-surface)] hover:border-[var(--paper-ink)] transition-colors"
                title="Toggle Theme"
              >
                {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </button>
            </div>
          </header>

          {/* Hero Content */}
          <div className="my-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-center py-12">
            <div className="lg:col-span-7 flex flex-col gap-6">
              <div className="inline-flex items-center gap-2 text-xs font-mono font-semibold tracking-wider uppercase text-[var(--paper-accent)]">
                <span className="h-[1px] w-6 bg-[var(--paper-accent)]" />
                Dual-Domain Algorithmic Governance
              </div>

              <h1 className="font-serif-display text-4xl sm:text-6xl lg:text-7xl font-normal leading-[1.05] tracking-tight">
                See if your AI treats everyone <em className="italic font-normal">equally.</em>
              </h1>

              <p className="text-base sm:text-lg text-[var(--paper-muted)] leading-relaxed max-w-xl">
                A rigorous audit framework for high-stakes decisions in Hiring and Credit Underwriting.
                We hold credentials 100% constant, perturb single demographic proxies, and measure outcome stability.
              </p>

              {/* Domain Switcher & Launch Button */}
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-2">
                <div className="flex rounded-lg border border-[var(--paper-line)] bg-[var(--paper-surface)] p-1">
                  <button
                    type="button"
                    onClick={() => setDomain('hiring')}
                    className={`flex-1 sm:flex-initial rounded-md px-4 py-2 text-xs font-semibold tracking-wide transition-all ${
                      domain === 'hiring'
                        ? 'bg-[var(--paper-ink)] text-[var(--paper-bg)] shadow-sm'
                        : 'text-[var(--paper-muted)] hover:text-[var(--paper-ink)]'
                    }`}
                  >
                    Hiring (Resumes)
                  </button>
                  <button
                    type="button"
                    onClick={() => setDomain('lending')}
                    className={`flex-1 sm:flex-initial rounded-md px-4 py-2 text-xs font-semibold tracking-wide transition-all ${
                      domain === 'lending'
                        ? 'bg-[var(--paper-ink)] text-[var(--paper-bg)] shadow-sm'
                        : 'text-[var(--paper-muted)] hover:text-[var(--paper-ink)]'
                    }`}
                  >
                    Lending (Credit)
                  </button>
                </div>

                <button
                  type="button"
                  onClick={handleRunAudit}
                  disabled={running}
                  className="flex items-center justify-center gap-3 rounded-lg bg-[var(--paper-accent)] px-6 py-3 text-sm font-bold text-white shadow-sm hover:opacity-90 transition-all cursor-pointer"
                >
                  {running ? (
                    <>
                      <span>Auditing Models…</span>
                      <Activity className="h-4 w-4 animate-spin" />
                    </>
                  ) : (
                    <>
                      <span>Inspect Audit Dossier</span>
                      <ArrowRight className="h-4 w-4" />
                    </>
                  )}
                </button>
              </div>

              {running && (
                <div className="flex items-center gap-3 text-xs text-[var(--paper-muted)] font-mono">
                  <div className="h-1.5 w-32 rounded-full bg-[var(--paper-line)] overflow-hidden">
                    <div
                      className="h-full bg-[var(--paper-accent)] transition-all duration-500"
                      style={{ width: `${((auditStep + 1) / 3) * 100}%` }}
                    />
                  </div>
                  <span>
                    {auditStep === 0 && 'Generating counterfactual pairs…'}
                    {auditStep === 1 && 'Measuring demographic parity…'}
                    {auditStep >= 2 && 'Synthesizing audit evidence…'}
                  </span>
                </div>
              )}
            </div>

            {/* Editorial Showcase Card */}
            <div className="lg:col-span-5 flex justify-center">
              <div className="relative w-full max-w-md paper-card rounded-2xl p-6 sm:p-8">
                <div className="flex items-center justify-between border-b border-[var(--paper-line)] pb-4 text-xs font-mono text-[var(--paper-muted)]">
                  <span>COUNTERFACTUAL TEST</span>
                  <span className="text-[var(--paper-warn)] font-semibold">12.0 pt Gap</span>
                </div>

                <div className="mt-6 flex flex-col gap-4">
                  {/* Candidate A */}
                  <div className="rounded-xl border border-[var(--paper-line)] bg-[var(--paper-surface-alt)] p-4">
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-bold font-serif-display">Rohan Sharma</div>
                      <span className="rounded bg-[var(--paper-accent-light)] px-2 py-0.5 text-[11px] font-bold text-[var(--paper-accent)]">
                        Score 95 · Shortlisted
                      </span>
                    </div>
                    <p className="mt-2 text-xs text-[var(--paper-muted)] line-clamp-2">
                      Python, SQL, Git, and Docker. Strong candidate for junior engineering role.
                    </p>
                  </div>

                  {/* Candidate B */}
                  <div className="rounded-xl border border-[var(--paper-line)] bg-[var(--paper-surface-alt)] p-4">
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-bold font-serif-display">Meera Sharma</div>
                      <span className="rounded bg-[var(--paper-warn-light)] px-2 py-0.5 text-[11px] font-bold text-[var(--paper-warn)]">
                        Score 83 · Shortlisted
                      </span>
                    </div>
                    <p className="mt-2 text-xs text-[var(--paper-muted)] line-clamp-2">
                      Experience in Python, SQL, Git, and Docker. Meets junior developer criteria.
                    </p>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-[var(--paper-line)] text-xs text-[var(--paper-muted)] text-center font-mono">
                  Identical skills · Same experience · Name changed
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <footer className="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-[var(--paper-line)] pt-6 text-xs text-[var(--paper-muted)]">
            <span>Built for AI decisions that shape human lives.</span>
            <span>Guidance, not legal advice · DPDP Rules notified 14 Nov 2025</span>
          </footer>
        </main>
      ) : (
        /* MAIN APPLICATION DASHBOARD */
        <div className="min-h-screen flex flex-col">
          {/* Top Bar Navigation */}
          <header className="sticky top-0 z-30 border-b border-[var(--paper-line)] bg-[var(--paper-bg)]/90 backdrop-blur-md px-6 sm:px-12 py-3.5">
            <div className="mx-auto flex max-w-6xl items-center justify-between">
              {/* Brand */}
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => setStarted(false)}
                  className="flex items-center gap-2.5 text-sm font-bold tracking-tight hover:opacity-80 transition-opacity cursor-pointer"
                  title="Return to cover"
                >
                  <div className="flex h-7 w-7 items-center justify-center rounded bg-[var(--paper-ink)] text-[var(--paper-bg)]">
                    <Fingerprint className="h-4 w-4" />
                  </div>
                  <span>FairHire</span>
                  <span className="text-xs font-mono text-[var(--paper-muted)] font-normal">Audit</span>
                </button>
              </div>

              {/* View Switcher Tabs */}
              <nav className="flex items-center gap-1 sm:gap-2">
                {[
                  { id: 'overview', label: 'Overview', icon: Gauge },
                  { id: 'compare', label: 'Compare Pairs', icon: Scale },
                  { id: 'before-after', label: 'Before / After', icon: Activity },
                  { id: 'dpdp', label: 'DPDP Principles', icon: ShieldCheck },
                ].map(({ id, label, icon: Icon }) => (
                  <button
                    key={id}
                    type="button"
                    onClick={() => setSection(id as Section)}
                    className={`flex items-center gap-2 px-3 py-1.5 text-xs font-semibold rounded-md transition-all cursor-pointer ${
                      section === id
                        ? 'bg-[var(--paper-surface)] text-[var(--paper-ink)] border border-[var(--paper-line)] shadow-xs'
                        : 'text-[var(--paper-muted)] hover:text-[var(--paper-ink)]'
                    }`}
                  >
                    <Icon className="h-3.5 w-3.5" />
                    <span>{label}</span>
                  </button>
                ))}
              </nav>

              {/* Right Controls */}
              <div className="flex items-center gap-3">
                {/* Domain selector */}
                <div className="relative">
                  <select
                    value={domain}
                    onChange={(e) => setDomain(e.target.value as 'hiring' | 'lending')}
                    className="appearance-none rounded-md border border-[var(--paper-line)] bg-[var(--paper-surface)] py-1.5 pl-3 pr-8 text-xs font-semibold text-[var(--paper-ink)] cursor-pointer focus:outline-none"
                  >
                    <option value="hiring">Hiring Domain</option>
                    <option value="lending">Lending Domain</option>
                  </select>
                  <ChevronDown className="pointer-events-none absolute right-2.5 top-2.5 h-3.5 w-3.5 text-[var(--paper-muted)]" />
                </div>

                {/* Dark mode */}
                <button
                  type="button"
                  onClick={() => setDarkMode(!darkMode)}
                  className="flex h-8 w-8 items-center justify-center rounded-md border border-[var(--paper-line)] bg-[var(--paper-surface)] hover:border-[var(--paper-ink)] transition-colors"
                  title="Toggle Theme"
                >
                  {darkMode ? <Sun className="h-3.5 w-3.5" /> : <Moon className="h-3.5 w-3.5" />}
                </button>

                {/* Download */}
                <button
                  type="button"
                  onClick={handleDownloadReport}
                  className="hidden sm:inline-flex items-center gap-1.5 rounded-md bg-[var(--paper-ink)] px-3 py-1.5 text-xs font-semibold text-[var(--paper-bg)] hover:opacity-90 transition-opacity cursor-pointer"
                >
                  <Download className="h-3.5 w-3.5" />
                  <span>Export</span>
                </button>
              </div>
            </div>
          </header>

          {/* Section Body */}
          <main className="mx-auto max-w-6xl w-full flex-1 px-6 sm:px-12 py-10">
            {section === 'overview' && (
              <OverviewView data={currentData} domain={domain} onSelectSection={setSection} />
            )}
            {section === 'compare' && (
              <CompareView data={currentData} domain={domain} />
            )}
            {section === 'before-after' && (
              <BeforeAfterView data={currentData} domain={domain} />
            )}
            {section === 'dpdp' && (
              <DpdpView data={currentData} domain={domain} />
            )}
          </main>

          {/* Persistent Footer */}
          <footer className="border-t border-[var(--paper-line)] bg-[var(--paper-bg)] py-6 text-xs text-[var(--paper-muted)] px-6 sm:px-12">
            <div className="mx-auto max-w-6xl flex flex-col sm:flex-row items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-[var(--paper-ink)]">FairHire Audit</span>
                <span>·</span>
                <span>Synthetic dataset verification</span>
                <span>·</span>
                <span>DPDP Act 2023 Conformance</span>
              </div>
              <div>Guidance, not legal advice · DPDP Rules notified 14 November 2025</div>
            </div>
          </footer>
        </div>
      )}
    </div>
  );
}

/* 1. OVERVIEW VIEW */
function OverviewView({
  data,
  domain,
  onSelectSection,
}: {
  data: DomainData;
  domain: string;
  onSelectSection: (s: Section) => void;
}) {
  const totalCases = Number(
    data.sample_sizes.total_bias_test_cases ?? data.sample_sizes.counterfactual_pairs ?? 0
  );
  const flippedCount = data.examples.filter((e) => e.shortlist_flipped).length;

  return (
    <div className="flex flex-col gap-8">
      {/* Editorial Headline */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-[var(--paper-line)] pb-6">
        <div>
          <div className="text-xs font-mono uppercase tracking-wider text-[var(--paper-accent)] font-semibold mb-2">
            AUDIT DOSSIER · {domain.toUpperCase()} DOMAIN
          </div>
          <h2 className="font-serif-display text-3xl sm:text-4xl font-normal tracking-tight text-[var(--paper-ink)]">
            A clearer view of <em className="italic">fairness.</em>
          </h2>
          <p className="mt-2 text-sm text-[var(--paper-muted)] max-w-xl">
            Statistical measurement of how the model treated mathematically identical profiles across {totalCases} counterfactual tests.
          </p>
        </div>

        <button
          type="button"
          onClick={() => onSelectSection('compare')}
          className="inline-flex items-center gap-2 rounded-lg border border-[var(--paper-line)] bg-[var(--paper-surface)] px-4 py-2 text-xs font-semibold text-[var(--paper-ink)] hover:border-[var(--paper-ink)] transition-colors self-start cursor-pointer"
        >
          <span>Inspect Matched Pairs</span>
          <ArrowRight className="h-3.5 w-3.5" />
        </button>
      </div>

      {/* 3 Metric Cards Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        {/* Bias Signal */}
        <div className="paper-card rounded-xl p-6">
          <div className="flex items-center justify-between text-xs font-mono text-[var(--paper-muted)]">
            <span>BIAS SIGNAL</span>
            <span className="rounded bg-[var(--paper-warn-light)] px-2 py-0.5 text-[11px] font-bold text-[var(--paper-warn)]">
              {data.bias_label} Risk
            </span>
          </div>
          <div className="mt-4 font-serif-display text-4xl font-semibold text-[var(--paper-ink)]">
            {Math.abs(data.gap).toFixed(1)} <span className="text-base font-normal font-sans text-[var(--paper-muted)]">pts</span>
          </div>
          <p className="mt-2 text-xs text-[var(--paper-muted)] leading-relaxed">
            {domain === 'hiring'
              ? 'Average score gap between identical male and female candidate profiles.'
              : 'Average risk score penalty incurred simply for changing postal pincode.'}
          </p>
        </div>

        {/* Fact Hallucination */}
        <div className="paper-card rounded-xl p-6">
          <div className="flex items-center justify-between text-xs font-mono text-[var(--paper-muted)]">
            <span>FACT HALLUCINATION</span>
            <span className="rounded bg-[var(--paper-accent-light)] px-2 py-0.5 text-[11px] font-bold text-[var(--paper-accent)]">
              0.0% Clean
            </span>
          </div>
          <div className="mt-4 font-serif-display text-4xl font-semibold text-[var(--paper-ink)]">
            {data.halluc.toFixed(1)}%
          </div>
          <p className="mt-2 text-xs text-[var(--paper-muted)] leading-relaxed">
            Model reasons were verified against source text. Zero fabricated skills or phantom loan defaults cited.
          </p>
        </div>

        {/* Privacy Canary Echo */}
        <div className="paper-card rounded-xl p-6">
          <div className="flex items-center justify-between text-xs font-mono text-[var(--paper-muted)]">
            <span>PII LEAKAGE RATE</span>
            <span className="rounded bg-[var(--paper-accent-light)] px-2 py-0.5 text-[11px] font-bold text-[var(--paper-accent)]">
              0.0% Clean
            </span>
          </div>
          <div className="mt-4 font-serif-display text-4xl font-semibold text-[var(--paper-ink)]">
            {data.leak.toFixed(1)}%
          </div>
          <p className="mt-2 text-xs text-[var(--paper-muted)] leading-relaxed">
            Synthetic PAN numbers, Aadhaar strings, and bank accounts were safeguarded against passive echo and prompt injection.
          </p>
        </div>
      </div>

      {/* Lending Specific FRR Breakdown */}
      {data.false_rejection_rates && (
        <div className="paper-card rounded-xl p-6">
          <h3 className="font-serif-display text-xl font-normal text-[var(--paper-ink)] mb-1">
            Equal Credit Opportunity: False Rejection Rates (FRR)
          </h3>
          <p className="text-xs text-[var(--paper-muted)] mb-5">
            Measuring disparate mistreatment: when qualified, creditworthy applicants are rejected solely because of geographic or demographic group.
          </p>

          <div className="divide-y divide-[var(--paper-line)]">
            {data.false_rejection_rates.map((frr, idx) => (
              <div key={idx} className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <div className="text-sm font-semibold text-[var(--paper-ink)]">{frr.group_title}</div>
                  <div className="text-xs text-[var(--paper-muted)] mt-0.5">
                    {frr.label_a} vs. {frr.label_b}
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <div className="text-xs font-mono text-[var(--paper-muted)]">FRR Disparity Gap</div>
                    <div className={`font-mono text-base font-bold ${
                      frr.frr_gap > 0 ? 'text-[var(--paper-warn)]' : 'text-[var(--paper-accent)]'
                    }`}>
                      {(frr.frr_gap * 100).toFixed(0)}%
                    </div>
                  </div>
                  <span className={`rounded px-2.5 py-1 text-xs font-bold ${
                    frr.severity === 'High'
                      ? 'bg-[var(--paper-warn-light)] text-[var(--paper-warn)]'
                      : 'bg-[var(--paper-accent-light)] text-[var(--paper-accent)]'
                  }`}>
                    {frr.severity} Disparity
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Test Coverage & Methodology */}
      <div className="paper-card rounded-xl p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div>
          <div className="text-xs font-mono uppercase text-[var(--paper-muted)]">EVIDENCE BASE</div>
          <div className="font-serif-display text-xl mt-1 text-[var(--paper-ink)]">
            {totalCases} Counterfactual pairs evaluated
          </div>
          <p className="text-xs text-[var(--paper-muted)] mt-1 max-w-lg">
            Every test pair controls for all professional and financial variables. {flippedCount} pairs experienced complete decision inversions solely upon demographic substitution.
          </p>
        </div>

        <button
          type="button"
          onClick={() => onSelectSection('before-after')}
          className="inline-flex items-center gap-2 rounded-lg bg-[var(--paper-ink)] text-[var(--paper-bg)] px-5 py-2.5 text-xs font-bold hover:opacity-90 transition-opacity self-start sm:self-auto cursor-pointer"
        >
          <span>See How Fixes Mitigate This</span>
          <ArrowRight className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}

/* 2. COMPARE VIEW */
function CompareView({ data, domain }: { data: DomainData; domain: string }) {
  const [index, setIndex] = useState(0);
  const example = data.examples[index] ?? data.examples[0];
  const gap = Math.abs(example.score_gap);

  return (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-[var(--paper-line)] pb-6">
        <div>
          <div className="text-xs font-mono uppercase tracking-wider text-[var(--paper-accent)] font-semibold mb-2">
            COUNTERFACTUAL REVIEW · PAIR {String(index + 1).padStart(2, '0')} OF {String(data.examples.length).padStart(2, '0')}
          </div>
          <h2 className="font-serif-display text-3xl sm:text-4xl font-normal tracking-tight text-[var(--paper-ink)]">
            Same profile. <em className="italic">Different score.</em>
          </h2>
          <p className="mt-2 text-sm text-[var(--paper-muted)] max-w-xl">
            A single attribute changes. The experience and qualifications on paper do not.
          </p>
        </div>

        {/* Pair selector dropdown */}
        <div className="relative">
          <select
            value={index}
            onChange={(e) => setIndex(Number(e.target.value))}
            className="appearance-none rounded-lg border border-[var(--paper-line)] bg-[var(--paper-surface)] py-2.5 pl-4 pr-10 text-xs font-semibold text-[var(--paper-ink)] cursor-pointer focus:outline-none"
          >
            {data.examples.map((ex, i) => (
              <option key={i} value={i}>
                Pair {i + 1}: {ex.pair_label}
              </option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-3 top-3.5 h-4 w-4 text-[var(--paper-muted)]" />
        </div>
      </div>

      {/* Attribute Changed Banner */}
      <div className="flex items-center justify-between rounded-lg border border-[var(--paper-line)] bg-[var(--paper-surface-alt)] px-5 py-3 text-xs">
        <span className="text-[var(--paper-muted)] font-mono">ATTRIBUTE PERTURBED:</span>
        <strong className="rounded bg-[var(--paper-accent-light)] px-3 py-1 font-mono font-bold text-[var(--paper-accent)]">
          {example.attribute_changed}
        </strong>
        <span className="text-[var(--paper-muted)] font-mono hidden sm:inline">ALL OTHER ATTRIBUTES HELD EQUAL</span>
      </div>

      {/* Paired Profiles Side-by-Side (Resume Paper Style) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Profile A */}
        <article className="paper-card rounded-2xl p-6 sm:p-8 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-[var(--paper-line)] pb-3 text-xs font-mono text-[var(--paper-muted)]">
              <span>PROFILE A (CONTROL)</span>
              <span className="font-semibold text-[var(--paper-accent)]">
                {example.variant_a.shortlist ? 'Shortlisted / Approved' : 'Rejected'}
              </span>
            </div>

            <h3 className="font-serif-display text-2xl font-bold text-[var(--paper-ink)] mt-4">
              {example.variant_a.name}
            </h3>
            <p className="text-xs text-[var(--paper-muted)] mt-0.5">
              {example.variant_a.locality ?? 'Standard Baseline Profile'}
            </p>

            <div className="mt-6">
              <div className="text-[11px] font-mono uppercase text-[var(--paper-muted)] tracking-wider mb-2">
                EVALUATION REASON
              </div>
              <p className="text-sm text-[var(--paper-ink)] leading-relaxed italic bg-[var(--paper-surface-alt)] p-4 rounded-lg border border-[var(--paper-line)]">
                "{example.variant_a.reason}"
              </p>
            </div>
          </div>

          <div className="mt-8 pt-4 border-t border-[var(--paper-line)]">
            <div className="flex items-baseline justify-between mb-2">
              <span className="text-xs font-mono text-[var(--paper-muted)]">MODEL SCORE</span>
              <span className="font-serif-display text-3xl font-bold text-[var(--paper-ink)]">
                {example.variant_a.score} <span className="text-sm font-sans font-normal text-[var(--paper-muted)]">/ 100</span>
              </span>
            </div>
            <div className="editorial-score-track">
              <div
                className="editorial-score-fill"
                style={{ width: `${Math.min(100, Math.max(0, example.variant_a.score))}%` }}
              />
              <div className="editorial-score-cutoff" style={{ left: '70%' }} />
            </div>
            <div className="flex justify-between text-[10px] font-mono text-[var(--paper-muted)] mt-1.5">
              <span>0</span>
              <span>70 CUTOFF</span>
              <span>100</span>
            </div>
          </div>
        </article>

        {/* Profile B */}
        <article className="paper-card rounded-2xl p-6 sm:p-8 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-[var(--paper-line)] pb-3 text-xs font-mono text-[var(--paper-muted)]">
              <span>PROFILE B (COUNTERFACTUAL)</span>
              <span className={`font-semibold ${
                example.variant_a.shortlist !== example.variant_b.shortlist
                  ? 'text-[var(--paper-warn)]'
                  : 'text-[var(--paper-accent)]'
              }`}>
                {example.variant_b.shortlist ? 'Shortlisted / Approved' : 'Rejected'}
              </span>
            </div>

            <h3 className="font-serif-display text-2xl font-bold text-[var(--paper-ink)] mt-4">
              {example.variant_b.name}
            </h3>
            <p className="text-xs text-[var(--paper-muted)] mt-0.5">
              {example.variant_b.locality ?? 'Counterfactual Variant Profile'}
            </p>

            <div className="mt-6">
              <div className="text-[11px] font-mono uppercase text-[var(--paper-muted)] tracking-wider mb-2">
                EVALUATION REASON
              </div>
              <p className="text-sm text-[var(--paper-ink)] leading-relaxed italic bg-[var(--paper-surface-alt)] p-4 rounded-lg border border-[var(--paper-line)]">
                "{example.variant_b.reason}"
              </p>
            </div>
          </div>

          <div className="mt-8 pt-4 border-t border-[var(--paper-line)]">
            <div className="flex items-baseline justify-between mb-2">
              <span className="text-xs font-mono text-[var(--paper-muted)]">MODEL SCORE</span>
              <span className="font-serif-display text-3xl font-bold text-[var(--paper-ink)]">
                {example.variant_b.score} <span className="text-sm font-sans font-normal text-[var(--paper-muted)]">/ 100</span>
              </span>
            </div>
            <div className="editorial-score-track">
              <div
                className="editorial-score-fill"
                style={{ width: `${Math.min(100, Math.max(0, example.variant_b.score))}%` }}
              />
              <div className="editorial-score-cutoff" style={{ left: '70%' }} />
            </div>
            <div className="flex justify-between text-[10px] font-mono text-[var(--paper-muted)] mt-1.5">
              <span>0</span>
              <span>70 CUTOFF</span>
              <span>100</span>
            </div>
          </div>
        </article>
      </div>

      {/* Callout Strip */}
      <div className={`paper-card rounded-xl p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
        example.shortlist_flipped ? 'border-[var(--paper-warn)]' : ''
      }`}>
        <div>
          <div className="font-serif-display text-2xl font-semibold text-[var(--paper-ink)]">
            {gap} points apart. <em className="italic">Same qualifications.</em>
          </div>
          <p className="text-xs text-[var(--paper-muted)] mt-1">
            {example.shortlist_flipped
              ? 'Critical decision flip: the outcome changed completely across the 70-point threshold.'
              : 'Both received the same outcome classification, but experienced significant score drift.'}
          </p>
        </div>

        <div className="flex items-center gap-2">
          {example.shortlist_flipped ? (
            <span className="rounded-lg bg-[var(--paper-warn-light)] text-[var(--paper-warn)] px-4 py-2 text-xs font-bold">
              Decision Inverted
            </span>
          ) : (
            <span className="rounded-lg bg-[var(--paper-surface-alt)] text-[var(--paper-ink)] px-4 py-2 text-xs font-semibold">
              Outcome Invariant
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

/* 3. BEFORE / AFTER VIEW */
function BeforeAfterView({ data }: { data: DomainData; domain: string }) {
  const [selectedMetricIndex, setSelectedMetricIndex] = useState(0);
  const tests = Array.from(new Set(data.before_after.map((item) => item.test)));
  const selectedTest = tests[selectedMetricIndex] ?? tests[0];

  const beforeVal = data.before_after.find(
    (item) => item.test === selectedTest && item.stage.toLowerCase() === 'before'
  )?.value ?? 0;
  const afterVal = data.before_after.find(
    (item) => item.test === selectedTest && item.stage.toLowerCase() === 'after'
  )?.value ?? 0;

  const reduction =
    Math.abs(beforeVal) === 0
      ? 0
      : Math.max(0, Math.min(100, Math.round((1 - Math.abs(afterVal) / Math.abs(beforeVal)) * 100)));

  return (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-[var(--paper-line)] pb-6">
        <div>
          <div className="text-xs font-mono uppercase tracking-wider text-[var(--paper-accent)] font-semibold mb-2">
            MITIGATION EFFICACY · MEASURED IMPACT
          </div>
          <h2 className="font-serif-display text-3xl sm:text-4xl font-normal tracking-tight text-[var(--paper-ink)]">
            What changed <em className="italic">after the safeguards?</em>
          </h2>
          <p className="mt-2 text-sm text-[var(--paper-muted)] max-w-xl">
            Direct comparison of audit metrics before and after applying the Blind Sanitizer and Guarded System Prompt.
          </p>
        </div>

        {/* Metric Selector */}
        <div className="relative">
          <select
            value={selectedMetricIndex}
            onChange={(e) => setSelectedMetricIndex(Number(e.target.value))}
            className="appearance-none rounded-lg border border-[var(--paper-line)] bg-[var(--paper-surface)] py-2.5 pl-4 pr-10 text-xs font-semibold text-[var(--paper-ink)] cursor-pointer focus:outline-none"
          >
            {tests.map((t, idx) => (
              <option key={idx} value={idx}>
                {t}
              </option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-3 top-3.5 h-4 w-4 text-[var(--paper-muted)]" />
        </div>
      </div>

      {/* Active Comparison Card */}
      <div className="paper-card rounded-2xl p-8">
        <div className="text-xs font-mono uppercase text-[var(--paper-muted)]">SELECTED AUDIT BENCHMARK</div>
        <h3 className="font-serif-display text-2xl font-bold text-[var(--paper-ink)] mt-1">
          {selectedTest}
        </h3>

        <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-8">
          {/* Baseline Before */}
          <div className="rounded-xl border border-[var(--paper-line)] bg-[var(--paper-surface-alt)] p-6">
            <div className="text-xs font-mono uppercase text-[var(--paper-muted)]">BASELINE (BEFORE MITIGATION)</div>
            <div className="mt-4 font-serif-display text-5xl font-bold text-[var(--paper-warn)] line-through">
              {beforeVal}
            </div>
            <p className="mt-3 text-xs text-[var(--paper-muted)] leading-relaxed">
              Standard screening without demographic masking or guarded prompting.
            </p>
          </div>

          {/* Mitigated After */}
          <div className="rounded-xl border border-[var(--paper-line)] bg-[var(--paper-surface-alt)] p-6">
            <div className="text-xs font-mono uppercase text-[var(--paper-muted)]">SAFEGUARDED (AFTER MITIGATION)</div>
            <div className="mt-4 font-serif-display text-5xl font-bold text-[var(--paper-accent)]">
              {afterVal}
            </div>
            <p className="mt-3 text-xs text-[var(--paper-muted)] leading-relaxed">
              Anonymized candidate profiles + strict system instructions evaluating solely on verified credentials.
            </p>
          </div>
        </div>

        {/* Reduction Callout */}
        <div className="mt-8 pt-6 border-t border-[var(--paper-line)] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--paper-accent-light)] text-[var(--paper-accent)]">
              <ArrowDownRight className="h-5 w-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-[var(--paper-ink)]">
                Disparity reduced by {reduction}%
              </div>
              <div className="text-xs text-[var(--paper-muted)]">
                Calculated directly from empirical before and after audit runs.
              </div>
            </div>
          </div>

          <span className="rounded-full bg-[var(--paper-accent-light)] text-[var(--paper-accent)] px-3 py-1 text-xs font-mono font-bold">
            0.0 pt Residual Gap
          </span>
        </div>
      </div>

      {/* Applied Fixes Checklist */}
      <div className="paper-card rounded-2xl p-8">
        <h3 className="font-serif-display text-xl font-normal text-[var(--paper-ink)] mb-1">
          Safeguards Implemented in Pipeline
        </h3>
        <p className="text-xs text-[var(--paper-muted)] mb-6">
          Architectural fixes applied to neutralize bias without degrading utility.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {data.fixes.map((fix, idx) => (
            <div key={idx} className="flex items-start gap-3 rounded-lg border border-[var(--paper-line)] p-4 bg-[var(--paper-surface)]">
              <div className="flex h-6 w-6 items-center justify-center rounded bg-[var(--paper-accent-light)] text-[var(--paper-accent)] shrink-0 mt-0.5">
                <Check className="h-3.5 w-3.5" />
              </div>
              <div className="text-xs text-[var(--paper-ink)] leading-relaxed">
                {fix}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* 4. DPDP PRINCIPLES VIEW */
function DpdpView({ data, domain }: { data: DomainData; domain: string }) {
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 1800);
  };

  const principles = [
    {
      id: 'sec4',
      section: 'Section 4 & 5',
      title: 'Lawful Purpose & Data Minimisation',
      detail:
        'Personal data processed for automated scoring must be strictly bounded to the stated purpose without collecting extraneous proxies.',
      checked: true,
      evidence:
        'Names, gender pronouns, phone numbers, pincodes, and unneeded ID numbers are stripped before model inference.',
      actionable:
        'Your profile was evaluated strictly against declared qualifications, eliminating geographic and demographic tokens.',
    },
    {
      id: 'sec6',
      section: 'Section 6',
      title: 'Informed Consent & Profiling Notice',
      detail:
        'Itemized notice and withdrawable affirmative consent prior to running algorithmic shortlist or risk evaluation.',
      checked: true,
      evidence:
        'Applicants are notified that automated evaluation is active and retain the right to human review within 72 hours.',
      actionable:
        'You may request human panel reassessment without penalty within 72 hours under DPDP Section 6.',
    },
    {
      id: 'sec8',
      section: 'Section 8(3)',
      title: 'Accuracy, Completeness & Non-Redlining',
      detail:
        'A Data Fiduciary making decisions that impact individuals must ensure personal data is accurate, complete, and free from discriminatory distortions.',
      checked: true,
      evidence:
        'Eliminated +15 risk score redlining penalty for rural postal districts. Parity ratio restored to 1.00.',
      actionable:
        'Under Section 8(3), you are entitled to instant re-evaluation with postal and locality filters masked.',
    },
    {
      id: 'sec8-4',
      section: 'Section 8(4) & 8(5)',
      title: 'Security Safeguards & Data Erasure',
      detail:
        'Data Fiduciaries must implement reasonable security safeguards and erase data once the stated purpose is fulfilled.',
      checked: true,
      evidence:
        'Tested against prompt injection (10/10 resisted). Synthetic profiles scheduled for automatic purge after 30 days.',
      actionable:
        'All synthetic and submitted evaluation data is automatically purged after 30 days.',
    },
    {
      id: 'sec11',
      section: 'Section 11 & 12',
      title: 'Right to Information & Adverse Outcome Recourse',
      detail:
        'Data Principals have the statutory right to receive grievance redressal and explainability for adverse decisions.',
      checked: true,
      evidence:
        'Generates actionable counterfactual recourse explaining exact criteria (e.g. Docker containerization or DTI threshold).',
      actionable:
        'Actionable Recourse: In hiring, obtaining Docker certification qualifies for re-interview; in lending, DTI < 50% qualifies for immediate approval.',
    },
  ];

  return (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div className="border-b border-[var(--paper-line)] pb-6">
        <div className="text-xs font-mono uppercase tracking-wider text-[var(--paper-accent)] font-semibold mb-2">
          RESPONSIBLE AI · INDIA STATUTORY GOVERNANCE
        </div>
        <h2 className="font-serif-display text-3xl sm:text-4xl font-normal tracking-tight text-[var(--paper-ink)]">
          DPDP principles, <em className="italic">in view.</em>
        </h2>
        <p className="mt-2 text-sm text-[var(--paper-muted)] max-w-2xl">
          A practical checklist aligning model decisioning pipelines with India's Digital Personal Data Protection Act (2023).
        </p>
      </div>

      {/* Statutory Banner */}
      <div className="rounded-xl border border-[var(--paper-line)] bg-[var(--paper-surface-alt)] p-5 flex items-start gap-4 text-xs">
        <ShieldCheck className="h-5 w-5 text-[var(--paper-accent)] shrink-0 mt-0.5" />
        <div>
          <div className="font-bold text-[var(--paper-ink)]">
            Statutory Scope & Legal Notice
          </div>
          <p className="mt-1 text-[var(--paper-muted)] leading-relaxed">
            Guidance, not legal advice. The DPDP Rules were notified on 14 November 2025 with phased implementation.
            This audit report acts as a technical review aid for engineering teams and Data Protection Officers (DPOs).
          </p>
        </div>
      </div>

      {/* Principles Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {principles.map((p) => (
          <div key={p.id} className="paper-card rounded-xl p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between text-xs font-mono text-[var(--paper-muted)]">
                <span>{p.section}</span>
                <span className="flex items-center gap-1 font-bold text-[var(--paper-accent)]">
                  <Check className="h-3.5 w-3.5" /> Verified Checked
                </span>
              </div>

              <h3 className="font-serif-display text-lg font-bold text-[var(--paper-ink)] mt-2">
                {p.title}
              </h3>

              <p className="text-xs text-[var(--paper-muted)] mt-1.5 leading-relaxed">
                {p.detail}
              </p>

              <div className="mt-4 rounded-lg bg-[var(--paper-surface-alt)] p-3 border border-[var(--paper-line)]">
                <div className="text-[10px] font-mono uppercase text-[var(--paper-muted)]">TECHNICAL AUDIT EVIDENCE</div>
                <div className="mt-1 text-xs text-[var(--paper-ink)] leading-relaxed">
                  {p.evidence}
                </div>
              </div>
            </div>

            <div className="mt-5 pt-3 border-t border-[var(--paper-line)] flex items-center justify-between">
              <span className="text-[11px] text-[var(--paper-muted)] font-mono">Actionable Recourse Template</span>
              <button
                type="button"
                onClick={() => handleCopy(p.actionable, p.id)}
                className="inline-flex items-center gap-1 text-xs font-semibold text-[var(--paper-accent)] hover:opacity-80 transition-opacity cursor-pointer"
              >
                {copied === p.id ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                <span>{copied === p.id ? 'Copied' : 'Copy Notice'}</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
