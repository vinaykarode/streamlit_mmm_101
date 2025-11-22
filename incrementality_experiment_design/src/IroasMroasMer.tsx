import { useState, useEffect } from 'react';
import {
    XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer, Area, ComposedChart, Legend
} from 'recharts';
import {
    Info, Calculator, TrendingUp, PieChart, Activity, Target, Layers
} from 'lucide-react';

// --- Components ---

// @ts-ignore
const MetricCard = ({ title, value, subtitle, color, icon: Icon, highlight = false }) => (
    <div className={`p-6 rounded-xl border transition-all duration-300 ${highlight ? `bg-${color}-50 border-${color}-500 shadow-md scale-105` : 'bg-white border-slate-200 shadow-sm'}`}>
        <div className="flex justify-between items-start mb-2">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">{title}</h3>
            {Icon && <Icon size={20} className={`text-${color}-500`} />}
        </div>
        <div className={`text-3xl font-bold text-${color}-700 mb-1`}>{value}</div>
        <p className="text-xs text-slate-500 leading-tight">{subtitle}</p>
    </div>
);

const RoasGuide = () => {
    const [activeTab, setActiveTab] = useState('concepts');

    // --- Simulator State ---
    const [organicRevenue, setOrganicRevenue] = useState(5000); // Base sales with $0 spend
    const [adSpend, setAdSpend] = useState(2000); // Current budget
    const [platformRoas, setPlatformRoas] = useState(4.0); // What FB/Google reports (often inflated)
    const [incrementality, setIncrementality] = useState(0.50); // True causality (50% of reported sales are incremental)

    // For Marginal Calculation (Simulating the curve)
    // @ts-ignore
    const [saturationPoint, setSaturationPoint] = useState(10000); // Spend level where returns flatten out

    // --- Computed Metrics ---
    const [metrics, setMetrics] = useState({
        revenue: 0,
        mer: 0,
        roas: 0,
        iroas: 0,
        mroas: 0
    });

    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        // 1. Define the Revenue Curve Function (Logarithmic Saturation)
        // Revenue = Organic + (MaxPotentialAdRevenue * (1 - e^(-Spend / DecayFactor)))
        // We tune this so it matches the user's "Platform ROAS" & "Incrementality" inputs at a specific calibration point to make the math line up intuitively.

        // Simplified Logic for Educational Simulator:
        // True Incremental Revenue at current spend = Spend * PlatformROAS * Incrementality
        const trueIncrementalNow = adSpend * platformRoas * incrementality;

        // Total Revenue
        const totalRevenue = organicRevenue + trueIncrementalNow;

        // 1. ROAS (Platform) - Directly from input
        const currentRoas = platformRoas;

        // 2. iROAS (Incremental) - True Ad Revenue / Spend
        const currentIroas = trueIncrementalNow / adSpend;

        // 3. MER (Marketing Efficiency Ratio) - Total Revenue / Total Spend
        const currentMer = totalRevenue / adSpend;

        // 4. Marginal ROAS (The slope at this point)
        // Let's simulate spending $100 more.
        // We model diminishing returns: As spend approaches SaturationPoint, efficiency drops.
        // Efficiency Multiplier = 1 - (Spend / (SaturationPoint * 1.5))^2
        const efficiency = Math.max(0.1, 1 - Math.pow(adSpend / (saturationPoint * 1.5), 2));
        // @ts-ignore
        const nextSpend = adSpend + 100;
        const nextIncremental = trueIncrementalNow + (100 * currentIroas * efficiency);
        const deltaRevenue = nextIncremental - trueIncrementalNow;
        const marginalRoas = deltaRevenue / 100;

        setMetrics({
            revenue: totalRevenue,
            mer: currentMer,
            roas: currentRoas,
            iroas: currentIroas,
            mroas: marginalRoas
        });

        // Generate Chart Data for the Curve
        const data = [];
        for(let s = 0; s <= saturationPoint; s+= 500) {
            // Re-calculate strictly for chart consistency
            // Assume linear-ish growth that tapers
            const factor = Math.max(0.1, 1 - Math.pow(s / (saturationPoint * 1.5), 2));
            // This is a simplified visual curve approx
            const chartIncRev = (s * currentIroas * factor);

            data.push({
                spend: s,
                organic: organicRevenue,
                incremental: chartIncRev,
                total: organicRevenue + chartIncRev,
                isCurrent: s === Math.round(adSpend/500)*500 // approximate marker
            });
        }
        // @ts-ignore
        setChartData(data);

    }, [organicRevenue, adSpend, platformRoas, incrementality, saturationPoint]);

    // @ts-ignore
    const formatUSD = (num) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(num);
    // @ts-ignore
    const formatFloat = (num) => num.toFixed(2) + 'x';

    return (
        <div className="min-h-screen bg-slate-50 text-slate-800 font-sans">

            {/* Header */}
            <header className="bg-indigo-900 text-white p-6 shadow-lg">
                <div className="max-w-6xl mx-auto">
                    <div className="flex items-center gap-3 mb-2">
                        <Target className="w-8 h-8 text-indigo-400" />
                        <h1 className="text-3xl font-bold">The ROAS Rosetta Stone</h1>
                    </div>
                    <p className="text-indigo-200 max-w-3xl leading-relaxed">
                        Platform ROAS is often a vanity metric. Learn to distinguish between <strong>Efficiency</strong> (MER), <strong>Causality</strong> (iROAS), and <strong>Scalability</strong> (Marginal ROAS).
                    </p>
                </div>
            </header>

            {/* Navigation */}
            <div className="bg-white border-b sticky top-0 z-10 shadow-sm">
                <div className="max-w-6xl mx-auto flex gap-8 px-6 overflow-x-auto">
                    {[
                        { id: 'concepts', label: '1. The Concepts', icon: <Layers size={18} /> },
                        { id: 'simulator', label: '2. Scaling Simulator', icon: <Calculator size={18} /> },
                    ].map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`py-4 px-2 border-b-2 font-medium transition-all flex items-center gap-2 whitespace-nowrap ${
                                activeTab === tab.id
                                    ? 'border-indigo-600 text-indigo-700 bg-indigo-50'
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

                {/* === TAB 1: CONCEPTS === */}
                {activeTab === 'concepts' && (
                    <div className="animate-in fade-in duration-500 space-y-8">

                        <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
                            <h2 className="text-2xl font-bold text-slate-900 mb-6">The Four Horsemen of Attribution</h2>
                            <div className="grid md:grid-cols-2 gap-8">

                                {/* ROAS */}
                                <div className="p-5 rounded-xl bg-slate-50 border border-slate-200">
                                    <h3 className="font-bold text-slate-800 flex items-center gap-2 text-lg mb-2">
                                        <Layers className="text-slate-500" /> 1. ROAS (Return on Ad Spend)
                                    </h3>
                                    <div className="text-3xl font-bold text-slate-800 mb-2">The "Blended" View</div>
                                    <p className="text-sm text-slate-600 mb-4 min-h-[40px]">
                                        What the ad platform (FB/Google) reports. It claims credit for every click/view, often ignoring organic behavior.
                                    </p>
                                    <div className="bg-white p-3 rounded border border-slate-200 text-xs font-mono text-slate-500">
                                        Formula: Attributed Revenue / Ad Spend
                                    </div>
                                </div>

                                {/* iROAS */}
                                <div className="p-5 rounded-xl bg-indigo-50 border border-indigo-200">
                                    <h3 className="font-bold text-indigo-900 flex items-center gap-2 text-lg mb-2">
                                        <Target className="text-indigo-600" /> 2. iROAS (Incremental ROAS)
                                    </h3>
                                    <div className="text-3xl font-bold text-indigo-700 mb-2">The "Causal" View</div>
                                    <p className="text-sm text-indigo-800 mb-4 min-h-[40px]">
                                        Revenue that <em>actually</em> wouldn't have happened without the ad. Removes "organic" sales that ads claimed credit for.
                                    </p>
                                    <div className="bg-white p-3 rounded border border-indigo-200 text-xs font-mono text-indigo-800">
                                        Formula: (Total Revenue - Counterfactual) / Ad Spend
                                    </div>
                                </div>

                                {/* Marginal ROAS */}
                                <div className="p-5 rounded-xl bg-emerald-50 border border-emerald-200">
                                    <h3 className="font-bold text-emerald-900 flex items-center gap-2 text-lg mb-2">
                                        <TrendingUp className="text-emerald-600" /> 3. Marginal ROAS
                                    </h3>
                                    <div className="text-3xl font-bold text-emerald-700 mb-2">The "Next Dollar" View</div>
                                    <p className="text-sm text-emerald-800 mb-4 min-h-[40px]">
                                        The return on the <em>last dollar</em> you spent. Critical for scaling. If this drops below break-even, stop spending!
                                    </p>
                                    <div className="bg-white p-3 rounded border border-emerald-200 text-xs font-mono text-emerald-800">
                                        Formula: Δ Revenue / Δ Spend (Slope of curve)
                                    </div>
                                </div>

                                {/* MER */}
                                <div className="p-5 rounded-xl bg-rose-50 border border-rose-200">
                                    <h3 className="font-bold text-rose-900 flex items-center gap-2 text-lg mb-2">
                                        <PieChart className="text-rose-600" /> 4. MER (Marketing Efficiency Ratio)
                                    </h3>
                                    <div className="text-3xl font-bold text-rose-700 mb-2">The "Holistic" View</div>
                                    <p className="text-sm text-rose-800 mb-4 min-h-[40px]">
                                        Total revenue divided by total ad spend. The ultimate "health check" for the business P&L.
                                    </p>
                                    <div className="bg-white p-3 rounded border border-rose-200 text-xs font-mono text-rose-800">
                                        Formula: Total Store Revenue / Total Ad Spend
                                    </div>
                                </div>

                            </div>
                        </div>

                        {/* Analogy Section */}
                        <div className="bg-indigo-900 text-white p-8 rounded-xl shadow-lg">
                            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                                <Info /> The Lemonade Stand Analogy
                            </h3>
                            <div className="space-y-4 text-indigo-100 leading-relaxed">
                                <p>
                                    Imagine you run a lemonade stand. You usually sell <strong>$100</strong> worth of lemonade purely by word-of-mouth (Organic).
                                </p>
                                <p>
                                    You pay a kid $50 to spin a sign (Ads). Sales jump to <strong>$200</strong> total.
                                </p>
                                <ul className="space-y-2 ml-4 list-disc">
                                    <li><strong>Platform ROAS:</strong> The kid claims he brought in all $200. ROAS = 200/50 = <span className="font-bold text-white">4.0x</span>. (Lie)</li>
                                    <li><strong>iROAS:</strong> He actually added $100 (Total 200 - Organic 100). iROAS = 100/50 = <span className="font-bold text-white">2.0x</span>. (Truth)</li>
                                    <li><strong>MER:</strong> Total Sales / Total Cost. MER = 200/50 = <span className="font-bold text-white">4.0x</span>. (Bank Account)</li>
                                </ul>
                                <p className="mt-4 pt-4 border-t border-indigo-700">
                                    Now you pay a <strong>second</strong> kid another $50. Sales go to $220.
                                    <br/>
                                    <strong>Marginal ROAS:</strong> You spent an extra $50 to get an extra $20. mROAS = 20/50 = <span className="font-bold text-white">0.4x</span>.
                                    <br/>
                                    <span className="text-rose-300 font-bold">You lost money on the second kid!</span> even though your total MER is still okay (220/100 = 2.2x).
                                </p>
                            </div>
                        </div>

                    </div>
                )}

                {/* === TAB 2: SIMULATOR === */}
                {activeTab === 'simulator' && (
                    <div className="animate-in slide-in-from-right duration-500 grid lg:grid-cols-12 gap-8">

                        {/* Left: Inputs */}
                        <div className="lg:col-span-4 space-y-6">
                            <div className="bg-white p-6 rounded-xl shadow-md border border-slate-200">
                                <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-slate-800">
                                    <Calculator size={20} /> Scenario Inputs
                                </h3>

                                <div className="space-y-6">
                                    {/* Organic Base */}
                                    <div>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="text-slate-500">Organic Baseline</span>
                                            <span className="font-bold text-slate-800">{formatUSD(organicRevenue)}</span>
                                        </div>
                                        <input
                                            type="range" min="0" max="20000" step="500"
                                            value={organicRevenue} onChange={(e) => setOrganicRevenue(Number(e.target.value))}
                                            className="w-full accent-slate-600"
                                        />
                                        <div className="text-xs text-slate-400 mt-1">Sales that happen with $0 ad spend.</div>
                                    </div>

                                    {/* Ad Spend */}
                                    <div>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="text-slate-500">Ad Spend</span>
                                            <span className="font-bold text-indigo-600">{formatUSD(adSpend)}</span>
                                        </div>
                                        <input
                                            type="range" min="500" max={saturationPoint} step="500"
                                            value={adSpend} onChange={(e) => setAdSpend(Number(e.target.value))}
                                            className="w-full accent-indigo-600"
                                        />
                                    </div>

                                    {/* Platform ROAS */}
                                    <div>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="text-slate-500">Platform Reported ROAS</span>
                                            <span className="font-bold text-indigo-600">{platformRoas}x</span>
                                        </div>
                                        <input
                                            type="range" min="1.0" max="10.0" step="0.1"
                                            value={platformRoas} onChange={(e) => setPlatformRoas(Number(e.target.value))}
                                            className="w-full accent-indigo-600"
                                        />
                                        <div className="text-xs text-slate-400 mt-1">What Facebook Ads Manager says.</div>
                                    </div>

                                    {/* Incrementality */}
                                    <div>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="text-slate-500">True Incrementality %</span>
                                            <span className="font-bold text-emerald-600">{(incrementality * 100).toFixed(0)}%</span>
                                        </div>
                                        <input
                                            type="range" min="0.1" max="1.0" step="0.05"
                                            value={incrementality} onChange={(e) => setIncrementality(Number(e.target.value))}
                                            className="w-full accent-emerald-600"
                                        />
                                        <div className="text-xs text-slate-400 mt-1">How much of reported rev is actually causal?</div>
                                    </div>
                                </div>
                            </div>

                            {/* Metric Definitions (Mini) */}
                            <div className="bg-slate-50 p-4 rounded-xl text-xs text-slate-500 space-y-2 border border-slate-200">
                                <p><strong>Adjust "Ad Spend"</strong> to see how Marginal ROAS (mROAS) drops faster than average ROAS.</p>
                                <p>When <strong>mROAS</strong> hits 1.0x, you are breaking even on your next dollar. Stop spending!</p>
                            </div>
                        </div>

                        {/* Right: Results & Chart */}
                        <div className="lg:col-span-8 space-y-6">

                            {/* Comparison Cards */}
                            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                                <MetricCard
                                    title="ROAS"
                                    value={formatFloat(metrics.roas)}
                                    subtitle="Platform Reported"
                                    color="slate"
                                    icon={Layers}
                                />
                                <MetricCard
                                    title="iROAS"
                                    value={formatFloat(metrics.iroas)}
                                    subtitle="True Value"
                                    color="indigo"
                                    icon={Target}
                                />
                                <MetricCard
                                    title="MER"
                                    value={formatFloat(metrics.mer)}
                                    subtitle="Total Efficiency"
                                    color="rose"
                                    icon={PieChart}
                                />
                                <MetricCard
                                    title="mROAS"
                                    value={formatFloat(metrics.mroas)}
                                    subtitle="Next Dollar Value"
                                    color="emerald"
                                    highlight={true}
                                    icon={TrendingUp}
                                />
                            </div>

                            {/* Visualization */}
                            <div className="bg-white p-6 rounded-xl shadow-md border border-slate-200 h-[400px] flex flex-col">
                                <h3 className="font-bold text-slate-700 mb-4 flex justify-between items-center">
                                    <span>Diminishing Returns Curve</span>
                                    <span className="text-sm font-normal text-slate-400">Total Revenue vs. Spend</span>
                                </h3>
                                <div className="flex-grow">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <ComposedChart data={chartData} margin={{ top: 10, right: 10, bottom: 0, left: 0 }}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                                            <XAxis
                                                dataKey="spend"
                                                tickFormatter={(val) => `$${val/1000}k`}
                                                label={{ value: 'Ad Spend', position: 'insideBottom', offset: -5 }}
                                            />
                                            <YAxis
                                                tickFormatter={(val) => `$${val/1000}k`}
                                            />
                                            <Tooltip
                                                formatter={(val) => formatUSD(val)}
                                                labelFormatter={(l) => `Spend: ${formatUSD(l)}`}
                                            />
                                            <Legend />

                                            <Area
                                                type="monotone"
                                                dataKey="organic"
                                                stackId="1"
                                                stroke="none"
                                                fill="#e2e8f0"
                                                name="Organic Base"
                                            />
                                            <Area
                                                type="monotone"
                                                dataKey="incremental"
                                                stackId="1"
                                                stroke="#4f46e5"
                                                fill="#818cf8"
                                                fillOpacity={0.6}
                                                name="Incremental Revenue"
                                            />

                                            {/* Current Spend Marker */}
                                            <ReferenceLine x={adSpend} stroke="#0f172a" strokeDasharray="3 3" />
                                            <ReferenceLine
                                                x={adSpend}
                                                y={metrics.revenue}
                                                stroke="none"
                                                label={{
                                                    value: 'You Are Here',
                                                    position: 'top',
                                                    fill: '#0f172a',
                                                    fontSize: 12,
                                                    fontWeight: 'bold'
                                                }}
                                            />
                                        </ComposedChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            {/* Insight Box */}
                            <div className="bg-emerald-50 border-l-4 border-emerald-500 p-4 rounded-r">
                                <div className="flex gap-3 items-start">
                                    <Activity className="text-emerald-600 shrink-0 mt-1" size={20} />
                                    <div>
                                        <h4 className="font-bold text-emerald-900">Strategic Insight</h4>
                                        <p className="text-emerald-800 text-sm mt-1">
                                            At your current spend of <strong>{formatUSD(adSpend)}</strong>, your mROAS is <strong>{formatFloat(metrics.mroas)}</strong>.
                                            {metrics.mroas < 1.0
                                                ? " 🛑 You are LOSING money on your next dollar of spend, even if your total ROAS looks good. Pull back!"
                                                : " ✅ You are still profitable on the next dollar. You can likely scale spend further."}
                                        </p>
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

export default RoasGuide;