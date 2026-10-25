ALIAS = "Project Meridian"  # public alias for the system that is running a live forward test


def bud(believed, broke, changed):
    return (f"<dl><dt>Believed</dt><dd>{believed}</dd><dt>What broke it</dt><dd class=\"broke\">{broke}</dd>"
            f"<dt>Changed</dt><dd>{changed}</dd></dl>")


# kind: lesson (something that failed), built (something I built), live (running now)
ROADMAP = [
    ("Forex at university", "Trading by hand, with nothing to measure it against.", "lesson",
     bud("Trading by hand would work if I tried hard enough.", "I had no way to tell skill from luck.", "I wanted to automate it, so a rule could be tested.")),
    ("A bought EA", "Paid for a robot. Lost the money.", "lesson",
     bud("Someone sells an automated system that works.", "I paid for one in my first job and lost the money. I could not check any claim it made.", "I started building my own, so I could inspect every step.")),
    ("An indicator-stack EA", "More indicators, a better backtest, a worse result.", "lesson",
     bud("RSI, stochastic, EMA and MACD together, tuned long enough, make a system.", "The backtest looked better than expected. Live, it did not. That is when I learned the word overfitting.", "I began testing one hypothesis at a time.")),
    ("Other people's strategies", "Converted public strategies to MQL5. Found nothing.", "lesson",
     bud("A strategy someone published probably has an edge.", "Converted and tested, none of them held up.", "I turned to machine learning.")),
    ("A first machine-learning system", "A spectacular backtest. A flat live result.", "lesson",
     bud("A CNN-LSTM with an XGBoost meta-model and Kelly sizing, built over several versions, would find the edge.", "The backtest was spectacular. Live, it was not. Tracing why taught me look-ahead bias.", "Results that look too good now start an investigation. Every feature has to be available at the moment of the decision, and I count every trial.")),
    ("Language models, then a harness", "Stopped asking for code. Started working inside rules.", "built",
     bud("Language models could speed up the coding.", "Early on they were weak at MQL5 and I stopped using them. They improved.", "I started working inside a harness: pre-registered hypotheses, tests, leakage checks, trial counts, real costs before anyone looks at a result.")),
    ("A pre-registered research framework", "Every idea written down before it is tested. None has survived.", "built",
     "<p>A register of hypotheses with rules, costs and decision gates committed first, and a runner that counts every trial. By its last entry 69 variants had been counted and none passed every gate. The plot above comes from it.</p>"),
    ("A data and cost audit", "Is the data what I think it is?", "built",
     "<p>A read-only audit of the broker clock, DST eras, spread regimes and sessions, re-derived by an independent second implementation. It found the server clock was not the fixed offset I had assumed, which had quietly shifted winter sessions by an hour.</p><p><a href=\"#repos\">See the repository</a></p>"),
    ("An ML filter under strict validation", "Does machine learning add anything once validation is honest?", "built",
     "<p>Triple-barrier labels, purged splits, CPCV and a shuffled-label leakage check. A gain on three markets disappeared when the basket widened to six, and the project was rejected on its own written gate.</p><p><a href=\"#repos\">See the repository</a></p>"),
    ("A discretionary method made testable", "A causal state machine that fails if it looks ahead.", "built",
     "<p>Sweeps, structure breaks and fair value gaps as a deterministic state machine with tests that try to leak the future. No published results yet.</p>"),
    ("The same discipline at home", "A pipeline for the Thai index futures market.", "built",
     "<p>Explicit contract rolls, point-in-time joins, cost-aware labels and walk-forward training with purging and an embargo. No results yet, and the broker adapter is a stub.</p>"),
    ("Language models behind a hard limit", "Agents can propose and veto. They cannot change a rule.", "built",
     "<p>An ML signal reviewed by agents, a plain-code risk gate that fails closed, and an executor with no model calls. No live results yet.</p><p><a href=\"#repos\">See the repository</a></p>"),
    (ALIAS, "Running now, as a live forward test.", "live", """
<p><strong>Status.</strong> A gold (XAUUSD) system on MetaTrader 5: rule-based entry engines propose trades, machine-learning layers decide which to take and how large, and a portfolio guard caps what everything can lose together. It is in a live forward test. There are no live results to report yet, so every number below is a backtest and I treat it as a hypothesis.</p>
<table class="mini"><caption>Backtest results, from my own tester runs and replay</caption>
<thead><tr><th scope="col">Run</th><th scope="col">Result</th></tr></thead><tbody>
<tr><td>Four core engines, raw rules vs with ML. Train 2018 to 2024, test 2025 to Oct 2026 (1,973 candidate trades)</td><td>Profit factor <span class="num">1.39</span> to <span class="num">1.97</span>. Net <span class="num">+213 R</span> to <span class="num">+242 R</span>. Max drawdown <span class="num">8.6%</span> to <span class="num">5.1%</span></td></tr>
<tr><td>Six engines, same split</td><td>Profit factor <span class="num">1.37</span> to <span class="num">1.80</span>. Net <span class="num">+269 R</span> to <span class="num">+308 R</span></td></tr>
<tr><td>Tester run, compounding, Jan 2025 to Oct 2026, $10,000 start</td><td><span class="num">+531.58%</span>, profit factor <span class="num">1.72</span>, Sharpe <span class="num">3.74</span>, win/loss ratio <span class="num">2.08</span>, max equity drawdown <span class="num">7.82%</span></td></tr>
<tr><td>Portfolio guard on vs off, small account, Jan to Jul 2026</td><td>Max drawdown <span class="num">23.7%</span> to <span class="num">14.5%</span>, profit about the same</td></tr>
</tbody></table>
<h4>How much to trust them</h4>
<ul>
<li>The test window is no longer clean. Several design changes were made while looking at 2025 and 2026: one version exists to fix a drawdown in summer 2025, and engine families were dropped or added by their results in that window. I call it a development period, not out of sample.</li>
<li>The five engines in the guard test were picked from about 25 tried on the same seven months. Treat that run as an upper bound.</li>
<li>The +531% figure is compounding. Per-trade statistics say more.</li>
<li>An independent test disagrees. Inside my research framework, under gates written first, the earlier five-rule set was rejected on FTMO-feed ticks (about 929 days, <span class="num">&minus;154 R</span>, profit factor <span class="num">0.92</span>) and on an earlier IUX-feed period (<span class="num">&minus;51 R</span>, profit factor <span class="num">0.97</span>), and an ML layer tested over those streams did not pass. I have not reconciled this with the numbers above. Feed, cost model and the ML implementation are candidate explanations, not established ones.</li>
</ul>
<h4>Data engineering</h4>
<p>Training data comes from tester trade reports and causal bar history with a long warm-up, split by date and never at random. I built a bar-level replay of the EA and checked it against MT5: it reproduced 231 of 233 entry bars and about 97% of win/loss outcomes, while its net profit ran about 1.6 times too high, so it ranks changes and does not forecast. Replaying against MT5 exposed three bugs that were costing money: an indicator updated on only a subset of bars, entries acting on the previous bar's signal, and a Friday close that never fired.</p>
<h4>Portfolio optimization</h4>
<p>Engines are pruned by individual expectancy, and a mean-reversion family that fought the trend was dropped. A guard above every engine applies a daily loss cap, a drawdown throttle, a drawdown halt and a cap on the total risk of open stops. A trade whose minimum size would break the per-trade risk limit is refused. On one seven-month path, a smaller drawdown with unchanged profit is partly luck. The structural part is the cap on oversized small-account trades.</p>
<h4>Machine learning</h4>
<p>Three small layers. A soft market-regime model replaced hard cutoffs, which had skipped 109 profitable trades at the boundary. Each engine has two heads: one estimates expected R from a regularized prior, and one estimates the chance of hitting the stop, using monotonic gradient-boosted trees so it cannot learn a relationship that points the wrong way. Microstructure inputs were added to the stop-risk model.</p>
<h4>What did not work</h4>
<p>A linear stop-risk filter that left stop-out cascades in place. Hard regime cutoffs. Two engine families and a mean-reversion family with negative expectancy. Grid and averaging-down systems in older projects. Trusting the replay's profit figure.</p>
<p><strong>Next.</strong> The forward test is the first evidence not shaped by my own decisions. I will publish its results, good or bad, next to everything else.</p>"""),
]
