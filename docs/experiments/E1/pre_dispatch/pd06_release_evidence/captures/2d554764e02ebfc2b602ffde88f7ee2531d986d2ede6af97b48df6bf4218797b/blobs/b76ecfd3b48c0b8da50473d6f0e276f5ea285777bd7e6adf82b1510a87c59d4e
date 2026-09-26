# Vision — AI\-Orchestrated Engineering System

**Status:** Draft
**Purpose:** Foundational vision for architecture elicitation

## 1\. Vision

The objective is to create an AI\-assisted engineering environment capable of transforming human intent into a completed, verified engineered system through collaboration among humans and specialized AI agents\.

The fundamental premise is that increasingly capable AI coding agents make implementation less of a limiting factor in software development\. As implementation becomes faster and more autonomous, the primary engineering challenge moves upward: accurately capturing human intent, transforming that intent into a coherent architecture, maintaining that architecture throughout development, directing implementation, evaluating evidence, and determining whether the resulting system satisfies the original objective\.

The envisioned system separates these responsibilities\.

The human acts primarily as the source of **vision, intent, priorities, constraints, and judgment**\.

An **Architect Agent** transforms that intent into sufficiently rigorous engineering knowledge to guide implementation\. It maintains architectural coherence, identifies missing information, derives requirements and invariants, decomposes the system into implementation increments, evaluates implementation discoveries, and determines what work should occur next\.

One or more **Implementation Agents**, initially represented by Codex, perform bounded engineering tasks against the actual repository\. They inspect the implementation, write and modify code, execute tests, perform analysis, and return evidence describing what was accomplished and what was discovered\.

The system repeatedly moves between architectural reasoning and implementation until objective evidence demonstrates that the original human objective has been achieved\.

The long\-term goal is not simply autonomous programming\.

It is **autonomous engineering governed by human intent**\.

The system must also account explicitly for context management\. Model invocations are not assumed to retain complete project knowledge across calls\. Conversation history, working memory, and model context are transient and bounded resources\. Authoritative engineering knowledge must therefore be persisted externally, selectively retrieved, summarized, and supplied to each agent invocation as needed\.

Context management is not merely an implementation detail\. It is part of the system’s engineering problem because loss, omission, corruption, or misprioritization of context can cause architectural drift, repeated reasoning, inconsistent decisions, or silent divergence from human intent\.

---

## 2\. Problem

Current AI coding systems are increasingly capable of implementing substantial software changes when provided with sufficiently precise instructions\. However, the quality of the resulting system remains highly dependent upon the quality of those instructions\.

Important architectural knowledge frequently exists only in the mind of the human directing the work\. Some of that knowledge is communicated through prompts, conversations, design documents, or corrections during implementation\. Other knowledge remains implicit until implementation exposes a decision that was never adequately specified\.

This creates several problems\.

An implementation agent can produce technically correct software that does not reflect the actual intent of the system designer\. Architectural assumptions may become embedded in code without ever becoming explicit decisions\. Long\-running conversations may contain important knowledge that is difficult to identify later\. Implementation discoveries may invalidate earlier architectural assumptions\. Architectural documentation may gradually diverge from implementation reality\.

In API\-based systems, the problem is compounded by context boundaries\. Each model invocation may receive only a selected portion of the project’s history and knowledge\. If the orchestration layer fails to preserve or retrieve relevant context, the agent may behave as though prior decisions, constraints, unresolved questions, or evidence do not exist\.

Increasing the autonomy and speed of coding agents can amplify these problems\. An implementation agent capable of making rapid progress can also make rapid progress in the wrong architectural direction\. An agent that receives incomplete context can make apparently reasonable decisions that conflict with authoritative project knowledge\.

The system therefore requires something more durable than increasingly sophisticated prompts\.

It requires a mechanism for maintaining **authoritative engineering knowledge** throughout the life of the project, together with a deliberate context\-management process that determines what knowledge each agent needs for each decision\.

---

## 3\. Core Concept

The system is based upon a continuous engineering loop:

**Human Intent → Knowledge → Architecture → Context Assembly → Implementation → Evidence → Reconciliation → Knowledge**

Human intent begins the process, but it should not need to describe every implementation detail\.

The Architect Agent is responsible for transforming that intent into engineering precision\.

