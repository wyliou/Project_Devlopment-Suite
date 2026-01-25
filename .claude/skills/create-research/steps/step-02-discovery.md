---
name: 'step-02-discovery'
description: 'Conduct comprehensive research - market, competitors, and users'

# File references
nextStepFile: '{skill_base}/steps/step-03-complete.md'
outputFile: '{planning_artifacts}/research-{{project_name}}.md'
deepDiveSkill: '{skills_root}/_deep-dive/skill.md'
partyModeSkill: '{skills_root}/_party-mode/skill.md'
---

# Step 2: Discovery

**Progress: Step 2 of 3** - Next: Complete

## STEP GOAL

Conduct comprehensive research covering market, competitors, and users through hybrid web search and collaborative discovery.

## EXECUTION RULES

- **Hybrid step** - web search + user validation
- You are a Research Analyst - gather real data, cite sources
- **NEVER** fabricate data - use web search or get from user
- Present findings with confidence levels (High/Medium/Low)

## SEQUENCE (Follow Exactly)

### 1. Load Context

Read `{outputFile}` to get product concept and research scope from Step 1.

### 2. Market Research

#### A. Web Search for Market Data

Execute searches:
- "[product category] market size 2024 2025"
- "[product category] industry trends"
- "[product category] growth forecast"
- "[problem space] statistics"

**Extract:**
- Total Addressable Market (TAM) estimates
- Market growth rates (CAGR)
- Key industry trends
- Timing factors

**Source Quality:**
- High: Industry reports (Gartner, Forrester, Statista)
- Medium: Expert blogs, company announcements
- Low: General articles, older data (>2 years)

#### B. Present Market Findings

"**Market Research Findings:**

**Market Size & Growth:**
- [Finding with source] - Confidence: [H/M/L]
- [Finding with source] - Confidence: [H/M/L]

**Key Trends:**
- [Trend with source]
- [Trend with source]

**Gaps:** [What I couldn't find]

Can you help fill gaps or correct anything?"

#### C. Fill Gaps (If Needed)

If web search insufficient, ask:
- "What's your estimate of market size?"
- "What trends are you seeing in this space?"
- "Why is now the right time for this product?"

### 3. Competitor Research

#### A. Web Search for Competitors

Execute searches:
- "[problem statement] solutions"
- "[product category] alternatives"
- "best [product category] tools/apps"
- "[competitor name] features pricing reviews" (for known competitors)

**Extract:**
- Competitor names and descriptions
- Key features and capabilities
- Pricing models (if public)
- User sentiment from reviews

#### B. Present Competitor Findings

"**Competitor Research Findings:**

**Direct Competitors:**
| Competitor | What They Do | Strengths | Weaknesses |
|------------|--------------|-----------|------------|
| [Name] | [Desc] | [+] | [-] |

**Indirect Competitors:**
- [Name]: [How they address the problem]

**Gaps I Noticed:**
- [What competitors seem to be missing]

Do you know competitors I missed? Corrections?"

#### C. Fill Gaps (If Needed)

If web search insufficient, ask:
- "Who do your potential customers currently use?"
- "What do existing solutions do well? Where do they fall short?"
- "What would make you different from [competitor]?"

### 4. User Research

#### A. Web Search for User Insights

Execute searches:
- "[competitor name] reviews"
- "[problem] reddit/forum"
- "[product category] complaints"
- "[problem] frustrating/annoying"
- "why I switched from [competitor]"

**Sources:**
- App store reviews, G2, Capterra, TrustPilot
- Reddit, Quora, Stack Overflow discussions
- Product Hunt comments

**Extract:**
- Direct user quotes about pain points
- Common complaints and frustrations
- Workarounds users have created
- Feature requests and wishes

#### B. Present User Findings

"**User Research Findings:**

**Pain Points:** (from real user feedback)
| Pain Point | Source | Example Quote |
|------------|--------|---------------|
| [Pain] | [Source] | '[Quote]' |

**How Users Cope:**
- [Current workaround]

**Unmet Needs:**
- [Need with source]

Does this match what you've heard? Insights to add?"

#### C. Fill Gaps (If Needed)

If web search insufficient, ask:
- "What frustrations have you heard from potential users?"
- "What workarounds do people use?"
- "What would make users say 'finally, someone gets it'?"

### 5. Update Document

Append all research to `{outputFile}`:

```markdown
## Market Research

### Market Overview
[Category and definition]

### Market Size & Growth
- TAM: [estimate] - Source: [url] - Confidence: [H/M/L]
- Growth Rate: [CAGR] - Source: [url]

### Key Trends
1. [Trend] - Source: [url]
2. [Trend] - Source: [url]

### Timing
[Why now is the right time]

---

## Competitor Research

### Competitive Landscape
[Summary of the competitive environment]

### Direct Competitors

#### [Competitor 1]
- **What they do:** [Description]
- **Key features:** [Features]
- **Pricing:** [Model]
- **Strengths:** [What they do well]
- **Weaknesses:** [Where they fall short]

### Indirect Competitors
- [Solution]: [How it addresses the need]

### Competitive Gap Analysis
1. [Gap/opportunity]
2. [Gap/opportunity]

---

## User Research

### Pain Points
1. **[Pain Point 1]**
   - Evidence: [Source and quote]
   - Severity: [High/Medium/Low]
   - Current workaround: [How users cope]

2. **[Pain Point 2]**
   - Evidence: [Source and quote]
   - Severity: [High/Medium/Low]

### Current User Behaviors
- [How users currently solve the problem]

### Unmet Needs
1. [Need with evidence]
2. [Need with evidence]

### What Users Value
- [What users appreciate in existing solutions]
```

### 6. Report & Menu

**Report:**
"Research discovery complete for {{project_name}}.

**Coverage:**
- ✅ Market Research (size, trends, timing)
- ✅ Competitor Analysis (landscape, gaps)
- ✅ User Research (pain points, needs)

**Key Insights:**
- [1-2 sentence summary of most important finding]

Ready to synthesize into recommendations?"

**Menu:**

**[C] Continue** - Proceed to Complete (Step 3)
**[R] Revise** - Discuss changes to research
**[D] Deep Dive** - Apply advanced elicitation on specific area
**[P] Party Mode** - Multi-agent perspectives on findings

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-02-discovery'`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` on market, competitors, or users section. Update document, return to menu.

**On [P]:** Invoke `/_party-mode` for multi-perspective analysis. Update document, return to menu.

---

## SUCCESS CRITERIA

- Web searches conducted for all three areas
- Findings presented with source attribution
- Confidence levels indicated
- User validation obtained
- Gaps filled through facilitated discovery
- All research appended to document
- User confirmed before proceeding
