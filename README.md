# Academic Application Skills: 用于撰写学术申请信的技能包

Portable agent skills for academic recommendation letters, advisor research, and PhD/RA/MSc outreach.

## Why This Repo Exists

Academic application writing often fails in two ways:

- Recommendation letters become polished self-statements instead of credible recommender testimony.
- Advisor outreach emails become generic cold emails that could be sent to any professor.

This repository provides two reusable, platform-light agent skills that force a better pipeline:

1. Extract the candidate's real evidence from a CV.
2. Separate direct observations from indirect CV facts.
3. Calibrate writing strength to the user's requested level.
4. Verify advisor facts before writing outreach.
5. Audit the final text for overclaiming, generic praise, weak fit, and unsupported claims.

## Included Skills

### `phd-recommendation-letter`

Draft, revise, audit, and score recommendation letters for:

- PhD applications
- RA or research internship applications
- MSc applications
- fellowships
- visiting-student applications
- academic reference letters

Core capabilities:

- CV profile extraction from PDF or text.
- Evidence ledger with direct, indirect, unsupported, and conflict claims.
- Strength calibration across `natural`, `strong`, `very strong`, `exceptional`, `custom-ranking`, and `concise`.
- Research taste and trajectory framing.
- Authenticity, bias, and hallucination audit.
- Heuristic recommendation-letter scoring.

### `phd-advisor-outreach`

Research advisors and draft targeted outreach emails for:

- prospective PhD students
- RA interns
- MSc pre-entry researchers
- visiting students
- summer interns

Core capabilities:

- Source-backed advisor research.
- Current email, lab, homepage, paper, and recruitment checks.
- Fit matrix for direct, adjacent, weak, or no fit.
- Application difficulty labels.
- Targeted subject lines and email drafts.
- Outreach email audit for length, specificity, and overclaiming.

## Repository Structure

```text
academic-application-skills/
├── README.md
├── LICENSE
├── .gitignore
├── examples/
│   ├── advisor-outreach-request.md
│   └── recommendation-letter-request.md
└── skills/
    ├── phd-advisor-outreach/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── references/
    │   └── scripts/
    └── phd-recommendation-letter/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/
        └── scripts/
```

## Usage

These skills are designed to be portable. The core instructions live in `SKILL.md`, detailed guidance lives in `references/`, and deterministic helpers live in `scripts/`.

### Option 1: Use In Codex

Clone the repo, then copy the skills into your Codex skills directory:

```bash
git clone https://github.com/<your-org>/academic-application-skills.git
cd academic-application-skills

mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
rsync -a skills/phd-recommendation-letter/ "${CODEX_HOME:-$HOME/.codex}/skills/phd-recommendation-letter/"
rsync -a skills/phd-advisor-outreach/ "${CODEX_HOME:-$HOME/.codex}/skills/phd-advisor-outreach/"
```

Then invoke the skills:

```text
Use $phd-recommendation-letter to revise this recommendation letter from my CV and recommender context.
```

```text
Use $phd-advisor-outreach to research this professor and draft a targeted RA email.
```

### Option 2: Use In Claude / Claude Code-Style Agents

Point the agent at a skill folder and ask it to follow the `SKILL.md` instructions:

```text
Use the skill at skills/phd-recommendation-letter to draft and audit this recommendation letter.
Read SKILL.md first, then load references only as needed.
```

```text
Use the skill at skills/phd-advisor-outreach to research this advisor and draft a targeted outreach email.
Read SKILL.md first, verify current facts online, and return the output contract.
```

### Option 3: Use With Any LLM Agent

For a generic agent:

1. Paste or attach the relevant `SKILL.md`.
2. Add any needed files from `references/`.
3. Run helper scripts manually if useful.
4. Ask the model to obey the output contract.

The skill folders do not require Codex-specific runtime features. `agents/openai.yaml` is optional UI metadata for OpenAI/Codex-style environments.

## Recommendation Letter Pipeline

1. Parse the candidate CV or profile.
2. Build an evidence ledger:
   - direct evidence observed by the recommender;
   - indirect CV evidence;
   - unsupported claims;
   - publication or role-status conflicts.
3. Identify research taste:
   - problem formulation;
   - failure analysis;
   - evaluation judgment;
   - ownership;
   - sustained research trajectory.
4. Calibrate strength:
   - `natural`;
   - `strong`;
   - `very strong`;
   - `exceptional`;
   - `custom-ranking`;
   - `concise`.
5. Draft the letter by paragraph role.
6. Audit authenticity, bias, overclaiming, and recommender-scope errors.
7. Score the letter and provide risk fixes.

## Advisor Outreach Pipeline

1. Parse the candidate CV and target intent.
2. Verify current advisor facts:
   - official homepage;
   - lab page;
   - email;
   - recent papers;
   - recruitment status.
3. Build the advisor research axis.
4. Build a candidate-to-advisor fit matrix.
5. Classify fit and difficulty.
6. Draft subject lines and outreach email.
7. Audit the email for generic praise, stale facts, weak fit, and unclear asks.

## What Makes These Skills Different

- They do not simply "make writing sound better."
- They separate what is directly observed from what is only present on a CV.
- They preserve user-requested strength, including custom rankings, while flagging risk.
- They require current, source-backed facts for advisor outreach.
- They are field-general and work across AI, engineering, medicine, biology, social sciences, humanities, and interdisciplinary applications.

## Example Prompts

See:

- [`examples/recommendation-letter-request.md`](examples/recommendation-letter-request.md)
- [`examples/advisor-outreach-request.md`](examples/advisor-outreach-request.md)

## Validation

Each skill follows a portable agent-skill structure:

```text
skill-name/
├── SKILL.md              # main agent instructions
├── agents/openai.yaml    # optional OpenAI/Codex UI metadata
├── references/           # optional just-in-time guidance
└── scripts/              # optional helper scripts
```

The bundled scripts are lightweight heuristics, not final admissions judgment. They are designed to catch common errors and force better evidence discipline.

## License

MIT License.