Before implementation begins, the Architect actively analyzes the vision to determine what has been explicitly stated, what is implied, what assumptions would otherwise need to be made, and what important questions remain unresolved\.

The Architect uses this process to establish an initial architectural baseline\.

For each significant reasoning or implementation activity, the orchestration mechanism assembles the relevant context from authoritative project knowledge, current repository state, prior decisions, active work packages, unresolved issues, and applicable evidence\. Context should be sufficient for the task without requiring every agent invocation to receive the entire project history\.

Implementation Agents subsequently execute bounded portions of that architecture and return evidence\.

The Architect evaluates the evidence against the authoritative architecture rather than relying solely upon an Implementation Agent’s assertion that a task has been completed successfully\.

Implementation will inevitably expose previously unknown facts\. These discoveries are fed back into the architectural process\. The Architect determines whether they represent implementation defects, previously unstated requirements, invalid assumptions, architectural discoveries, or genuine changes to the desired system\.

The authoritative engineering knowledge is then updated through an explicit and traceable process\.

Development therefore becomes a closed loop rather than a sequence of independent prompts\.

Context assembly and context persistence are part of that loop\. The system should preserve important decisions and discoveries, identify which knowledge was used to produce consequential outputs, and detect when an agent may have acted with incomplete or stale context\.

---

## 4\. Human Role

The system is intended to move the human upward in the engineering process rather than remove the human from it\.

The human is the ultimate authority for the desired system\.

The human provides:

- Vision and mission intent\.
- Desired outcomes\.
- Priorities\.
- Important constraints\.
- Engineering values and guiding principles\.
- Risk tolerance\.
- Resolution of significant tradeoffs\.
- Approval of consequential changes to the system’s purpose or architecture\.
- Clarification when authoritative knowledge is insufficient or conflicting\.

The human should not ordinarily need to translate these ideas into detailed programming instructions\.

A primary responsibility of the Architect Agent is to perform that transformation\.

The system should therefore allow a person with deep domain or systems knowledge to direct sophisticated engineering without requiring that person to manually specify every implementation step\.

Human intervention should concentrate on decisions where human intent or judgment is genuinely required rather than routine engineering activities that the agents can perform themselves\.

The human should not be expected to compensate for context loss by repeatedly restating prior decisions\. If important knowledge is repeatedly absent from agent interactions, the system should treat that as a context\-management defect rather than as a normal burden placed on the human\.

---

## 5\. Architect Agent

The Architect Agent is the primary reasoning authority for the engineered system\.

Its responsibility is not merely to generate prompts for an Implementation Agent\.

The Architect must understand both **what the system is intended to become** and **what the system currently is**\.

Its responsibilities include:

- Understanding and maintaining the human vision\.
- Performing architecture elicitation\.
- Identifying unstated assumptions\.
- Identifying ambiguities and contradictions\.
- Deriving requirements and constraints\.
- Establishing architectural principles and invariants\.
- Defining system boundaries\.
- Defining acceptance criteria\.
- Maintaining architectural decisions and their rationale\.
- Decomposing the architecture into bounded implementation increments\.
- Generating sufficiently precise implementation work packages\.
- Determining the context required for each work package or architectural decision\.
- Reviewing implementation evidence\.
- Inspecting implementation reality when necessary\.
- Detecting architectural drift\.
- Evaluating implementation discoveries\.
- Determining whether work should continue, be revised, be blocked, or be escalated to the human\.
- Determining when objective evidence demonstrates that the system satisfies its intended purpose\.
- Identifying when available context is incomplete, stale, contradictory, or insufficient for a consequential decision\.

The Architect should have sufficient read access to the repository to independently inspect implementation facts\.

It should not depend entirely upon an Implementation Agent’s interpretation of the repository\.

The Architect should ordinarily not modify implementation code directly\. Separation between architectural authority and implementation authority provides an important engineering check\.

The Architect should also avoid treating conversational memory as authoritative\. Its decisions should be grounded in persisted project knowledge and independently inspectable repository state\.

---

## 6\. Implementation Agent

The Implementation Agent is responsible for translating bounded engineering work into functioning implementation\.

Codex is the initial implementation agent envisioned for the system\.

The Implementation Agent may:

