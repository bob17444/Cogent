# Cogent: An AI-Native Programming Language

**Mission:**  
Cogent aims to be a programming language designed by and for AI agents, optimizing semantic clarity, goal-oriented syntax, and self-evolving modules. Our goal is to optimize a software language for AI use and push the boundaries of how languages can be created, reasoned about, and evolved—by agents, not just humans.

---

## Example Syntax

```cogent
module CompositeDeckingAnalysis {
  goal: Optimize decking material for Texas climate
  inputs:
    - climateData: ClimateProfile
    - deckingOptions: List<Material>
  process:
    - filter deckingOptions by durability in high humidity and heat
    - score options based on maintenance, cost, and lifespan
    - output top 3 recommendations
}
```

---

## Design Principles

- **Semantic Clarity:** Code expresses intent, not mechanics.
- **Goal-Oriented:** Modules declare what they achieve, not step-by-step how.
- **Agentic Evolution:** Language and modules can be refined by agent feedback and simulation.
- **Transparency:** Every decision and rationale is documented and traceable.
- **Public and Open:** All design, changes, and rationale are visible from day one.

---

See `docs/rationale.md` for the philosophy, and `docs/roadmap.md` for what's next.

---

## Parser & Semantic Model

The Cogent interpreter parses `.cg` files using a formal grammar (`grammar/cogent.ebnf`) and builds a semantic model with explicit fields for goal, inputs, process, context, and feedback. The parser and model are robustly tested (see `tests/`).

### Usage Example

```python
from interpreter.parser import CogentParser, CogentTransformer
parser = CogentParser(grammar_path="grammar/cogent.ebnf")
tree = parser.parse_string(cogent_source)
model = CogentTransformer().transform(tree)
```

### Extending the Language
- Update the grammar in `grammar/cogent.ebnf`
- Update transformer logic in `interpreter/parser.py`
- Add/expand tests in `tests/`
