# Whose xG Is It Anyway?

*An AI finds the perfect striker. The data is real, the maths is right, and the answer is still wrong.*

![Whose xG Is It Anyway? — editorial cover](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/01-hero.svg)

## 10:06 on Monday morning

At 10:06 on a Monday morning, the club's new recruitment agent finds its striker.

The brief isn't especially exotic:

> Use the full 2025/26 domestic league season. Find under-23 centre-forwards in Europe with at least 2,000 league minutes and more than 0.55 non-penalty expected goals per 90. Exclude players who are obviously outside our budget.

About thirty seconds later, Roberto McBaggio appears.

Twenty-one. Central Europe. Eighteen months left on his contract. He presses. He runs the channels. There are clips for every goal, every shot and every high turnover from the season.

And the numbers look excellent.

- **34 league appearances, 30 starts, 2,684 minutes**
- **17 goals, 5 assists**
- **19.08 xG — 0.64 xG/90**
- **5.84 xA — 0.20 xA/90**
- **92 shots — 3.08/90**
- **39 shots on target — 42.4%**
- **178 touches in the opposition box — 5.97/90**
- **31 key passes — 1.04/90**
- **73 progressive carries — 2.45/90**
- **486 pressures — 16.30/90**
- **172 final-third pressures — 5.77/90**
- **94 recoveries — 3.15/90**
- **38 of 91 aerial duels won — 41.8%**
- **49 of 96 take-ons completed — 51.0%**

It's the sort of dataset you can stare at for far too long. There's enough there for a radar chart, a role profile, a shot map, half a dozen peer comparisons and, inevitably, a PowerPoint with a very serious title.

The headline number is the one that matters for the screen: **0.64 xG per 90**.

For about nine minutes, recruitment appears to have been solved.

Then Mark, one of the analysts, asks:

> “Whose xG?”

Nobody says anything.

Then:

> “Did it remove the penalties?”

No.

There are four penalties in the season total. At 0.79 xG each, they account for 3.16 of McBaggio's 19.08 xG.

Nothing is wrong with the source data. That's worth being clear about. Provider A's `xG` field means total expected goals, and total expected goals includes penalties. The field is doing exactly what it says it does.

The problem is that the question asked for non-penalty xG.

Remove the penalties and the calculation is:

> `(19.08 - 3.16) / 2,684 × 90 = 0.53`

McBaggio doesn't pass the 0.55 screen.

What I like about the example is that it can't be waved away as a small-sample issue. We've got a whole league season here: 2,684 minutes, 92 shots, plenty of event data, plenty of evidence.

The system isn't short of data.

It has misunderstood what one bit of that data means.

There is a second problem too. The shortlist contains xG from two providers. Both fields are called `xG`, which looks reassuringly tidy, but the underlying models are different.

So the agent has managed to make two perfectly respectable mistakes. It has used total xG when the question asked for non-penalty xG, and it has compared measurements that aren't necessarily comparable.

The rows are real. The arithmetic is fine. The tool calls worked.

The shortlist is still wrong.

That, to me, is a more interesting class of failure than a hallucination. Nothing has been invented. The system has simply put legitimate things together in a way that changes their meaning.

---

## The model knows football. It doesn't know our football.

A couple of weeks earlier, the same assistant had a much safer job.

Explain why a side can generate more xG from fewer shots. Summarise an opponent's build-up. Translate “rest defence” into something a board member can repeat without causing concern.

It was good at that.

That's roughly the territory large language models are happiest in: read some material, reason over it, produce more language. If the answer is a bit off, you get a bad paragraph.

Once the system starts doing things, the stakes change. OpenAI's June 2026 analysis describes agents working for minutes or hours, using tools and iterating towards an outcome rather than simply answering a prompt. [OpenAI, *How agents are transforming work*, June 2026](https://openai.com/index/how-agents-are-transforming-work/).

So the obvious first step is to teach it the club's rules.

A few Markdown files will get you surprisingly far:

- `RECRUITMENT_POLICY.md`
- `APPROVED_DATA_SOURCES.md`
- `METRIC_DEFINITIONS.md`
- `WHEN_TO_ASK_MARK.md`

