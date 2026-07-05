---
name: phd-recommendation-letter
description: Draft, revise, audit, and score PhD, RA, MSc, fellowship, and academic recommendation letters from CVs, recommender context, project evidence, publication records, and target-program goals. Use when the user asks for a letter of recommendation, reference letter, recommendation scoring, recommender-perspective rewrite, research-potential framing, evidence-led letter drafting, authenticity checks, or bias/hallucination audits for graduate-school or research applications.
---

# PhD Recommendation Letter

## Purpose

Use this skill to produce recommendation letters that sound like a credible recommender, not a polished self-statement. Treat the letter as an evidence-led argument for research potential, using direct observations first and CV facts only as supporting context.

Default output:

1. English letter draft.
2. Brief explanation in the user's language when useful.
3. Scorecard and remaining risk flags.
4. Optional replacement sentences for risky claims.

## Required Inputs

Before drafting, identify or ask for:

- Candidate CV or profile text.
- Recommender identity, institution, title, and relationship to the candidate.
- Directly observed work: projects, courses, meetings, mentorship, manuscripts, or lab work.
- Target application type: PhD, RA, MSc, fellowship, visiting student, or internship.
- Requested strength and length: `natural`, `strong`, `very strong`, `exceptional`, `custom-ranking`, or `concise`. Default to `strong but credible`.

If a CV PDF is provided, run `scripts/extract_cv_profile.py` when file access is available. If the script cannot parse the PDF, ask the user for pasted CV text.

## Core Workflow

1. Build an evidence ledger.
   - Direct evidence: what the recommender personally observed.
   - Indirect evidence: CV items the recommender can mention but did not supervise.
   - Unsupported claims: claims that need confirmation or must be softened.
   - Conflict flags: accepted vs under review, transferred vs accepted, first author vs co-first, submitted vs published.

2. Load references only as needed.
   - Use `references/recommendation-rubric.md` for scoring and admissions dimensions.
   - Use `references/research-taste-and-trajectory.md` when the letter must show research taste, ownership, or a multi-project arc.
   - Use `references/authenticity-and-bias-audit.md` before finalizing or when the draft sounds generic.

3. Draft by paragraph role.
   - Relationship and credibility.
   - Comparative judgment calibrated to the requested strength.
   - One concrete observed episode.
   - Research insight and problem formulation.
   - Sustained trajectory and future potential.
   - Collaboration style and independence.
   - Final recommendation.

4. Audit the draft.
   - Run `scripts/score_recommendation_letter.py` on the draft when possible.
   - Remove empty praise: "hard-working", "smart", "excellent" without evidence.
   - Reduce repeated phrases such as "research judgment", "ownership", and "potential".
   - Verify every publication status and role against the CV or user confirmation.

## Hard Rules

- Follow the strength requested by the user or recommender. If they ask for `top 5%`, `top 1%`, `best in X years`, or another ranking, use it when it is consistent with the recommender relationship and evidence ledger.
- If the requested strength is stronger than the evidence supports, still draft the closest credible version, but flag the risk and provide a safer alternative sentence.
- Do not write that the recommender supervised, guided, or observed work they only know from the CV.
- Do not turn a CV into a paragraph of venue names. Explain what the trajectory proves.
- Do not overstate "accepted", "published", "oral", "first author", or "corresponding author".
- If the CV says `transferred`, `under review`, `submitted`, or has conflict with user wording, flag it before finalizing.
- Do not write the candidate's statement of purpose in recommender voice.

## Strength And Tone Modes

- `natural`: credible positive tone, fewer superlatives, no hard ranking, more recommender voice.
- `strong`: clear endorsement, "one of the strongest" style comparison, one concrete episode, explicit PhD readiness.
- `very strong`: stronger comparison such as "among the strongest in recent years" or "comparable to a strong beginning PhD student" when evidence supports it.
- `exceptional`: decisive letter with rare comparison, ranking, or "best in X years" wording when the user/recommender asks for it and the evidence ledger supports it.
- `custom-ranking`: preserve the user's exact allowed ranking such as `top 5%`, `top 1-2 students`, or `best undergraduate I have supervised`, while checking scope and risk.
- `concise`: 4-6 paragraphs, focused on relationship, two evidence points, and final recommendation.

## Output Contract

For a full drafting request, return:

1. `Letter Draft` in English.
2. `What This Letter Is Arguing` as 3-5 bullets.
3. `Evidence Ledger` with direct, indirect, unsupported, and conflict items.
4. `Score` using the rubric in `references/recommendation-rubric.md`.
5. `Risk Fixes` with exact replacement lines for any risky claims.

For a review-only request, lead with findings and scores before giving rewrite suggestions.
