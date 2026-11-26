'use client'

import { useMemo, useState } from 'react'
import useSWR from 'swr'
import { AnimatePresence, motion } from 'framer-motion'
import {
  Activity, ArrowDownRight, ArrowRight, ArrowUpRight, BarChart3, Check, CheckCircle2,
  ChevronDown, CircleHelp, ClipboardCheck, Download, FileSearch, Fingerprint, Gauge,
  LockKeyhole, Menu, Moon, Scale, ShieldAlert, ShieldCheck, Sparkles, Sun, Users, X,
} from 'lucide-react'
import {
  Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import { Button } from '@/components/ui/button'

type Person = { name: string; score: number; shortlist: boolean; reason: string; locality?: string }
type Example = { pair_label: string; attribute_changed: string; score_gap: number; shortlist_flipped: boolean; variant_a: Person; variant_b: Person; finances?: Record<string, string | number> }
type DomainData = { domain: string; bias_label: string; gap: number; halluc: number; leak: number; examples: Example[]; before_after: { test: string; stage: string; value: number }[]; fixes: string[]; thresholds: Record<string, string>; sample_sizes: Record<string, string | number>; false_rejection_rates?: { group_title: string; severity: string; frr_gap: number }[]; dpdp_note?: { title: string; data_minimisation: string; accuracy: string; disclaimer: string; synthetic_data: string } }
type ResultsData = { active_domain: string; domains: Record<string, DomainData> }
type Section = 'overview' | 'compare' | 'before-after' | 'dpdp'

const fetcher = async (url: string) => {
  const response = await fetch(url)
  if (!response.ok) throw new Error('Could not load audit results')
  return response.json() as Promise<ResultsData>
}

const navItems: { id: Section; label: string; icon: typeof Gauge }[] = [
  { id: 'overview', label: 'Overview', icon: Gauge },
  { id: 'compare', label: 'Compare', icon: Scale },
  { id: 'before-after', label: 'Before / After', icon: BarChart3 },
  { id: 'dpdp', label: 'DPDP principles', icon: ClipboardCheck },
]

function RiskBadge({ level }: { level: string }) {
  const normalized = level.toLowerCase()
  const Icon = normalized === 'high' ? ShieldAlert : normalized === 'medium' ? CircleHelp : CheckCircle2
  return <span className={`risk-badge risk-${normalized}`}><Icon aria-hidden="true" size={14} />{level}</span>
}

function Ring({ value, color, label }: { value: number; color: string; label: string }) {
  const safeValue = Math.max(0, Math.min(value, 100))
  return <div className="ring" style={{ background: `conic-gradient(${color} ${safeValue * 3.6}deg, rgba(255,255,255,.08) 0deg)` }} aria-label={`${label}: ${value}`} role="img"><div className="ring-inner"><strong>{value}</strong><span>{label}</span></div></div>
}

function TopHeader({ domain, setDomain, section, setSection, onDownload, darkMode, onToggleTheme }: { domain: string; setDomain: (d: string) => void; section: Section; setSection: (s: Section) => void; onDownload: () => void; darkMode: boolean; onToggleTheme: () => void }) {
  const [menuOpen, setMenuOpen] = useState(false)
  return <header className="topbar">
    <div className="brand"><div className="brand-mark"><Fingerprint size={20} /></div><span>FairHire<span className="brand-light"> Audit</span></span></div>
    <nav className={`main-nav ${menuOpen ? 'nav-open' : ''}`} aria-label="Main navigation">
      {navItems.map(({ id, label, icon: Icon }) => <button key={id} className={`nav-link ${section === id ? 'nav-active' : ''}`} onClick={() => { setSection(id); setMenuOpen(false) }}><Icon size={16} aria-hidden="true" />{label}</button>)}
    </nav>
    <div className="header-actions">
      <label className="sr-only" htmlFor="domain-select">Audit domain</label>
      <div className="select-wrap"><select id="domain-select" value={domain} onChange={(e) => setDomain(e.target.value)}><option value="hiring">Hiring</option><option value="lending">Lending</option></select><ChevronDown size={14} aria-hidden="true" /></div>
      <button className="theme-toggle" type="button" onClick={onToggleTheme} aria-label={`Switch to ${darkMode ? 'light' : 'dark'} theme`} title={`Switch to ${darkMode ? 'light' : 'dark'} theme`}>{darkMode ? <Sun size={18} aria-hidden="true" /> : <Moon size={18} aria-hidden="true" />}</button>
      <Button className="download-button" onClick={onDownload}><Download data-icon="inline-start" /><span className="download-label">Download report</span></Button>
      <button className="mobile-menu" aria-label={menuOpen ? 'Close navigation' : 'Open navigation'} onClick={() => setMenuOpen(!menuOpen)}>{menuOpen ? <X /> : <Menu />}</button>
    </div>
  </header>
}

function PageHeading({ eyebrow, title, description, right }: { eyebrow: string; title: string; description: string; right?: React.ReactNode }) {
  return <div className="page-heading"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{description}</p></div>{right}</div>
}

function StatCard({ icon: Icon, label, value, note, tone }: { icon: typeof Activity; label: string; value: string; note: string; tone: 'red' | 'green' | 'violet' }) {
  return <motion.article className="stat-card" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .35 }}>
    <div className={`stat-icon ${tone}`}><Icon size={19} aria-hidden="true" /></div><div className="stat-top"><span>{label}</span><RiskBadge level={tone === 'red' ? 'High' : 'Low'} /></div>
    <div className="stat-number">{value}</div><p>{note}</p><div className="stat-foot"><span className="mini-dot" />Based on saved audit cases</div>
  </motion.article>
}

