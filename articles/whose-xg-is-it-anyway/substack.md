![A scouting dashboard puts McBaggio at 0.64 total xG per 90, then flags four penalties and a provider mismatch before showing 0.53 non-penalty xG per 90.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/01-hero.svg)

## 10:06 on Monday

The club's recruitment agent has found a centre-forward. It has only been running for thirty seconds, but the name at the top of the shortlist looks promising: Roberto McBaggio, 21, eighteen months left on his contract. The budget screen doesn't flag him. He presses, gets into the box and, in the clips, keeps arriving at the near post half a step before his marker.

Here is the brief it was given:

> Use the full 2025/26 domestic league season. Find under-23 centre-forwards in Europe with at least 2,000 league minutes and more than 0.55 non-penalty expected goals per 90. Leave out players obviously beyond our budget.

McBaggio has 34 league appearances, 30 starts and 2,684 minutes. There are clips for the goals, the shots and the high turnovers. Here is his season:

- **Output:** 17 goals and five assists; 19.08 xG (0.64 per 90) and 5.84 xA (0.20 per 90).
- **Shooting:** 92 shots (3.08 per 90), 39 on target (42.4%).
- **In possession:** 178 touches in the opposition box (5.97 per 90), 31 key passes (1.04 per 90) and 73 progressive carries (2.45 per 90).
- **Without the ball:** 486 pressures (16.30 per 90), including 172 in the final third (5.77 per 90), plus 94 recoveries (3.15 per 90).
- **The fiddlier bits:** 38 of 91 aerial duels won (41.8%) and 49 of 96 take-ons completed (51.0%).

I made McBaggio and the club up. I gave him the whole season on purpose. The error here survives a large, plausible dossier; it isn't a trick played with a tiny sample.

The shortlist shows **0.64 xG per 90** beside his name. For about nine minutes, this looks like the easiest recruitment meeting of the year.

Then Mark, an analyst, asks whose xG it is. The answer is Provider A. Fine. His next question is shorter.

> “Did it remove the penalties?”

No. McBaggio took four penalties and scored them all. In this fictional dataset, each penalty has an xG value of 0.79, so the four account for 3.16 of his 19.08 total xG. Provider A has reported that total correctly. A penalty belongs in total xG. It just doesn't belong in the metric the club asked for.

Subtract 3.16 and you get 15.92 non-penalty xG. Use the same 2,684 league minutes:

> (19.08 − 3.16) ÷ 2,684 × 90 = **0.53 non-penalty xG per 90**

That still leaves 88 non-penalty shots and 13 non-penalty goals. The screen requires *more than* 0.55, though, and McBaggio doesn't clear it.

Nothing about his football has changed in the last nine minutes. The agent picked up a valid number and used it to answer a different question.

There is another wrinkle in the shortlist. Some candidates' xG comes from Provider B. Both feeds call the field “xG”, but they use different models. Subtracting penalties fixes McBaggio's rate; it cannot establish that the two providers' outputs can be ranked together. For that, the club needs an approved comparison method or a common source.

McBaggio might still be worth watching. He was a false positive **for this brief**, not a verdict on whether he can play.

The job is to keep the meaning of that number intact from provider to calculation to decision. Someone should be able to retrace why a player made the list.

## Five green ticks, one bad shortlist

![Five green checks for lookup, minutes, xG, ranking and writing a shortlist still put McBaggio wrongly in first place; the problem is how the evidence was combined.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/02-five-green-ticks.svg)

The agent looked up the player, fetched his appearances and events, ran the arithmetic and wrote the shortlist. Each step returned green. The arithmetic would also pass a unit test if the test asked it to calculate total xG per 90. It was never the requested calculation.