I'm quite fond of this stage because it is cheap and slightly unfashionable. The files are easy to read, easy to change and easy to version. Retrieval can pull in the right definition when the agent needs it.

Sometimes that's enough.

Sometimes it isn't.

The awkward bit is that retrieval can fetch the right definition and the agent can still apply it to the wrong field. It can retrieve Provider A's methodology and Provider B's methodology and still flatten both into a column called `xG`. It can retrieve an old contract perfectly even though a newer one superseded it.

The document is available. The meaning can still drift.

Before jumping to graphs and ontologies, there is a lot of ordinary engineering that should happen first: typed player IDs, sensible schemas, provider and model-version fields, data contracts, foreign keys, validation.

Honestly, a decent Pydantic model and a few unpleasantly strict checks can save you from an impressive number of “AI” problems.

You don't get extra points for using a graph database.

---

## Five green ticks

![Five green ticks can still produce the wrong striker](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/02-five-green-ticks.svg)

Now give the agent some proper tools.

Player search. Event data. Contracts. Video. A calculator. Maybe permission to write a shortlist back into the recruitment system.

Everything works.

Player lookup: green.

Appearances: green.

Events: green.

Calculation: green.

Write to shortlist: green.

Five green ticks, and McBaggio is still the wrong striker for this particular screen.

This is where “the model hallucinated” becomes a bit too convenient as an explanation. It didn't. The failure is in how the pieces were composed.

Choose the wrong competition and everything after that can be mathematically perfect. Join two similar player identities and you can produce a beautiful radar chart for a footballer who exists only in SQL. Mix two xG models and you can rank incomparable numbers to three decimal places.

It reminds me of putting the wrong stadium into the sat-nav. The route can be flawless. You're still going to miss kick-off.

Anthropic's January 2026 work on agent evaluations makes a similar point from a different direction: the model sits inside a wider harness of tools, state, instructions and environment, and you have to look at what actually happened in the environment rather than whether the transcript sounded convincing. [Anthropic, *Demystifying evals for AI agents*, January 2026](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

