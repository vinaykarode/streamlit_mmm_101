// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import { useState, useEffect } from 'react';
import {
    Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer, Area, ComposedChart, Legend
} from 'recharts';
import {
    Calculator, Calendar, TrendingUp, Activity, AlertTriangle, CheckCircle, Search, BookOpen, GitCompare, Sigma
} from 'lucide-react';

// --- Components ---

const MetricCard = ({ title, value, subtitle, status, icon: Icon }) => (
    <div className={`tw:p-6 tw:rounded-xl tw:border tw:transition-all tw:duration-300 tw:bg-white tw:border-slate-200 tw:shadow-sm`}>
        <div className="tw:flex tw:justify-between tw:items-start tw:mb-2">
            <p className="tw:text-sm tw:font-bold tw:uppercase tw:tracking-wider tw:text-slate-500">{title}</p>
            {Icon && <Icon size={20} className="tw:text-indigo-500" />}
        </div>
        <div className={`tw:text-3xl tw:font-bold tw:mb-1 ${
            status === 'good' ? 'tw:text-emerald-600' : status === 'bad' ? 'tw:text-rose-600' : 'tw:text-slate-800'
        }`}>
            {value}
        </div>
        <p className="tw:text-xs tw:text-slate-500 tw:leading-tight">{subtitle}</p>
    </div>
);

const AlgoCard = ({ title, acronym, bestFor, difficulty, description }) => (
    <div className="tw:bg-white tw:p-5 tw:rounded-xl tw:border tw:border-slate-200 tw:shadow-sm hover:tw:shadow-md tw:transition-shadow">
        <div className="tw:flex tw:justify-between tw:items-start tw:mb-3">
            <div>
                <p className="tw:font-bold tw:text-slate-900">{title}</p>
                <span className="tw:text-xs tw:font-bold tw:bg-slate-100 tw:text-slate-500 tw:px-2 tw:py-1 tw:rounded">{acronym}</span>
            </div>
            <div className={`tw:text-xs tw:font-bold tw:px-2 tw:py-1 tw:rounded ${
                difficulty === 'Low' ? 'tw:bg-emerald-100 tw:text-emerald-700' :
                    difficulty === 'Medium' ? 'tw:bg-amber-100 tw:text-amber-700' :
                        'tw:bg-rose-100 tw:text-rose-700'
            }`}>
                Complexity: {difficulty}
            </div>
        </div>
        <p className="tw:text-sm tw:text-slate-600 tw:mb-3">{description}</p>
        <div className="tw:text-xs tw:bg-indigo-50 tw:text-indigo-800 tw:p-2 tw:rounded tw:border tw:border-indigo-100">
            <p className="tw:font-bold tw:inline">Best For:</p> {bestFor}
        </div>
    </div>
);

