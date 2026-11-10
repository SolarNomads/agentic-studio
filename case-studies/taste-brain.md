# Taste brain: measuring "which one is better" with agents

[Back to overview](../README.md)

## Problem
Agents can produce content, but taste (which cover stops a scroll, which story pulls you in) is the weak point. The question: can a model judge pairs the way the owner does, and how would we know?

## System built
- **Reference capture:** each reference gets a record (numbers, frames, transcript, cuts, the specific insight, the general principle it supports). A principle becomes a rule only after three independent references or an explicit owner rule.
- **A/B eval sets:** typed pairs (cover, reel strip of 8 frames plus story, story, lettering, colour, transition, comment) with matching rules enforced by a validator: different posts, same topic family, randomised position, no view counts shown. Frozen test sets are hashed and never trained on.
- **Niche pair sourcing:** per-niche candidate lists from public top lists, with off-niche filtering and logged exclusions.
- **Outcome-pair engine:** pairs built from public performance, judged relative to each creator's own size and median, then scored by several model judges.
- **Sharing:** friends can label the same sets through guest links; their answers produce an agreement share and are never merged into the owner's gold labels.

## Evidence (all small samples; read the caveats)
- Gold v1: the owner answered 60 pairs. Model judges asked a different question agreed at about chance (46.7 to 51.9%). Asked the exact question, two judges reached 27 of 41 pairs (65.9%, 95% interval 50.5 to 78.4); still below the 75% bar set for using a judge to label at scale. 10 Nov 2026. [E10](../evidence/README.md#e10)
- Outcome-pair smoke test, 10 Nov 2026: 24 pairs (16 same-creator, 8 cross-creator). One judge scored 72.9% (interval 52.9 to 86.6), another 68.8% (48.8 to 83.6), a third 50% on 16 pairs. The interval for the best judge is wide: 24 pairs is a smoke test, so no judge is promoted; the rule is at least 200 pairs per niche. [E10](../evidence/README.md#e10)
- Eval v2 built 10 Nov 2026: 111 frozen pairs in 7 types (an eighth type could not be filled), plus further niche sets of 16 to 40 pairs. Not every designed type could be filled (some types had too little clean material) and nothing was padded.
- An audit of the first mixed set found that only 37 of 108 pairs had both sides with explicit niche terms; an earlier "108 of 108" check was too lenient and was corrected.

## What I would do for a client
Define the label meaning first ("which would you stop and watch"), freeze a test set, and report every judge with its interval and sample size. Use judges to pre-rank only after they beat the bar on held-out pairs, and keep the human in the loop for new formats.
