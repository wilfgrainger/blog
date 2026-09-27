# Whose xG Is It Anyway?

*Five green ticks. One player on the wrong shortlist.*

![A scouting dashboard puts McBaggio at 0.64 total xG per 90, then flags four penalties and a provider mismatch before showing 0.53 non-penalty xG per 90.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/01-hero.svg)

The recruitment agent has been running for thirty seconds when it puts Roberto McBaggio at the top of the list. He is 21, has eighteen months left on his contract, and the budget check hasn't ruled him out. In the clips he keeps arriving at the near post just before the defender. Mark, the club's analyst, could happily spend the afternoon watching him.

The brief was fairly specific: under-23 centre-forwards in Europe, at least 2,000 minutes in the 2025/26 domestic league season, and **more than 0.55 non-penalty expected goals per 90**. McBaggio has 2,684 minutes. The shortlist shows 0.64 xG per 90. It looks like an easy yes.

Mark asks two questions. Whose xG? Provider A's. And did the agent remove the penalties?

It didn't.

McBaggio, the club and the numbers in this story are fictional. I've given him a whole season rather than a suspiciously convenient handful of matches. He played 34 league games, started 30, scored 17 goals and took 92 shots. His 19.08 total xG is a perfectly valid Provider A number. Four of his goals came from penalties, worth 0.79 xG each in this invented dataset. That's 3.16 xG the brief explicitly asked us to leave out.

> (19.08 − 3.16) ÷ 2,684 × 90 = **0.53 non-penalty xG per 90**

He still has 88 non-penalty shots and 13 non-penalty goals. I would still watch the clips. But 0.53 is below the club's *more than 0.55* cut-off. The agent calculated the rate correctly for the field it picked up. It picked up the wrong field for this question.

There is a second problem lurking further down the list. Some players have xG from Provider B. Its model is different from Provider A's. Even if we strip out every penalty, we have not established that the two providers' estimates belong in one ranking. Those players need an approved way to compare the feeds, or a common source; until then, the honest answer is that we cannot rank them against McBaggio.

The agent hasn't made up a player or invented a number. That is what makes the mistake easy to miss.

## Why everything looked green

![Five green checks for lookup, minutes, xG, ranking and writing a shortlist still put McBaggio wrongly in first place; the problem is how the evidence was combined.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/02-five-green-ticks.svg)

Player lookup worked. The appearances and shot events came back. The arithmetic ran. The shortlist was written. Each tool could report success without knowing that the original request said *non-penalty*.