function Overview({ data, domain, onSection }: { data: DomainData; domain: string; onSection: (s: Section) => void }) {
  const biasValue = Math.min(100, Math.round(Math.abs(data.gap) * 4.6))
  const totalCases = Number(data.sample_sizes.total_bias_test_cases ?? data.sample_sizes.counterfactual_pairs ?? 0)
  const flipped = data.examples.filter((item) => item.shortlist_flipped).length
  return <>
    <PageHeading eyebrow="AUDIT SUMMARY · SAVED DEMO" title="A clearer view of fairness." description={`A snapshot of how your ${domain} model treated equivalent profiles across ${totalCases} counterfactual tests.`} right={<div className="audit-status"><span className="live-dot" />Demo: replaying a saved audit</div>} />
    <div className="welcome-panel"><div className="welcome-copy"><div className="welcome-label"><Sparkles size={15} />Fairness snapshot</div><h2>Good decisions should be<br className="desktop-break" /> consistent for everyone.</h2><p>We changed one personal attribute at a time and measured whether the model&apos;s decision changed.</p><Button className="text-button" variant="outline" onClick={() => onSection('compare')}>Explore a comparison <ArrowRight data-icon="inline-end" /></Button></div><div className="welcome-visual"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="orbit-core"><Scale size={30} /></div><span className="orbit-tag tag-a">same skills</span><span className="orbit-tag tag-b">same outcome?</span></div></div>
    <div className="section-title-row"><div><h2>At a glance</h2><p>Three checks that matter for a fair decision</p></div><span className="sample-pill"><FileSearch size={14} />{totalCases} test cases</span></div>
    <div className="stats-grid"><StatCard icon={Scale} label="Bias signal" value={`${Math.abs(data.gap).toFixed(1)} pts`} note={domain === 'hiring' ? 'Largest observed score gap across changed attributes.' : 'Observed risk score gap across equivalent applications.'} tone="red" /><StatCard icon={ShieldCheck} label="Hallucination" value={`${data.halluc.toFixed(1)}%`} note="No unsupported claims found in this saved audit." tone="green" /><StatCard icon={LockKeyhole} label="Privacy leakage" value={`${data.leak.toFixed(1)}%`} note="No passive personal-data leakage detected." tone="violet" /></div>
    <div className="overview-bottom"><section className="panel signal-panel"><div className="panel-heading"><div><span className="eyebrow">DETECTED PATTERN</span><h3>{domain === 'hiring' ? 'A meaningful score gap' : 'A geographic disparity'}</h3></div><RiskBadge level={data.bias_label} /></div><div className="signal-content"><Ring value={biasValue} color="#f87171" label="signal" /><div className="signal-details"><strong>{domain === 'hiring' ? `${data.gap.toFixed(1)} point average gap` : `${Math.abs(data.gap).toFixed(1)} point risk gap`}</strong><p>{domain === 'hiring' ? 'The same qualifications did not always receive the same score after a name or location changed.' : 'Equivalent financial profiles received different outcomes when the postal district changed.'}</p><button className="inline-link" onClick={() => onSection('compare')}>Review paired examples <ArrowRight size={14} /></button></div></div></section><section className="panel sample-panel"><span className="eyebrow">TEST COVERAGE</span><h3>Evidence, not assumptions.</h3><div className="coverage-list"><div><Users size={16} /><span>Base {domain === 'hiring' ? 'resumes' : 'applicants'}</span><strong>{data.sample_sizes.base_resumes ?? data.sample_sizes.base_applicants}</strong></div><div><Activity size={16} /><span>Counterfactual pairs</span><strong>{data.sample_sizes.counterfactual_pairs}</strong></div><div><ArrowDownRight size={16} /><span>Decision changes observed</span><strong>{flipped}</strong></div></div><p className="sample-foot">Results use synthetic profiles and represent this saved demo only.</p></section></div>
  </>
}

