# Whose xG Is It Anyway?

*The AI found a striker. Every tool worked. The shortlist was still wrong.*

![A shortlisted footballer casts a red fish-shaped shadow across a tactics board, beside checkmarked scouting reports.](https://raw.githubusercontent.com/wilfgrainger/blog/25d67a697ac8bcee49f8c2eb2381f3fe559b5614/articles/whose-xg-is-it-anyway/images/01-cover.jpg)

At 10:06 on Monday, the club's new AI recruitment assistant finds its next number nine.

The brief is straightforward:

> Find under-23 forwards in Europe with at least 900 league minutes and more than 0.55 non-penalty expected goals per 90. Exclude anyone obviously outside our budget.

Thirty seconds later, Roberto McBaggio appears.

Twenty-one. Eighteen months left on his contract. Runs the channels. The assistant has even found six clips of him arriving between the centre-back and full-back.

And then there is the number: **0.64 xG per 90.**

For approximately nine glorious minutes, recruitment has been solved.

Then Mark, one of the analysts, asks two irritatingly short questions.

> “Whose xG?”

Nobody answers.

> “And did it remove the penalties?”

It did not.

McBaggio is fictional. So are the club and the records below. The failure is a useful one to build on purpose.

His 0.64 came from **7.27 total xG over 1,020 minutes**, all supplied by Provider A, model v3. But 2.37 of that came from three penalties: an average of 0.79 each in this invented dataset, not a universal penalty value.

Remove them:

```text
(7.27 − 2.37) ÷ 1,020 × 90 = 0.43 non-penalty xG per 90
```

He no longer meets the brief.

![McBaggio's total rate of 0.64 includes 0.21 penalty xG per 90. Removing those penalties leaves 0.43 non-penalty xG per 90, below the 0.55 recruitment threshold.](https://raw.githubusercontent.com/wilfgrainger/blog/25d67a697ac8bcee49f8c2eb2381f3fe559b5614/articles/whose-xg-is-it-anyway/images/02-metric-dissection.png)

*The threshold applies to the non-penalty metric. The first answer crossed it using the wrong number. Values shown to two decimal places.*

There is a second problem. Another candidate, Mateo Kovac, was scored by Provider B. The club approved Provider A, model v3 for this screen, yet the assistant ranked both providers' figures together.

The two mistakes need different repairs. Removing penalties fixes McBaggio's metric. It does nothing to establish whether another provider's outputs belong in the same ranking.

McBaggio might be brilliant. He is still a red herring for this particular question.

## Five green ticks

The player lookup succeeded. The appearance query succeeded. The event query succeeded. The arithmetic succeeded. The shortlist write succeeded.

Five green ticks. Wrong striker.

Nothing needed to be invented. The system could use real records, execute valid queries and calculate correctly while gradually answering a different question.

That is the failure I want to examine: **successful execution, invalid decision**.

It is the football-data equivalent of entering the wrong stadium into the sat-nav. Every turn can be correct. You are still missing kick-off.

An agent makes this especially interesting because it can choose the next step. It searches for appearances, requests events, retrieves definitions, calculates a rate and writes a shortlist. Each action depends on what the previous result was taken to mean.

Anthropic's [guide to evaluating agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) makes a useful distinction between the transcript and the resulting state of the environment. A booking agent saying it booked a flight is different from a reservation existing in the database. Here, a persuasive explanation of the brief is different from a shortlist that satisfies it.

We should evaluate the decision the system produced, including the records it excluded and the comparisons it refused. Tool completion alone misses the interesting failure.

## Start with the club handbook

Two weeks earlier, the assistant had a smaller job: explain the opposition's build-up and translate “rest defence” into something a board member could repeat without frightening the coaching staff.

For that, a few good Markdown files were a sensible beginning:

- `RECRUITMENT_POLICY.md`
- `METRIC_DEFINITIONS.md`
- `APPROVED_DATA_SOURCES.md`
- `WHEN_TO_ASK_MARK.md`

The model knows football. These files describe **our club's football**: which competitions count, which provider we use, what “affordable” means and who resolves an uncertain contract record.

Writing them is useful engineering. It exposes disagreements before anybody commissions a twelve-month “Football Knowledge Fabric” programme and orders the branded quarter-zips.

Retrieval helps bring the relevant section into context. It is an open-book exam with an extremely fast librarian.

But the assistant can retrieve the correct definition of non-penalty xG and still use a column containing penalties. It can retrieve two providers' methodology notes and still combine their outputs. It can retrieve yesterday's contract perfectly after today's record has superseded it.

**A retrieved definition is not an enforced invariant.**

This is also why a longer prompt, a stronger reasoning model or more attention over the supplied context does not settle the problem. Those may improve the model's choices. They do not, by themselves, impose a boundary on the data a tool accepts or the results a downstream system will commit.

The next step depends on the failure we need to prevent.

## Make this brief executable

xG is a model output, rather than a fact found growing on the pitch. Providers can use different features and assign different probabilities to the same shot; [Hudl's explanation](https://www.hudl.com/blog/expected-goals-xg-explained) gives concrete examples.

A column called `xG` therefore leaves important questions unanswered. Which model produced it? Which shots belong in the population? Are penalties included? Do the minutes describe the same appearances?

For this screen, the club needs a small, explicit contract:

- Identify the player and evaluate age at the screening date.
- Use the agreed league scope and season for both xG and minutes.
- Accept Provider A, model v3; withhold other sources unless the club has approved a method of making them comparable.
- Remove penalty xG and calculate per 90 using the qualifying minutes.
- Apply the minimum of 900 minutes and the strict threshold of **more than** 0.55, before rounding.
- Keep the evidence and the reason for each decision.

A typed record, a metric definition and ordinary validation code can do this. A graph database is not a prerequisite.

The important boundary sits around the calculation and screening service. The model can request a screen, inspect its result and explain it. It cannot turn a validation failure into an accepted result by producing a stirring paragraph about movement in the box.

![An agent submits a request to a deterministic screening service. The service checks an approved contract against candidate evidence and returns separate outcomes: rank, exclude, or withhold.](https://raw.githubusercontent.com/wilfgrainger/blog/25d67a697ac8bcee49f8c2eb2381f3fe559b5614/articles/whose-xg-is-it-anyway/images/03-decision-boundary.png)

*The contract and evidence are inputs to the checks. The model's explanation comes after the result; it cannot approve its own exception.*

Those three outcomes matter:

**Rank:** the evidence is usable and the player meets the brief.

**Exclude:** the evidence is usable and shows that the player fails the brief.

**Withhold:** the evidence is missing or incompatible, so the service cannot make that comparison.

“He does not qualify” and “we cannot establish whether he qualifies” should never become the same database flag. One is a finding. The other is unfinished work.

## Try to break the shortlist

The [companion example](https://github.com/wilfgrainger/blog/tree/25d67a697ac8bcee49f8c2eb2381f3fe559b5614/articles/whose-xg-is-it-anyway/example) contains three fictional players, one CSV and a small Python screen. It uses Python 3.10 or later and needs no model, API key or external package. From this article's directory:

```bash
python3 example/recruitment.py
python3 -m unittest discover -s example -v
```

First, the deliberately flawed screen ranks total xG per 90 without enforcing the provider rule. McBaggio comes first at 0.64, ahead of Mateo Kovac at 0.62 and Elliot Ward at 0.60.

Then the validated screen applies the contract:

- **Elliot Ward: ranked at 0.60.** His evidence meets the approved definitions and the threshold.
- **Roberto McBaggio: excluded at 0.43.** His evidence is comparable, but his non-penalty rate is too low.
- **Mateo Kovac: withheld.** His record uses Provider B, model v1. Under this policy, his apparent 0.62 cannot be used to rank him against Ward.

Ward leads the **validated subset**. We have not established that he is better than Kovac. The missing comparison belongs in the answer, where the recruitment team can see it.

The example also changes every candidate to the unapproved provider. This time there is no validated ranking to return. A system that silently falls back to the incompatible values would recreate the original failure with better documentation.

The fixture is deliberately small. Ages and affordability are supplied screening facts. Aggregates and minutes are assumed to cover the same qualifying appearances. The code checks the declared evidence; it does not independently prove that a provider collected it correctly.

That limit is part of the example. Passing a contract proves compliance with the checks we implemented, not truth about the world. There is no LLM evaluation hidden in these results either: this is a test of the deterministic boundary an agent would call.

## Mark is an undocumented API

Mark already knows which columns to distrust.

He knows that two Roberto McBaggio records describe different people, that the play-offs do not count for this screen, and that one contract feed is authoritative while another is useful mainly for starting arguments.

Mark is an undocumented API with an annual-leave allowance.

Some of what he knows resembles a latent ontology: the club's working concepts and relationships. Some is policy, some is data-quality knowledge, and some is judgement. Treating it all as one kind of “context” makes it harder to decide what to do with it.

Our three-player example needs a small contract and checks. Now imagine the same concepts moving between scouting, medical, contracts, finance and several agents. Each system has its own player identifiers, competition definitions and understanding of which source wins.

The question changes from “can this service calculate the metric?” to “can these systems use the same concept without quietly redefining it?”

That is where an ontology can earn its place: as a formal, shared description of concepts and relationships. A semantic layer can map source-specific fields onto those agreed definitions. A knowledge graph can hold and connect actual instances when traversing those relationships is useful.

These are separate responsibilities. Schemas and registries can also carry important meaning; an ontology has no monopoly on it. The choice should follow the boundaries across which that meaning must survive.

For a richer football system, I would want an evidence path from the player to qualifying appearances, from appearances to shots, and from each shot to its penalty status and provider/model version. The minutes must come from the same qualifying appearances. The result should identify the definition and policy versions used.

That path makes the calculation reconstructable. Validation still has to check it. Merely drawing the relationships does not establish that required evidence is present or that the links are correct.

There is a technical wrinkle here for the ontology enthusiasts: OWL's open-world semantics do not mean that an absent field automatically fails a business rule. Completeness constraints still need explicit validation, whether in application code or, for RDF graphs, a mechanism such as [SHACL](https://www.w3.org/TR/shacl/). The [W3C OWL primer](https://www.w3.org/TR/owl2-primer/) explains the underlying distinction.

An ontology can publish the agreement. Someone still has to own that agreement, check the evidence and enforce the decision.

## 14:17. Same bug, different shirt

At 14:17, an asset-management agent is checking a proposed trade.

Here is another fictional example. The mandate caps exposure at **£8 million per immediate legal parent**. The portfolio holds £6 million of Issuer A and proposes to buy £3 million of Issuer B. We keep currency and exposure amounts fixed so that the ownership relationship is the only thing changing.

Yesterday's record places the issuers under different parents. On that view, the trade passes: £6 million in one group, £3 million in the other.

An ownership change became legally effective at **09:00 today**. Issuer B now shares Issuer A's parent. An authoritative notice describing that change was available at 09:15.

The agent has retrieved yesterday's record at 14:17.

It adds the numbers correctly and clears the trade against an ownership structure that is no longer current.

On the effective relationship, the proposed group exposure is **£6 million + £3 million = £9 million**. The £8 million limit is exceeded.

![A fictional ownership change takes effect at 09:00 and is published at 09:15. At 14:17, yesterday's separate-parent snapshot would approve a trade, while the current shared-parent relationship produces £9 million of exposure against an £8 million limit.](https://raw.githubusercontent.com/wilfgrainger/blog/25d67a697ac8bcee49f8c2eb2381f3fe559b5614/articles/whose-xg-is-it-anyway/images/04-ownership-timeline.png)

*A fresh retrieval can return a stale relationship. Legal effective time, source publication time and decision time answer different questions.*

We have met McBaggio again. This time the wrong interpretation survives a limit check.

The repair requires an agreed definition of the relationship, its source, its period of validity and what supersedes it. If the system cannot establish the relationship effective at the decision time, it should withhold approval under this example's policy.

“Use the newest document” is insufficient: a notice published today might describe a change that takes effect next month. Source freshness is necessary evidence, but it is not a substitute for the relationship's effective dates.

Real mandates have more involved definitions of grouping and exposure. The [Financial Industry Business Ontology](https://edmcouncil.org/financial-industry-business-ontology/) provides shared financial concepts and relationships; it does not make this toy mandate a universal rule, or make a stale source current.

The Bank/FCA AI Consortium's [June 2026 minutes](https://www.bankofengland.co.uk/minutes/2026/june/ai-consortium-minutes-3-june-2026) also discuss governance across whole AI systems and keeping agent actions within defined limits. Those are member discussions, not regulatory instructions for this example.

Our engineering problem is concrete: the limit checker can enforce the arithmetic perfectly while the relationship supplied to it is wrong.

## Leave room for judgement. Be precise about authority.

Some uncertainty is the point of the job.

Will McBaggio adapt to another league? Does his movement against a low block compensate for weaker numbers? A scout is supposed to form hypotheses. We should be suspicious of an architecture that claims to settle them.

I think of an **ambiguity budget** as the unresolved interpretation a workflow can tolerate before it needs more evidence, a person or a stop. Uncertainty about future potential belongs in scouting. Uncertainty about whether a “non-penalty” metric contains penalties belongs on the defect list.

Then ask how much authority the agent has:

**Explain xG → recommend players → decide the shortlist → contact agents → submit an offer.**

The underlying model could be identical at every stage. Its permissions and the consequences are not.

As authority grows, I want stronger evidence requirements, controlled write access, an action log, a recovery plan where recovery is possible, and explicit approval for commitments. A generated explanation cannot grant those permissions or waive the checks.

Nor should the agent silently rewrite the metric contract because it would produce a more satisfying answer. It can propose an exception for a person to assess. The proposal and the authorised change are different events.

## Build the smallest thing that catches McBaggio

My starting point would be one narrow workflow, a clear brief and examples of decisions an expert would reject.

Write the definitions down. Agree who owns them. Give the agent the minimum tools it needs. Put the non-negotiable rules in the service that calculates or acts, then test the resulting decisions.

The awkward cases are the useful ones: a duplicate player, an unapproved provider, a missing penalty field, mismatched minutes, a superseded relationship and a value exactly on the threshold. Include cases where the right answer is a refusal, as well as cases where a player should pass.

I would measure false positives against expert-reviewed cases, missing-evidence cases incorrectly treated as valid, coverage of the intended candidate population, and how often Mark has to repair the same ambiguity. A high refusal rate may reveal poor data coverage rather than a trustworthy product. A low one may mean the service never learned to stop.

Only then would I formalise more of the shared domain. If a registry and a few validators solve the problem, keep them. If the same definitions repeatedly diverge across systems, a shared ontology may help. If following relationships is central to the work, evaluate a graph.

Every component should have a failure it is responsible for preventing. Otherwise the architecture risks becoming an expensive illustration of the article.

## Back to Monday morning

The assistant reruns the screen.

Elliot Ward leads the comparable subset. McBaggio is excluded by the numerical rule. Kovac is withheld pending comparable evidence. The explanation says all three things.

Nothing about the LLM became more intelligent. The system now preserves the question long enough to answer it.

Evidence lives in source records. Definitions live in the shared contract. Code tests the rule. Permissions limit the action. Mark still decides what the numbers cannot.

He looks at the revised shortlist and puts McBaggio back on the scouting list anyway. He likes his movement against a low block.

That is fine. It is a recorded human judgement, made with the correct number in view.

The bug was allowing a machine to present different meanings as one comparable fact.

Football made it easier to see.

And Mark can finally go on holiday.
