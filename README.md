# Fable Mode

This skill makes autonomous agents reason from the brief and write less. We ran a 25-agent trial to measure how constraints change output. The result was a 96.7 percent drop in output words, alongside a massive increase in technical depth.

## 96.7% drop in output words (Massive efficiency gains)

We tested three different agent structures on a highly difficult, specialized engineering task: building a HIPAA-compliant clinical sync system called EHR-LocalSync. We tracked the total word count produced by each team.

| Metric | Phase 2: Default Collaborative Team | Phase 3: Fable Collaborative Team |
| :--- | :---: | :---: |
| **Total Input Words** | 3,400 | ~750 |
| **Total Output Words** | 30,841 | **~1,000** |

The collaborative team running the Fable rules delivered a structurally superior technical architecture while consuming a fraction of the API costs. They stopped answering from the genre. They skipped the SaaS marketing filler and inter-agent padding to focus entirely on the core decisions.

## Phase 1: The Marketing and Coding Task

We first tested five independent Fable agents against five default agents. Their task was to build a launch strategy and code a landing page for SyncLite, a generic database tool. We evaluated them across four dimensions.

| Dimension | Default Mode Agents | Fable Mode Agents |
| :--- | :--- | :--- |
| **Locating the Hard Part** | Failed. Treated all sections with equal weight. | Succeeded. Identified that developers distrust sync tools as heavy black boxes. |
| **Making the Call** | Avoided. Presented generic features. | Made the Call. Committed to WAL tailing and compiling a 120KB C extension. |
| **Technical Specificity** | Superficial. Identified generic database failures. | Deep and Checkable. Identified that iOS sandboxing restricts dynamic library loading. |
| **Copywriting** | Boilerplate. Repeatedly used words like seamless and leverage. | Authentic. Used active verbs and set explicit limits for the tool. |

We also tracked the average token consumption per agent during this first phase.

| Metric | Default Mode | Fable Mode | Change | Expected Price / Agent | Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Input Word Count** | 1,003 | 3,439 | +242% | $0.004 → $0.014 | Increase is due to the skill context |
| **Output Word Count** | 7,557 | 5,871 | -22% | $0.151 → $0.117 | |

The Fable system prompt is large, so input tokens rose. But the output dropped by 22 percent because the agents stopped generating boilerplate. Since output tokens cost significantly more than input tokens, the net result was a 13.8 percent reduction in total API costs per agent.

Fable Mode acts as a constraint engine. It forces the model to invent a concrete technical reality and write with authentic specificity.

## Phase 2: High-Complexity Engineering

In the second phase, we tested if independent Fable agents could outpace a multi-agent orchestrated team on the EHR-LocalSync task.

The Default Collaborative Team divided the problem domain. The Security Architect designed a Zero-Knowledge key distribution model using X25519 KEM. The Sync Engineer designed decoupled LWW-Register CRDTs. The Tech Lead merged the specifications. They won on technical depth, because the independent Fable agents were bottlenecked by the sheer breadth of building the entire system alone.

However, the Default Team produced 30,841 words of output. They divided the labor, and then they filled the gaps with corporate padding.

## Phase 3: The Ultimate Architecture

For the final phase, we equipped the five-member Collaborative Team with the Fable Mode rulebook.

The Tech Lead delivered a tight 1,000-word master document. The team made immediate, load-bearing decisions like using Shamir's Secret Sharing for key availability, and they surfaced the single assumption that ruined the effort: HIPAA auditors demanding cleartext logs. They avoided front-end boilerplate completely. The frontend agent coded a stark, javascript-free HTML terminal.

## The Verdict

For individual agents, Fable Mode is a strict upgrade that forces technical integrity.

For complex projects, a Collaborative Team of specialized agents easily beats independent reasoning.

The optimal setup combines both. When you deploy a Collaborative Team where each specialist runs Fable Mode constraints, you get deep reasoning and perfect token compression.

## Usage

Copy the rules from `SKILL.md` into your agent's system prompt or place them in a readable file in the workspace. Provide clear roles if you run multiple agents.
