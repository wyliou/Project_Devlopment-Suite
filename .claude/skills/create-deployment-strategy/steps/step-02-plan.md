---
name: 'step-02-plan'
description: 'Create deployment strategy with schedules and gates'

# File references
outputFile: '{project_root}/docs/deployment-strategy.md'
deepDiveSkill: '{skills_dir}/_deep-dive/skill.md'
partyModeSkill: '{skills_dir}/_party-mode/skill.md'
---

# Step 2: Plan

**Progress: Step 2 of 2** - Final Step

## STEP GOAL

Create comprehensive deployment plan including detailed phase definitions, rollout schedule, feature flags, rollback triggers, communication plan, and success metrics.

## EXECUTION RULES

- **Hybrid step** - plan based on scope + user validation
- You are a Release Manager - create specific, actionable plans
- All phases must have clear entry/exit criteria
- Consider both technical and business readiness

## SEQUENCE (Follow Exactly)

### 1. Load Context

Read `{outputFile}` to get scope from Step 1:
- Chosen strategy
- Phase structure
- Pilot group details
- Success criteria
- Constraints

### 2. Create Phase Definitions

For each phase, create detailed definition:

**Present Phase Definitions:**
"**Phase Definitions:**

### Phase 1: Pilot
**Scope:**
- Features included: [List FRs or feature names]
- Features excluded: [Any held back]

**Users:**
- Group: {Pilot group name}
- Count: {Number of users}
- Selection criteria: {Why these users}

**Duration:**
- Start: {Relative date, e.g., 'Week 1'}
- End: {Relative date, e.g., 'Week 2'}

**Success Criteria:**
| Metric | Target | Measurement |
|--------|--------|-------------|
| System uptime | 99.5% | Monitoring |
| Error rate | <1% | Log analysis |
| User satisfaction | >3.5/5 | Survey |
| Critical bugs | 0 | Bug tracker |

**Go/No-Go Gate:**
- All success criteria met
- No open P1/P2 bugs
- Pilot users approve expansion
- Decision maker: {Role}

---

### Phase 2: Early Adopters
**Scope:**
- Features included: [All pilot features + any new]
- Features excluded: [Any still held back]

**Users:**
- Group: {Department/Region/Role}
- Count: {Number of users}
- Selection criteria: {Why these users}

**Duration:**
- Start: {After Phase 1 gate passes}
- End: {Duration}

**Success Criteria:**
| Metric | Target | Measurement |
|--------|--------|-------------|
| System uptime | 99.9% | Monitoring |
| Response time | <500ms p95 | APM |
| User adoption | 80% active | Analytics |
| Support tickets | <10/day | Help desk |

**Go/No-Go Gate:**
- All success criteria met
- Support team trained and ready
- Documentation complete
- Decision maker: {Role}

---

### Phase 3: General Availability
**Scope:**
- Features included: All features
- Features excluded: None

**Users:**
- Group: All users
- Count: {Total user count}

**Duration:**
- Start: {After Phase 2 gate passes}
- Completion: Full rollout over {duration}

**Success Criteria:**
| Metric | Target | Measurement |
|--------|--------|-------------|
| System uptime | 99.9% | Monitoring |
| User adoption | 90% within 30 days | Analytics |
| Training completion | 100% | LMS |

Does this phase structure work for your rollout?"

Wait for user confirmation.

### 3. Create Pilot Program Details

If pilot is part of strategy:

**Present Pilot Program:**
"**Pilot Program:**

**Pilot Groups:**
| Group | Users | Why Selected |
|-------|-------|--------------|
| {Team A} | 10 | Tech-savvy, early adopters |
| {Team B} | 15 | Heavy users of current system |
| {Team C} | 5 | Represents edge cases |

**Pilot Duration:** {X weeks}

**Feedback Collection:**
| Method | Frequency | Owner |
|--------|-----------|-------|
| Daily standup | Daily | Pilot lead |
| Feedback form | Ongoing | Product team |
| Survey | End of pilot | Product team |
| Usage analytics | Continuous | Dev team |

**Pilot Support:**
- Dedicated Slack channel
- Direct access to dev team
- Priority bug fixes

**Graduation Criteria:**
- [ ] All P1/P2 bugs resolved
- [ ] 80% pilot user satisfaction
- [ ] No data loss incidents
- [ ] Performance within targets
- [ ] Support team sign-off

Any adjustments to the pilot program?"

Wait for user confirmation.

### 4. Create Rollout Schedule

**Present Schedule:**
"**Rollout Schedule:**

| Phase | Start | End | Users | Regions | Dependencies |
|-------|-------|-----|-------|---------|--------------|
| Pilot | Week 1 | Week 2 | 30 | HQ | Infrastructure ready |
| Early Adopters | Week 3 | Week 5 | 200 | NA | Pilot complete |
| GA Wave 1 | Week 6 | Week 7 | 500 | NA + EU | Early adopters complete |
| GA Wave 2 | Week 8 | Week 9 | 1000 | All regions | Wave 1 complete |
| GA Complete | Week 10 | - | All | All | Wave 2 complete |

**Key Milestones:**
| Milestone | Date | Criteria |
|-----------|------|----------|
| Pilot launch | Week 1 | Infrastructure approved |
| Pilot gate | Week 2 | Success criteria met |
| CAB approval | Week 2.5 | CAB sign-off |
| GA launch | Week 6 | All gates passed |
| Decommission legacy | Week 12 | 100% migrated |

Does this timeline work with your constraints?"

Wait for user confirmation.

### 5. Define Feature Flags

**Present Feature Flags:**
"**Feature Flags:**