[Anthropic's guide to agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) makes a useful separation between the agent's transcript and what actually changed in the environment. Here the thing to inspect is the shortlist: who was ranked, who was left out, what evidence made them comparable, and what the agent refused to decide. Five successful tool calls won't tell you that.

Other errors can take the same route. Query the wrong competition and the rates can be calculated perfectly. Join two players who share a name and you can draw an excellent radar chart for someone who exists only in SQL. The failure is often in the hand-off between one plausible step and the next.

## Start with the handbook

Before anyone says “ontology”, I would write down what the club means.

Four short files are a decent start: `RECRUITMENT_POLICY.md` for the brief, `METRIC_DEFINITIONS.md` for xG and minutes, `APPROVED_DATA_SOURCES.md` for providers, and `WHEN_TO_ASK_MARK.md` for the cases that need a person. Version them. Ask the analysts where they disagree. That conversation will probably be more useful than the first architecture diagram.

Retrieval can put the right page in front of the agent. The definition of non-penalty xG could be present in the prompt while the calculation still uses total xG. A stronger model might catch that more often. The service doing the screening should catch it every time.

So give the screen a contract: player identity, age at the screening date, position, region, budget eligibility, season, eligible league appearances, minutes drawn from those appearances, provider and model version, total xG, penalty xG, and the definition of the derived rate. Compare the unrounded result with 0.55. Withhold a comparison when required evidence is missing. Record which version of the policy made the call.

That can be a typed schema, a registry entry and some strict application code. A graph database is not needed to subtract 3.16 from 19.08.

[xG itself is a model estimate](https://www.hudl.com/blog/expected-goals-xg-explained), which is why the provider and model version matter. The useful label isn't simply “19.08 xG”. It is “19.08 total xG from Provider A's approved model, over these league appearances, with penalties included”. Less elegant on a scouting card, admittedly. Far safer at the point where software acts on it.

## The bit Mark knows

Mark can look at two records named Roberto McBaggio and know they are different people. He knows whether a play-off counts as league football here, which contract feed was superseded on Friday and why Provider B's numbers stay off this particular ranking.

Some of that is data cleaning. Some is club policy. Some is judgement. Calling all of it “context” saves a word and loses the distinctions the system needs.

When this is one screen run by one team, the contract above may be enough. When scouting, contracts, medical, finance and several agents start using the same player and competition concepts, you can spend your life translating between their near-identical field names. That is when shared semantics earns its keep.

An ontology is an agreed account of those concepts and relationships: a player makes an appearance in a match; a shot belongs to an appearance; an xG value comes from a provider and model; a contract is valid for a period. A semantic layer maps local data onto those meanings. A knowledge graph can store the connected records when traversing those relationships is useful. You can use the ontology without putting every data store into a graph.

What would I ask Mark to review? Probably the evidence path, not a box labelled “football ontology”:

> McBaggio → eligible league appearances → shots and penalty status → Provider A/model version → matching minutes → screening decision.

That path still needs checking. A shot could be recorded against the wrong player; an appearance could be missing. You need source ownership, validation and a way to correct bad links. A schema can enforce much of this before a formal ontology is justified.

![McBaggio's 19.08 total xG minus 3.16 penalty xG leaves 15.92 non-penalty xG across 2,684 minutes: 0.53 per 90, below the 0.55 cut-off.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/03-mcbaggio-repair.svg)

There are two different outcomes here. **Excluded** means the evidence fails the screen. **Withheld** means the evidence cannot support the comparison. Provider B candidates belong in the second category under this club's policy. Treating them as poor performers would invent a result.

## Where the uncertainty belongs

A scout can reasonably disagree with a numerical cut-off. Perhaps McBaggio's runs against a low block are more useful to this team than the model captures. I would want the agent to show Mark the correct 0.53 and let him argue about the football.

I would not want it to argue about whether four penalties happened. Nor should it decide, on the fly, that Provider B is close enough to Provider A because the ranking looks nicer.

That is what I mean by an *ambiguity budget*: how much unresolved interpretation can this job carry before it needs more evidence or a person? Explaining xG to a board member can carry more than submitting a £25 million offer. The same model might be involved in both jobs. Its authority, the evidence required and the checks around its actions ought to change.

![From explain to recommend, decide, act and commit, the diagram shows less tolerated ambiguity and stronger controls; the example commitment is a £25 million offer.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/04-authority-ambiguity.svg)

The chart is a prompt for a design conversation, not a measured risk curve. If the agent can recommend players, someone can challenge the list. If it can contact agents or commit money, the system needs explicit permissions, an action record and an authorised route for exceptions. An eloquent paragraph from the model isn't an exception route.

## 14:17, somewhere without football shirts

In a fictional investment workflow, a mandate caps proposed exposure at £8 million per immediate legal parent. The portfolio holds £6 million of Issuer A. An agent checks a £3 million purchase of Issuer B. Yesterday, they had different parents. The trade appears to pass.

At 09:00 today, B moves under A's parent. The authoritative notice is available at 09:15. At 14:17 the agent checks yesterday's relationship and approves the trade. The actual proposed exposure is **£6 million + £3 million = £9 million**. No price or currency changed. The relationship did.

The checker needs the relationship effective at decision time. Publication date alone won't do: today's document might describe next month's change. Withhold approval while the relationship is unresolved; reject the proposal once the £9 million exposure is established.

[FIBO](https://edmcouncil.org/financial-industry-business-ontology/) provides a shared vocabulary for financial concepts and relationships. It does not supply this fictional mandate. A limit checker can enforce £8 million perfectly and still receive the wrong ownership relation.

## The part I would actually ship

Put the agreed screen in a service called `screen_recruits`. It checks the candidate and data scope, performs the calculation and returns the decision with its evidence. The service selects the effective policy version; the agent cannot supply an older one. If nobody has comparable evidence, it returns no ranking.

On AWS, [Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) could host the agent. [Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-core-concepts.html) would expose the service as an MCP tool, with [AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/use-gateway-with-policy.html) allowing the authenticated recruitment role to request a screen and denying it permission to submit an offer. Policy can say *who may call what*. The penalty check belongs inside the screening service.

Here is the small [local replay](https://github.com/wilfgrainger/blog/tree/main/articles/whose-xg-is-it-anyway/examples) I would use to pin down that behaviour. It runs the metric check and a recruitment-only tool permission without an AWS account; the AgentCore setup above is the deployment design. The fixture supplies Provider A/model v3.4, the full-season totals and 2,684 matching minutes. The service holds screening policy `recruitment-v1`. Its output, abridged:

```text
screen_recruits("mcbaggio-21")
  excluded · NPxG/90: 0.53 · required: > 0.55
  evidence: season-2025-26-mcbaggio
  policy: recruitment-v1 · source: A/v3.4

screen_recruits("provider-b-only")
  withheld · no approved provider comparison

submit_offer("mcbaggio-21", GBP=25000000)
  denied · recruitment role lacks permission
  offer function was never called
```

The first call is authorised and produces an exclusion. The last is stopped before the offer function runs. Those are separate checks, with separate reasons a reviewer can inspect.

Extend the checks to duplicate IDs, missing penalty events, competition mismatches and a request for yesterday's policy. Compare the unrounded rate: exactly 0.55 must fail a *more than 0.55* rule. [AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) can trace the calls; [Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) can assess the agent's explanation. Keep exact assertions for the numbers, decisions and denied actions.

If half the cohort is withheld, take the coverage problem back to the team. If nobody is ever withheld, inspect the assumptions. Formalise the ontology when teams start passing their own tests while disagreeing about “league minutes” or player identity. By then, the working screen will show where a shared definition would help.

## Back to Monday

The agent runs the screen again. Mark can see who failed the brief, who needs better evidence and why. He doesn't have to interrogate every decimal before discussing the players.

Mark has another look at the clips. He adds McBaggio to the scouting watchlist anyway because he likes how the lad moves against a low block. That is an opinion he can own, made with the right number in front of him.

Maybe now he can take a holiday without packing half the club's data model.