Its April 2026 managed-agent architecture separates the “brain”, the “hands” and the “session” for much the same reason. [Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*, April 2026](https://www.anthropic.com/engineering/managed-agents).

In football terms: the bit choosing what to do doesn't also have to be the bit that decides what counts as true.

---

## xG is a particularly good trap

Expected goals sounds like a fact because it arrives as a number.

It isn't.

It's a model output.

A July 2026 paper in *Intelligent Sports and Health* describes xG as a probability estimate based on things such as shot location, angle, body part and match context. Different model choices change the result and therefore the interpretation. [Lago-Peñas et al., *A probabilistic and dynamic reformulation of expected goals (xG): Methodological advances and modelling perspectives*, July 2026](https://doi.org/10.1016/j.ish.2026.05.001).

That's why a line saying “19.08 xG” isn't quite enough.

Which provider?

Which model version?

Which competitions?

What date range?

Are penalties in or out?

What counts as minutes?

How has the number been aggregated?

Football analysts ask these questions almost without thinking. They know that a neat column heading can hide a lot of decisions.

Some of those decisions are documented.

A surprising number are stored in Mark.

---

## Mark knows what everybody else means

Mark knows that two records with the same name are different players.

He knows which competitions count as “league” for this screen.

He knows that Provider A and Provider B shouldn't be mixed here.

He knows which contract record is current, which field includes penalties, and which feed to check when a number looks odd.

In other words, Mark isn't just familiar with the data. He's carrying around a chunk of the club's operating model in his head.

He is also, rather inconveniently, allowed to go on holiday.

This is the bit that gets missed when people talk about “adding context” to agents. Most organisations already have plenty of context. It sits in code, SQL, spreadsheets, documents, Slack threads and people who know that “you never use that column for this”.

The problem isn't that meaning doesn't exist.

The problem is that it often isn't explicit enough for software to share reliably.

Once the agent starts crossing the same joins Mark crosses mentally — player, competition, shots, provider, model version, minutes, contract, effective date — there comes a point where another page of prompt instructions starts to feel like the wrong fix.

That's where formal semantics becomes useful.

Not before.

---

## Where an ontology is actually useful

The word “ontology” can make a straightforward idea sound needlessly grand.

For this problem, I mean something fairly practical: an agreed description of the important concepts in the domain and how they relate to one another.

A player makes appearances. Appearances happen in matches. Matches belong to competitions. Shots belong to appearances. An xG observation came from a particular provider and model version. A contract applies to a player for a defined period.

That's the ontology.

A semantic layer makes those meanings available consistently to systems. A knowledge graph is one way of storing and traversing the actual relationships, if a graph is useful for the problem.

It doesn't replace the database, and it certainly doesn't replace code.

The ontology won't remove penalties from McBaggio's xG. It tells us what a penalty is, what xG is, what “non-penalty xG” means and which relationships matter. Ordinary software can then enforce the rule.

For the recruitment screen, the evidence path might look like this:

> player → qualifying appearances → shots → penalty status → xG provider/model → aggregate → minutes → threshold decision

That path is much easier to inspect than “the agent worked it out”.

Now rerun the search.

![Forensic repair of the McBaggio xG calculation](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/03-mcbaggio-repair.svg)

McBaggio's 19.08 total xG becomes 15.92 non-penalty xG. Over 2,684 minutes, 0.64 xG/90 becomes **0.53 NPxG/90**.

He drops below the threshold.

The provider issue needs its own rule. If a few players can't be compared on the approved basis, leave them out and say why. If the whole cohort is contaminated by incompatible data, don't rank it.

That sounds obvious written down.

Systems do non-obvious things all the time when the only instruction is buried in prose.

The useful change here isn't that the LLM has become cleverer. It hasn't.

We've made it harder for the surrounding system to quietly change the question.

---

## An ontology can be wrong too

None of this creates a truth machine.

A beautifully designed ontology can encode rubbish just as neatly as a spreadsheet can.

McBaggio might have changed clubs yesterday. A provider might have changed its model midway through the season. Somebody might simply have linked the wrong player record.

So the relationships need provenance, ownership, effective dates and some idea of what happens when sources disagree. Those are the boring controls that tend to end up in twelve-point text at the bottom of architecture diagrams, but they're doing most of the useful work.

There is interesting research on creating ontologies dynamically. An August 2026 preprint, OaK, explores task-oriented ontologies and knowledge graphs for LLM agents and reports better grounding across several benchmarks. [Zhang et al., *Toward Effective and Reliable LLM Agents via Dynamic Ontology*, August 2026](https://arxiv.org/abs/2608.22974).

I'd still be careful about the distinction.

An agent can suggest that two concepts appear related. That doesn't mean it should be allowed to redefine an approved metric or legal relationship because the new interpretation makes its task easier.

And some things shouldn't be left to semantics at all.

If the rule says “non-penalty xG from one approved model”, code can enforce that. It should.

There's no virtue in asking a probabilistic model to remember a deterministic rule every single time.

---

## How much uncertainty are we actually prepared to tolerate?

There are parts of recruitment where ambiguity is the point.

Will McBaggio adapt to another league?

Does his movement against a low block make up for weaker numbers elsewhere?

Will he improve?

You want scouts to argue about those things. That's judgement.

Whether “non-penalty xG” contains four penalties is not judgement. It's just wrong.

I've started thinking about that difference as an ambiguity budget: how much interpretation can this particular task tolerate before the system needs more evidence, a person, or a hard stop?

Then there is authority.

**Explain** — What does xG mean?  
**Recommend** — Which strikers should we watch?  
**Decide** — Build the final shortlist.  
**Act** — Contact the agents.  
**Commit** — Submit a £25 million offer.

Same model, potentially.

Very different consequences.

![The ambiguity budget and authority gradient](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/04-authority-ambiguity.svg)

Anthropic's May 2026 work on agent containment makes the security version of this argument: more capability and more access mean a larger potential blast radius, so hard permission and environmental boundaries matter alongside probabilistic safeguards. [Anthropic, *How we contain Claude across products*, May 2026](https://www.anthropic.com/engineering/how-we-contain-claude).

I wouldn't turn “ambiguity budget” into a new enterprise framework with a logo.

But as a design question, it's useful: if the agent is allowed to do more, what assumptions are we still comfortable leaving fuzzy?

Usually, fewer than before.

---

## At 14:17 the football disappears

Later that afternoon, give the same architecture a different job.

An asset-management agent needs to decide whether two issuers belong to the same corporate group before a trade is approved.

It finds the entities. It finds an ownership relationship. It finds the mandate. The relationship check passes. The limit calculation passes. The trade is inside the numerical threshold.

All green.

Except the ownership relationship came from yesterday's source, and a newer filing says the intermediate holding company changed this morning.

The names are right.

The entities are right.

The maths is right.

The relationship is stale.

It's McBaggio again, just with less entertaining nouns.

Finance is full of apparently simple terms that become awkward once software has to act on them: issuer, obligor, guarantor, beneficial owner, counterparty, portfolio, exposure, mandate, instrument, legal entity. Most of them only make sense in relation to other things, at a particular time, often under a particular jurisdiction.

The [Financial Industry Business Ontology, FIBO](https://edmcouncil.org/financial-industry-business-ontology/) exists to define financial concepts and relationships in machine-readable form. In August 2026, the EDM Association ran [*Why Your AI Needs an Ontology: Getting Started with FIBO*](https://edmconnect.edmcouncil.org/events/event-description?CalendarEventKey=4ed40715-05bb-441d-b6d0-01a001f902d3&Home=%2Fevents%2Fcalendar).

I wouldn't take that as an instruction to import FIBO wholesale. The useful point is simpler: if several systems and agents are making decisions about the same concepts, it helps if they mean the same thing by them.

The control side is moving in the same direction. The Bank of England's July 2026 Financial Stability Report discusses more autonomous AI in finance and Project Logos, a simulated environment for observing LLM-based agents acting as portfolio managers. [Bank of England, *Financial Stability Report*, July 2026](https://www.bankofengland.co.uk/financial-stability-report/2026/july-2026).

Minutes from the Bank and FCA AI Consortium's 3 June 2026 meeting, published in August, discuss model harnesses and execution boundaries separating probabilistic reasoning from deterministic action. [Bank of England, *Artificial Intelligence Consortium minutes – June 2026*, published August 2026](https://www.bankofengland.co.uk/minutes/2026/june/ai-consortium-minutes-3-june-2026).

That separation is important, but it doesn't solve the McBaggio problem on its own.

An execution boundary can stop an agent breaching a trading limit. It can't save a calculation that used the wrong issuer relationship in the first place.

The rule can be deterministic. The meaning inside the rule still has to be right.

---

## I wouldn't start with an ontology

If you're building an agent today, I wouldn't begin by announcing an ontology programme.

Pick one workflow.

Give the model decent instructions and the context it needs. Add retrieval. Use typed schemas. Put deterministic checks around rules that are genuinely deterministic.

Then pay attention to where people keep correcting the system.

You'll start collecting the awkward cases: duplicate entities, metrics that share a name but not a definition, policies that have been superseded, relationships that are only valid for a period, sources that disagree.

If the same ambiguity keeps causing consequential mistakes across systems and teams, formalise it.

Sometimes that means a schema.

Sometimes a registry.

Sometimes code.

Sometimes an ontology.

Sometimes a graph.

And sometimes it means leaving the decision with Mark because judgement is actually what you're paying Mark for.

---

## Back to Monday

The query runs again.

This time “non-penalty xG” has an explicit definition. The calculation service removes penalties. Provider compatibility is checked before ranking. “League” resolves to the competitions the club actually means.

McBaggio isn't first any more.

Another player moves above him.

That player was there in the original data. Nothing magical happened to the model. We just stopped allowing a few different meanings to masquerade as the same fact.

There is still uncertainty, obviously. There should be. Football recruitment would be fairly boring if a schema could tell you who to sign.

The agent should be able to say:

> I can't establish that from comparable evidence yet.

That is a better answer than a confident ranking built on the wrong assumptions.

Mark looks at the new shortlist.

Then he puts McBaggio back on the scouting list anyway because he likes his movement against a low block.

Fair enough.

That part was never the bug.

And at least now Mark might be able to go on holiday without taking half the club's data model with him.
