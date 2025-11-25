// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import React, { useState, useEffect } from 'react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ComposedChart, Bar, ReferenceLine
} from 'recharts';
import {
    TrendingUp, Filter, Target, Brain, Shield, Users, ShoppingCart, Eye, CloudRain, Tv, GitBranch, ArrowRight, CheckCircle, XCircle, Search, Mail, Map, Sliders, Sigma, Info, AlertTriangle, Scale
} from 'lucide-react';

// --- Components ---

const NavButton = ({ id, label, icon: Icon, activeTab, setActiveTab }) => (
    <button
        onClick={() => setActiveTab(id)}
        className={`tw:py-4 tw:px-6 tw:border-b-2 tw:font-medium tw:transition-all tw:flex tw:items-center tw:gap-2 tw:whitespace-nowrap ${
            activeTab === id
                ? 'tw:border-indigo-600 tw:text-indigo-700 tw:bg-indigo-50/50'
                : 'tw:border-transparent tw:text-slate-500 hover:tw:text-slate-700 hover:tw:bg-slate-50'
        }`}
    >
        <Icon size={18} />
        {label}
    </button>
);

const UserCard = ({ step, icon: Icon, title, desc, isRetargeting }) => (
    <div className={`tw:relative tw:p-4 tw:rounded-xl tw:border-2 tw:transition-all tw:duration-500 ${isRetargeting ? 'tw:border-indigo-500 tw:bg-indigo-50' : 'tw:border-slate-200 tw:bg-white'}`}>
        <div className="tw:flex tw:items-center tw:gap-3 tw:mb-2">
            <div className={`tw:p-2 tw:rounded-full ${isRetargeting ? 'tw:bg-indigo-200 tw:text-indigo-700' : 'tw:bg-slate-100 tw:text-slate-600'}`}>
                <Icon size={20} />
            </div>
            <p className="tw:font-bold tw:text-slate-800 tw:text-sm tw:uppercase tw:tracking-wide">{step}</p>
        </div>
        <p className="tw:font-bold tw:text-lg tw:mb-1">{title}</p>
        <p className="tw:text-sm tw:text-slate-600">{desc}</p>
        {isRetargeting && (
            <div className="tw:absolute tw:-top-3 tw:-right-3 tw:bg-indigo-600 tw:text-white tw:text-xs tw:font-bold tw:px-3 tw:py-1 tw:rounded-full tw:shadow-lg">
                Ad Shown!
            </div>
        )}
    </div>
);

const IvRequirement = ({ title, desc, icon: Icon, status }) => (
    <div className="tw:bg-white tw:p-3 tw:rounded-lg tw:border tw:border-slate-200 tw:flex tw:items-start tw:gap-3">
        <div className={`tw:p-2 tw:rounded-full tw:shrink-0 ${status === 'check' ? 'tw:bg-emerald-100 tw:text-emerald-600' : 'tw:bg-indigo-100 tw:text-indigo-600'}`}>
            <Icon size={16} />
        </div>
        <div>
            <p className="tw:font-bold tw:text-slate-800 tw:text-sm">{title}</p>
            <p className="tw:text-xs tw:text-slate-500 tw:mt-1">{desc}</p>
        </div>
    </div>
);

