import { useState, useEffect } from 'react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer, Legend
} from 'recharts';
import {
    Calculator, Activity, Globe, AlertTriangle, CheckCircle, HelpCircle, Clock, TrendingUp, Scale, BookOpen
} from 'lucide-react';

// --- Math Helpers ---

// @ts-ignore
function normInv(p) {
    // Approximation for Inverse Cumulative Normal Distribution (Probit)
    if (p <= 0 || p >= 1) return 0;
    const a1 = -39.6968302866538, a2 = 220.946098424521, a3 = -275.928510446969;
    const a4 = 138.357751867269, a5 = -30.6647980661472, a6 = 2.50662827745924;
    const b1 = -54.4760987982241, b2 = 161.585836858041, b3 = -155.698979859887;
    const b4 = 66.8013118877197, b5 = -13.2806815528857, c1 = -7.78489400243029e-03;
    const c2 = -0.322396458041136, c3 = -2.40075827716184, c4 = -2.54973253934373;
    const c5 = 4.37466414146497, c6 = 2.93816398269878;
    const d1 = 7.78469570904146e-03, d2 = 0.32246712907004, d3 = 2.445134137143;
    const d4 = 3.75440866190742;
    const p_low = 0.02425, p_high = 1 - p_low;
    let q, r;
    if (p < p_low) {
        q = Math.sqrt(-2 * Math.log(p));
        return (((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) /
            ((((d1 * q + d2) * q + d3) * q + d4) * q + 1);
    } else if (p <= p_high) {
        q = p - 0.5;
        r = q * q;
        return (((((a1 * r + a2) * r + a3) * r + a4) * r + a5) * r + a6) * q /
            (((((b1 * r + b2) * r + b3) * r + b4) * r + b5) * r + 1);
    } else {
        q = Math.sqrt(-2 * Math.log(1 - p));
        return -(((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) /
            ((((d1 * q + d2) * q + d3) * q + d4) * q + 1);
    }
}

// --- Components ---
// @ts-ignore
const Card = ({ title, icon: Icon, children, className = "" }) => (
    <div className={`bg-white p-6 rounded-xl shadow-sm border border-slate-200 ${className}`}>
        <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            {Icon && <Icon size={20} className="text-emerald-600" />}
            {title}
        </h3>
        {children}
    </div>
);
// @ts-ignore
const DefinitionBox = ({ term, definition, analogy }) => (
    <div className="mb-6 last:mb-0">
        <h4 className="font-bold text-emerald-800 text-md flex items-center gap-2 mb-1">
            {term}
        </h4>
        <p className="text-slate-700 text-sm mb-2 leading-relaxed">{definition}</p>
        <div className="bg-emerald-50 p-3 rounded-lg text-xs text-emerald-900 border border-emerald-100 flex gap-2">
            <span className="font-bold uppercase tracking-wide text-[10px] mt-0.5">Analogy:</span>
            <span className="italic">{analogy}</span>
        </div>
    </div>
);

const IncrementalityGuide = () => {
    const [activeTab, setActiveTab] = useState('guide');

    // --- Simulator State ---
    const [dailyRevenue, setDailyRevenue] = useState(10000);
    const [volatility, setVolatility] = useState(0.15); // 15% daily standard deviation
    const [expectedLift, setExpectedLift] = useState(0.05); // 5% lift
    const [plannedDuration, setPlannedDuration] = useState(14); // 2 weeks
    // @ts-ignore
    const [power, setPower] = useState(0.80);
    // @ts-ignore
    const [alpha, setAlpha] = useState(0.10); // 90% Confidence is common in Biz

    // --- Calculated Outputs ---
    const [powerCurveData, setPowerCurveData] = useState([]);
    const [currentMDE, setCurrentMDE] = useState(0);
    const [testStatus, setTestStatus] = useState('optimal'); // optimal, underpowered, overpowered

    useEffect(() => {
        // 1. Calculate Power Curve (Duration vs MDE)
        // Formula derived for Geo Testing: MDE = (Z_alpha + Z_beta) * sigma / sqrt(n)
        // where sigma is relative volatility * daily_revenue
        // We simplify to Relative MDE = (Z_alpha + Z_beta) * Volatility / sqrt(Days)

        const z_alpha = normInv(1 - alpha / 2);
        const z_beta = normInv(power);
        const factor = (z_alpha + z_beta) * volatility;

        const data = [];
        // Calculate for 1 to 60 days
        for(let d = 3; d <= 60; d++) {
            const mde = factor / Math.sqrt(d);
            data.push({
                days: d,
                mde: mde,
                mdePct: (mde * 100).toFixed(2),
                targetLift: expectedLift * 100
            });
        }
        // @ts-ignore
        setPowerCurveData(data);

        // 2. Calculate specific MDE for current planned duration
        const calculatedMDE = factor / Math.sqrt(plannedDuration);
        setCurrentMDE(calculatedMDE);

        // 3. Determine Status
        if (calculatedMDE > expectedLift) {
            setTestStatus('underpowered'); // MDE is 7%, Lift is 5% -> Can't see it.
        } else if (calculatedMDE < expectedLift * 0.5) {
            setTestStatus('overpowered'); // MDE is 1%, Lift is 5% -> Waste of time.
        } else {
            setTestStatus('optimal');
        }

    }, [dailyRevenue, volatility, expectedLift, plannedDuration, power, alpha]);

    // @ts-ignore
    const formatUSD = (num) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(num);
    // @ts-ignore
    const formatPct = (num) => `${(num * 100).toFixed(1)}%`;

    return (
        <div className="min-h-screen bg-slate-50 text-slate-800 font-sans">

            {/* Header */}
            <header className="bg-slate-900 text-white p-6 shadow-lg">
                <div className="max-w-6xl mx-auto">
                    <div className="flex items-center gap-3 mb-2">
                        <Globe className="w-8 h-8 text-emerald-400" />
                        <h1 className="text-3xl font-bold">Incrementality Experiment Design</h1>
                    </div>
                    <p className="text-slate-300 max-w-3xl leading-relaxed">
                        A practical guide to <strong>Power Analysis</strong> for real-world experiments.
                        Learn how to calculate the correct duration for your geo-lift tests and understand the critical difference between <em>what you expect to happen</em> (Lift) and <em>what you can actually measure</em> (MDE).
                    </p>
                </div>
            </header>

            {/* Navigation */}
            <div className="bg-white border-b sticky top-0 z-10 shadow-sm">
                <div className="max-w-6xl mx-auto flex gap-8 px-6 overflow-x-auto">
                    {[
                        { id: 'guide', label: '1. The Concepts', icon: <BookOpen size={18} /> },
                        { id: 'simulator', label: '2. Design Your Test', icon: <Calculator size={18} /> },
                    ].map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`py-4 px-2 border-b-2 font-medium transition-all flex items-center gap-2 whitespace-nowrap ${
                                activeTab === tab.id
                                    ? 'border-emerald-600 text-emerald-700 bg-emerald-50'
                                    : 'border-transparent text-slate-500 hover:text-slate-700'
                            }`}
                        >
                            {tab.icon}
                            {tab.label}
                        </button>
                    ))}
                </div>
            </div>

            <main className="max-w-6xl mx-auto p-6">

                {/* === TAB 1: THE CONCEPTS === */}
                {activeTab === 'guide' && (
                    <div className="animate-in fade-in duration-500 grid lg:grid-cols-3 gap-8">

                        {/* Left Column: Narrative */}
                        <div className="lg:col-span-2 space-y-8">
                            <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
                                <h2 className="text-2xl font-bold text-slate-900 mb-4">The Scenario: "The Sneaker Drop"</h2>
                                <p className="text-lg text-slate-600 leading-relaxed mb-6">
                                    You are the Marketing Director for a sneaker brand. You want to run Facebook Ads in <strong>California</strong> to see if it drives extra sales.
                                    <br/><br/>
                                    Your boss asks: <em>"If we spend $50k, how do we know the sales wouldn't have happened anyway?"</em>
                                    <br/><br/>
                                    You decide to run an <strong>Incrementality Test</strong> (Geo-Test). You will compare California (Test) against a synthetic baseline (Control) for 2 weeks. But before you launch, you must do a <strong>Power Analysis</strong>.
                                </p>

                                <div className="bg-indigo-50 border-l-4 border-indigo-500 p-4 rounded-r">
                                    <h3 className="font-bold text-indigo-900 flex items-center gap-2">
                                        <Activity size={18}/> The Core Problem: Signal vs. Noise
                                    </h3>
                                    <p className="text-indigo-800 mt-2 text-sm leading-relaxed">
                                        California's daily sales are not a flat line. They bounce up and down by roughly $1,500 every day just due to weather, mood, or randomness. This is the <strong>Noise</strong>.
                                        <br/><br/>
                                        Your ads might add $500/day in sales. This is the <strong>Signal (Lift)</strong>.
                                        <br/><br/>
                                        <strong>Power Analysis</strong> answers one question: <em>Is the Signal ($500) strong enough to be seen through the Noise ($1,500)?</em>
                                    </p>
                                </div>
                            </div>

                            <Card title="The Vocabulary of Experiments" icon={BookOpen}>
                                <DefinitionBox
                                    term="Lift (Effect Size)"
                                    definition="The actual real-world impact you hope to achieve. This is your hypothesis. E.g., 'I believe ads will increase sales by 5%'."
                                    analogy="The brightness of the star you are trying to find."
                                />
                                <DefinitionBox
                                    term="MDE (Minimum Detectable Effect)"
                                    definition="The smallest lift your experiment is CAPABLE of detecting with statistical confidence. This is determined by your sample size (duration) and noise."
                                    analogy="The resolution of your telescope. If your telescope can only see big stars (High MDE), it will miss the small star (Low Lift)."
                                />
                                <DefinitionBox
                                    term="Power"
                                    definition="The probability (usually 80%) that you will successfully detect the lift IF it actually exists. It's your 'Batting Average' for finding truth."
                                    analogy="If there is a star, how likely are we to spot it? 80% power means we miss it 20% of the time."
                                />
                                <DefinitionBox
                                    term="Duration (Sample Size)"
                                    definition="In geo-testing, Time = Data. Running the test longer gathers more data points, which averages out the daily noise and lowers your MDE."
                                    analogy="The exposure time of your camera. Longer exposure = clearer image = ability to see fainter stars."
                                />
                            </Card>
                        </div>

                        {/* Right Column: Visual Summary */}
                        <div className="lg:col-span-1 space-y-6">
                            <div className="bg-slate-800 text-white p-6 rounded-xl shadow-lg">
                                <h3 className="font-bold text-emerald-400 mb-4 flex items-center gap-2">
                                    <Scale size={20} /> The Golden Rule
                                </h3>
                                <div className="space-y-6 text-sm">
                                    <div>
                                        <div className="font-bold mb-1 text-white">Case A: Lift &gt; MDE</div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <div className="h-2 w-16 bg-emerald-500 rounded"></div>
                                            <span className="text-xs text-emerald-300">Lift (5%)</span>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <div className="h-2 w-8 bg-slate-500 rounded"></div>
                                            <span className="text-xs text-slate-400">MDE (2%)</span>
                                        </div>
                                        <p className="mt-2 text-emerald-200 italic">
                                            "Success! The signal is louder than the threshold. We will likely get a Significant result."
                                        </p>
                                    </div>

                                    <div className="border-t border-slate-700 pt-4">
                                        <div className="font-bold mb-1 text-white">Case B: Lift &lt; MDE</div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <div className="h-2 w-8 bg-emerald-500/50 rounded"></div>
                                            <span className="text-xs text-emerald-300/50">Lift (2%)</span>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <div className="h-2 w-16 bg-rose-500 rounded"></div>
                                            <span className="text-xs text-rose-300">MDE (5%)</span>
                                        </div>
                                        <p className="mt-2 text-rose-200 italic">
                                            "Failure. The effect exists, but your experiment is too 'blurry' (noisy) to see it. You will get a False Negative."
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-blue-50 p-6 rounded-xl border border-blue-100 text-blue-900 text-sm">
                                <h4 className="font-bold mb-2 flex items-center gap-2">
                                    <HelpCircle size={16}/> Why Duration Matters
                                </h4>
                                <p>
                                    In A/B testing (users), you add more users to lower MDE.
                                    <br/><br/>
                                    In Geo-Testing, you can't add more "Californias". <strong>You add more Days.</strong>
                                    <br/><br/>
                                    Doubling the duration reduces noise by roughly $\sqrt{2}$ (approx 30%).
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                {/* === TAB 2: SIMULATOR === */}
                {activeTab === 'simulator' && (
                    <div className="animate-in slide-in-from-right duration-500 grid lg:grid-cols-12 gap-8">

                        {/* INPUT PANEL */}
                        <div className="lg:col-span-4 space-y-6">
                            <Card title="Experiment Parameters" icon={Calculator}>
                                {/* Revenue */}
                                <div className="mb-5">
                                    <label className="text-xs font-bold text-slate-500 uppercase mb-1 block">Avg. Daily Sales</label>
                                    <div className="flex items-center justify-between mb-2">
                                        <input
                                            type="range" min="1000" max="50000" step="1000"
                                            value={dailyRevenue} onChange={(e) => setDailyRevenue(Number(e.target.value))}
                                            className="w-full mr-4 accent-emerald-600 cursor-pointer"
                                        />
                                        <span className="font-mono font-bold text-slate-700">{formatUSD(dailyRevenue)}</span>
                                    </div>
                                </div>

                                {/* Volatility */}
                                <div className="mb-5">
                                    <label className="text-xs font-bold text-slate-500 uppercase mb-1 block">
                                        Daily Volatility (Noise)
                                        <span className="ml-2 inline-block bg-slate-100 text-slate-500 rounded-full px-1.5 text-[10px] normal-case font-normal cursor-help" title="Standard Deviation / Mean. How much do sales swing day-to-day?">?</span>
                                    </label>
                                    <div className="flex items-center justify-between mb-2">
                                        <input
                                            type="range" min="0.05" max="0.30" step="0.01"
                                            value={volatility} onChange={(e) => setVolatility(Number(e.target.value))}
                                            className="w-full mr-4 accent-indigo-600 cursor-pointer"
                                        />
                                        <span className="font-mono font-bold text-indigo-600">{formatPct(volatility)}</span>
                                    </div>
                                </div>

                                {/* Expected Lift */}
                                <div className="mb-5">
                                    <label className="text-xs font-bold text-slate-500 uppercase mb-1 block">Expected Lift (Hypothesis)</label>
                                    <div className="flex items-center justify-between mb-2">
                                        <input
                                            type="range" min="0.01" max="0.15" step="0.005"
                                            value={expectedLift} onChange={(e) => setExpectedLift(Number(e.target.value))}
                                            className="w-full mr-4 accent-emerald-600 cursor-pointer"
                                        />
                                        <span className="font-mono font-bold text-emerald-600">+{formatPct(expectedLift)}</span>
                                    </div>
                                    <p className="text-xs text-slate-400">"We think ads will add this much."</p>
                                </div>

                                {/* Duration */}
                                <div className="mb-5 pt-4 border-t border-slate-100">
                                    <label className="text-xs font-bold text-slate-900 uppercase mb-1 block">Planned Duration</label>
                                    <div className="flex items-center justify-between mb-2">
                                        <input
                                            type="range" min="3" max="60" step="1"
                                            value={plannedDuration} onChange={(e) => setPlannedDuration(Number(e.target.value))}
                                            className="w-full mr-4 accent-slate-800 cursor-pointer"
                                        />
                                        <span className="font-mono font-bold text-slate-900">{plannedDuration} Days</span>
                                    </div>
                                    <p className="text-xs text-slate-400">Drag to see MDE change on the chart.</p>
                                </div>
                            </Card>

                            {/* RESULTS CARD */}
                            <div className={`p-6 rounded-xl shadow-lg transition-colors duration-300 ${
                                testStatus === 'underpowered' ? 'bg-rose-900 text-white' :
                                    testStatus === 'overpowered' ? 'bg-blue-900 text-white' :
                                        'bg-emerald-900 text-white'
                            }`}>
                                <h3 className="text-xs font-bold uppercase opacity-80 mb-2">Analysis Result</h3>

                                <div className="flex justify-between items-end mb-4">
                                    <div>
                                        <div className="text-3xl font-bold">{formatPct(currentMDE)}</div>
                                        <div className="text-sm opacity-80">Calculated MDE</div>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-xl font-bold opacity-60">{formatPct(expectedLift)}</div>
                                        <div className="text-sm opacity-60">Target Lift</div>
                                    </div>
                                </div>

                                <div className="pt-4 border-t border-white/20">
                                    {testStatus === 'underpowered' && (
                                        <div className="flex gap-3 items-start">
                                            <AlertTriangle className="text-rose-400 shrink-0" />
                                            <div className="text-sm">
                                                <strong>Design Failed: Underpowered.</strong><br/>
                                                Your MDE is higher than your Lift. You cannot reliably detect a {formatPct(expectedLift)} increase.
                                                <br/><u className="cursor-pointer mt-1 block">Fix: Increase duration or target bigger lift.</u>
                                            </div>
                                        </div>
                                    )}
                                    {testStatus === 'optimal' && (
                                        <div className="flex gap-3 items-start">
                                            <CheckCircle className="text-emerald-400 shrink-0" />
                                            <div className="text-sm">
                                                <strong>Design Optimal.</strong><br/>
                                                Your MDE is smaller than your Lift. You should be able to detect the effect if it exists.
                                            </div>
                                        </div>
                                    )}
                                    {testStatus === 'overpowered' && (
                                        <div className="flex gap-3 items-start">
                                            <Clock className="text-blue-400 shrink-0" />
                                            <div className="text-sm">
                                                <strong>Design Wasteful.</strong><br/>
                                                You are running too long. You can detect {formatPct(currentMDE)}, but you expect {formatPct(expectedLift)}. You could likely stop earlier.
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* CHART PANEL */}
                        <div className="lg:col-span-8">
                            <Card title="The Power Curve: Duration vs. Detectability" icon={TrendingUp} className="h-full flex flex-col">
                                <div className="flex-grow min-h-[400px]">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <LineChart data={powerCurveData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                                            <XAxis
                                                dataKey="days"
                                                label={{ value: 'Experiment Duration (Days)', position: 'bottom', offset: 0 }}
                                                padding={{ left: 20, right: 20 }}
                                            />
                                            <YAxis
                                                label={{ value: 'Minimum Detectable Effect (MDE %)', angle: -90, position: 'insideLeft' }}
                                                tickFormatter={(val) => `${(val*100).toFixed(0)}%`}
                                            />
                                            <Tooltip
                                                // @ts-ignore
                                                formatter={(val, name) => [name === 'mde' ? `${(val*100).toFixed(2)}%` : `${val}%`, name === 'mde' ? 'MDE' : 'Target Lift']}
                                                labelFormatter={(l) => `${l} Days`}
                                            />
                                            <Legend verticalAlign="top" height={36}/>

                                            {/* The MDE Curve */}
                                            <Line
                                                type="monotone"
                                                dataKey="mde"
                                                stroke="#6366f1"
                                                strokeWidth={3}
                                                dot={false}
                                                name="MDE (What you can see)"
                                            />

                                            {/* The Target Lift Line */}
                                            <ReferenceLine y={expectedLift} stroke="#10b981" strokeDasharray="5 5" label="Expected Lift (Goal)" />

                                            {/* Current Selection Marker */}
                                            <ReferenceLine x={plannedDuration} stroke="#334155" strokeDasharray="3 3">
                                            </ReferenceLine>

                                            {/* Intersection Dot */}
                                            <ReferenceLine
                                                y={currentMDE}
                                                x={plannedDuration}
                                                stroke="none"
                                                label={{ position: 'top', value: 'You Are Here', fill: '#334155', fontSize: 12, fontWeight: 'bold' }}
                                            />

                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>
                                <div className="mt-4 text-sm text-slate-500 bg-slate-50 p-4 rounded-lg border border-slate-100">
                                    <strong>How to read this chart:</strong> The Blue Line is your MDE. It drops as you add more days (Time = Clarity).
                                    The Green Dashed Line is your goal. You need the Blue Line to go <em>below</em> the Green Line to have a successful test.
                                </div>
                            </Card>
                        </div>

                    </div>
                )}

            </main>
        </div>
    );
};

export default IncrementalityGuide;