const TbrGuide = () => {
    const [activeTab, setActiveTab] = useState('concepts');

    // --- Simulator State ---
    const [trendStrength, setTrendStrength] = useState(20); // Underlying growth
    const [seasonality, setSeasonality] = useState(500); // Wiggles
    const [trueLift, setTrueLift] = useState(1500); // Intervention Impact
    const [modelFit, setModelFit] = useState(0.95); // R-Squared (Inverse of noise)

    // --- Computed Metrics ---
    const [chartData, setChartData] = useState([]);
    const [metrics, setMetrics] = useState({
        rSquared: 0,
        estimatedLift: 0,
        confidence: 'Low'
    });

    useEffect(() => {
        // Generate Time Series Data (100 Days)
        // Days 0-70: Training (Pre-Test)
        // Days 71-100: Intervention (Post-Test)

        const interventionDay = 70;
        const totalDays = 100;
        const data = [];

        let cumulativeActual = 0;
        let cumulativePred = 0;
        let sumSquaredTotal = 0;
        let sumSquaredResidual = 0;
        const meanY = 5000 + (trendStrength * 35); // Approx mean for R2 calc

        // Noise amplitude is inversely related to Model Fit
        const noiseBase = 1000 * (1 - modelFit);

        for(let t = 0; t <= totalDays; t++) {
            // 1. The "True" Underlying Business Pattern (Counterfactual)
            const baseTrend = 5000 + (t * trendStrength);
            const seasonalComp = Math.sin(t / 5) * seasonality;

            // 2. The Model's Prediction (Smoothed version of truth)
            const predictionNoise = (Math.random() - 0.5) * noiseBase;
            const predictedY = baseTrend + seasonalComp + predictionNoise;

            // 3. The "Actual" Observed Data
            // Actual has its own random daily noise, PLUS the Lift if after day 70.
            const dailyRandomness = (Math.random() - 0.5) * 200; // Inherent business noise
            const impact = t > interventionDay ? trueLift : 0;
            const actualY = baseTrend + seasonalComp + dailyRandomness + impact;

            // Stats for Pre-Test period only (to calc R2)
            if (t <= interventionDay) {
                sumSquaredTotal += Math.pow(actualY - meanY, 2);
                sumSquaredResidual += Math.pow(actualY - predictedY, 2);
            } else {
                // Calculate Lift Impact in Post-Period
                cumulativeActual += actualY;
                cumulativePred += predictedY;
            }

            data.push({
                day: t,
                Actual: Math.round(actualY),
                Counterfactual: Math.round(predictedY),
                isIntervention: t > interventionDay
            });
        }

        // Calculate R-Squared (Pre-Test Fit)
        // R2 = 1 - (SS_res / SS_tot)
        const r2 = Math.max(0, 1 - (sumSquaredResidual / sumSquaredTotal));

        // Estimated Lift
        const totalEstLift = cumulativeActual - cumulativePred;

        // Simple Confidence Heuristic
        let conf = 'High';
        if (r2 < 0.8) conf = 'Medium';
        if (r2 < 0.6) conf = 'Low';

        setMetrics({
            rSquared: r2.toFixed(2),
            estimatedLift: totalEstLift,
            confidence: conf
        });

        setChartData(data);

    }, [trendStrength, seasonality, trueLift, modelFit]);

    const formatNum = (num) => new Intl.NumberFormat('en-US').format(Math.round(num));

    return (
        <div className="tw:min-h-screen tw:bg-slate-50 tw:text-slate-800 tw:font-sans">
            {/* POLYFILL: This style block manually enables the responsive grid classes
                that might be failing due to Tailwind prefix + variant conflicts.
            */}
            <style>{`
                @media (min-width: 768px) {
                    .md\\:tw\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
                }
                @media (min-width: 1024px) {
                    .lg\\:tw\\:grid-cols-12 { grid-template-columns: repeat(12, minmax(0, 1fr)); }
                    .lg\\:tw\\:col-span-4 { grid-column: span 4 / span 4; }
                    .lg\\:tw\\:col-span-8 { grid-column: span 8 / span 8; }
                }
            `}</style>

            {/* Header */}
            <header className="tw:bg-indigo-900 tw:text-white tw:p-6 tw:shadow-lg">
                <div className="tw:max-w-6xl tw:mx-auto">
                    <div className="tw:flex tw:items-center tw:gap-3 tw:mb-2">
                        <Calendar className="tw:w-8 tw:h-8 tw:text-indigo-400" />
                        <p className="tw:text-3xl tw:font-bold">Incrementality Algorithms: Time-Based Regression (TBR) Simulator</p>
                    </div>
                    <p className="tw:text-indigo-200 tw:max-w-3xl tw:leading-relaxed">
                        A guide to measuring the impact of TV ads, billboards, and pricing changes using <span className="tw:font-bold">Counterfactuals</span>.
                    </p>
                </div>
            </header>

            {/* Navigation */}
            <div className="tw:bg-white tw:border-b tw:sticky tw:top-0 tw:z-10 tw:shadow-sm">
                <div className="tw:max-w-6xl tw:mx-auto tw:flex tw:gap-8 tw:px-6 tw:overflow-x-auto">
                    {[
                        { id: 'concepts', label: '1. Real World Example', icon: <BookOpen size={18} /> },
                        { id: 'simulator', label: '2. Impact Simulator', icon: <Activity size={18} /> },
                        { id: 'advanced', label: '3. Deep Dive & Algorithms', icon: <GitCompare size={18} /> },
                    ].map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`tw:py-4 tw:px-2 tw:border-b-2 tw:font-medium tw:transition-all tw:flex tw:items-center tw:gap-2 tw:whitespace-nowrap ${
                                activeTab === tab.id
                                    ? 'tw:border-indigo-600 tw:text-indigo-700 tw:bg-indigo-50'
                                    : 'tw:border-transparent tw:text-slate-500 hover:tw:text-slate-700'
                            }`}
                        >
                            {tab.icon}
                            {tab.label}
                        </button>
                    ))}
                </div>
            </div>

            <main className="tw:max-w-6xl tw:mx-auto tw:p-6">

                {/* === TAB 1: CONCEPTS === */}
                {activeTab === 'concepts' && (
                    <div className="tw:animate-in tw:fade-in tw:duration-500 tw:space-y-8">

                        <div className="tw:bg-white tw:p-8 tw:rounded-xl tw:shadow-sm tw:border tw:border-slate-200">
                            <p className="tw:text-2xl tw:font-bold tw:text-slate-900 tw:mb-6">Scenario: The Coffee Shop TV Ad</p>
                            <div className="tw:grid md:tw:grid-cols-2 tw:gap-12 tw:items-center">
                                <div className="tw:space-y-6 tw:text-slate-600 tw:leading-relaxed">
                                    <p>
                                        You own "Java Joy," a local coffee chain. You decide to run a TV Commercial for one month.
                                    </p>
                                    <div className="tw:bg-indigo-50 tw:p-4 tw:rounded-lg tw:border tw:border-indigo-100">
                                        <p className="tw:font-bold tw:text-indigo-900 tw:mb-2">The Problem:</p>
                                        <p className="tw:text-sm">
                                            When someone walks in to buy a latte, you don't know if they saw the TV ad. There is no "cookie" or "click ID" on a human being.
                                            <br/><br/>
                                            <span className="tw:font-bold">You cannot A/B test a TV commercial.</span> Everyone in the city sees it at the same time.
                                        </p>
                                    </div>

                                    <div className="tw:space-y-4">
                                        <p className="tw:font-bold tw:text-slate-900">How TBR solves this:</p>
                                        <ul className="tw:space-y-4">
                                            <li className="tw:flex tw:gap-3">
                                                <div className="tw:bg-slate-100 tw:p-2 tw:rounded-lg tw:text-slate-700 tw:h-fit">1</div>
                                                <div>
                                                    <p className="tw:font-bold tw:text-slate-900">Training (Pre-Test):</p>
                                                    <p className="tw:text-sm tw:mt-1">We study your sales from the last year. We learn that "Mondays are slow" and "Cold weather boosts Latte sales."</p>
                                                </div>
                                            </li>
                                            <li className="tw:flex tw:gap-3">
                                                <div className="tw:bg-slate-100 tw:p-2 tw:rounded-lg tw:text-slate-700 tw:h-fit">2</div>
                                                <div>
                                                    <p className="tw:font-bold tw:text-slate-900">Prediction (Counterfactual):</p>
                                                    <p className="tw:text-sm tw:mt-1">We ask the model: <em>"Assuming no TV ad existed, how much coffee would we have sold this month?"</em></p>
                                                </div>
                                            </li>
                                            <li className="tw:flex tw:gap-3">
                                                <div className="tw:bg-emerald-100 tw:p-2 tw:rounded-lg tw:text-emerald-700 tw:h-fit">3</div>
                                                <div>
                                                    <p className="tw:font-bold tw:text-slate-900">Measurement (The Lift):</p>
                                                    <p className="tw:text-sm tw:mt-1">
                                                        Actual Sales (High) - Predicted Sales (Low) = <span className="tw:font-bold">TV Ad Impact</span>.
                                                    </p>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </div>

                                <div className="tw:bg-slate-900 tw:text-white tw:p-6 tw:rounded-xl tw:shadow-lg">
                                    <p className="tw:font-bold tw:text-slate-200 tw:mb-6 tw:uppercase tw:text-xs tw:tracking-wider tw:border-b tw:border-slate-700 tw:pb-2">Visualizing the Counterfactual</p>

                                    {/* Visual Diagram */}
                                    <div className="tw:relative tw:h-[200px] tw:flex tw:items-end tw:justify-between tw:gap-2 tw:px-2">
                                        {[30, 45, 35, 50, 40, 60, 55, 80, 75, 90].map((h, i) => (
                                            <div key={i} className="tw:w-full tw:flex tw:flex-col tw:justify-end tw:h-full tw:gap-1 tw:relative tw:group">
                                                {/* The Counterfactual (Ghost) Bar */}
                                                {i > 6 && (
                                                    <div
                                                        className="tw:w-full tw:border-2 tw:border-dashed tw:border-slate-500 tw:absolute tw:bottom-0"
                                                        style={{ height: `${h * 0.7}%` }}
                                                    >
                                                    </div>
                                                )}

                                                {/* The Actual Bar */}
                                                <div
                                                    className={`tw:w-full tw:rounded-t ${i > 6 ? 'tw:bg-emerald-500' : 'tw:bg-indigo-500'}`}
                                                    style={{ height: `${h}%` }}
                                                >
                                                </div>

                                                {/* Tooltip for concept */}
                                                {i === 8 && (
                                                    <div className="tw:absolute tw:bottom-full tw:mb-2 tw:left-1/2 tw:-translate-x-1/2 tw:bg-white tw:text-slate-900 tw:text-xs tw:p-2 tw:rounded tw:whitespace-nowrap tw:font-bold tw:shadow-lg">
                                                        Gap = Lift
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                    <div className="tw:flex tw:justify-between tw:text-xs tw:mt-4 tw:text-slate-400 tw:font-mono">
                                        <span>PRE-TEST (Training)</span>
                                        <span>POST-TEST (Intervention)</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* === TAB 2: SIMULATOR === */}
                {activeTab === 'simulator' && (
                    <div className="tw:animate-in tw:slide-in-from-right tw:duration-500 tw:space-y-8">
                        <div className="tw:grid lg:tw:grid-cols-12 tw:gap-8">
                            {/* Left: Inputs */}
                            <div className="lg:tw:col-span-4 tw:space-y-6">
                                <div className="tw:bg-white tw:p-6 tw:rounded-xl tw:shadow-md tw:border tw:border-slate-200">
                                    <p className="tw:text-lg tw:font-bold tw:mb-4 tw:flex tw:items-center tw:gap-2 tw:text-slate-800">
                                        <Calculator size={20} /> Experiment Controls
                                    </p>

                                    <div className="tw:space-y-6">
                                        {/* True Lift */}
                                        <div>
                                            <div className="tw:flex tw:justify-between tw:text-sm tw:mb-1">
                                                <span className="tw:text-slate-500 tw:font-bold">Intervention Impact (Lift)</span>
                                                <span className="tw:font-bold tw:text-emerald-600">+{formatNum(trueLift)}</span>
                                            </div>
                                            <input
                                                type="range" min="0" max="3000" step="100"
                                                value={trueLift} onChange={(e) => setTrueLift(Number(e.target.value))}
                                                className="tw:w-full tw:accent-emerald-600"
                                            />
                                            <div className="tw:text-xs tw:text-slate-400 tw:mt-1">How much revenue your campaign actually added.</div>
                                        </div>

                                        {/* Model Fit */}
                                        <div className="tw:pt-4 tw:border-t tw:border-slate-100">
                                            <div className="tw:flex tw:justify-between tw:text-sm tw:mb-1">
                                                <span className="tw:text-slate-500 tw:font-bold">Model Fit Quality (R²)</span>
                                                <span className={`tw:font-bold ${metrics.rSquared > 0.8 ? 'tw:text-indigo-600' : 'tw:text-rose-600'}`}>
                            {metrics.rSquared}
                        </span>
                                            </div>
                                            <input
                                                type="range" min="0.10" max="0.99" step="0.01"
                                                value={modelFit} onChange={(e) => setModelFit(Number(e.target.value))}
                                                className={`tw:w-full ${metrics.rSquared > 0.8 ? 'tw:accent-indigo-600' : 'tw:accent-rose-500'}`}
                                            />
                                            <div className="tw:text-xs tw:text-slate-400 tw:mt-1">
                                                Drag LOW to see how a bad model makes the Counterfactual (dashed line) go crazy.
                                            </div>
                                        </div>

                                        {/* Seasonality */}
                                        <div className="tw:pt-4 tw:border-t tw:border-slate-100">
                                            <div className="tw:flex tw:justify-between tw:text-sm tw:mb-1">
                                                <span className="tw:text-slate-500">Seasonality Strength</span>
                                                <span className="tw:font-bold tw:text-slate-600">High</span>
                                            </div>
                                            <input
                                                type="range" min="0" max="1000" step="50"
                                                value={seasonality} onChange={(e) => setSeasonality(Number(e.target.value))}
                                                className="tw:w-full tw:accent-slate-500"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Status Box */}
                                <div className={`tw:p-4 tw:rounded-xl tw:border ${metrics.confidence === 'High' ? 'tw:bg-emerald-50 tw:border-emerald-200 tw:text-emerald-800' : 'tw:bg-rose-50 tw:border-rose-200 tw:text-rose-800'}`}>
                                    <p className="tw:font-bold tw:text-sm tw:flex tw:items-center tw:gap-2">
                                        {metrics.confidence === 'High' ? <CheckCircle size={16}/> : <AlertTriangle size={16}/>}
                                        Experiment Reliability: {metrics.confidence}
                                    </p>
                                    <p className="tw:text-xs tw:mt-1 tw:opacity-80">
                                        {metrics.confidence === 'High'
                                            ? "Model fits historical data well. The calculated lift is trustworthy."
                                            : "Model fit is poor. The 'Counterfactual' is erratic, so the estimated lift is likely noise."}
                                    </p>
                                </div>
                            </div>

                            {/* Right: Chart & Metrics */}
                            <div className="lg:tw:col-span-8 tw:space-y-6">

                                {/* Chart */}
                                <div className="tw:bg-white tw:p-6 tw:rounded-xl tw:shadow-md tw:border tw:border-slate-200 tw:h-[450px] tw:flex tw:flex-col">
                                    <p className="tw:font-bold tw:text-slate-700 tw:mb-2 tw:flex tw:justify-between tw:items-center">
                                        <span>Time Series Analysis</span>
                                        <span className="tw:text-xs tw:bg-slate-100 tw:px-2 tw:py-1 tw:rounded tw:text-slate-500">Days 0-70: Training • Days 71-100: Test</span>
                                    </p>
                                    <div className="tw:flex-grow">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <ComposedChart data={chartData} margin={{ top: 10, right: 10, bottom: 0, left: 0 }}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                                                <XAxis
                                                    dataKey="day"
                                                    label={{ value: 'Days', position: 'insideBottomRight', offset: -5 }}
                                                />
                                                <YAxis hide domain={['auto', 'auto']} />
                                                <Tooltip
                                                    formatter={(val) => Math.round(val)}
                                                />
                                                <Legend verticalAlign="top"/>

                                                {/* Intervention Line */}
                                                <ReferenceLine x={70} stroke="#64748b" strokeDasharray="3 3" label={{ value: "Intervention Starts", position: 'insideTopLeft', fill:'#64748b', fontSize: 10 }} />

                                                {/* Counterfactual Area (The Gap) */}
                                                <Area
                                                    type="monotone"
                                                    dataKey="Actual"
                                                    stroke="none"
                                                    fill="#10b981"
                                                    fillOpacity={0.1}
                                                />

                                                {/* Lines */}
                                                <Line
                                                    type="monotone"
                                                    dataKey="Actual"
                                                    stroke="#0f172a"
                                                    strokeWidth={2}
                                                    dot={false}
                                                    name="Actual Sales (Solid)"
                                                />
                                                <Line
                                                    type="monotone"
                                                    dataKey="Counterfactual"
                                                    stroke="#6366f1"
                                                    strokeWidth={2}
                                                    strokeDasharray="5 5"
                                                    dot={false}
                                                    name="Counterfactual (Dashed)"
                                                />
                                            </ComposedChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>

                                {/* Metrics Grid */}
                                <div className="tw:grid tw:grid-cols-2 tw:gap-4">
                                    <MetricCard
                                        title="Pre-Test Fit (R²)"
                                        value={metrics.rSquared}
                                        subtitle="Target: > 0.80"
                                        status={metrics.confidence === 'High' ? 'good' : 'bad'}
                                        icon={Search}
                                    />
                                    <MetricCard
                                        title="Est. Cumulative Lift"
                                        value={`+${formatNum(metrics.estimatedLift)}`}
                                        subtitle={`True Input Lift: +${formatNum(trueLift * 30)}`} // 30 days of test
                                        status="neutral"
                                        icon={TrendingUp}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Deep Dive Section (Bottom of Simulator) */}
                        <div className="tw:bg-slate-50 tw:border tw:border-slate-200 tw:rounded-xl tw:p-6">
                            <p className="tw:text-lg tw:font-bold tw:text-slate-800 tw:mb-4 tw:flex tw:items-center tw:gap-2">
                                <Sigma size={20} className="tw:text-indigo-600"/> The Math Under the Hood
                            </p>
                            <div className="tw:grid md:tw:grid-cols-2 tw:gap-8 tw:text-sm">
                                <div className="tw:space-y-2">
                                    <p className="tw:font-mono tw:bg-white tw:p-3 tw:rounded tw:border tw:border-slate-200 tw:text-slate-600">
                                        Y<sub>t</sub> = &alpha; + &beta;<sub>1</sub>Time + &beta;<sub>2</sub>Season + &epsilon;
                                    </p>
                                    <p className="tw:text-slate-600 tw:leading-relaxed">
                                        <span className="tw:font-bold">1. Training Phase (Days 0-70):</span> We fit a regression line to predict Sales (Y) based on Time Trend and Seasonality. This creates our "Model".
                                    </p>
                                </div>
                                <div className="tw:space-y-2">
                                    <p className="tw:font-mono tw:bg-white tw:p-3 tw:rounded tw:border tw:border-slate-200 tw:text-slate-600">
                                        Lift = &sum; (Actual<sub>t</sub> - Predicted<sub>t</sub>)
                                    </p>
                                    <p className="tw:text-slate-600 tw:leading-relaxed">
                                        <span className="tw:font-bold">2. Test Phase (Days 71-100):</span> We use the Model to draw the dashed line (Counterfactual). We subtract that from what actually happened. The remainder is your Lift.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* === TAB 3: DEEP DIVE & ALGORITHMS === */}
                {activeTab === 'advanced' && (
                    <div className="tw:animate-in tw:fade-in tw:duration-500 tw:max-w-5xl tw:mx-auto tw:space-y-10">

                        <div className="tw:bg-white tw:p-8 tw:rounded-xl tw:shadow-sm tw:border tw:border-slate-200">
                            <p className="tw:text-2xl tw:font-bold tw:text-slate-900 tw:mb-6 tw:flex tw:items-center tw:gap-2">
                                <GitCompare className="tw:text-indigo-600"/> Algorithm Battle Royale
                            </p>
                            <p className="tw:text-lg tw:text-slate-600 tw:mb-8">
                                TBR is just one way to generate a Counterfactual. Here is how it compares to the other heavyweights in causal inference.
                            </p>

                            <div className="tw:grid md:tw:grid-cols-2 tw:gap-6">
                                <AlgoCard
                                    title="Time-Based Regression"
                                    acronym="TBR"
                                    difficulty="Low"
                                    bestFor="Single region tests (e.g. Total US TV Ad) with strong historical patterns."
                                    description="Uses only the region's own history to predict the future. Simple, transparent, but fails if an external shock (like a pandemic) happens during the test."
                                />
                                <AlgoCard
                                    title="Diff-in-Differences"
                                    acronym="DiD"
                                    difficulty="Medium"
                                    bestFor="When you have a Control group that tracks parallel to the Test group."
                                    description="Subtracts the drift of a Control group from the Test group. More robust than TBR against external shocks, but requires finding a good parallel control."
                                />
                                <AlgoCard
                                    title="Synthetic Control"
                                    acronym="SCM"
                                    difficulty="High"
                                    bestFor="State-level tests (e.g., California) where no single other state is a good match."
                                    description="Creates a 'Frankenstein' control by mathematically weighting multiple regions (e.g., 20% NY + 30% TX + 50% FL) to perfectly match the Test region's history."
                                />
                                <AlgoCard
                                    title="CausalImpact (BSTS)"
                                    acronym="BSTS"
                                    difficulty="High"
                                    bestFor="Complex time series with seasonality, holidays, and multiple control variables."
                                    description="Uses Bayesian Structural Time Series. It's basically TBR on steroids. It gives you probability intervals (e.g., '95% chance lift is between $1k and $2k') rather than a single number."
                                />
                                <AlgoCard
                                    title="Interrupted Time Series"
                                    acronym="ITS"
                                    difficulty="Low"
                                    bestFor="Policy changes or sudden interventions where no control group exists."
                                    description="Very similar to TBR but often uses segmented regression lines (slope change) rather than just subtracting a prediction. Good for measuring long-term trend shifts."
                                />
                            </div>
                        </div>

                        <div className="tw:bg-indigo-900 tw:text-white tw:p-8 tw:rounded-xl tw:shadow-lg">
                            <p className="tw:text-xl tw:font-bold tw:mb-4">When to use which?</p>
                            <div className="tw:space-y-4 tw:text-indigo-100">
                                <div className="tw:flex tw:gap-4 tw:items-start">
                                    <CheckCircle className="tw:shrink-0 tw:mt-1 tw:text-emerald-400"/>
                                    <div>
                                        <p className="tw:font-bold">Do you have a Control Group (e.g., a region where ads didn't run)?</p>
                                        <p className="tw:text-sm tw:opacity-80 tw:mt-1">Yes? Use <span className="tw:font-bold">Diff-in-Diff</span> or <span className="tw:font-bold">Synthetic Control</span>. They are safer.</p>
                                    </div>
                                </div>
                                <div className="tw:flex tw:gap-4 tw:items-start">
                                    <CheckCircle className="tw:shrink-0 tw:mt-1 tw:text-emerald-400"/>
                                    <div>
                                        <p className="tw:font-bold">Is it a nationwide change (e.g., Superbowl Ad)?</p>
                                        <p className="tw:text-sm tw:opacity-80 tw:mt-1">Yes? You have no control group. You MUST use <span className="tw:font-bold">TBR</span> or <span className="tw:font-bold">CausalImpact (BSTS)</span>.</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                )}

            </main>
        </div>
    );
};

export default TbrGuide;