const SelectionBiasGuide = () => {
    const [activeTab, setActiveTab] = useState('story');

    // --- Simulator State ---
    const [showRetargeting, setShowRetargeting] = useState(false);
    const [chartData, setChartData] = useState([]);

    // --- IV Deep Dive State ---
    const [showIvDeepDive, setShowIvDeepDive] = useState(false);

    // Generate Chart Data
    useEffect(() => {
        const data = [];
        for (let i = 1; i <= 10; i++) {
            // Base organic sales fluctuate slightly
            const organicBase = 50 + Math.random() * 10;

            // When retargeting is ON, we spend money
            const retargetingSpend = showRetargeting ? 40 : 0;

            // The Illusion: Platform counts "View-Through" conversions
            // It claims credit for organic users who just saw the ad (60% of organic traffic)
            const platformAttributed = showRetargeting ? (organicBase * 0.6) : 0;

            // The Truth: Retargeting only adds a TINY incremental lift (maybe 10% of spend)
            const trueIncremental = showRetargeting ? (retargetingSpend * 0.1) : 0;

            data.push({
                day: `Day ${i}`,
                organic: organicBase,
                incremental: trueIncremental,
                platformClaim: platformAttributed,
                total: organicBase + trueIncremental
            });
        }
        setChartData(data);
    }, [showRetargeting]);

    return (
        <div className="tw:min-h-screen tw:bg-slate-50 tw:text-slate-800 tw:font-sans tw:pb-20">
            {/* POLYFILL: Fixes for prefixed responsive classes */}
            <style>{`
                @media (min-width: 768px) {
                    .md\\:tw\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
                    .md\\:tw\\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
                    .md\\:tw\\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
                }
                @media (min-width: 1024px) {
                    .lg\\:tw\\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
                    .lg\\:tw\\:col-span-2 { grid-column: span 2 / span 2; }
                }
            `}</style>

            {/* Header */}
            <header className="tw:bg-slate-900 tw:text-white tw:p-8 tw:shadow-xl">
                <div className="tw:max-w-6xl tw:mx-auto">
                    <div className="tw:flex tw:items-center tw:gap-3 tw:mb-4">
                        <Filter className="tw:w-10 tw:h-10 tw:text-rose-400" />
                        <p className="tw:text-4xl tw:font-bold">The Selection Bias Paradox</p>
                    </div>
                    <p className="tw:text-indigo-200 tw:text-lg tw:max-w-2xl tw:leading-relaxed">
                        Why algorithms (and managers) take credit for sales that would have happened anyway,
                        and how <span className="tw:font-bold">Instrumental Variables (IV)</span> help us find the truth.
                    </p>
                </div>
            </header>

            {/* Navigation */}
            <div className="tw:bg-white tw:border-b tw:sticky tw:top-0 tw:z-50 tw:shadow-sm">
                <div className="tw:max-w-6xl tw:mx-auto tw:flex tw:overflow-x-auto">
                    <NavButton id="story" label="1. The Real World Example" icon={Users} activeTab={activeTab} setActiveTab={setActiveTab} />
                    <NavButton id="math" label="2. The Mathematical Trap" icon={TrendingUp} activeTab={activeTab} setActiveTab={setActiveTab} />
                    <NavButton id="fix" label="3. The MMM Solution (IV)" icon={Brain} activeTab={activeTab} setActiveTab={setActiveTab} />
                </div>
            </div>

            <main className="tw:max-w-6xl tw:mx-auto tw:p-6 tw:mt-6">

                {/* === TAB 1: THE STORY === */}
                {activeTab === 'story' && (
                    <div className="tw:animate-in tw:fade-in tw:slide-in-from-bottom-4 tw:duration-500 tw:space-y-8">

                        {/* Narrative Section */}
                        <div className="tw:bg-white tw:p-8 tw:rounded-2xl tw:shadow-sm tw:border tw:border-slate-200">
                            <p className="tw:text-2xl tw:font-bold tw:text-slate-900 tw:mb-6">What is Selection Bias?</p>

                            {/* Diagram for the concept */}


                            <div className="tw:bg-indigo-50 tw:border-l-4 tw:border-indigo-500 tw:p-4 tw:mb-8 tw:text-indigo-900 tw:text-sm tw:leading-relaxed">
                                <span className="tw:font-bold">Definition:</span> Selection bias occurs when the treatment (who sees an ad) isn't random.
                                Instead, it targets people who possess characteristics (like "High Intent" or "Engaged") that <em>also</em> cause the outcome (Buying).
                            </div>

                            <div className="tw:grid md:tw:grid-cols-2 tw:gap-8 tw:mb-8">
                                <div className="tw:bg-white tw:p-4 tw:border tw:border-slate-200 tw:rounded-xl">
                                    <div className="tw:flex tw:items-center tw:gap-2 tw:font-bold tw:text-slate-700 tw:mb-2">
                                        <Target className="tw:text-rose-500"/> Example A: Retargeting
                                    </div>
                                    <p className="tw:text-sm tw:text-slate-600">
                                        You target users who <span className="tw:font-bold">Added to Cart</span>. They buy.
                                        <br/><br/>
                                        Did the ad cause the purchase? Or did the fact that they "Added to Cart" cause the purchase? You can't separate them.
                                    </p>
                                </div>
                                <div className="tw:bg-white tw:p-4 tw:border tw:border-slate-200 tw:rounded-xl">
                                    <div className="tw:flex tw:items-center tw:gap-2 tw:font-bold tw:text-slate-700 tw:mb-2">
                                        <Mail className="tw:text-emerald-500"/> Example B: Email Lists
                                    </div>
                                    <p className="tw:text-sm tw:text-slate-600">
                                        You email "Engaged Customers" (purchased in last 30d). They buy again.
                                        <br/><br/>
                                        The email looks like it has 20x ROAS. But "Engaged" people are <em>by definition</em> people who buy frequently.
                                    </p>
                                </div>
                            </div>

                            <p className="tw:font-bold tw:text-lg tw:mb-6 tw:pt-6 tw:border-t tw:border-slate-100">See it in action (The "SneakerHead" Simulator)</p>

                            <div className="tw:grid md:tw:grid-cols-4 tw:gap-4 tw:relative">
                                {/* Connector Line */}
                                <div className="tw:absolute tw:top-1/2 tw:left-0 tw:w-full tw:h-1 tw:bg-slate-100 tw:-translate-y-1/2 tw:z-0 tw:hidden md:tw:block"></div>

                                <UserCard
                                    step="Step 1"
                                    icon={Eye}
                                    title="High Intent"
                                    desc="Sarah visits directly. She adds shoes to cart."
                                />

                                <div className="tw:relative tw:z-10">
                                    {showRetargeting ? (
                                        <UserCard
                                            step="Step 2"
                                            icon={Target}
                                            title="The Interception"
                                            desc="You pay $2 to show her an Ad on Instagram."
                                            isRetargeting={true}
                                        />
                                    ) : (
                                        <div className="tw:h-full tw:border-2 tw:border-dashed tw:border-slate-300 tw:rounded-xl tw:flex tw:items-center tw:justify-center tw:bg-slate-50 tw:p-6 tw:text-center tw:text-slate-400">
                                            <p className="tw:text-sm tw:font-bold">No Ad Shown</p>
                                        </div>
                                    )}
                                </div>

                                <UserCard
                                    step="Step 3"
                                    icon={ShoppingCart}
                                    title="The Purchase"
                                    desc="Sarah checks out. $150 Revenue."
                                />

                                <div className="tw:bg-slate-900 tw:text-white tw:p-4 tw:rounded-xl tw:relative tw:z-10 tw:flex tw:flex-col tw:justify-center tw:shadow-lg">
                                    <p className="tw:text-xs tw:font-bold tw:text-slate-400 tw:uppercase">The Result</p>
                                    {showRetargeting ? (
                                        <div>
                                            <div className="tw:text-xl tw:font-bold tw:text-emerald-400 tw:mb-1">Ad Claims Credit!</div>
                                            <div className="tw:text-xs tw:text-slate-300">ROAS: 75x</div>
                                        </div>
                                    ) : (
                                        <div>
                                            <div className="tw:text-xl tw:font-bold tw:text-white tw:mb-1">Organic Sale</div>
                                            <div className="tw:text-xs tw:text-slate-300">Cost: $0</div>
                                        </div>
                                    )}
                                </div>
                            </div>

                            <div className="tw:mt-8 tw:flex tw:justify-center">
                                <button
                                    onClick={() => setShowRetargeting(!showRetargeting)}
                                    className="tw:bg-indigo-600 hover:tw:bg-indigo-700 tw:text-white tw:px-8 tw:py-3 tw:rounded-full tw:font-bold tw:shadow-lg tw:transition-transform active:tw:scale-95 tw:flex tw:items-center tw:gap-2"
                                >
                                    {showRetargeting ? "Turn Retargeting OFF" : "Turn Retargeting ON"}
                                </button>
                            </div>
                        </div>

                        {/* Simulator Chart */}
                        <div className="tw:grid lg:tw:grid-cols-3 tw:gap-8">
                            <div className="lg:tw:col-span-2 tw:bg-white tw:p-6 tw:rounded-2xl tw:shadow-sm tw:border tw:border-slate-200 tw:h-[450px] tw:flex tw:flex-col">
                                <div className="tw:flex tw:justify-between tw:items-center tw:mb-6">
                                    <p className="tw:font-bold tw:text-slate-700 tw:text-lg">Sales Volume Analysis</p>
                                    <div className="tw:flex tw:gap-4 tw:text-xs tw:font-medium">
                                        <div className="tw:flex tw:items-center tw:gap-1"><div className="tw:w-3 tw:h-3 tw:bg-slate-300 tw:rounded"></div> Organic Baseline</div>
                                        {showRetargeting && <div className="tw:flex tw:items-center tw:gap-1"><div className="tw:w-3 tw:h-3 tw:bg-indigo-500 tw:rounded"></div> True Ad Lift</div>}
                                        {showRetargeting && <div className="tw:flex tw:items-center tw:gap-1"><div className="tw:w-3 tw:h-3 tw:border-2 tw:border-dashed tw:border-rose-400 tw:bg-rose-50 tw:rounded"></div> Platform "Credit"</div>}
                                    </div>
                                </div>

                                <div className="tw:flex-grow">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <ComposedChart data={chartData} margin={{ top: 20, right: 20, bottom: 0, left: 0 }}>
                                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                                            <XAxis dataKey="day" tick={{fontSize: 12}} />
                                            <YAxis hide />
                                            <Tooltip />

                                            {/* Organic Base */}
                                            <Bar dataKey="organic" stackId="a" fill="#cbd5e1" />

                                            {/* True Lift */}
                                            <Bar dataKey="incremental" stackId="a" fill="#6366f1" />

                                            {/* The Illusion (Reference Line) */}
                                            {showRetargeting && (
                                                <Line
                                                    type="step"
                                                    dataKey="platformClaim"
                                                    stroke="#fb7185"
                                                    strokeWidth={3}
                                                    strokeDasharray="4 4"
                                                    dot={false}
                                                    name="Platform Claim"
                                                />
                                            )}
                                        </ComposedChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            <div className="tw:bg-indigo-50 tw:border tw:border-indigo-100 tw:p-6 tw:rounded-2xl tw:flex tw:flex-col tw:justify-center tw:space-y-6">
                                <div>
                                    <p className="tw:font-bold tw:text-indigo-900 tw:mb-2 tw:flex tw:items-center tw:gap-2">
                                        <Target size={20}/> The Bias Defined
                                    </p>
                                    <p className="tw:text-sm tw:text-indigo-800 tw:leading-relaxed">
                                        It is impossible to tell if the email/ad caused the purchase, or if you just selected people who were going to buy regardless.
                                    </p>
                                </div>
                                <div className="tw:bg-white tw:p-4 tw:rounded-xl tw:shadow-sm">
                                    <div className="tw:text-xs tw:font-bold tw:text-slate-400 tw:uppercase tw:tracking-wider tw:mb-1">True Incrementality</div>
                                    <div className={`tw:text-3xl tw:font-bold ${showRetargeting ? 'tw:text-rose-500' : 'tw:text-slate-300'}`}>
                                        {showRetargeting ? "5%" : "N/A"}
                                    </div>
                                    <div className="tw:text-xs tw:text-slate-500 tw:mt-1">Most sales were Organic.</div>
                                </div>
                                <div className="tw:bg-white tw:p-4 tw:rounded-xl tw:shadow-sm">
                                    <div className="tw:text-xs tw:font-bold tw:text-slate-400 tw:uppercase tw:tracking-wider tw:mb-1">Platform Reported</div>
                                    <div className={`tw:text-3xl tw:font-bold ${showRetargeting ? 'tw:text-indigo-600' : 'tw:text-slate-300'}`}>
                                        {showRetargeting ? "60%" : "N/A"}
                                    </div>
                                    <div className="tw:text-xs tw:text-slate-500 tw:mt-1">Includes "Hijacked" sales.</div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* === TAB 2: THE MATH TRAP (DAG) === */}
                {activeTab === 'math' && (
                    <div className="tw:animate-in tw:fade-in tw:slide-in-from-bottom-4 tw:duration-500 tw:max-w-4xl tw:mx-auto">
                        <div className="tw:bg-white tw:p-10 tw:rounded-2xl tw:shadow-sm tw:border tw:border-slate-200">
                            <p className="tw:text-2xl tw:font-bold tw:text-slate-900 tw:mb-6 tw:text-center">Why Regression Fails: The Confounder</p>

                            <div className="tw:relative tw:h-[300px] tw:bg-slate-50 tw:rounded-xl tw:border tw:border-slate-100 tw:mb-8 tw:overflow-hidden">

                                {/* Diagram for DAG concept */}


                                {/* THE CONFOUNDER (INTENT) */}
                                <div className="tw:absolute tw:top-10 tw:left-1/2 tw:-translate-x-1/2 tw:flex tw:flex-col tw:items-center tw:z-20">
                                    <div className="tw:bg-rose-100 tw:text-rose-800 tw:font-bold tw:px-6 tw:py-3 tw:rounded-full tw:shadow-sm tw:border tw:border-rose-200 tw:flex tw:items-center tw:gap-2">
                                        <Brain size={20} /> Customer Intent
                                    </div>
                                    <p className="tw:text-xs tw:text-rose-600 tw:mt-2 tw:font-medium">The Invisible Variable (Unobserved)</p>
                                </div>

                                {/* ARROWS */}
                                <div className="tw:absolute tw:top-24 tw:left-1/2 tw:-translate-x-1/2 tw:w-full tw:h-full">
                                    <svg width="100%" height="100%" viewBox="0 0 400 200" preserveAspectRatio="none">
                                        {/* Arrow Intent -> Spend */}
                                        <path d="M 180 20 L 100 100" fill="none" stroke="#fb7185" strokeWidth="2" markerEnd="url(#arrowhead-rose)" />
                                        {/* Arrow Intent -> Sales */}
                                        <path d="M 220 20 L 300 100" fill="none" stroke="#fb7185" strokeWidth="2" markerEnd="url(#arrowhead-rose)" />
                                        {/* Arrow Spend -> Sales (The False Link) */}
                                        <path d="M 140 120 L 260 120" fill="none" stroke="#94a3b8" strokeWidth="2" strokeDasharray="5 5" markerEnd="url(#arrowhead-gray)" />
                                    </svg>
                                    <defs>
                                        <marker id="arrowhead-rose" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                            <polygon points="0 0, 10 3.5, 0 7" fill="#fb7185" />
                                        </marker>
                                        <marker id="arrowhead-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                            <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
                                        </marker>
                                    </defs>
                                </div>

                                {/* SPEND */}
                                <div className="tw:absolute tw:bottom-10 tw:left-20 tw:z-20">
                                    <div className="tw:bg-white tw:border-2 tw:border-indigo-500 tw:text-slate-800 tw:font-bold tw:px-6 tw:py-4 tw:rounded-xl tw:shadow-lg tw:w-40 tw:text-center">
                                        Spend
                                    </div>
                                </div>

                                {/* SALES */}
                                <div className="tw:absolute tw:bottom-10 tw:right-20 tw:z-20">
                                    <div className="tw:bg-white tw:border-2 tw:border-emerald-500 tw:text-slate-800 tw:font-bold tw:px-6 tw:py-4 tw:rounded-xl tw:shadow-lg tw:w-40 tw:text-center">
                                        Sales
                                    </div>
                                </div>
                            </div>

                            <div className="tw:grid md:tw:grid-cols-2 tw:gap-8 tw:text-sm tw:leading-relaxed tw:text-slate-600">
                                <div className="tw:bg-rose-50 tw:p-6 tw:rounded-xl tw:border tw:border-rose-100">
                                    <p className="tw:font-bold tw:text-rose-800 tw:mb-2">The Trap</p>
                                    <p>
                                        A standard MMM sees that <span className="tw:font-bold">Spend</span> is high when <span className="tw:font-bold">Sales</span> is high. It calculates a high correlation.
                                        <br/><br/>
                                        It <em>doesn't see</em> <span className="tw:font-bold">Intent</span>. It doesn't know that Intent caused BOTH the high spend (via Retargeting algos) AND the high sales.
                                    </p>
                                </div>
                                <div className="tw:bg-indigo-50 tw:p-6 tw:rounded-xl tw:border tw:border-indigo-100">
                                    <p className="tw:font-bold tw:text-indigo-800 tw:mb-2">The Result</p>
                                    <p>
                                        The model attributes the sales to the Spend, overestimating ROAS by 10x or more. This is called <span className="tw:font-bold">Omitted Variable Bias</span> or Endogeneity.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* === TAB 3: THE SOLUTION === */}
                {activeTab === 'fix' && (
                    <div className="tw:animate-in tw:fade-in tw:slide-in-from-bottom-4 tw:duration-500 tw:max-w-5xl tw:mx-auto tw:space-y-8">
                        <div className="tw:bg-slate-900 tw:text-white tw:p-8 tw:rounded-2xl tw:shadow-lg">
                            <p className="tw:text-2xl tw:font-bold tw:mb-4 tw:flex tw:items-center tw:gap-3">
                                <Shield className="tw:text-emerald-400" />
                                The MMM Solution Suite
                            </p>
                            <p className="tw:text-slate-300 tw:text-lg">
                                To fix Selection Bias, we need to break the link between "Intent" and "Spend".
                            </p>
                        </div>

                        {/* --- HIGH LEVEL OVERVIEW --- */}
                        <div className="tw:grid md:tw:grid-cols-3 tw:gap-6">

                            {/* Strategy 1: Controls */}
                            <div className="tw:bg-white tw:p-6 tw:rounded-xl tw:border tw:border-slate-200 tw:shadow-sm hover:tw:shadow-md tw:transition-shadow">
                                <div className="tw:bg-indigo-100 tw:w-12 tw:h-12 tw:rounded-full tw:flex tw:items-center tw:justify-center tw:text-indigo-600 tw:mb-4">
                                    <Filter size={24}/>
                                </div>
                                <p className="tw:font-bold tw:text-lg tw:text-slate-900 tw:mb-2">1. Control Variables</p>
                                <p className="tw:text-sm tw:text-slate-600 tw:mb-4">
                                    Add proxies for "Intent" like <span className="tw:font-bold">Brand Search Volume</span>. The model attributes sales to Search first, Spend gets leftovers.
                                </p>
                            </div>

                            {/* Strategy 2: Priors */}
                            <div className="tw:bg-white tw:p-6 tw:rounded-xl tw:border tw:border-slate-200 tw:shadow-sm hover:tw:shadow-md tw:transition-shadow">
                                <div className="tw:bg-emerald-100 tw:w-12 tw:h-12 tw:rounded-full tw:flex tw:items-center tw:justify-center tw:text-emerald-600 tw:mb-4">
                                    <Brain size={24}/>
                                </div>
                                <p className="tw:font-bold tw:text-lg tw:text-slate-900 tw:mb-2">2. Bayesian Priors</p>
                                <p className="tw:text-sm tw:text-slate-600 tw:mb-4">
                                    Mathematically constrain the model. Force the retargeting coefficient to be low (e.g., max 0.5x ROAS).
                                </p>
                            </div>

                            {/* Strategy 3: IVs (Highlighted) */}
                            <div className="tw:bg-white tw:p-6 tw:rounded-xl tw:border-2 tw:border-indigo-500 tw:shadow-lg tw:scale-105 tw:flex tw:flex-col">
                                <div className="tw:absolute tw:top-0 tw:right-0 tw:bg-indigo-600 tw:text-white tw:text-[10px] tw:font-bold tw:px-2 tw:py-1 tw:rounded-bl-lg">GOLD STANDARD</div>
                                <div className="tw:bg-indigo-100 tw:w-12 tw:h-12 tw:rounded-full tw:flex tw:items-center tw:justify-center tw:text-indigo-600 tw:mb-4">
                                    <GitBranch size={24}/>
                                </div>
                                <p className="tw:font-bold tw:text-lg tw:text-slate-900 tw:mb-2">3. Instrumental Variables</p>
                                <p className="tw:text-sm tw:text-slate-600 tw:mb-4">
                                    Using a "Random Shock" (like Rain or Geo-Test) to isolate clean causal impact.
                                </p>
                            </div>
                        </div>

                        {/* --- IV DEEP DIVE --- */}
                        <div className="tw:animate-in tw:fade-in tw:slide-in-from-right tw:duration-500 tw:mt-10 tw:border-t tw:pt-10 tw:border-slate-200">
                            <div className="tw:bg-white tw:p-8 tw:rounded-2xl tw:shadow-sm tw:border tw:border-slate-200 tw:mb-8">
                                <p className="tw:text-2xl tw:font-bold tw:text-slate-900 tw:mb-8 tw:flex tw:items-center tw:gap-2">
                                    <GitBranch className="tw:text-indigo-600"/> How IV Solves the Trap
                                </p>

                                {/* Diagram for IV solution */}


                                {/* IV DAG DIAGRAM */}
                                <div className="tw:relative tw:h-[300px] tw:bg-slate-50 tw:rounded-xl tw:border tw:border-slate-100 tw:mb-8 tw:overflow-hidden">

                                    {/* INTENT (Ghost) */}
                                    <div className="tw:absolute tw:top-10 tw:left-1/2 tw:-translate-x-1/2 tw:flex tw:flex-col tw:items-center tw:opacity-40 tw:z-10">
                                        <div className="tw:bg-slate-200 tw:text-slate-500 tw:font-bold tw:px-6 tw:py-3 tw:rounded-full tw:border tw:border-slate-300 tw:flex tw:items-center tw:gap-2">
                                            <Brain size={20} /> Customer Intent
                                        </div>
                                        <p className="tw:text-xs tw:text-slate-400 tw:mt-2 tw:font-medium">Ignored / Blocked</p>
                                    </div>

                                    {/* INSTRUMENT (New Hero) */}
                                    <div className="tw:absolute tw:bottom-10 tw:left-10 tw:z-20">
                                        <div className="tw:bg-emerald-100 tw:text-emerald-800 tw:border-2 tw:border-emerald-500 tw:font-bold tw:px-6 tw:py-4 tw:rounded-xl tw:shadow-lg tw:w-40 tw:text-center tw:flex tw:flex-col tw:items-center">
                                            <CloudRain size={24} className="tw:mb-2"/>
                                            Instrument (Z)
                                        </div>
                                        <div className="tw:text-center tw:text-xs tw:text-emerald-600 tw:mt-2 tw:font-bold tw:bg-emerald-50 tw:rounded tw:px-2">"Random Shock"</div>
                                    </div>

                                    {/* ARROWS */}
                                    <div className="tw:absolute tw:top-0 tw:left-0 tw:w-full tw:h-full tw:z-0">
                                        <svg width="100%" height="100%" viewBox="0 0 600 300" preserveAspectRatio="none">
                                            {/* Z -> Spend (Clean Path) */}
                                            <path d="M 150 220 L 250 220" fill="none" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrowhead-emerald)" />

                                            {/* Spend -> Sales (Causal) */}
                                            <path d="M 350 220 L 450 220" fill="none" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrowhead-emerald)" />

                                            {/* Intent -> Sales (Still happens, but we ignore it) */}
                                            <path d="M 320 60 L 480 180" fill="none" stroke="#cbd5e1" strokeWidth="2" strokeDasharray="5 5" />

                                            {/* Intent -> Spend (We block this path mathmatically) */}
                                            <path d="M 280 60 L 120 180" fill="none" stroke="#cbd5e1" strokeWidth="2" strokeDasharray="5 5" />
                                        </svg>
                                        <defs>
                                            <marker id="arrowhead-emerald" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                                <polygon points="0 0, 10 3.5, 0 7" fill="#10b981" />
                                            </marker>
                                        </defs>
                                    </div>

                                    {/* SPEND */}
                                    <div className="tw:absolute tw:bottom-10 tw:left-1/2 tw:-translate-x-1/2 tw:z-20">
                                        <div className="tw:bg-white tw:border-2 tw:border-slate-300 tw:text-slate-800 tw:font-bold tw:px-6 tw:py-4 tw:rounded-xl tw:shadow-sm tw:w-32 tw:text-center">
                                            Spend (X)
                                        </div>
                                    </div>

                                    {/* SALES */}
                                    <div className="tw:absolute tw:bottom-10 tw:right-10 tw:z-20">
                                        <div className="tw:bg-white tw:border-2 tw:border-slate-300 tw:text-slate-800 tw:font-bold tw:px-6 tw:py-4 tw:rounded-xl tw:shadow-sm tw:w-32 tw:text-center">
                                            Sales (Y)
                                        </div>
                                    </div>
                                </div>

                                <div className="tw:grid md:tw:grid-cols-2 tw:gap-6">

                                    {/* Example 1: The Textbook Case (Rain) */}
                                    <div className="tw:bg-indigo-50 tw:border tw:border-indigo-100 tw:rounded-xl tw:p-6">
                                        <p className="tw:font-bold tw:text-indigo-900 tw:mb-4 tw:flex tw:items-center tw:gap-2">
                                            <Tv size={20}/> The Textbook Case: Rain
                                        </p>

                                        {/* Diagram for rain example */}


                                        <p className="tw:text-slate-600 tw:text-sm tw:mb-4">
                                            <span className="tw:font-bold">Problem:</span> Holiday demand causes both High Spend and High Sales (Bias).
                                            <br/>
                                            <span className="tw:font-bold">Solution:</span> Rain forces people inside to watch TV randomly.
                                        </p>
                                        <div className="tw:bg-white tw:p-4 tw:rounded tw:font-mono tw:text-xs tw:text-slate-500 tw:space-y-3 tw:shadow-inner">
                                            <div>
                                                <div className="tw:text-indigo-500 tw:font-bold tw:mb-1">// Stage 1: Predict Exposure from Rain</div>
                                                TV_Viewership = &alpha; + &gamma;(Rain) + &epsilon;
                                            </div>
                                            <div>
                                                <div className="tw:text-emerald-600 tw:font-bold tw:mb-1">// Stage 2: Measure Effect</div>
                                                Sales = &beta;(Predicted_Viewership) + Controls
                                            </div>
                                        </div>
                                    </div>

                                    {/* Example 2: The Real World (Geo-Test) */}
                                    <div className="tw:bg-emerald-50 tw:border tw:border-emerald-100 tw:rounded-xl tw:p-6">
                                        <p className="tw:font-bold tw:text-emerald-900 tw:mb-4 tw:flex tw:items-center tw:gap-2">
                                            <Target size={20}/> The Retargeting Fix: Geo-Test
                                        </p>
                                        <p className="tw:text-slate-600 tw:text-sm tw:mb-4">
                                            <span className="tw:font-bold">Problem:</span> User Intent causes both Ad View and Purchase (Bias).
                                            <br/>
                                            <span className="tw:font-bold">Solution:</span> Randomly force Spend to 0 in "Control Cities".
                                        </p>
                                        <div className="tw:bg-white tw:p-4 tw:rounded tw:font-mono tw:text-xs tw:text-slate-500 tw:space-y-3 tw:shadow-inner">
                                            <div>
                                                <div className="tw:text-indigo-500 tw:font-bold tw:mb-1">// Instrument: Geography</div>
                                                We can't rely on nature (Rain) for digital ads.
                                                We must <span className="tw:font-bold">manufacture</span> the random shock by turning ads OFF in Ohio.
                                            </div>
                                            <div className="tw:flex tw:gap-2 tw:mt-2">
                                                <span className="tw:bg-slate-100 tw:px-2 tw:py-1 tw:rounded">Z = Is_Test_City</span>
                                                <span className="tw:bg-slate-100 tw:px-2 tw:py-1 tw:rounded">X = Spend</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* How to Use Geo-Tests in MMM (Deep Dive) */}
                                <div className="tw:mt-8 tw:pt-8 tw:border-t tw:border-slate-200">
                                    <p className="tw:text-xl tw:font-bold tw:text-slate-900 tw:mb-4 tw:flex tw:items-center tw:gap-2">
                                        <Sliders size={20} className="tw:text-indigo-600"/> Connecting Geo-Tests to MMM
                                    </p>
                                    <div className="tw:bg-slate-50 tw:p-6 tw:rounded-xl tw:border tw:border-slate-200">
                                        <p className="tw:text-slate-700 tw:mb-6 tw:font-medium">
                                            You run a Geo-Test on Retargeting. It shows true lift is 5% (not the 50% the platform claims). How do you feed this into the model?
                                        </p>

                                        <div className="tw:grid md:tw:grid-cols-2 tw:gap-8 tw:mb-6">
                                            <div>
                                                <p className="tw:font-bold tw:text-slate-900 tw:mb-2 tw:flex tw:items-center tw:gap-2">
                                                    <CheckCircle size={16} className="tw:text-emerald-600"/> Method A: Calibration (Prior)
                                                </p>
                                                <p className="tw:text-sm tw:text-slate-600 tw:mb-3">
                                                    We tell the Bayesian model: <em>"I already know the answer is around 0.05."</em>
                                                </p>
                                                <div className="tw:bg-white tw:p-3 tw:rounded tw:font-mono tw:text-xs tw:text-slate-600 tw:border tw:border-slate-200">
                                                    <span className="tw:text-purple-600">Prior:</span> Beta_Retargeting ~ Normal(0.05, 0.01)
                                                </div>
                                                <div className="tw:mt-2 tw:text-xs tw:text-slate-500">
                                                    Most common approach. It constrains the model from chasing the biased correlation.
                                                </div>
                                            </div>

                                            <div>
                                                <p className="tw:font-bold tw:text-slate-900 tw:mb-2 tw:flex tw:items-center tw:gap-2">
                                                    <Sigma size={16} className="tw:text-indigo-600"/> Method B: Instrumentation (2SLS)
                                                </p>
                                                <p className="tw:text-sm tw:text-slate-600 tw:mb-3">
                                                    We use the <span className="tw:font-bold">Test Region Status</span> directly in the regression to predict spend.
                                                </p>
                                                <div className="tw:bg-white tw:p-3 tw:rounded tw:font-mono tw:text-xs tw:text-slate-600 tw:border tw:border-slate-200 tw:space-y-1">
                                                    <div>1. Predict_Spend = &alpha; + &gamma;(Is_Test_City)</div>
                                                    <div>2. Sales = &beta;(Predict_Spend) + Controls</div>
                                                </div>
                                                <div className="tw:mt-2 tw:text-xs tw:text-slate-500">
                                                    Forces model to use ONLY the variance caused by the experiment, ignoring user intent.
                                                </div>
                                            </div>
                                        </div>

                                        {/* NEW SECTION: When to use which? */}
                                        <div className="tw:bg-white tw:p-4 tw:rounded-lg tw:border tw:border-slate-200 tw:text-sm">
                                            <p className="tw:font-bold tw:text-slate-800 tw:mb-2 tw:flex tw:items-center tw:gap-2">
                                                <Info size={16} className="tw:text-indigo-500"/> When to use which?
                                            </p>
                                            <ul className="tw:space-y-2 tw:text-slate-600">
                                                <li className="tw:flex tw:gap-2">
                                                    <span className="tw:font-bold tw:text-emerald-700 tw:whitespace-nowrap">Method A (Priors):</span>
                                                    <span>Best for one-off tests or when you have limited data. It stabilizes the model by "anchoring" it to the test result.</span>
                                                </li>
                                                <li className="tw:flex tw:gap-2">
                                                    <span className="tw:font-bold tw:text-indigo-700 tw:whitespace-nowrap">Method B (2SLS):</span>
                                                    <span>Best for "Always-On" testing where you have continuous experimental variation. Requires more data but is statistically purer.</span>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>

                                {/* NEW SECTION: The Reality Check (Risks & Triangulation) */}
                                <div className="tw:mt-8 tw:bg-amber-50 tw:border tw:border-amber-200 tw:p-6 tw:rounded-xl">
                                    <p className="tw:text-lg tw:font-bold tw:text-amber-900 tw:mb-3 tw:flex tw:items-center tw:gap-2">
                                        <AlertTriangle size={20}/> The Reality Check: It's Not a Magic Bullet
                                    </p>
                                    <div className="tw:grid md:tw:grid-cols-2 tw:gap-6 tw:text-sm tw:text-amber-800">
                                        <div>
                                            <span className="tw:block tw:font-bold tw:mb-1">Challenge 1: Flawed Tests</span>
                                            <p>If your geo-test had a spillover or an external shock, you are now baking that error into every future estimate (especially with Priors).</p>
                                        </div>
                                        <div>
                                            <span className="tw:block tw:font-bold tw:mb-1">Challenge 2: Weak Instruments</span>
                                            <p>If your "Random Shock" (Instrument) is too weak (e.g., test budget was too small), IV can introduce <em>more</em> bias than a standard regression.</p>
                                        </div>
                                    </div>
                                    <div className="tw:mt-4 tw:pt-4 tw:border-t tw:border-amber-200 tw:flex tw:items-start tw:gap-3">
                                        <Scale className="tw:shrink-0 tw:mt-1 tw:text-amber-700" size={20}/>
                                        <p className="tw:text-sm tw:text-amber-900">
                                            <span className="tw:font-bold">Conclusion: Triangulation is Key.</span> No single method is perfect.
                                            Run periodic experiments to <em>bound</em> your MMM estimates, but don't let them blindly dictate the model. Stay humble with your data.
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

export default SelectionBiasGuide;