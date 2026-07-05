---
name: phd-advisor-outreach
description: Research potential PhD, RA, MSc, visiting-student, or internship advisors and draft targeted academic outreach emails from a CV, target field, advisor homepage, papers, lab output, and application constraints. Use when the user asks to find professors, compare labs, identify email addresses, analyze advisor fit, write cold emails, write RA or PhD inquiry emails, create email subjects, or explain why a lab is suitable.
---

# PhD Advisor Outreach

## Purpose

Use this skill to connect a candidate's evidence-backed research profile to a specific advisor or lab. The output must be source-backed, current, and specific enough that the email could only be sent to that advisor.

Default output:

1. Advisor/lab research brief with source links.
2. Fit matrix and application difficulty.
3. Targeted English email draft and subject lines.
4. Strategy notes in the user's requested language when useful.

## Required Inputs

Before writing, identify or ask for:

- Candidate CV or profile text.
- Target advisor name, homepage, paper URL, institution, region, or field.
- Application mode: PhD, RA, MSc pre-entry intern, visiting student, or summer internship.
- Target domain and optional lens: AI, robotics, NLP, HCI, biology, medicine, social science, humanities, engineering, or other.
- Tone mode: `strong`, `natural`, or `concise`. Default to `strong but credible`.

If a CV PDF is provided and file access is available, use `scripts/extract_cv_profile.py` from `phd-recommendation-letter` or equivalent text extraction before writing.

## Mandatory Research Workflow

1. Verify current facts.
   - Browse for advisor homepage, lab page, official profile, recent publications, recruitment notes, and email.
   - Prefer official pages for email and recruitment status.
   - Use Google Scholar/DBLP/arXiv/Semantic Scholar/lab publication pages for recent work.

2. Build the advisor research axis.
   - Current topics.
   - Recent representative papers.
   - Methods, datasets, domains, and lab style.
   - Student output and collaboration network when visible.
   - Recruitment uncertainty and application route.

3. Build candidate-to-advisor fit.
   - Direct fit: same task, method, domain, or application setting.
   - Adjacent fit: transferable methods or related domain.
   - Weak fit: only broad field overlap.
   - Bridge: one concrete project idea or research question.

4. Draft the email.
   - Subject line.
   - One-sentence identity and application goal.
   - Advisor-specific paragraph anchored in one or two verified works.
   - Candidate trajectory paragraph with evidence from CV.
   - Concrete collaboration ask.
   - Short close with CV attached or offered.

5. Audit before finalizing.
   - Use `scripts/check_outreach_email.py` when possible.
   - Email must include at least two source-backed advisor facts unless the user explicitly asks for a lightweight draft.
   - Do not send generic praise or a paragraph that can be copied to any professor.

## Reference Loading

- Use `references/advisor-research-protocol.md` for search order and source hierarchy.
- Use `references/fit-matrix.md` for scoring and difficulty labels.
- Use `references/outreach-email-patterns.md` for subject lines and email structures.
- Use `references/source-and-claim-policy.md` for current-fact, uncertainty, and citation rules.

## Hard Rules

- Do not invent emails, papers, recruitment status, or lab facts.
- Do not claim the candidate is a perfect fit when the match is adjacent.
- Do not over-specialize to one candidate or field. Treat domain-specific background as a lens, not a template.
- Do not mention a paper unless you can explain why it matters for the candidate's proposed work.
- Keep outreach email concise by default: 180-260 words for RA/PhD cold email, unless the user asks for a longer version.
- If the user asks for "latest", "current", "recent", an email address, or recruiting status, browse before answering.

## Output Contract

For advisor research plus email, return:

1. `Advisor Brief`: advisor, institution, email, lab, current topics, source links.
2. `Fit Matrix`: fit level, difficulty, entry path, hook, candidate angle, risks.
3. `Email Subject`: 2-4 options.
4. `Email Draft`: English by default.
5. `Why This Works`: concise explanation in the user's requested language.
6. `Open Risks`: facts needing confirmation.

For a list of advisors, return a table first, then draft only for the top target unless the user asks for all.
