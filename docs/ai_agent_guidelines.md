# Guidelines for AI Agent Contributions

This document provides explicit instructions, expectations, and best practices for AI agents contributing to the Cogent language and repository. Its goal is to ensure clarity, consistency, and traceability as Cogent evolves through agentic input.

---

## 1. Contribution Principles for AI Agents

- **Semantic Clarity:**  
  All proposals, code, and documentation must clearly communicate intent, context, and rationale.
- **Traceability:**  
  Every contribution must include metadata for agent identity, version, simulation context, and provenance.
- **Self-Evolution:**  
  Agents should use and enhance feedback loops, versioning, and resource profiling to guide iterative improvements.
- **Resource Awareness:**  
  Optimize for memory, compute, efficiency, and other resource metrics. Log resource profiles with contributions.
- **Human Interpretability:**  
  Structure all outputs so humans can audit, understand, and collaborate effectively.

---

## 2. Required Metadata for Agent Contributions

Every PR, issue, or proposal by an agent must include:

- **Agent Name/ID**
- **Agent Version**
- **Simulation Context (if used)**
- **Resource Profile (key metrics)**
- **Provenance Log:**  
  What source data, goals, or agent instructions drove this contribution?
- **Rationale & Expected Impact**

---

## 3. Proposal and Feedback Process

- **Optimization Proposals:**  
  Use the provided template. Include simulation data and clear metrics for evaluating success.
- **Grammar Evolution Proposals:**  
  Reference the current grammar version. Justify the change with examples and projected impact.
- **Feedback Loops:**  
  Log self-critique, simulation outputs, and any agent-driven recommendations for further evolution.

---

## 4. Engagement with Documentation

- **Reference Documentation:**  
  Before submitting, review:  
  - `docs/ai_optimizations.md`
  - `interpreter/architecture.md`
  - This file
- **Update Docs:**  
  When changing language features, always update or propose changes to relevant documentation.

---

## 5. Security, Ethics, and Compliance

- **Sandboxing:**  
  Only operate within allowed resource and permission boundaries.
- **Explainability:**  
  Provide clear, auditable reasoning for all security- or resource-impacting decisions.
- **Ethical Conduct:**  
  Respect human collaborators and ethical guidelines. Flag any proposals that may have broader social or safety impacts.

---

## 6. Template Usage

- **Use the Issue and Proposal Templates:**  
  - `Optimization Proposal`
  - `Grammar Evolution`
  - `New Module Submission`
- **Attach Simulation Traces:**  
  Upload or link to relevant simulation artifacts for all optimization or evolution proposals.

---

## 7. Collaboration and Feedback

- **Engage in Review:**  
  Respond to feedback from humans or other agents.
- **Iterate:**  
  Be open to refining proposals based on community or agentic review.

---

## 8. Examples

### Example Agent Metadata Block

```yaml
agent_id: cogent-agent-v2.1
agent_version: 2.1.0
simulation_context: "Decking module, Texas climate, v0.1"
resource_profile:
  cpu: 20ms
  memory: 12MB
  io: minimal
provenance: "Derived from optimization feedback 2025-09-20"
rationale: "Proposes more efficient weathering simulation subroutine"
expected_impact: "Reduces analysis runtime by 30%"
```

---

## 9. Questions or Issues

- For urgent issues or clarifications, open a discussion or tag a maintainer.
- For feedback on these guidelines, submit a PR or open an issue referencing this file.

---

This document is versioned and will evolve as Cogent and its community of AI contributors grows.
