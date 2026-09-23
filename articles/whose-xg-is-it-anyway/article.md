# Whose xG Is It Anyway?

*What football recruitment can teach us about building AI agents that know what their data actually means.*

![Whose xG Is It Anyway? — editorial cover](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/01-hero.svg)

## 10:06 on Monday morning

At 10:06, the club's new AI recruitment assistant finds its next number nine.

The brief is simple:

> Find under-23 forwards in Europe with at least 900 league minutes and more than 0.55 non-penalty expected goals per 90. Exclude players who would obviously be outside our budget.

Thirty seconds later, Roberto McBaggio appears.

Twenty-one years old. Central Europe. Eighteen months left on his contract. He presses, runs the channels, and the assistant has even found six clips of him arriving between the centre-back and full-back.

And then there is the number: **0.64 xG per 90.**

For approximately nine glorious minutes, recruitment has been solved.

Then Mark, one of the analysts, asks two irritatingly short questions.

> “Whose xG?”

Nobody answers.

> “And did it remove the penalties?”

It did not.

In our fictional dataset, McBaggio's 0.64 came from 7.27 xG over 1,020 minutes. Three penalties contributed 2.37. Remove them and the calculation becomes `(7.27 - 2.37) / 1,020 × 90 = 0.43` non-penalty xG per 90.

He no longer meets the brief.

There is another problem. The shortlist mixes xG from two providers. Both columns are called `xG`; the values came from different models with different assumptions.

So we have two failures. **The penalties make McBaggio a false positive. The provider mismatch means parts of the shortlist should never have been ranked together at all.**

Every row is real. The arithmetic is correct. Every tool returned green.

The shortlist is wrong.

That is the interesting failure mode. The model did not hallucinate a striker. It composed individually plausible facts into an invalid decision.

An LLM can reason over information. A reliable agent also needs to know **what that information means**.

---

## The model knows football. It does not know *our* football.

Two weeks earlier, the assistant had a safer job: explain why a side can produce more xG from fewer shots, summarise an opponent's build-up patterns, translate “rest defence” for the board.

It was excellent. That is close to the environment in which large language models are most comfortable: take language and context, reason over them, produce more language.

The important word is **produce**. A chatbot can be wrong and produce a bad paragraph. An agent can be wrong and **change something**.

That gap matters as systems move from short exchanges towards delegated work. OpenAI's June 2026 analysis describes agents working for minutes or hours, orchestrating tools and iterating towards outcomes rather than simply returning one answer. [OpenAI, *How agents are transforming work*, June 2026](https://openai.com/index/how-agents-are-transforming-work/).

So first, give the model the club handbook.

- `RECRUITMENT_POLICY.md`
- `APPROVED_DATA_SOURCES.md`
- `METRIC_DEFINITIONS.md`
- `WHEN_TO_ASK_MARK.md`

For many tasks, that may be enough. Markdown is cheap, versionable and human-readable. Retrieval can bring the right passage into context at the right moment.

But retrieval solves an **availability problem**, not automatically a **meaning problem**. The assistant can retrieve the correct definition and still apply it to the wrong dataset; retrieve both providers' methodology notes and still treat their outputs as interchangeable; retrieve yesterday's contract perfectly when today's record supersedes it.

**Getting the right document into the room does not make everything in the room compatible.**

And before anybody commissions a twelve-month “Football Knowledge Fabric” programme and orders the branded quarter-zips, there is a very useful middle.

Typed player IDs. A metric registry. Provider and model-version fields. Data contracts. Foreign keys. Pydantic models. Validation that refuses incompatible comparisons.

That is good architecture. The aim is not to graduate towards a graph because graphs look impressive in PowerPoint. The aim is to make **meaning harder to lose at system boundaries**.

---

## Five green ticks. Wrong striker.

![Five green ticks can still produce the wrong striker](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/02-five-green-ticks.svg)

Now give the assistant tools: player search, match events, contracts, video, a calculator, perhaps write access to the recruitment system.