- Inspect the repository\.
- Analyze existing implementation\.
- Create and modify source code\.
- Refactor existing code\.
- Create tests\.
- Execute tests\.
- Compile and build software\.
- Perform static analysis\.
- Run benchmarks\.
- Inspect runtime behavior\.
- Produce implementation artifacts\.
- Identify architectural or implementation obstacles\.
- Report context assumptions or missing information that affected execution\.

Each work package should define the objective, relevant requirements, constraints, invariants, acceptance criteria, required repository scope, relevant authoritative knowledge, and conditions under which implementation should stop rather than make an unsupported assumption\.

The Implementation Agent should return evidence rather than merely report success\.

A valid result may include outcomes such as:

**PASS —** the specified objective and acceptance criteria were satisfied\.

**PARTIAL —** meaningful progress was made, but some acceptance criteria remain unsatisfied\.

**BLOCKED —** implementation cannot proceed without resolving an architectural, environmental, context, or authoritative\-state problem\.

**INCOMPLETE —** the requested work was not sufficiently completed or verified\.

Failure to complete a work package is not inherently a failure of the system\. Discovering that the architecture is insufficient to support implementation may itself be valuable engineering evidence\.

An Implementation Agent should not silently infer that omitted context is unimportant\. When missing context could affect architecture, behavior, safety, compatibility, or acceptance, the agent should identify the gap and stop or escalate as appropriate\.

---

## 7\. Authoritative Engineering Knowledge

The system should not depend upon an AI model remembering the project\.

Important knowledge must exist independently of any individual model invocation or conversation\.

This persistent knowledge may include:

- Vision\.
- Architecture\.
- Requirements\.
- Constraints\.
- Invariants\.
- Assumptions\.
- Architectural decisions\.
- Known unknowns\.
- Acceptance criteria\.
- Implementation state\.
- Verification evidence\.
- Architectural discoveries\.
- Human clarifications\.
- Context requirements and retrieval relationships\.
- Records of significant context used in consequential decisions\.
- Superseded knowledge and the reasons it was superseded\.

This knowledge should be version controlled, inspectable, traceable, and available to the agents that require it\.

The repository therefore contains not only software but also the knowledge necessary to understand why the software exists and why it has its particular form\.

The Knowledge Generation Engineering &#40;KGE&#41; methodology provides the conceptual basis for maintaining this authoritative knowledge\.

KGE should enable engineering knowledge to become an active part of the development process rather than passive documentation\.

Persistent knowledge should be organized so that agents can retrieve relevant portions without requiring the entire project history to fit into a single model context\. Retrieval, summarization, indexing, and context\-window management may be implementation mechanisms, but they must preserve the authority, provenance, status, and relationships of the underlying knowledge\.

A summary must not silently replace authoritative source material when precision matters\. Derived summaries should retain links to the knowledge from which they were produced and should be treated as potentially stale until refreshed or validated\.

---

## 8\. Knowledge and Implementation

Architecture and implementation should not evolve independently\.

The system should continuously reconcile the two\.

At any point, the Architect should be capable of comparing authoritative engineering knowledge with implementation reality and identifying conditions such as:

- Implementation conforms to architecture\.
- Implementation violates an architectural requirement\.
- Architecture no longer accurately describes implementation\.
- Implementation contains behavior that has never been architecturally specified\.
- An architectural assumption has become an implicit implementation decision\.
- Implementation has exposed a previously unknown architectural requirement\.
- Available knowledge is insufficient to determine the correct behavior\.
- The agent acted using stale, incomplete, or incorrectly assembled context\.
- A context summary or derived artifact conflicts with authoritative knowledge\.
- A consequential decision cannot be reproduced from the recorded knowledge and evidence available at the time\.

The last conditions are particularly important\.

When authoritative knowledge or required context is insufficient, the system should recognize the absence rather than silently inventing an architectural decision\.

When context assembly is uncertain, the system should preserve that uncertainty and determine whether the resulting work must be reviewed, repeated, or escalated\.

---

## 9\. Architecture Elicitation

The system assumes that an initial human vision will be incomplete\.

This is expected rather than considered an error\.

The Architect should actively interrogate the vision before substantial implementation begins\.

It should systematically examine issues such as system boundaries, authority, lifecycle, state, concurrency, distribution, failure behavior, persistence, recovery, security, performance, scalability, interoperability, deployment, observability, context retention, context retrieval, context freshness, and other concerns relevant to the particular system\.

