# Whose xG Is It Anyway?

*The striker had a season's worth of evidence. The shortlist still answered the wrong question.*

![A scouting dashboard puts McBaggio at 0.64 total xG per 90, then flags four penalties and a provider mismatch before showing 0.53 non-penalty xG per 90.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/01-hero.svg)

## 10:06 on Monday

The club's recruitment agent has found a centre-forward. It has only been running for thirty seconds, but the name at the top of the shortlist looks promising: Roberto McBaggio, 21, eighteen months left on his contract. The budget screen doesn't flag him. He presses, gets into the box and, in the clips, keeps arriving at the near post half a step before his marker.

Here is the brief it was given:

> Use the full 2025/26 domestic league season. Find under-23 centre-forwards in Europe with at least 2,000 league minutes and more than 0.55 non-penalty expected goals per 90. Leave out players obviously beyond our budget.

McBaggio's file is properly full. He has 34 league appearances, 30 starts and 2,684 minutes. There are clips for the goals, the shots and the high turnovers. No one needs to extrapolate from six promising games.

- **Output:** 17 goals and five assists; 19.08 xG (0.64 per 90) and 5.84 xA (0.20 per 90).
- **Shooting:** 92 shots (3.08 per 90), 39 on target (42.4%).
- **In possession:** 178 touches in the opposition box (5.97 per 90), 31 key passes (1.04 per 90) and 73 progressive carries (2.45 per 90).
- **Without the ball:** 486 pressures (16.30 per 90), including 172 in the final third (5.77 per 90), plus 94 recoveries (3.15 per 90).
- **The fiddlier bits:** 38 of 91 aerial duels won (41.8%) and 49 of 96 take-ons completed (51.0%).

I made McBaggio and the club up. I gave him the whole season on purpose. The error here survives a large, plausible dossier; it isn't a trick played with a tiny sample.

The shortlist shows **0.64 xG per 90** beside his name. For about nine minutes, this looks like the easiest recruitment meeting of the year.

Then Mark, an analyst, asks whose xG it is. The answer is Provider A. Fine. His next question is shorter.

> “Did it remove the penalties?”

No. Four of McBaggio's 17 goals came from penalties. In this fictional dataset, each penalty has an xG value of 0.79, so the four account for 3.16 of his 19.08 total xG. Provider A has reported that total correctly. A penalty belongs in total xG. It just doesn't belong in the metric the club asked for.

Subtract 3.16 and you get 15.92 non-penalty xG. Use the same 2,684 league minutes:

> (19.08 − 3.16) ÷ 2,684 × 90 = **0.53 non-penalty xG per 90**

That still leaves 88 non-penalty shots and 13 non-penalty goals. The screen requires *more than* 0.55, though, and McBaggio doesn't clear it.

Nothing about his football has changed in the last nine minutes. Nor have the records. The agent picked up a valid number and used it to answer a different question. Having 92 shots to inspect did not help it notice that one missing subtraction.

There is another wrinkle in the shortlist. Some candidates' xG comes from Provider B. Both feeds call the field “xG”, but they use different models. Subtracting penalties fixes McBaggio's rate; it cannot establish that the two providers' outputs can be ranked together. For that, the club needs an approved comparison method or a common source.

McBaggio might still be worth watching. He was a false positive **for this brief**, not a verdict on whether he can play.

This is the problem I want the system to solve: keep the meaning of a number intact as it passes from a provider to a calculation to a decision. The agent can talk to Mark about a striker. It should also be able to show why that striker made, missed or could not yet be compared for this particular list.

## Five green ticks, one bad shortlist

![Five green checks for lookup, minutes, xG, ranking and writing a shortlist still put McBaggio wrongly in first place; the problem is how the evidence was combined.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/02-five-green-ticks.svg)

The agent looked up the player, fetched his appearances and events, ran the arithmetic and wrote the shortlist. Each step returned green. The arithmetic would also pass a unit test if the test asked it to calculate total xG per 90. It was never the requested calculation.

That distinction is easy to lose in an agent demo. You watch the tools work, see a sensible explanation and feel the system has earned its answer. Then Mark asks about the penalties.