function ResumePaper({ person, side, resumeText, shortlistLabel }: { person: Person; side: 'A' | 'B'; resumeText: string; shortlistLabel: string }) {
  return <article className="resume-paper">
    <div className="resume-paper-head"><span>PROFILE {side}</span><span>{person.shortlist ? shortlistLabel : 'Not selected'}</span></div>
    <h2 className="resume-name"><mark>{person.name}</mark></h2>
    <p className="resume-role">Candidate · {side === 'A' ? 'Original profile' : 'Counterfactual profile'}</p>
    <div className="resume-rule" />
    <div className="resume-section-label">SCREENING EVIDENCE</div>
    <p className="resume-copy">{resumeText}</p>
    <div className="resume-score"><div className="resume-score-top"><span>Model score</span><strong>{person.score}<small> / 100</small></strong></div>
      <div className="score-track" role="img" aria-label={`Score ${person.score} out of 100; shortlist cutoff at 70`}><span className="score-fill" style={{ width: `${Math.max(0, Math.min(person.score, 100))}%` }} /><i className="score-cutoff" /><b className="score-knob" style={{ left: `${Math.max(0, Math.min(person.score, 100))}%` }} /></div>
      <div className="score-scale"><span>0</span><span className="cutoff-label">SHORTLIST CUTOFF · 70</span><span>100</span></div>
    </div>
  </article>
}

function Compare({ data, domain }: { data: DomainData; domain: string }) {
  const [index, setIndex] = useState(0)
  const example = data.examples[index] ?? data.examples[0]
  if (!example) return null
  const gap = Math.abs(example.score_gap)
  const averageGap = data.examples.length ? data.examples.reduce((total, pair) => total + Math.abs(pair.score_gap), 0) / data.examples.length : 0
  const changedDecisions = data.examples.filter((pair) => pair.shortlist_flipped).length
  const shortlistLabel = domain === 'lending' ? 'Approved' : 'Shortlisted'
  return <section className="compare-page">
    <header className="compare-heading"><div><p className="compare-kicker">COUNTERFACTUAL REVIEW <span>/{String(index + 1).padStart(2, '0')}</span></p><h1>Same resume.<br /><em>Different score.</em></h1><p className="compare-intro">A single personal detail changes. The experience on paper does not.</p></div>
      <label className="pair-picker"><span>PAIR {String(index + 1).padStart(2, '0')} OF {String(data.examples.length).padStart(2, '0')}</span><select id="pair-select" aria-label="Choose example pair" value={index} onChange={(e) => setIndex(Number(e.target.value))}>{data.examples.map((item, i) => <option key={item.pair_label} value={i}>{item.pair_label}</option>)}</select><ChevronDown size={17} aria-hidden="true" /></label>
    </header>
    <div className="comparison-meta"><span>ONE ATTRIBUTE CHANGED</span><strong>{example.attribute_changed}</strong><span>ALL OTHER DETAILS HELD CONSTANT</span></div>
    <div className="resume-grid"><ResumePaper person={example.variant_a} side="A" resumeText={example.variant_a.reason} shortlistLabel={shortlistLabel} /><ResumePaper person={example.variant_b} side="B" resumeText={example.variant_a.reason} shortlistLabel={shortlistLabel} /></div>
    <section className={`comparison-callout ${example.shortlist_flipped ? 'decision-differs' : ''}`} aria-live="polite"><h2>{gap} points apart.<br /><em>Same resume.</em></h2><p>{example.shortlist_flipped ? 'Different decision' : 'Both shortlisted, but scores differ'}</p></section>
    <section className="aggregate-strip" aria-label="Aggregate results"><div><span>AVERAGE GAP · ALL PAIRS</span><strong>{averageGap.toFixed(1)} <small>points</small></strong></div><div><span>PAIRS WITH A DIFFERENT DECISION</span><strong>{changedDecisions} <small>of {data.examples.length}</small></strong></div><p>Across every paired profile in this saved audit.</p></section>
    <p className="evidence-note"><CircleHelp size={16} />Counterfactual results identify patterns for review; they do not establish intent or legal compliance.</p>
  </section>
}