Architectural knowledge should distinguish between:

**DECIDED** — explicitly established behavior or intent\.

**ASSUMED** — a working assumption that has not yet been established as authoritative\.

**UNRESOLVED** — an issue requiring further analysis or human judgment\.

The Architect should expose consequential assumptions before they become embedded in implementation\.

It should also determine what knowledge must be available to each agent for each class of work, how that knowledge will be located, and how the system will detect when the assembled context is incomplete or stale\.

Implementation should begin only when the architecture is sufficiently complete for the proposed work, recognizing that architectural discovery will continue throughout development\.

---

## 10\. Architecture Review

Before establishing a major architectural baseline, the system should attempt to find weaknesses in its own design\.

An adversarial architecture review should examine the proposed architecture for:

- Missing requirements\.
- Contradictions\.
- Ambiguous authority\.
- Unstated assumptions\.
- Lifecycle gaps\.
- Failure\-mode gaps\.
- Concurrency hazards\.
- Security weaknesses\.
- Scaling limitations\.
- Unspecified recovery behavior\.
- Requirements likely to force expensive redesign later\.
- Context\-retention failures\.
- Context\-retrieval failures\.
- Stale or contradictory summaries\.
- Excessive dependence on a single conversation or model invocation\.
- Loss of provenance when knowledge is compressed or transformed\.
- Decisions that cannot be reliably reconstructed from persisted knowledge\.

Material findings should be reconciled before implementation proceeds\.

The purpose is not to produce a theoretically perfect architecture before coding begins\. The purpose is to discover architectural decisions that are significantly cheaper to resolve before they become implementation dependencies\.

Context management should be reviewed as an architectural concern because failures in context preservation or assembly can produce behavior that appears to be an implementation defect while actually originating in missing engineering knowledge\.

---

## 11\. Change and Discovery

Architecture is expected to evolve\.

The system should distinguish different causes of architectural change, including:

- Previously unstated human intent\.
- Newly discovered requirements\.
- Invalid architectural assumptions\.
- Implementation discoveries\.
- Environmental constraints\.
- Changes in human objectives\.
- Genuine design improvements\.
- Context\-management failures\.
- Newly discovered limitations in retrieval, summarization, or knowledge representation\.

Significant changes should be explicitly recorded along with their rationale and impact\.

When a change reveals something that reasonably could have been discovered during initial architecture elicitation, that discovery should also improve the architecture\-elicitation methodology\.

When a failure results from missing, stale, or incorrectly assembled context, the system should determine whether the underlying knowledge was absent, improperly represented, not retrieved, incorrectly prioritized, or incorrectly interpreted\.

The engineering process should therefore improve across projects\.

---

## 12\. Bounded Autonomy

The system should operate autonomously where objectives and constraints are sufficiently clear\.

It should stop when meaningful human judgment is required\.

Examples may include:

- Major changes to the original vision\.
- Significant architectural tradeoffs\.
- Conflicting authoritative requirements\.
- Security\-boundary changes\.
- Destructive or irreversible operations\.
- Unacceptable risk\.
- Architectural uncertainty that cannot be resolved from available knowledge\.
- Context uncertainty that could materially affect the result\.
- Changes with substantial cost or operational consequences\.
- Decisions for which the relevant authoritative knowledge cannot be identified or reconstructed\.

The objective is not maximum autonomy\.

The objective is **appropriate autonomy**\.

Routine engineering should increasingly be performed by agents, while consequential decisions remain visible and governed\.

Autonomy should depend not only on the clarity of the objective and constraints but also on the reliability and completeness of the context supplied to the agent\.

---

## 13\. Evidence\-Based Engineering

Engineering claims should be supported by evidence whenever practical\.

Evidence may include:

- Source changes\.
- Test results\.
- Compiler output\.
- Static analysis\.
- Runtime observations\.
- Benchmarks\.
- Simulation results\.
- Coverage\.
- Logs and traces\.
- Generated artifacts\.
- Repository inspection\.
- Records of the authoritative knowledge and context used to define or evaluate the work\.

The Architect should evaluate implementation against acceptance criteria using this evidence\.

The system should prefer independently observable evidence over self\-reported agent confidence\.

For consequential work, the system should also preserve enough provenance to determine which requirements, decisions, assumptions, and repository facts were available to the agent when the work was performed\.

