# Fable Mode

We ran a double-blind trial to test if an artificial constraint could fix AI writing, and the result surprised me. When you apply these rules to an autonomous agent team, output drops by 96.7 percent while technical depth actually increases.

We tested a five-agent team building a local-first medical sync engine (EHR-LocalSync). Without the skill, the team generated 30,841 words. With the skill, they generated 1,000 words. They skipped the UI padding and marketing fluff to make concrete decisions about Shamir's Secret Sharing and offline CRDT conflict resolution.

Fable Mode operates as a token compression engine. It forces the model to answer from the brief instead of the genre.

## The trial

We ran three phases.

Phase 1 tested independent agents building a generic database tool called SyncLite. Default agents wrote generic features and used words like leverage and seamless. Fable agents identified concrete risks instead. They pointed out that iOS sandboxing breaks dynamic library loading for a C extension, a detail the default agents missed completely.

For Phase 2, we pitched five independent Fable agents against a collaborative team of default agents. The team won on technical depth but failed on verbosity. Each independent agent redundantly planned the entire system. The team divided the labor but filled the gaps with corporate padding.

The final trial gave the collaborative team the Fable rules, and because they were no longer trying to perform their roles for a generic audience, the output collapsed into a tight technical specification. The Tech Lead surfaced the single assumption that invalidated the effort (HIPAA auditors demanding cleartext logs) and the frontend agent built a javascript-free HTML terminal.

## How it works

Most prompts ask a model to write a specific document type. A project plan triggers a template with risk matrices and phases. A landing page triggers hero sections and testimonials.

Fable breaks the template. It asks the agent to find the hard part first. It demands decisions instead of balanced options. It bans invented facts, and it forces the output to serve the reader's immediate next step.

When a model stops trying to fill out a genre template, the API cost plummets because you stop paying for the ceremony and start paying only for the reasoning.

## Usage

Copy the rules into your agent's system prompt or place them in a readable file in the workspace. Provide clear roles if you run multiple agents.