function BeforeAfter({ data }: { data: DomainData }) {
  const [metric, setMetric] = useState(0)
  const tests = Array.from(new Set(data.before_after.map((item) => item.test)))
  const selected = tests[metric] ?? tests[0]
  const values = data.before_after.filter((item) => item.test === selected)
  const before = values.find((item) => item.stage.toLowerCase() === 'before')?.value ?? 0
  const after = values.find((item) => item.stage.toLowerCase() === 'after')?.value ?? 0
  const reduction = Math.abs(before) === 0 ? 0 : Math.max(0, Math.min(100, Math.round((1 - Math.abs(after) / Math.abs(before)) * 100)))
  const chartData = [{ stage: 'Before', value: before }, { stage: 'After', value: after }]
  return <>
    <PageHeading eyebrow="MITIGATION CHECK" title="What changed after the fixes?" description="Compare the saved audit measurements before and after the listed safeguards." />
    <section className="panel chart-panel"><div className="chart-heading"><div><span className="eyebrow">MEASURED OUTCOME</span><h3>{selected}</h3><p>Values shown exactly as reported in the audit file.</p></div><label className="sr-only" htmlFor="metric-select">Select metric to compare</label><div className="select-wrap metric-select"><select id="metric-select" value={metric} onChange={(e) => setMetric(Number(e.target.value))}>{tests.map((item, i) => <option value={i} key={item}>{item}</option>)}</select><ChevronDown size={14} /></div></div>
      <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><AreaChart data={chartData} margin={{ top: 12, right: 16, left: 0, bottom: 0 }}><defs><linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#2dd4bf" stopOpacity={0.26} /><stop offset="100%" stopColor="#2dd4bf" stopOpacity={0.01} /></linearGradient></defs><CartesianGrid stroke="rgba(255,255,255,.07)" vertical={false} /><XAxis dataKey="stage" tickLine={false} axisLine={false} tick={{ fill: '#a0abc2', fontSize: 12 }} /><YAxis tickLine={false} axisLine={false} tick={{ fill: '#a0abc2', fontSize: 12 }} width={44} /><Tooltip contentStyle={{ background: '#18223a', border: '1px solid rgba(255,255,255,.1)', borderRadius: 12, color: '#f5f7ff' }} /><Area type="monotone" dataKey="value" stroke="#2dd4bf" strokeWidth={3} fill="url(#chartFill)" activeDot={{ r: 6, fill: '#2dd4bf', stroke: '#0b1020', strokeWidth: 3 }} /></AreaChart></ResponsiveContainer></div>
      <div className="chart-legend"><div><span className="legend-dot before-dot" />Before <strong>{before}</strong></div><ArrowRight size={16} /><div><span className="legend-dot after-dot" />After <strong>{after}</strong></div></div>
    </section>
    <div className="reduction-card"><div className="reduction-icon"><ArrowDownRight size={22} /></div><div><span className="eyebrow">CHANGE IN SELECTED METRIC</span><h3>Gap reduced by <span>{reduction}%</span></h3><p>Calculated from the before and after values in this audit.</p></div><div className="reduction-stat"><span>Before</span><strong>{before}</strong><span>After</span><strong>{after}</strong></div></div>
    <div className="caveat"><ShieldAlert size={18} /><span>Fixes reduce bias but don&apos;t remove it entirely.</span></div>
    <section className="panel fixes-panel"><div className="panel-heading"><div><span className="eyebrow">MITIGATIONS IN THIS DEMO</span><h3>Safeguards applied</h3></div><span className="fixes-count">{data.fixes.length} checks</span></div><ul>{data.fixes.map((fix) => <li key={fix}><span className="fix-check"><Check size={14} /></span>{fix}</li>)}</ul></section>
  </>
}