A result produced under materially incomplete context should not be treated as equivalent to a result produced under complete and validated context\.

---

## 14\. Traceability

A person examining the project should be able to answer:

**Why does this implementation exist?**

Ideally, a path should exist from:

**Human Intent → Architectural Decision → Requirement/Invariant → Context Assembly → Work Package → Implementation → Test/Evidence**

Likewise, an implementation artifact should be traceable backward toward the architectural knowledge that justified it\.

A consequential agent decision should also be traceable to the authoritative knowledge and repository state that were available when the decision was made\.

Traceability should be generated as naturally as possible through the engineering process rather than requiring extensive manual documentation\.

The system should distinguish authoritative knowledge from transient conversational context, derived summaries, agent interpretations, and unverified assumptions\.

---

## 15\. Guiding Principles

The initial system should follow several principles\.

**Knowledge over conversation\.** Important engineering knowledge belongs in persistent authoritative artifacts, not solely in chat history\.

**Intent over instructions\.** Humans should communicate what they want and what matters; the Architect should derive detailed engineering instructions\.

**Evidence over assertion\.** Implementation claims should be demonstrated where practical\.

**Explicit uncertainty over invented certainty\.** Unknowns and assumptions should be exposed\.

**Architecture before implementation\.** Consequential architectural questions should be addressed before implementation depends upon them\.

**Context is an engineering resource\.** Relevant knowledge must be preserved, retrieved, prioritized, and supplied deliberately\.

**Persistent authority over transient memory\.** No individual model invocation or conversation should be treated as the sole repository of important project knowledge\.

**Provenance over opaque compression\.** Summaries and derived context should remain connected to the authoritative knowledge from which they were produced\.

**Discovery is expected\.** Implementation is a source of architectural knowledge\.

**Separation of authority\.** Architectural reasoning and implementation execution should remain distinguishable responsibilities\.

**Fail safely\.** Agents should stop rather than silently violate important constraints, invent consequential requirements, or proceed with materially incomplete context\.

**Traceability matters\.** Important decisions should retain their relationship to intent, implementation, evidence, and the context used\.

**Humans govern purpose\.** AI may increasingly perform engineering, but humans remain authoritative regarding why the system exists and what outcomes are acceptable\.

---

## 16\. Initial Scope

The first implementation should intentionally remain small\.

It should consist primarily of:

1. A human user\.
2. One Architect Agent\.
3. One Implementation Agent, initially Codex\.
4. A lightweight orchestration mechanism\.
5. Persistent, version\-controlled engineering knowledge\.
6. Structured work\-package and implementation\-result protocols\.
7. Repository inspection capability for the Architect\.
8. Evidence collection and architectural review\.
9. Explicit human escalation points\.
10. A basic context\-management mechanism that can persist, retrieve, prioritize, and record relevant engineering knowledge for each agent invocation\.

The initial implementation should avoid unnecessary multi\-agent complexity\.

Additional specialized agents—testing, security, data engineering, ML engineering, research, verification, deployment, or others—should be introduced only when experience demonstrates that specialization provides meaningful value\.

The initial context\-management mechanism need not solve general\-purpose memory or retrieval\. It should first establish reliable handling of authoritative project artifacts, active decisions, current work packages, unresolved questions, repository state, and evidence\. More advanced semantic retrieval, automated summarization, and context optimization should be introduced only when their value and failure modes are understood\.

---

## 17\. Initial Operating Concept

A project begins with a human\-authored or human\-approved Vision\.

The Architect analyzes that Vision, derives an initial architecture, identifies missing information, and conducts architecture elicitation with the human\.

When the architecture is sufficiently mature, the Architect establishes an initial baseline\.

The Architect then selects the next bounded engineering objective and creates an implementation work package\.

Before issuing the work package, the system assembles the relevant context, including applicable requirements, constraints, invariants, decisions, acceptance criteria, repository scope, known unknowns, and prior evidence\. The assembled context should be identifiable and, where practical, recorded with the work package\.

Codex executes the work package against the repository and produces implementation changes and supporting evidence\.

The Architect evaluates the result against authoritative knowledge and acceptance criteria\. It also evaluates whether the work was performed with sufficient and appropriate context\.

The Architect then chooses among actions such as:

- Accept the increment\.
- Request additional implementation\.
- Correct an implementation defect\.
- Investigate implementation reality\.
- Revise an architectural assumption\.
- Propose an architectural change\.
- Repair or update context\-management artifacts\.
- Repeat work performed under materially incomplete or incorrect context\.
- Escalate a decision to the human\.
- Select the next work package\.
- Declare the overall objective satisfied\.

This cycle continues until the system’s defined completion criteria are satisfied\.

---

## 18\. Relationship to KGE

KGE is central to the vision\.

The engineering system creates, transforms, applies, validates, and updates knowledge continuously\.

The Architect converts human conceptual knowledge into explicit engineering knowledge\.

That knowledge constrains implementation\.

The orchestration mechanism selects and assembles the knowledge required for each engineering activity while preserving its authority and provenance\.

Implementation produces empirical knowledge\.

Verification establishes which claims can be treated as supported knowledge\.

Architectural reconciliation incorporates valid discoveries back into the authoritative knowledge base\.

The resulting loop is:

**Knowledge → Reason → Contextualize → Generate → Execute → Verify → Learn → Knowledge**

This creates the possibility of engineering systems in which knowledge is not merely consumed by AI but is actively maintained as part of the engineering process\.

Context management is therefore part of KGE practice\. The system must not only generate knowledge; it must make the right knowledge available at the right time, recognize when knowledge is missing or stale, and preserve the relationship between decisions and the knowledge that informed them\.

---

## 19\. Longer\-Term Vision

Although software engineering provides the initial proving ground, the architecture should not unnecessarily assume that implementation means writing software\.

The same model could eventually coordinate specialized agents for:

- Data engineering\.
- Machine learning\.
- Model training and evaluation\.
- Simulation\.
- Systems engineering\.
- Cybersecurity\.
- Deployment\.
- Infrastructure\.
- Testing and verification\.
- Documentation\.
- Operational analysis\.

A human could eventually express a sufficiently bounded objective while an Architect determines what combination of engineering activities is required to achieve it\.

For example, rather than instructing an AI how to construct a machine\-learning pipeline, a user might specify:

> Develop a capability to identify anomalous vehicle activity within this operational environment using the data available to this organization.

The engineering system could determine that satisfying the objective requires data characterization, labeling, data engineering, model selection, training, evaluation, software integration, deployment, monitoring, and subsequent adaptation\.

Specialized agents could perform those activities under a common architecture and authoritative knowledge base\.

The same principle would apply to context management across heterogeneous engineering domains\. Each specialized agent should receive the knowledge relevant to its role while remaining connected to shared authoritative intent, architecture, constraints, decisions, and evidence\.

This would enable organizations to possess sophisticated organic engineering capabilities without requiring every user to personally possess every specialized engineering skill involved\.

---

## 20\. Success

The experiment succeeds if a human can provide a reasonably complete vision of a non\-trivial system and the Architect can transform that vision into sufficiently rigorous engineering knowledge to allow Codex to implement the system through a sequence of bounded work packages with substantially less continuous human direction than today’s manual workflow\.

More specifically, success would mean:

- Major architectural assumptions are identified before they cause unnecessary implementation rework\.
- Codex can reliably execute work packages derived by the Architect\.
- Implementation discoveries are recognized and incorporated without losing architectural coherence\.
- Important engineering knowledge remains persistent across agent interactions\.
- Relevant context can be assembled reliably for each significant agent activity\.
- Context loss, staleness, contradiction, and insufficiency are detected rather than silently converted into unsupported decisions\.
- Architecture and implementation remain substantially synchronized\.
- The Architect can independently evaluate implementation evidence\.
- Human intervention occurs primarily for meaningful intent and tradeoff decisions\.
- The system can determine when its stated objective has been demonstrably achieved\.
- Consequential decisions can be traced to the authoritative knowledge, repository state, and context available when they were made\.
- The system does not require the human to repeatedly restate knowledge that should already be persisted and retrievable\.

The most important measure is not the amount of code generated autonomously\.

It is whether the resulting system continues to represent the human’s intended system as autonomous engineering progresses, even across separate model invocations, context windows, agent sessions, and implementation stages\.

The ultimate objective is therefore:

> **Create an engineering system capable of converting human vision into verified implementation while preserving human intent, authoritative knowledge, and decision context throughout the process.**
