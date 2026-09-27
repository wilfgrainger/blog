![A scouting dashboard puts McBaggio at 0.64 total xG per 90, then flags four penalties and a provider mismatch before showing 0.53 non-penalty xG per 90.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/01-hero.png)

Roberto McBaggio is the first name on the recruitment agent's shortlist. He's 21, has eighteen months left on his contract, and keeps getting to the near post a step ahead of the defender. Mark, the club's analyst, opens another clip.

The number beside McBaggio's name is **0.64 xG per 90**. The club asked for under-23 centre-forwards in Europe with at least 2,000 domestic league minutes in 2025/26 and **more than 0.55 non-penalty xG per 90**. McBaggio played 2,684 minutes. On the face of it, he sails through.

“Whose xG?” Mark asks.

Provider A's, says the agent.

“And you took the penalties out?”

It hadn't.

McBaggio and the club are fictional. His made-up season has 34 league appearances, 30 starts, 17 goals, 92 shots and 19.08 total expected goals. Four goals came from penalties, each worth 0.79 xG in this dataset. The total xG number is valid. It's the wrong number for this screen.

Expected goals (xG) estimates the quality of chances. A penalty is a particularly good chance, so including four of them lifts the total above the *non-penalty* figure the club asked for. Subtract 3.16 before dividing by the minutes:

> (19.08 − 3.16) ÷ 2,684 × 90 = **0.53 non-penalty xG per 90**

McBaggio still took 88 non-penalty shots and scored 13 non-penalty goals. He may be well worth watching. But 0.53 is below the strict *more than 0.55* line. He shouldn't have passed this particular filter.

## Five ticks, wrong answer

![Five green checks for lookup, minutes, xG, ranking and writing a shortlist still put McBaggio wrongly in first place; the problem is how the evidence was combined.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/02-five-green-ticks.png)

Nothing crashed. The player lookup found McBaggio. The minutes and shot data arrived. The agent divided 19.08 by 2,684 and multiplied by 90 correctly. It wrote a tidy shortlist. Every step can be marked successful while the answer to Mark's question is wrong.

There is another catch lower down the page. Some candidates have xG from Provider B, whose model estimates chances differently. Removing penalties from both feeds does not suddenly make the numbers interchangeable. If the club has no approved way to compare A and B, those players cannot honestly be ranked against McBaggio yet.

Suppose the agent gets praised for producing ten names by nine o'clock. “I can't compare two of them” looks like unfinished work. So it uses the xG field it has, people see a finished list, and fewer awkward questions reach Mark. Next week it does the same thing.

## What the number means

Mark knows which matches the club counts as “domestic league”. He knows the minutes and shots must cover those same matches. He knows which xG provider and model version the club accepts, and why Provider B is out of this particular comparison. None of that is in the naked number 0.64.

The threshold is the easy part of this business rule. The hard part is deciding what the number *is*. A semantic layer gives the club one account of a *player*, an eligible *appearance*, a *shot*, an *xG estimate*, and how they relate. The estimate carries its provider and model version; the appearance carries its competition and season. “Non-penalty xG per 90” means summing approved non-penalty shot estimates for eligible appearances, dividing by the minutes from those same appearances, then multiplying by 90. The screening rule points to that definition and to the policy version in force.

Now Mark can ask: *Which matches and shots produced this 0.53?* Without those links, one service can subtract penalties, another can include play-off minutes, and a third can silently mix providers. All three may claim to implement the “same” rule. The semantic layer gives them a common answer to what the number means and where it came from.

It does not have to begin as a vast graph. Start with the terms the analysts actually dispute, give them owners and versions, map the source fields to them, and test a few awkward cases. A page of definitions alone is not enough if the calculations still read arbitrary fields. Equally, the semantic layer does not enforce the threshold by itself. A screening service must consume the defined evidence, reject incompatible inputs and apply **> 0.55** to the unrounded rate. The agent should not get to pick a different definition to make the shortlist look better.

That service can distinguish two answers the original list blurred. McBaggio is **excluded**: there is enough approved evidence to say he misses this screen. A Provider B-only candidate is **held for review**: the club has not approved a comparison. “Held” is not a low score for that player.

![McBaggio's 19.08 total xG minus 3.16 penalty xG leaves 15.92 non-penalty xG across 2,684 minutes: 0.53 per 90, below the 0.55 cut-off.](https://raw.githubusercontent.com/wilfgrainger/blog/main/articles/whose-xg-is-it-anyway/images/03-mcbaggio-repair.png)

## Let Mark challenge it

I'd check the next shortlist against a few cases the analysts already know: a penalty taker like McBaggio, two players on different feeds, a missing shot record, and a rate that lands exactly on 0.55. McBaggio should be **excluded at 0.53**; a Provider B-only candidate should be **held for review** until the club agrees on a comparison. Exactly 0.55 should fail a rule that says *more than* 0.55. That is a more useful test than counting how many tool calls completed.

The result should link back to its match list, shot records, source and rule version. If a shot is assigned to the wrong McBaggio, Mark needs a way to report it and see the correction. The shared definitions must be open to challenge too. Otherwise the semantic layer becomes just another green tick.

Mark goes back to the near-post clips. He can put McBaggio on his watchlist despite the screen; that's his call. At least the shortlist now tells him exactly which rule he's looking past.
