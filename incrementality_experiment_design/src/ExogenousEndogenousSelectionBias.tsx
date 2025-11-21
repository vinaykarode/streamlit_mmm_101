import { useState } from 'react';
import {
    CloudSun,
    TrendingUp,
    MousePointerClick,
    ArrowRight,
    AlertCircle,
    CheckCircle2,
    Wrench,
    BookOpen,
    Sigma,
    Filter
} from 'lucide-react';
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Legend
} from 'recharts';

// --- Components ---

// @ts-ignore
const ScenarioCard = ({ title, icon: Icon, isActive, onClick, description }) => (
    <button
        onClick={onClick}
        className={`flex flex-col items-start p-4 rounded-xl border-2 transition-all w-full text-left h-full ${
            isActive
                ? 'border-blue-600 bg-blue-50 shadow-md'
                : 'border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50'
        }`}
    >
        <div className={`p-2 rounded-lg mb-3 ${isActive ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600'}`}>
            <Icon size={24} />
        </div>
        <h3 className={`font-bold text-lg mb-1 ${isActive ? 'text-blue-900' : 'text-slate-800'}`}>
            {title}
        </h3>
        <p className={`text-sm leading-snug ${isActive ? 'text-blue-800' : 'text-slate-500'}`}>
            {description}
        </p>
    </button>
);