[Anthropic's guide to agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) makes a useful separation between the agent's transcript and what actually changed in the environment. Here the thing to inspect is the shortlist: who was ranked, who was left out, what evidence made them comparable, and what the agent refused to decide. Five successful tool calls won't tell you that.

Other errors can take the same route. Query the wrong competition and the rates can be calculated perfectly. Join two players who share a name and you can draw an excellent radar chart for someone who exists only in SQL. The failure is often in the hand-off between one plausible step and the next.

## Start with the handbook

Before anyone says “ontology”, I would write down what the club means.

Four short files are a decent start: `RECRUITMENT_POLICY.md` for the brief, `METRIC_DEFINITIONS.md` for xG and minutes, `APPROVED_DATA_SOURCES.md` for providers, and `WHEN_TO_ASK_MARK.md` for the cases that need a person. Version them. Ask the analysts where they disagree. That conversation will probably be more useful than the first architecture diagram.

Retrieval can put the right page in front of the agent. It cannot guarantee that the agent then selects the right column. McBaggio's case is almost rude in its simplicity: the definition of non-penalty xG could be present in the prompt while the calculation still uses total xG. A stronger model might catch that more often. The service doing the screening should catch it every time.

So give the screen a contract: player identity, age at the screening date, position, region, budget eligibility, season, eligible league appearances, minutes drawn from those appearances, provider and model version, total xG, penalty xG, and the definition of the derived rate. Compare the unrounded result with 0.55. Withhold a comparison when required evidence is missing. Record which version of the policy made the call.

That can be a typed schema, a registry entry and some strict application code. A graph database is not needed to subtract 3.16 from 19.08.

[xG itself is a model estimate](https://www.hudl.com/blog/expected-goals-xg-explained), which is why the provider and model version matter. The useful label isn't simply “19.08 xG”. It is “19.08 total xG from Provider A's approved model, over these league appearances, with penalties included”. Less elegant on a scouting card, admittedly. Far safer at the point where software acts on it.

## The bit Mark knows

Mark can look at two records named Roberto McBaggio and know they are different people. He knows whether a play-off counts as league football here, which contract feed was superseded on Friday and why Provider B's numbers stay off this particular ranking.

Some of that is data cleaning. Some is club policy. Some is judgement. Calling all of it “context” saves a word and loses the distinctions the system needs.

When this is one screen run by one team, the contract above may be enough. When scouting, contracts, medical, finance and several agents start using the same player and competition concepts, you can spend your life translating between their near-identical field names. That is when shared semantics earns its keep.

An ontology, in this setting, is an agreed account of the concepts and relationships: a player makes an appearance in a match; a match belongs to a competition; a shot belongs to an appearance; an xG value comes from a named provider and model; a contract is valid for a period. A semantic layer maps the local data onto those meanings. A knowledge graph can store and traverse the instances if the relationships are the problem you need to solve. The ontology can also be represented and used without turning every data store into a graph.

What would I ask Mark to review? Probably the evidence path, not a box labelled “football ontology”:

> McBaggio → eligible league appearances → shots → penalty status → Provider A/model version → 19.08 total xG − 3.16 penalty xG → 2,684 matching minutes → 0.53 → excluded by the current screen.

That is a claim somebody else can retrace. It also shows the limit of the design. A beautiful set of relationships will not tell you whether a shot was recorded against the wrong player, or whether an appearance is missing. You still need source ownership, validation and a way to correct bad links. A schema can express and enforce a surprising amount of this before a formal ontology is justified.

![McBaggio's 19.08 total xG minus 3.16 penalty xG leaves 15.92 non-penalty xG across 2,684 minutes: 0.53 per 90, below the 0.55 cut-off.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/03-mcbaggio-repair.svg)

The repaired screen should return different answers for different problems. McBaggio is **excluded**: his comparable, complete evidence puts him at 0.53. A candidate whose only evidence is from the unapproved Provider B is **withheld**: the screen cannot make the requested comparison. If everybody in the cohort is in that second category, it should return no ranking at all. It should not silently lower the evidence standard just so the page has a winner.

Those distinctions sound fussy until someone acts on the shortlist.

## Where the uncertainty belongs

A scout can reasonably disagree with a numerical cut-off. Perhaps McBaggio's runs against a low block are more useful to this team than the model captures. I would want the agent to show Mark the correct 0.53 and let him argue about the football.

I would not want it to argue about whether four penalties happened. Nor should it decide, on the fly, that Provider B is close enough to Provider A because the ranking looks nicer.

That is what I mean by an *ambiguity budget*: how much unresolved interpretation can this job carry before it needs more evidence or a person? Explaining xG to a board member can carry more than submitting a £25 million offer. The same model might be involved in both jobs. Its authority, the evidence required and the checks around its actions ought to change.

![From explain to recommend, decide, act and commit, the diagram shows less tolerated ambiguity and stronger controls; the example commitment is a £25 million offer.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/04-authority-ambiguity.svg)

The chart is a prompt for a design conversation, not a measured risk curve. If the agent can recommend players, someone can challenge the list. If it can contact agents or commit money, the system needs explicit permissions, an action record and an authorised route for exceptions. An eloquent paragraph from the model isn't an exception route.

## 14:17, somewhere without football shirts

Try the same mistake in a fictional investment workflow. A mandate limits the *proposed* exposure to £8 million per immediate legal parent. The portfolio already holds £6 million of Issuer A; an agent is checking a £3 million purchase of Issuer B.

Yesterday's ownership record puts A under Parent X and B under Parent Y. Each group appears below £8 million, so the trade passes. The arithmetic is correct for that record.

At 09:00 today, a change of ownership takes legal effect: B is now also under Parent X. The authoritative notice is available at 09:15. At 14:17 the agent fetches yesterday's relationship, adds the same amounts and approves the proposed trade.

Under the relationship effective at decision time, Parent X has **£6 million + £3 million = £9 million** of proposed exposure. The limit is breached. No price or currency changed. The relationship did.

“Fetch the latest document” is not quite a fix. A document published today could describe a change effective next month. The system needs to know which relationship applied at 14:17, which source establishes it and what to do when that answer is missing. For this fictional mandate, the right response would be to withhold approval until the relationship is established.

Financial terms such as issuer, obligor, guarantor and parent carry relationships and dates. [FIBO](https://edmcouncil.org/financial-industry-business-ontology/) is one example of a shared vocabulary for this domain; it does not make our made-up £8 million rule a standard mandate. The [Bank/FCA AI Consortium's June 2026 minutes](https://www.bankofengland.co.uk/minutes/2026/june/ai-consortium-minutes-3-june-2026) discuss whole-system governance and keeping agent actions within defined limits. Those were members' discussions, not instructions issued to this fictional asset manager.

A limit checker can enforce £8 million perfectly and still receive the wrong ownership relation. It is McBaggio with a different noun in the middle of the calculation.

## The part I would actually ship

Give the recruitment team one approved screen, with a versioned definition and an unambiguous player ID. Put the penalty subtraction, eligible-minute selection, provider check and strict threshold in a small service called `screen_recruits`. The service selects the policy version effective for the request; the agent cannot supply an older one. The agent asks it for a screen; the service returns a result for each candidate: **ranked**, **excluded** or **withheld**, with the inputs, calculation, source, model and policy version that produced it. If no candidates have comparable evidence, there is no ranking. The agent explains those results to Mark; it cannot promote an excluded player by writing a nicer sentence.

If the club uses AWS, [Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) could host the agent, and [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-core-concepts.html) could expose `screen_recruits` as a tool backed by that service. [AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html) identifies the calling workload; [AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/use-gateway-with-policy.html) can govern whether it may invoke that Gateway tool. An offer-submission tool would need a separate permission and approval path. Policy can say *who may call what*. It cannot know that McBaggio's 19.08 included four penalties. That check belongs inside `screen_recruits`, against the club's definition and the underlying evidence.

The result for McBaggio would carry 19.08 total xG, 3.16 penalty xG, 15.92 non-penalty xG, 2,684 eligible minutes and **0.53: excluded**. A Provider B-only candidate would be **withheld**, with the missing comparison basis stated plainly. Mark could still add McBaggio to a scouting watchlist, recording that as his own choice. He should not have to falsify the screen to do it.

I'd test the awkward records before trusting a demo: duplicate IDs, missing penalty events, minutes joined from another competition, a provider switch, exactly 0.55, and an attempt to request yesterday's screening policy. Tests of the service should assert the exact number and status, including a whole cohort for which the answer is “no ranking”. The investment checker needs its own test for ownership relationships effective today but recorded yesterday. [AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) can trace tool calls, and [AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) can help assess the agent's explanation. Neither replaces an assertion that this particular candidate was excluded for this particular reason. Keep the evidence and policy version with the tool result so someone can inspect the decision after the chat has ended.

If half the cohort is withheld, that is a problem with data coverage to take back to the team. If nobody is ever withheld, inspect what the service assumes. I'd wait to formalise an ontology until different teams start passing local tests while disagreeing about “league minutes”, player identity or which ownership relationship was valid at decision time. By then there is a real shared meaning problem, and a working screen to show exactly where it hurts.

## Back to Monday

The agent runs the screen again. McBaggio's total xG is still 19.08 and the four penalties are still in that valid total. The derived *non-penalty* rate is 0.53. His record says excluded by this numerical screen, with the calculation visible. Provider B candidates wait for comparable evidence; the system doesn't pretend they lost a ranking it could not fairly run.

Mark has another look at the clips. He adds McBaggio to the scouting watchlist anyway because he likes how the lad moves against a low block. That is an opinion he can own, made with the right number in front of him.

Maybe now he can take a holiday without packing half the club's data model.