This is a familiar trap in agent work. We inspect the trail of calls because it is visible and tidy. The decision it produced takes more effort to examine. [Anthropic's guide to agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) distinguishes the transcript from what happened in the environment. In this case, I would test the shortlist: who got in, who was excluded, whose evidence couldn't support a comparison, and what the agent was allowed to do next.

The club could fix this one result and still have the same problem next week. Imagine the team measuring its agent by how quickly it returns a complete list. A request for more evidence looks like a failure; a populated ranking looks like a success. People learn to trust the green ticks, so fewer odd-looking decisions reach Mark. Nothing in that loop improves the meaning of the numbers. Faster runs just produce more lists that nobody quite knows how to challenge.

There are other ways to get there. Ask for domestic league minutes and accidentally include a play-off. Join two players with the same name and produce a lovely radar chart for a footballer who exists only in SQL. Each step can be defensible on its own. The meaning slips where the steps meet.

## What Mark was carrying around in his head

Mark knows which competition this club means by “league”. He remembers that a contract feed was superseded on Friday. He knows why Provider B stays out of this ranking. Some of that is source quality, some is club policy, and some is his judgement about football. If it all lives in Mark's head, annual leave becomes a data dependency.

I would start by asking him and the other analysts to write down the contested definitions. Which appearances count? Do the minutes and shots come from the same matches? Which model versions are approved? What should happen when the answer is missing? A few versioned pages and an uncomfortable meeting may do more good than a grand data programme.

Putting those pages in a prompt helps the agent find them. It does not guarantee that a calculation uses them. The screening service should accept an identified player, a season, eligible appearances and matching minutes, the provider and model version, and the total and penalty xG from that source. It should apply the current club policy itself, using the unrounded rate. The agent shouldn't get to choose yesterday's policy because today's answer is inconvenient.

That service can distinguish two results the original shortlist blurred. McBaggio is **excluded**: there is enough approved evidence to say he misses this screen. A Provider B-only candidate is **withheld**: under this fictional club's policy, the available feed cannot support comparison. Calling that player a poor performer would be fiction piled on fiction.

![McBaggio's 19.08 total xG minus 3.16 penalty xG leaves 15.92 non-penalty xG across 2,684 minutes: 0.53 per 90, below the 0.55 cut-off.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/03-mcbaggio-repair.svg)

A typed contract and strict code could handle this screen. The case for something more shared appears when scouting, medical, contracts, finance and several agents all have their own near-matches for “player”, “appearance” and “season”. You find yourself repairing the same misunderstanding at every hand-off.

That is where I would consider an ontology: an agreed description of the things and relationships the club relies on. A shot belongs to an appearance; an appearance belongs to a player in a competition; an xG estimate comes from a particular provider and model. A semantic layer can map local fields onto that description. A graph may help if the club needs to traverse those links. None of this requires moving every store into a graph, and none of it rescues a bad source record by magic. Someone still has to own and correct the links.

The test is whether Mark can follow a result back through those links. If a shot is assigned to the wrong McBaggio or the denominator includes different matches from the numerator, he needs a place to report it and a way to see what changed. A shared definition that nobody can challenge will become another green tick.

## How much can the agent assume?

Mark may think McBaggio is unusually good against a low block. He can disagree with a numerical cut-off and put him on a watchlist. That is the part I want a scout to argue about. I don't want the agent quietly treating four penalties as open-play chances or deciding that Provider B is “close enough”.

I've taken to thinking of this as an *ambiguity budget*. A chat answer about xG can survive a loose explanation and a follow-up question. A shortlist sent to a recruitment meeting needs traceable evidence. A £25 million offer cannot rest on an unresolved player identity, an unapproved source comparison or a model's persuasive explanation of why it probably meant well. The greater the authority to act, the less room there is to guess.

![From explain to recommend, decide, act and commit, the diagram shows less tolerated ambiguity and stronger controls; the example commitment is a £25 million offer.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/04-authority-ambiguity.svg)

That drawing is a design prompt, not a measured risk curve. The practical question is who can stop the next step, on what evidence, and whether the stop actually holds. Otherwise the agent has merely learned to write a very convincing exception request to itself.

It is not just a football problem. Take a fictional investment mandate with an £8 million exposure limit per immediate legal parent. The portfolio holds £6 million of Issuer A; an agent proposes £3 million of Issuer B. Yesterday the issuers had different parents. At 09:00 today B moved under A's parent, with an authoritative notice available at 09:15. At 14:17 the agent checks yesterday's relationship and approves the trade. The addition is right. The answer is wrong: the proposed exposure is £9 million.

The checker needs the ownership relationship effective at the time of the decision, not merely the newest document it can find. A document published today could describe a change that takes effect next month. While the relationship is unresolved, withhold approval; once today's relationship is established, reject the proposal. [FIBO](https://edmcouncil.org/financial-industry-business-ontology/) offers a vocabulary for financial relationships. It does not know this fictional mandate or whether the portfolio has a reliable ownership record. Same awkward hand-off, more expensive consequences.

## What I would build first

I would give the recruitment agent one `screen_recruits` service. It returns a ranked candidate only when the evidence is comparable, an exclusion with the calculation when someone fails the rule, and a withheld result when the evidence cannot carry the comparison. It records the source and effective policy version so Mark can dispute a decision without reconstructing it from chat logs.

If I were deploying it on AWS, [Bedrock AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) could run the agent, [Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-core-concepts.html) could expose the screening tool, and [AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/use-gateway-with-policy.html) could let a recruitment role request a screen while denying an offer submission. The penalty subtraction and provider rules belong inside the screening service. A permission check cannot tell you what xG means.

I put together a [small local replay](https://github.com/wilfgrainger/blog/tree/main/articles/whose-xg-is-it-anyway/examples) to make that distinction testable. With McBaggio's full-season evidence, an authorised screen returns **excluded, 0.53, required > 0.55**. A Provider B-only candidate comes back **withheld**. A request to submit a £25 million offer is denied before the offer function runs. The replay tests those behaviours locally; it is not a deployed AgentCore policy.

Mark can now look at the shortlist and see both the decision and the route back to the evidence. He can still say that McBaggio's near-post runs are worth another look. In fact, he puts him on the watchlist.

This time he knows exactly which rule he is choosing to look beyond.