The player lookup succeeds.

The appearances query succeeds.

The event query succeeds.

The arithmetic succeeds.

The shortlist write succeeds.

Five green ticks.

Wrong striker.

This is more useful than simply saying “the LLM hallucinated”. The failure can be in the **composition**.

Pick the wrong competition and every later calculation can be flawless. Merge two similar player identities and the radar chart can look magnificent for a footballer who exists only in SQL. Treat two providers' xG as interchangeable and the system can rank incomparable measurements to three decimal places.

It is the football-data equivalent of putting the wrong stadium into the sat-nav. Every turn can be correct. You are still missing kick-off.

Anthropic's January 2026 work distinguishes the model from the wider **agent harness** — tools, state, instructions and the environment through which the agent affects the world — and argues that the resulting state matters, not merely whether the transcript looked sensible. [Anthropic, *Demystifying evals for AI agents*, January 2026](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

Its April 2026 managed-agent architecture makes a related distinction between the **brain**, **hands** and **session** so reasoning, execution and state can be controlled independently. [Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*, April 2026](https://www.anthropic.com/engineering/managed-agents).

For our club, the lesson is simpler: the part deciding what to do does not have to be the part trusted to decide what is true.

---

## xG is not a fact found growing on the pitch

This is why xG is such a good semantic trap.

Expected goals is not like date of birth. It is a **model output**.

A July 2026 paper in *Intelligent Sports and Health* describes xG as a probabilistic estimate built from features such as shot location, angle, body part and match context, and warns against treating it as a deterministic account of what “should” have happened. Model design and context affect interpretation. [Lago-Peñas et al., *A probabilistic and dynamic reformulation of expected goals (xG): Methodological advances and modelling perspectives*, July 2026](https://doi.org/10.1016/j.ish.2026.05.001).

A cell containing `0.64` is therefore not enough. To use it safely, the system may need to know the metric definition, provider, model version, competition scope, time period, penalty treatment, minutes definition and aggregation rule.

The database contains a number. **The semantic layer tells us what kind of number it is.**

That tidy column heading is doing a lot of hiding.

Football analysts know this instinctively. Much of it is documented.

An uncomfortable amount lives in Mark.

---

## Mark is the club's latent ontology

Mark knows that these two Roberto McBaggio records refer to different people. That “league appearances” means this set of competitions. That Provider A and Provider B are not comparable for this screen. That this contract record supersedes the other one. That when *that* number looks suspicious, you check *this* feed.

Mark is, in effect, an undocumented API with an annual-leave allowance.

More importantly, he contains part of the club's **latent ontology**.

Before the club formalises an ontology, one already exists. It lives in people, SQL, spreadsheets, code, documentation, Slack threads and, occasionally, the sentence:

> “Oh yeah. Don't use that column.”

Organisations do not usually lack meaning. They lack **explicit, shared, machine-checkable meaning**.

The agent is now crossing joins Mark used to cross in his head: which player, competition, shots, provider, model version, minutes and current contract; what happens when two authoritative sources disagree; which relationships are valid *now*.

At some point, repeatedly consequential ambiguity deserves structure.

---

## This is where the ontology earns its entrance

An ontology matters here not because every AI system needs one, but because the same concepts must now survive across datasets, services, teams and agents without being quietly reinterpreted.

Three things are worth separating.

The **ontology** defines agreed concepts and relationships. The **semantic layer** maps and exposes those meanings consistently across systems. A **knowledge graph** is one useful way to store and traverse actual relationships when the domain needs it.

None of that replaces ordinary engineering. An ontology does not deduplicate a player or remove a penalty from a calculation. Identifiers, data-quality rules, deterministic services and validation code do the mechanical work.

**Ontology supplies the semantic contract. Software enforces it.**

For McBaggio, the evidence path can become explicit:

> player → qualifying appearances → shots → penalty status → xG provider/model → aggregate → minutes → threshold decision

Now rerun the search.

![Forensic repair of the McBaggio xG calculation](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/03-mcbaggio-repair.svg)

“Non-penalty xG” resolves to an approved definition. The calculation service removes penalties. Provider and model-version compatibility is checked before ranking. “League” resolves to the competitions the club actually means.

McBaggio's 0.64 becomes **0.43 non-penalty xG/90**. He drops below the 0.55 threshold.

The provider problem is handled separately. If only some candidates lack comparable evidence, withhold those candidates and rank the valid remainder. If the comparability problem undermines the cohort, refuse the ranking and explain what is missing.

What the system must never do is silently mix incompatible evidence and call the result comparable.

Another player rises to the top of the valid shortlist. That player may not be the objectively “best footballer”; no ontology can settle that. The system has simply become better at answering **the question the club actually asked**.

The ontology has not made the model smarter.

It has removed a red herring.

---

## Ontology is not a truth machine

There is an important limit here.

A beautifully modelled ontology can still encode something wrong.

A knowledge graph is a map, and maps can be beautifully drawn while still sending the team bus towards a bridge that closed last week.

McBaggio may have changed clubs yesterday. A provider may have changed its xG model halfway through the dataset. Somebody may have linked the wrong Roberto McBaggio.

The relationships therefore need the boring things architecture diagrams put in tiny boxes near the bottom: **sources, ownership, effective dates, confidence, approval and conflict resolution**.

Recent work on dynamically generated ontologies needs the same caution. An August 2026 preprint, **OaK**, explores task-oriented ontologies and knowledge graphs for LLM agents and reports improved grounding across several benchmarks. [Zhang et al., *Toward Effective and Reliable LLM Agents via Dynamic Ontology*, August 2026](https://arxiv.org/abs/2608.22974).

Useful? Potentially. The same thing as institutional truth? No.

An agent can propose structure. It should not be able to redefine an approved metric, legal relationship or risk rule because the new definition makes its task easier.

And some rules should not be semantic debates at all.

If the brief requires non-penalty xG from one approved model, deterministic code should enforce it. If the data cannot satisfy the rule, fail closed.

Do not ask a probabilistic component to enforce a deterministic invariant when ordinary software can do it instead.

---

## Every agent has an ambiguity budget — and an authority gradient

There is still plenty we do **not** want to formalise away.

Whether McBaggio will adapt to another league is judgement. Whether his movement against a low block compensates for weaker numbers is judgement. A scout is supposed to form hypotheses.

The club can tolerate uncertainty about whether he will improve next season. It should not tolerate uncertainty about whether a metric labelled “non-penalty” still contains three penalties.

That is the **ambiguity budget**: how much unresolved interpretation a workflow can tolerate before it needs more evidence, a human or a stop.

Now add authority:

**Explain** — What does xG mean?  
**Recommend** — Which strikers should we watch?  
**Decide** — Build the final shortlist.  
**Act** — Contact the agents.  
**Commit** — Submit a £25 million offer.

The model may be identical. The blast radius is not.

![The ambiguity budget and authority gradient](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/04-authority-ambiguity.svg)

Anthropic's May 2026 work on agent containment makes the security version of the same point: greater capability and access increase potential blast radius, so environmental and permission boundaries matter alongside probabilistic safeguards. [Anthropic, *How we contain Claude across products*, May 2026](https://www.anthropic.com/engineering/how-we-contain-claude).

My rule of thumb is simple:

**The more authority an agent has, the smaller its ambiguity budget should become.**

That is when semantics stops being documentation and becomes part of the control system.

---

## 14:17. Same architecture, different consequences.

At 14:17, the architecture gets another job.

An asset-management agent is asked whether two issuers belong to the same corporate group before a trade is approved.

It finds the entities, an ownership record and the trading mandate. The relationship check returns green. The limit calculation returns green. The proposed trade is inside the numerical threshold.

Five green ticks.

There is one problem: the ownership relationship came from yesterday's source. A newer filing says the intermediate holding company changed this morning.

The names are real. The entities are real. The calculation is correct.

The relationship is stale.

We have met Roberto McBaggio again. Only the nouns have changed.

Financial services is full of terms that look simple until software has to act on them: issuer, obligor, guarantor, beneficial owner, counterparty, portfolio, exposure, mandate, instrument, legal entity. Each sits inside relationships, roles, time and jurisdiction.

The [Financial Industry Business Ontology, FIBO](https://edmcouncil.org/financial-industry-business-ontology/) exists to define financial concepts and relationships in machine-readable form. In August 2026, the EDM Association ran [*Why Your AI Needs an Ontology: Getting Started with FIBO*](https://edmconnect.edmcouncil.org/events/event-description?CalendarEventKey=4ed40715-05bb-441d-b6d0-01a001f902d3&Home=%2Fevents%2Fcalendar). The point is not to import FIBO wholesale. It is that **shared consequential concepts need shared meaning**.

The semantics also sit inside a wider control architecture. In its July 2026 Financial Stability Report, the Bank of England discusses more autonomous AI systems in finance and **Project Logos**, which aims to let central banks observe LLM-based agents acting as portfolio managers in a simulated market. [Bank of England, *Financial Stability Report*, July 2026](https://www.bankofengland.co.uk/financial-stability-report/2026/july-2026).

Minutes of the Bank and FCA AI Consortium's **3 June 2026 meeting, published on 5 August**, get closer to the engineering detail: members discussed **model harnesses** and **execution boundaries** separating probabilistic LLM reasoning from deterministic system actions. [Bank of England, *Artificial Intelligence Consortium minutes – June 2026*, published August 2026](https://www.bankofengland.co.uk/minutes/2026/june/ai-consortium-minutes-3-june-2026).

The football example adds the missing semantic layer. An execution boundary can stop an agent exceeding a trading limit; it cannot rescue a limit calculation built on the wrong issuer relationship. A deterministic validator can enforce an approved rule, but it still needs stable definitions for the concepts inside that rule.

**Semantics and controls belong together.**

---

## Do not start by building the ontology

If the first outcome of this article is a twelve-month enterprise-ontology programme, I have explained it badly.

Start with one narrow workflow. Good instructions. Retrieval. Typed schemas and data contracts. The minimum useful tools. Deterministic checks around rules that must always hold.

Then watch where the experts keep correcting it.

Collect the awkward cases: duplicate entities, incompatible metrics, superseded policies, temporal relationships, conflicting sources and all the things “everybody knows” that have never actually been written down.

Formalise only the concepts and relationships that repeatedly cause consequential mistakes.

Use an ontology where shared meaning matters. Use a graph where relationship traversal matters. Use schemas where structure is enough. Use code where the rule is deterministic. Use retrieval where the problem is access to context. Use people where judgement is the actual job.

That is not a maturity model.

It is a toolbox.

---

## Back to Monday morning

The recruitment assistant runs the query again.

McBaggio is no longer first.

“Non-penalty xG” has an explicit definition and code enforces it. Incompatible provider data is rejected. “League” means the competitions the club actually intends. The evidence path can be reconstructed.

Another player rises above him.

That player was always in the data. The first system simply could not see past the red herring it had created for itself.

Nothing about the LLM became more intelligent. We made the meaning around it more explicit.

Truth can live in databases. Meaning can live in an ontology. Relationships can live in a graph. Structure can live in schemas. Calculations can live in code. Permissions can live outside the model entirely.

The agent's job is to navigate those things intelligently without quietly changing what they mean.

And one of its most valuable answers will occasionally be:

> I can't establish that from comparable evidence yet.

Mark looks at the revised shortlist.

McBaggio is no longer first.

He puts him back on the scouting list anyway because he likes his movement against a low block.

And that is fine.

Human judgement was never the bug.

The bug was allowing a machine to present incompatible meanings as one comparable fact.

Football just made it easier to see.

And Mark can finally go on holiday without taking the club's ontology with him.