| Feature | Flag Name | Phase | Default | Override |
|---------|-----------|-------|---------|----------|
| New Dashboard | `feature.new_dashboard` | Pilot | Off | On for pilot group |
| Advanced Reports | `feature.advanced_reports` | Phase 2 | Off | On for early adopters |
| Bulk Export | `feature.bulk_export` | GA | Off | On for all |
| Beta Features | `feature.beta` | Future | Off | On for opt-in users |

**Flag Management:**
- Platform: [LaunchDarkly/Split/Custom/Config file]
- Kill switch: All features can be disabled instantly
- Rollout %: Gradual increase supported

**Flag Lifecycle:**
1. Created (before pilot)
2. Pilot enabled (pilot group only)
3. Progressive rollout (% based)
4. Generally available (100%)
5. Removed from code (cleanup)

Any features that need flag control?"

Wait for user confirmation.

### 6. Define Rollback Triggers

**Present Rollback Triggers:**
"**Rollback Triggers:**

| Trigger | Threshold | Action | Decision Maker |
|---------|-----------|--------|----------------|
| System outage | >5 minutes | Immediate rollback | On-call engineer |
| Error rate spike | >5% | Investigate, rollback if unresolved in 30min | Dev lead |
| Data integrity issue | Any data loss | Immediate rollback | Data owner |
| Security incident | Any | Immediate rollback | Security team |
| User-blocking bug | P1 bug affecting >10% | Disable feature flag | Product owner |
| Performance degradation | >2x baseline | Disable feature flag | Dev lead |

**Rollback Procedures:**

| Scenario | Procedure | Est. Time |
|----------|-----------|-----------|
| Feature issue | Disable feature flag | <1 minute |
| Full rollback (blue-green) | Switch traffic to blue | <5 minutes |
| Full rollback (traditional) | Redeploy previous version | <30 minutes |
| Database rollback | Restore from snapshot | <2 hours |

**Rollback Authority:**
- Feature flags: Any team member
- Application rollback: Dev lead or above
- Database rollback: DBA + Product owner

Any adjustments to rollback criteria?"

Wait for user confirmation.

### 7. Create Communication Plan

**Present Communication Plan:**
"**Communication Plan:**

| Audience | When | Channel | Message | Owner |
|----------|------|---------|---------|-------|
| All staff | T-14d | Email | Upcoming changes announcement | Comms |
| Pilot users | T-7d | Email + Meeting | Pilot program details | Product |
| Pilot users | T-1d | Slack | Go-live reminder | Product |
| IT Support | T-7d | Training session | Support runbook | Support lead |
| Pilot users | T+1d | Survey | Feedback request | Product |
| Early adopters | T+14d | Email | Expansion announcement | Comms |
| All users | T+35d | Email | GA announcement | Comms |
| All users | T+35d | Training | Self-paced training available | L&D |

**Communication Templates:**
- Announcement email
- Pilot invitation
- Go-live notification
- Feedback survey
- Support escalation guide

Any stakeholders missing from the communication plan?"

Wait for user confirmation.

### 8. Define Success Metrics by Phase

**Present Success Metrics:**
"**Success Metrics by Phase:**

| Phase | Metric | Target | Actual | Status |
|-------|--------|--------|--------|--------|
| **Pilot** | | | | |
| | Uptime | 99.5% | TBD | - |
| | Error rate | <1% | TBD | - |
| | User satisfaction | >3.5/5 | TBD | - |
| | Critical bugs | 0 | TBD | - |
| **Early Adopters** | | | | |
| | Uptime | 99.9% | TBD | - |
| | Response time p95 | <500ms | TBD | - |
| | User adoption | 80% | TBD | - |
| | Support tickets | <10/day | TBD | - |
| **GA** | | | | |
| | Uptime | 99.9% | TBD | - |
| | User adoption | 90% | TBD | - |
| | Training completion | 100% | TBD | - |
| | User satisfaction | >4/5 | TBD | - |

**Measurement Tools:**
- Uptime: {Monitoring tool}
- Performance: {APM tool}
- Adoption: {Analytics tool}
- Satisfaction: {Survey tool}

Any metrics to add or adjust?"

Wait for user confirmation.

### 9. Update Document

Update `{outputFile}` with all sections:

- Replace *Pending* sections with actual content
- Update frontmatter: `stepsCompleted: ['step-01-scope', 'step-02-plan']`
- Update document status to "Complete"

### 10. Report & Menu

**Report:**
"Deployment strategy complete for {project_name}.

**Coverage:**
- ✅ Phase Definitions ({N} phases)
- ✅ Pilot Program (if applicable)
- ✅ Rollout Schedule
- ✅ Feature Flags ({N} flags)
- ✅ Rollback Triggers
- ✅ Communication Plan
- ✅ Success Metrics by Phase

**Key Dates:**
- Pilot start: {Date}
- GA target: {Date}
- Legacy decommission: {Date}

**Next Steps:**
1. Review with stakeholders
2. Create CAB change request (`/create-change-request`)
3. Prepare operational runbook (`/create-runbook`)
4. Create user documentation (`/create-user-docs`)

Document saved at `{outputFile}`"

**Menu:**

**[R] Revise** - Make changes to any section
**[D] Deep Dive** - Explore specific area (e.g., rollback scenarios)
**[P] Party Mode** - Get Release/Ops/Support perspectives
**[X] Exit** - Workflow complete

**On [R]:** Discuss changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` on selected section. Update document, return to menu.

**On [P]:** Invoke `/_party-mode` with deployment team personas. Update document, return to menu.

---

## SUCCESS CRITERIA

- All phases defined with clear scope and users
- Success criteria measurable for each phase
- Go/No-Go gates specified with decision makers
- Rollout schedule aligned with constraints
- Feature flags documented for controlled rollout
- Rollback triggers and procedures clear
- Communication plan covers all stakeholders
- User validated each section
- Document updated with complete deployment strategy