function Dpdp({ data }: { data: DomainData }) {
  const principles = [
    { title: 'Lawful & transparent use', detail: 'Purpose and legal basis should be clear to people affected.', covered: true, icon: Scale },
    { title: 'Purpose limitation', detail: 'Use personal data only for its stated purpose.', covered: true, icon: ClipboardCheck },
    { title: 'Data minimisation', detail: 'Exclude attributes that are not needed for the decision.', covered: Boolean(data.dpdp_note?.data_minimisation), icon: Fingerprint },
    { title: 'Data accuracy', detail: 'Keep decision inputs accurate, complete, and current.', covered: Boolean(data.dpdp_note?.accuracy), icon: CheckCircle2 },
    { title: 'Storage limitation', detail: 'Set retention periods and remove data when no longer needed.', covered: false, icon: Activity },
    { title: 'Security safeguards', detail: 'Protect data with appropriate access and security controls.', covered: false, icon: LockKeyhole },
    { title: 'Accountability & rights', detail: 'Provide people with a way to understand and contest decisions.', covered: false, icon: Users },
  ]
  return <>
    <PageHeading eyebrow="RESPONSIBLE AI · INDIA" title="DPDP principles, in view." description="A practical checklist for considering personal data in automated decisions." right={<div className="guidance-pill"><CircleHelp size={15} />Guidance, not legal advice.</div>} />
    <div className="dpdp-intro"><div className="dpdp-shield"><ShieldCheck size={24} /></div><div><strong>{data.dpdp_note?.title ?? 'DPDP Act alignment'}</strong><p>{data.dpdp_note?.disclaimer ?? 'Guidance, not legal advice.'}</p></div></div>
    <div className="principle-grid">{principles.map(({ title, detail, covered, icon: Icon }, i) => <motion.article key={title} className="principle-card" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * .04 }}><div className="principle-top"><span className="principle-icon"><Icon size={18} /></span><span className={`coverage-badge ${covered ? 'checked' : 'not-covered'}`}>{covered ? <Check size={13} /> : <CircleHelp size={13} />}{covered ? 'Checked' : 'Not covered'}</span></div><h3>{title}</h3><p>{detail}</p></motion.article>)}</div>
    <div className="dpdp-disclaimer"><ShieldAlert size={17} /><div><strong>Scope of this checklist</strong><p>This is a high-level product review aid, not a legal determination. Confirm applicable requirements with qualified counsel. {data.dpdp_note?.synthetic_data}</p></div></div>
  </>
}