// @ts-ignore
const DeepDiveSectionMMM = ({ scenario }) => {
    const content = {
        exogenous: {
            concept: "Omitted Variable Bias (OVB)",
            fix: "Control Variables",
            explanation: (
                <div className="space-y-4 text-slate-700">
                    <p>
                        <strong>The MMM Fix:</strong> You must explicitly collect data for external factors (Weather, Competitor Price, Consumer Confidence) and add them as columns in your dataset.
                    </p>
                    <p>
                        By including <strong>Weather</strong> in the regression equation, the model mathematically "subtracts" the variance caused by heat.
                    </p>
                    <div className="bg-blue-50 p-4 rounded-lg border border-blue-100 font-mono text-sm">
                        <div className="text-xs text-slate-500 mb-1 uppercase">Bad Model:</div>
                        <div className="mb-3 text-red-800">Sales = β(AdSpend) + Error</div>
                        <div className="text-xs text-slate-500 mb-1 uppercase">Corrected Model:</div>
                        <div className="text-emerald-800">Sales = β₁(AdSpend) + <strong>β₂(Weather)</strong> + Error</div>
                    </div>
                </div>
            )
        },
        endogenous: {
            concept: "Reverse Causality",
            fix: "Bayesian Priors & Constraints",
            explanation: (
                <div className="space-y-4 text-slate-700">
                    <p>
                        <strong>The MMM Fix:</strong> When Spend is reactive (high correlation with Sales), standard regression (OLS) breaks. It will assign a huge coefficient to Ads.
                    </p>
                    <p>
                        To fix this without an experiment, we use <strong>Bayesian MMM</strong>. We tell the model:
                        <span className="italic"> "I know for a fact that Facebook ROAS is likely between 0.5 and 2.0. It is physically impossible for it to be 20.0."</span>
                    </p>
                    <p>
                        This "Prior Belief" constrains the model. Even though the data shows a perfect correlation, the model is forced to attribute the bulk of the sales to the Base (Seasonality) rather than the Ads.
                    </p>
                </div>
            )
        },
        bias: {
            concept: "Selection Bias",
            fix: "Funnel Control Variables",
            explanation: (
                <div className="space-y-4 text-slate-700">
                    <p>
                        <strong>The MMM Fix:</strong> Retargeting ads correlate with Sales because they correlate with <strong>User Intent</strong>.
                    </p>
                    <p>
                        To fix this, you must include a variable that represents that Intent, such as <strong>"Organic Website Sessions"</strong> or <strong>"Branded Search Volume"</strong>.
                    </p>
                    <div className="bg-purple-50 p-4 rounded-lg border border-purple-100">
                        <p className="text-sm text-purple-900">
                            When you add "Organic Traffic" to the model, it "soaks up" the credit for the base sales. The Retargeting variable is then forced to explain only the <strong>incremental lift</strong> on top of that organic traffic.
                        </p>
                    </div>
                </div>
            )
        }
    };
    // @ts-ignore
    const current = content[scenario];

    return (
        <div className="mt-8 bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="bg-slate-50 border-b border-slate-200 p-4 flex items-center gap-2">
                <BookOpen className="text-slate-500" size={20} />
                <h3 className="font-bold text-slate-800">Deep Dive: How to Fix it in MMM</h3>
            </div>

            <div className="p-6 grid md:grid-cols-3 gap-8">
                {/* Left: The Concept */}
                <div className="md:col-span-1 space-y-6">
                    <div>
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">The Problem</div>
                        <div className="text-xl font-bold text-slate-800">{current.concept}</div>
                    </div>

                    <div>
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">The MMM Solution</div>
                        <div className="bg-emerald-100 p-3 rounded-lg font-bold text-emerald-800 flex items-center gap-2">
                            <Wrench size={18} />
                            {current.fix}
                        </div>
                    </div>

                    <div className="p-4 bg-yellow-50 border border-yellow-100 rounded-lg text-sm text-yellow-800">
                        <strong>Note:</strong> These statistical fixes are powerful, but never perfect. They are "Best Guesses" based on math. Real experiments (Randomization) are still the only way to be 100% sure.
                    </div>
                </div>

                {/* Right: The Explanation */}
                <div className="md:col-span-2">
                    {current.explanation}
                </div>
            </div>
        </div>
    );
};
// @ts-ignore
const DeepDiveSection = ({ scenario }) => {
    const content = {
        exogenous: {
            concept: "Omitted Variable Bias (OVB)",
            math: "Y = β₁(AdSpend) + β₂(Weather) + ε",
            explanation: (
                <div className="space-y-4 text-slate-700">
                    <p>
                        In statistical modeling, if you leave out a significant variable (like <strong>Weather</strong>) that is correlated with your outcome (Sales), the model tries to "force" that variance onto the variables it <em>does</em> know about (like <strong>Ad Spend</strong>).
                    </p>
                    <p>
                        Because you often spend more during peak seasons (high correlation), the model mistakenly assigns the <span className="text-orange-600 font-bold">Weather's</span> credit to your <span className="text-emerald-600 font-bold">Ads</span>. This inflates your ROAS/ROI estimates, leading you to overspend.
                    </p>
                    <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                        <h4 className="font-bold text-blue-900 mb-2">Real World Examples:</h4>
                        <ul className="list-disc pl-5 space-y-1 text-sm">
                            <li><strong>Seasonality:</strong> Ice cream sales naturally spike in summer.</li>
                            <li><strong>Competitor Pricing:</strong> A competitor raises prices, causing your sales to spike.</li>
                            <li><strong>Macroeconomics:</strong> Stimulus checks hit bank accounts, increasing conversion rates across the board.</li>
                        </ul>
                    </div>
                </div>
            )
        },
        endogenous: {
            concept: "Reverse Causality (Simultaneity)",
            math: "Sales → Spend (Feedback Loop)",
            explanation: (
                <div className="space-y-4 text-slate-700">
                    <p>
                        Standard Regression (MMM) assumes <strong>X causes Y</strong>. However, in modern marketing, <strong>Y often causes X</strong>.
                    </p>
                    <p>
                        If you use an algorithm that says <em>"Spend more when conversion rates are good,"</em> or if a manager says <em>"We had a good month, let's reinvest,"</em> you have created a feedback loop.
                    </p>
                    <p>
                        The model sees a perfect correlation: <br/>
                        <span className="italic">"Every time Spend goes up, Sales go up!"</span> <br/>
                        It doesn't realize the Spend went up <em>because</em> the Sales were already rising. This leads to a massive overestimation of ad effectiveness.
                    </p>
                    <div className="bg-emerald-50 p-4 rounded-lg border border-emerald-100">
                        <h4 className="font-bold text-emerald-900 mb-2">Real World Examples:</h4>
                        <ul className="list-disc pl-5 space-y-1 text-sm">
                            <li><strong>Target CPA / ROAS Bidding:</strong> Ad platforms auto-spend more when users are converting well.</li>
                            <li><strong>Budget Fluidity:</strong> CFO approves extra budget in Q4 because Q3 revenue was high.</li>
                        </ul>
                    </div>
                </div>
            )
        },
        bias: {
            concept: "Selection Bias (Confounding)",
            math: "P(Buy | Ads) vs P(Buy | No Ads)",
            explanation: (
                <div className="space-y-4 text-slate-700">
                    <p>
                        This occurs when the group of people who see your ads is fundamentally different from the general population. Specifically, they already have a higher <strong>propensity to buy</strong> (User Intent).
                    </p>
                    <p>
                        Comparing "People who saw ads" vs "People who didn't" is unfair because the "Saw Ads" group includes all your loyal customers and site visitors. The ad didn't <em>create</em> the intent; it just <em>intercepted</em> it.
                    </p>
                    <div className="bg-purple-50 p-4 rounded-lg border border-purple-100">
                        <h4 className="font-bold text-purple-900 mb-2">Real World Examples:</h4>
                        <ul className="list-disc pl-5 space-y-1 text-sm">
                            <li><strong>Retargeting:</strong> Showing ads to people who added items to cart but didn't checkout.</li>
                            <li><strong>Branded Search:</strong> Bidding on your own brand name. Those users were searching for YOU specifically.</li>
                            <li><strong>Email Marketing:</strong> Sending coupons to your most active loyalists.</li>
                        </ul>
                    </div>
                </div>
            )
        }
    };
    // @ts-ignore
    const current = content[scenario];

    return (
        <div className="mt-8 bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="bg-slate-50 border-b border-slate-200 p-4 flex items-center gap-2">
                <BookOpen className="text-slate-500" size={20} />
                <h3 className="font-bold text-slate-800">Deep Dive Analysis</h3>
            </div>

            <div className="p-6 grid md:grid-cols-3 gap-8">
                {/* Left: The Concept */}
                <div className="md:col-span-1 space-y-6">
                    <div>
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Statistical Concept</div>
                        <div className="text-xl font-bold text-slate-800">{current.concept}</div>
                    </div>

                    <div>
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">The Math Problem</div>
                        <div className="bg-slate-100 p-3 rounded-lg font-mono text-sm text-slate-700 flex items-center gap-2">
                            <Sigma size={16} className="text-slate-400" />
                            {current.math}
                        </div>
                    </div>

                    <div className="p-4 bg-yellow-50 border border-yellow-100 rounded-lg text-sm text-yellow-800">
                        <strong>Why it matters:</strong> If you ignore this, your MMM model isn't just slightly off—it's fundamentally wrong. You will allocate budget to channels that aren't actually driving growth.
                    </div>
                </div>

                {/* Right: The Explanation */}
                <div className="md:col-span-2">
                    {current.explanation}
                </div>
            </div>
        </div>
    );
};
// @ts-ignore
const ExplanationBox = ({ type, isSolution }) => {
    const content = {
        exogenous: {
            problem: {
                title: "The Problem: Misattribution",
                subtitle: "Weather drives sales, but the model credits Ads.",
                color: "blue",
                points: [
                    "Sales (Blue) rise because of Heat (Orange).",
                    "If you don't tell the model about Heat, it assumes Ads caused the lift.",
                    "Result: Over-investing in high-season."
                ]
            },
            solution: {
                title: "The MMM Fix: Decomposition",
                subtitle: "Add 'Weather' as a Control Variable.",
                color: "emerald",
                points: [
                    "We add a 'Weather' column to the dataset.",
                    "The model now calculates: Sales = Weather + Ads.",
                    "The Chart shows 'Base Sales' (Grey) soaking up the heatwave, leaving the true (small) lift for Ads."
                ]
            }
        },
        endogenous: {
            problem: {
                title: "The Problem: Feedback Loop",
                subtitle: "Spend reacting to Sales breaks the math.",
                color: "emerald",
                points: [
                    "Manager spends more when Sales are high.",
                    "Correlation is 100%. The model thinks Ads caused the Sales.",
                    "Result: ROAS is massively overestimated."
                ]
            },
            solution: {
                title: "The MMM Fix: Bayesian Priors",
                subtitle: "Constrain the model with business logic.",
                color: "purple",
                points: [
                    "We use a 'Prior': We tell the math that ROAS cannot exceed 2.0x.",
                    "This forces the model to attribute the summer spike to Seasonality (Base), even though Spend was high.",
                    "The Spend line (Green) is still high, but the Attributed Sales (Blue) are corrected."
                ]
            }
        },
        bias: {
            problem: {
                title: "The Problem: Selection Bias",
                subtitle: "Taking credit for existing intent.",
                color: "purple",
                points: [
                    "Retargeting ads target people with High Intent.",
                    "These people were likely to buy anyway.",
                    "Result: Huge reported ROAS, zero actual lift."
                ]
            },
            solution: {
                title: "The MMM Fix: Funnel Controls",
                subtitle: "Add 'Organic Traffic' as a variable.",
                color: "blue",
                points: [
                    "We add 'Organic Sessions' (Grey) to the model.",
                    "This variable correlates with Intent and 'steals' the credit back from Retargeting.",
                    "The Retargeting variable is left explaining only the tiny incremental lift on top."
                ]
            }
        }
    };
    // @ts-ignore
    const data = isSolution ? content[type].solution : content[type].problem;

    return (
        <div className={`bg-${data.color}-50 border border-${data.color}-200 rounded-xl p-6 animate-in fade-in duration-500 h-full`}>
            <h3 className={`text-xl font-bold text-${data.color}-900 flex items-center gap-2 mb-1`}>
                {isSolution ? <Wrench size={20} /> : <AlertCircle size={20} />}
                {data.title}
            </h3>
            <p className={`text-${data.color}-700 font-medium mb-4`}>{data.subtitle}</p>
            <ul className="space-y-3">
                {/*// @ts-ignore*/}
                {data.points.map((point, i) => (
                    <li key={i} className={`flex items-start gap-3 text-${data.color}-800`}>
                        <CheckCircle2 size={18} className={`mt-0.5 shrink-0 opacity-60`} />
                        <span className="text-sm">{point}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
};

// --- Main Component ---

export default function MMMExplainer() {
    const [scenario, setScenario] = useState('exogenous');
    const [showSolution, setShowSolution] = useState(false);

    // --- Data Generation ---
    const generateData = () => {
        const data = [];

        for (let i = 1; i <= 12; i++) {
            // @ts-ignore
            const time = i;

            // Base curves
            const seasonalWave = Math.sin((i - 6) / 2) * 20 + 50; // Peak in middle (Summer)
            const randomNoise = Math.random() * 3;

            let item = { time: `Week ${i}` };

            // 1. EXOGENOUS
            if (scenario === 'exogenous') {
                if (showSolution) {
                    // Stacked view: Model correctly identifies Base vs Incremental
                    // @ts-ignore
                    item.baseSales = seasonalWave * 1.4; // Weather contribution
                    // @ts-ignore
                    item.incrementalSales = 15; // True ad contribution
                    // @ts-ignore
                    item.totalSales = item.baseSales + item.incrementalSales;
                } else {
                    // Problem view: We just see total sales
                    // @ts-ignore
                    item.external = seasonalWave;
                    // @ts-ignore
                    item.sales = seasonalWave * 1.5 + randomNoise;
                    // @ts-ignore
                    item.spend = 30;
                }
            }
            // 2. ENDOGENOUS
            else if (scenario === 'endogenous') {
                // In both cases, the SPEND is the same (Reactive).
                // The difference is how the MODEL interprets it.
                const reactiveSpend = (seasonalWave * 1.5) * 0.6; // Spend follows sales

                if (showSolution) {
                    // Bayesian Prior Solution:
                    // Even though spend is high, we force the model to attribute it to Base.
                    // @ts-ignore
                    item.spend = reactiveSpend;
                    // @ts-ignore
                    item.baseSales = seasonalWave * 1.4; // Model correctly assigns this to Seasonality
                    // @ts-ignore
                    item.incrementalSales = reactiveSpend * 0.1; // Model forced to assign low ROAS
                    // Note: Visual trick to make the chart look stacked correctly
                } else {
                    // Problem: Spend follows Sales
                    // @ts-ignore
                    item.sales = seasonalWave * 1.5 + randomNoise;
                    // @ts-ignore
                    item.spend = reactiveSpend;
                }
            }
            // 3. SELECTION BIAS
            else if (scenario === 'bias') {
                const userIntent = seasonalWave; // Intent is high in season

                if (showSolution) {
                    // Solution: Decomposition using "Organic Traffic"
                    // Organic traffic (Base) explains most of it.
                    // @ts-ignore
                    item.baseSales = userIntent * 1.0; // Organic Traffic contribution
                    // @ts-ignore
                    item.incrementalSales = userIntent * 0.2; // True Retargeting Lift
                } else {
                    // Problem view
                    // @ts-ignore
                    item.intent = userIntent;
                    // @ts-ignore
                    item.sales = userIntent * 1.2;
                    // @ts-ignore
                    item.spend = userIntent * 0.8;
                }
            }

            data.push(item);
        }
        return data;
    };

    const data = generateData();

    const renderChart = () => {
        return (
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                    <defs>
                        <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.1}/>
                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorSpend" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.1}/>
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorBase" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.2}/>
                            <stop offset="95%" stopColor="#94a3b8" stopOpacity={0.1}/>
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <Legend />

                    {/* --- PROBLEM STATE LAYERS --- */}
                    {!showSolution && (
                        <>
                            {/* Exogenous Context */}
                            {scenario === 'exogenous' && (
                                <Area type="monotone" dataKey="external" stroke="#fb923c" strokeWidth={2} strokeDasharray="5 5" fill="none" name="Temp (Exogenous)" />
                            )}
                            {/* Bias Context */}
                            {scenario === 'bias' && (
                                <Area type="monotone" dataKey="intent" stroke="#94a3b8" strokeWidth={2} strokeDasharray="5 5" fill="#f1f5f9" name="User Intent (Hidden)" />
                            )}

                            {/* Main Lines */}
                            <Area type="monotone" dataKey="sales" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorSales)" name="Total Sales" />
                            <Area type="monotone" dataKey="spend" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorSpend)" name="Ad Spend" />
                        </>
                    )}

                    {/* --- SOLUTION STATE LAYERS (DECOMPOSITION) --- */}
                    {showSolution && (
                        <>
                            <Area
                                type="monotone"
                                dataKey="baseSales"
                                stackId="1"
                                stroke="#94a3b8"
                                fill="url(#colorBase)"
                                name={
                                    scenario === 'exogenous' ? "Base Sales (Weather)" :
                                        scenario === 'endogenous' ? "Base Sales (Seasonal)" :
                                            "Base Sales (Organic Traffic)"
                                }
                            />
                            <Area
                                type="monotone"
                                dataKey="incrementalSales"
                                stackId="1"
                                stroke="#3b82f6"
                                fill="#3b82f6"
                                name="True Ad Lift"
                            />
                            {/* For Endogenous, we still show the High Spend line to prove it was reactive */}
                            {scenario === 'endogenous' && (
                                <Area
                                    type="monotone"
                                    dataKey="spend"
                                    stroke="#10b981"
                                    strokeWidth={2}
                                    strokeDasharray="5 5"
                                    fill="none"
                                    name="Ad Spend (Still High)"
                                />
                            )}
                        </>
                    )}

                </AreaChart>
            </ResponsiveContainer>
        );
    };

    return (
        <div className="min-h-screen bg-slate-50 p-6 font-sans text-slate-900">
            <div className="max-w-6xl mx-auto space-y-8">

                {/* Header */}
                <div className="text-center max-w-2xl mx-auto pb-4">
                    <h1 className="text-3xl font-bold text-slate-900 mb-3">Causality in Marketing</h1>
                    <p className="text-slate-500">
                        Visualizing the 3 Big Problems in MMM & Attribution.
                    </p>
                </div>

                {/* Navigation Grid */}
                <div className="grid md:grid-cols-3 gap-4">
                    <ScenarioCard
                        title="1. Exogenous Variables"
                        description="External factors (Weather) confusing the model."
                        icon={CloudSun}
                        isActive={scenario === 'exogenous'}
                        onClick={() => { setScenario('exogenous'); setShowSolution(false); }}
                    />
                    <ScenarioCard
                        title="2. Endogenous Variables"
                        description="Reactive spending creating false feedback loops."
                        icon={TrendingUp}
                        isActive={scenario === 'endogenous'}
                        onClick={() => { setScenario('endogenous'); setShowSolution(false); }}
                    />
                    <ScenarioCard
                        title="3. Selection Bias"
                        description="Taking credit for existing user intent."
                        icon={MousePointerClick}
                        isActive={scenario === 'bias'}
                        onClick={() => { setScenario('bias'); setShowSolution(false); }}
                    />
                </div>

                {/* Main Visualization Area */}
                <div className="grid lg:grid-cols-3 gap-8">

                    {/* Chart Section */}
                    <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-slate-200 h-[450px] flex flex-col">
                        <div className="flex justify-between items-center mb-6">
                            <h3 className="font-bold text-lg text-slate-700">
                                {showSolution ? "The MMM Solution View" : "The Problem View"}
                            </h3>

                            <button
                                onClick={() => setShowSolution(!showSolution)}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold transition-all ${
                                    showSolution
                                        ? 'bg-slate-800 text-white shadow-lg'
                                        : 'bg-white border-2 border-blue-600 text-blue-600 hover:bg-blue-50'
                                }`}
                            >
                                {showSolution ? <ArrowRight size={16} className="rotate-180"/> : <Filter size={16} />}
                                {showSolution ? "Back to Problem" : "Apply MMM Fix"}
                            </button>
                        </div>

                        <div className="flex-grow">
                            {renderChart()}
                        </div>
                    </div>

                    {/* Explanation Sidebar */}
                    <div className="lg:col-span-1 flex flex-col justify-center h-full">
                        <ExplanationBox type={scenario} isSolution={showSolution} />
                    </div>

                </div>

                {/* Deep Dive Section */}
                <DeepDiveSection scenario={scenario} />
                <DeepDiveSectionMMM scenario={scenario} />

            </div>
        </div>
    );
}