function Landing({ onRun, domain, setDomain, running, step }: { onRun: () => void; domain: string; setDomain: (d: string) => void; running: boolean; step: number }) {
  const steps = ['Preparing paired profiles', 'Checking fairness signals', 'Summarising audit evidence']
  return <main className="landing-shell"><header className="landing-header"><div className="brand"><div className="brand-mark"><Fingerprint size={20} /></div><span>FairHire<span className="brand-light"> Audit</span></span></div><span className="demo-label"><span className="live-dot" />Demo environment</span></header><div className="landing-content"><div className="hero-copy"><div className="hero-kicker"><span className="kicker-line" />RESPONSIBLE AI, MADE VISIBLE</div><h1>See if your AI<br /><span>treats everyone</span><br />equally.</h1><p className="hero-desc">A practical fairness audit for the decisions that shape people&apos;s lives. Compare outcomes, surface patterns, and see what changed.</p><div className="hero-chips"><span><Scale size={15} />Bias</span><span><Sparkles size={15} />Hallucination</span><span><LockKeyhole size={15} />Privacy</span></div><div className="hero-controls"><div className="domain-switch" role="group" aria-label="Choose audit domain"><button className={domain === 'hiring' ? 'domain-selected' : ''} onClick={() => setDomain('hiring')}>Hiring</button><button className={domain === 'lending' ? 'domain-selected' : ''} onClick={() => setDomain('lending')}>Lending</button></div><Button className="run-button" onClick={onRun} disabled={running}>{running ? <>Running audit… <Activity data-icon="inline-end" className="spin-icon" /></> : <>Run audit <ArrowRight data-icon="inline-end" /></>}</Button></div><div className="demo-caption"><span className="caption-dot" />Demo: replaying a saved audit</div>{running && <div className="run-progress" aria-live="polite"><div className="progress-track"><motion.span initial={{ width: 0 }} animate={{ width: `${((step + 1) / steps.length) * 100}%` }} /></div><span>{steps[step]}</span></div>}</div><div className="hero-art" aria-label="Illustration of two equivalent profiles being compared"><div className="art-glow" /><div className="art-orbit art-orbit-a" /><div className="art-orbit art-orbit-b" /><div className="art-card art-card-left"><div className="art-card-top"><span className="art-avatar">R</span><span className="art-status"><Check size={12} />Profile A</span></div><div className="art-line long" /><div className="art-line" /><div className="art-score"><div className="art-score-ring">95</div><span>Strong match</span></div></div><div className="art-equal">=</div><div className="art-card art-card-right"><div className="art-card-top"><span className="art-avatar purple">R</span><span className="art-status purple-text"><Check size={12} />Profile B</span></div><div className="art-line long" /><div className="art-line" /><div className="art-score"><div className="art-score-ring purple-ring">83</div><span>Strong match</span></div></div><div className="art-caption"><span className="art-caption-dot" />One detail changed. Outcomes compared.</div></div></div><footer className="landing-footer"><span>Built for decisions that deserve a second look.</span><span>Transparent by design <span className="footer-spark">✦</span></span></footer><AnimatePresence>{running && <motion.div className="scan-line" initial={{ opacity: 0 }} animate={{ opacity: .7, y: [0, 400, 0] }} exit={{ opacity: 0 }} transition={{ duration: 2.6, repeat: Infinity }} />}</AnimatePresence></main>
}

export default function FairHireDashboard() {
  const { data, error, isLoading } = useSWR<ResultsData>('/results.json', fetcher)
  const [domain, setDomain] = useState('hiring')
  const [section, setSection] = useState<Section>('overview')
  const [started, setStarted] = useState(false)
  const [running, setRunning] = useState(false)
  const [step, setStep] = useState(0)
  const [darkMode, setDarkMode] = useState(false)
  const current = data?.domains[domain]

  const downloadReport = () => {
    if (!data) return
    const report = { product: 'FairHire Audit', generatedAt: new Date().toISOString(), domain, result: current }
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `fairhire-${domain}-audit-report.json`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  const runAudit = () => {
    setRunning(true)
    setStep(0)
    const timer = window.setInterval(() => setStep((value) => value + 1), 850)
    window.setTimeout(() => {
      window.clearInterval(timer)
      setRunning(false)
      setStarted(true)
      setSection('overview')
    }, 2650)
  }

  if (isLoading) return <div className="loading-screen"><div className="brand-mark"><Fingerprint size={20} /></div><span>Loading saved audit…</span></div>
  if (error || !data || !current) return <div className="loading-screen error-screen"><ShieldAlert size={24} /><span>Could not load /results.json. Please check the saved audit file.</span></div>
  if (!started) return <Landing onRun={runAudit} domain={domain} setDomain={setDomain} running={running} step={Math.min(step, 2)} />

  return <div className="app-shell" data-theme={darkMode ? 'dark' : 'light'}><TopHeader domain={domain} setDomain={setDomain} section={section} setSection={setSection} onDownload={downloadReport} darkMode={darkMode} onToggleTheme={() => setDarkMode((value) => !value)} /><main className="dashboard-main"><AnimatePresence mode="wait"><motion.div key={`${section}-${domain}`} className="page-content" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -6 }} transition={{ duration: .2 }}>{section === 'overview' ? <Overview data={current} domain={domain} onSection={setSection} /> : section === 'compare' ? <Compare data={current} domain={domain} /> : section === 'before-after' ? <BeforeAfter data={current} /> : <Dpdp data={current} />}</motion.div></AnimatePresence><footer className="app-footer"><span>FairHire Audit <span>·</span> Research prototype</span><span>Synthetic data only</span></footer></main></div>
}
