# ML Paper Writing Philosophy & Best Practices

This reference collects optional writing heuristics. Use the sections that help the current draft; preserve the author's structure and terminology where they work. Formulas, page allocations, and checklists below are examples, not venue requirements. Verify any attributed quotation or venue rule against its source before quoting it externally.

---

## Contents

- [The Narrative Principle](#the-narrative-principle)
- [Time Allocation](#time-allocation)
- [Abstract Writing Formula](#abstract-writing-formula)
- [Introduction Structure](#introduction-structure)
- [Sentence-Level Clarity](#sentence-level-clarity)
- [Word Choice and Precision](#word-choice-and-precision)
- [Mathematical Writing](#mathematical-writing)
- [Figure Design](#figure-design)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

## The Narrative Principle

### From Neel Nanda

"A paper is a short, rigorous, evidence-based technical story with a takeaway readers care about."

The narrative rests on three pillars that must be crystal clear by the end of your introduction:

**The "What"**: One to three specific novel claims fitting within a cohesive theme. Vague contributions like "we study X" fail immediately—reviewers need precise, falsifiable claims.

**The "Why"**: Rigorous empirical evidence that convincingly supports those claims, including strong baselines honestly tuned and experiments that distinguish between competing hypotheses rather than merely showing "decent results."

**The "So What"**: Why readers should care, connecting your contribution to problems the community recognizes as important.

### From Andrej Karpathy

"A paper is not a random collection of experiments you report on. The paper sells a single thing that was not obvious or present before. The entire paper is organized around this core contribution with surgical precision."

This applies whether you're presenting a new architecture, a theoretical result, or improved understanding of existing methods—NeurIPS explicitly notes that "originality does not necessarily require an entirely new method."

**Practical Implication**: If you cannot state your contribution in one sentence, you don't yet have a paper. Everything else—experiments, related work, discussion—exists only to support that core claim.

---

## Time Allocation

### From Neel Nanda

Spend approximately **the same amount of time** on each of:
1. The abstract
2. The introduction
3. The figures
4. Everything else combined

This isn't hyperbole—most reviewers form preliminary judgments before reaching your methods section. Readers encounter your paper in a predictable pattern: **title → abstract → introduction → figures → maybe the rest.**

### Reviewer Reading Patterns

Readers may begin with the abstract, introduction, and figures. Make the contribution and supporting evidence understandable in those places without assuming a fixed reading order.

---

## Abstract Writing Formula

### Sebastian Farquhar's 5-Sentence Formula

1. **What you achieved**: "We introduce...", "We prove...", "We demonstrate..."
2. **Why this is hard and important**
3. **How you do it** (with specialist keywords for discoverability)
4. **What evidence you have**
5. **Your most remarkable number/result**

### Example (Good Abstract)

```
We prove that gradient descent on overparameterized neural networks
converges to global minima at a linear rate. [What]
This resolves a fundamental question about why deep learning works
despite non-convex optimization landscapes. [Why hard/important]
Our proof relies on showing that the Neural Tangent Kernel remains
approximately constant during training, reducing the problem to
kernel regression. [How with keywords]
We validate our theory on CIFAR-10 and ImageNet, showing that
predicted convergence rates match experiments within 5%. [Evidence]
This is the first polynomial-time convergence guarantee for
networks with practical depth and width. [Remarkable result]
```

### What to Avoid

From Zachary Lipton: "If the first sentence can be pre-pended to any ML paper, delete it."

**Delete these openings**:
- "Large language models have achieved remarkable success..."
- "Deep learning has revolutionized..."
- "In recent years, neural networks have..."

**Start with your specific contribution instead.**

---

## Introduction Structure

### Possible Starting Structure

For a short two-column paper, a concise introduction and a few specific contribution statements can help. Adapt their length, position, and use of bullets to the actual paper and venue.

### Structure Template

```markdown
1. Opening Hook (2-3 sentences)
   - State the problem your paper addresses
   - Why it matters RIGHT NOW

2. Background/Challenge (1 paragraph)
   - What makes this problem hard?
   - What have others tried? Why is it insufficient?

3. Your Approach (1 paragraph)
   - What do you do differently?
   - Key insight that enables your contribution

4. Contribution Bullets (2-4 items)
   - Be specific and falsifiable
   - Each bullet: 1-2 lines maximum

5. Results Preview (2-3 sentences)
   - Most impressive numbers
   - Scope of evaluation

6. Paper Organization (optional, 1-2 sentences)
   - "Section 2 presents... Section 3 describes..."
```

### Contribution Bullets: Good vs Bad

**Good:**
- We prove that X converges in O(n log n) time under assumption Y
- We introduce Z, a 3-layer architecture that reduces memory by 40%
- We demonstrate that A outperforms B by 15% on benchmark C

**Bad:**
- We study the problem of X (not a contribution)
- We provide extensive experiments (too vague)
- We make several contributions to the field (says nothing)

---

## Sentence-Level Clarity

### From Gopen & Swan: "The Science of Scientific Writing"

The seminal 1990 paper by George Gopen and Judith Swan establishes that **readers have structural expectations** about where information appears in prose. Violating these expectations forces readers to spend energy on structure rather than content.

> "If the reader is to grasp what the writer means, the writer must understand what the reader needs."

#### The 7 Principles of Reader Expectations

**Principle 1: Subject-Verb Proximity**

Keep grammatical subject and verb close together. Anything intervening reads as interruption of lesser importance.

**Weak**: "The model, which was trained on 100M tokens and fine-tuned on domain-specific data using LoRA with rank 16, achieves state-of-the-art results"

**Strong**: "The model achieves state-of-the-art results after training on 100M tokens and fine-tuning with LoRA (rank 16)"

**Principle 2: Stress Position (Save the Best for Last)**

Readers naturally emphasize the **last words of a sentence**. Place your most important information there.

**Weak**: "Accuracy improves by 15% when using attention"
**Strong**: "When using attention, accuracy improves by **15%**"

**Principle 3: Topic Position (First Things First)**

The beginning of a sentence establishes perspective. Put the "whose story" element first—readers expect the sentence to be about whoever shows up first.

**Weak**: "A novel attention mechanism that computes alignment scores is introduced"
**Strong**: "To address the alignment problem, we introduce a novel attention mechanism"

**Principle 4: Old Information Before New**

Put familiar information (old) in the topic position for backward linkage; put new information in the stress position for emphasis.

**Weak**: "Sparse attention was introduced by Child et al. The quadratic complexity of standard attention motivates this work."
**Strong**: "Standard attention has quadratic complexity. To address this, Child et al. introduced sparse attention."

**Principle 5: One Unit, One Function**

Each unit of discourse (sentence, paragraph, section) should serve a single function. If you have two points, use two units.

**Principle 6: Articulate Action in the Verb**

Express the action of each sentence in its verb, not in nominalized nouns.

**Weak**: "We performed an analysis of the results" (nominalization)
**Strong**: "We analyzed the results" (action in verb)

**Principle 7: Context Before New Information**

Provide context before asking the reader to consider anything new. This applies at all levels—sentence, paragraph, section.

**Weak**: "Equation 3 shows that convergence is guaranteed when the learning rate satisfies..."
**Strong**: "For convergence to be guaranteed, the learning rate must satisfy the condition in Equation 3..."

#### Summary Table

| Principle | Rule | Mnemonic |
|-----------|------|----------|
| Subject-Verb Proximity | Keep subject and verb close | "Don't interrupt yourself" |
| Stress Position | Emphasis at sentence end | "Save the best for last" |
| Topic Position | Context at sentence start | "First things first" |
| Old Before New | Familiar → unfamiliar | "Build on known ground" |
| One Unit, One Function | Each paragraph = one point | "One idea per container" |
| Action in Verb | Use verbs, not nominalizations | "Verbs do, nouns sit" |
| Context Before New | Explain before presenting | "Set the stage first" |

---

---

## Micro-Level Writing Tips

### From Ethan Perez (Anthropic)

These practical micro-level tips improve clarity at the sentence and word level.

#### Pronoun Management

**Minimize pronouns** ("this," "it," "these," "that"). When pronouns are necessary, use them as adjectives with a noun:

**Weak**: "This shows that the model converges."
**Strong**: "This result shows that the model converges."

**Weak**: "It improves performance."
**Strong**: "This modification improves performance."

#### Verb Placement

**Position verbs early** in sentences for better parsing:

**Weak**: "The gradient, after being computed and normalized, updates the weights."
**Strong**: "The gradient updates the weights after being computed and normalized."

#### Apostrophe Unfolding

Transform possessive constructions for clarity:

**Original**: "X's Y" → **Unfolded**: "The Y of X"

**Before**: "The model's accuracy on the test set"
**After**: "The accuracy of the model on the test set"

This isn't always better, but when sentences feel awkward, try unfolding.

#### Words to Eliminate

Delete these filler words in almost all cases:
- "actually"
- "a bit"
- "fortunately" / "unfortunately"
- "very" / "really"
- "quite"
- "basically"
- "essentially"
- Excessive connectives ("however," "moreover," "furthermore" when not needed)

#### Sentence Construction Rules

1. **One idea per sentence** - If struggling to express an idea in one sentence, it needs two
2. **No repeated sounds** - Avoid similar-sounding words in the same sentence
3. **Every sentence adds information** - Delete sentences that merely restate
4. **Prefer clear agency** - Use active voice when the actor matters; passive voice can suit a method or result whose actor is irrelevant
5. **Expand contractions** - "don't" → "do not" for formality

#### Paragraph Architecture

- **First sentence**: State the point clearly
- **Middle sentences**: Support with evidence
- **Last sentence**: Reinforce or transition

Don't bury key information in the middle of paragraphs.

---

## Word Choice and Precision

### From Zachary Lipton

**Eliminate hedging** unless genuine uncertainty exists:
- Delete "may" and "can" unless necessary
- "provides *very* tight approximation" drips with insecurity
- "provides tight approximation" is confident

**Avoid vacuous intensifiers**:
- Delete: very, extremely, highly, significantly (unless statistical)
- These words signal insecurity, not strength

### From Jacob Steinhardt

**Precision over brevity**: Replace vague terms with specific ones.

| Vague | Specific |
|-------|----------|
| performance | accuracy, latency, throughput |
| improves | increases accuracy by X%, reduces latency by Y |
| large | 1B parameters, 100M tokens |
| fast | 3x faster, 50ms latency |
| good results | 92% accuracy, 0.85 F1 |

**Consistent terminology**: Referring to the same concept with different terms creates confusion.

**Choose one and stick with it**:
- "model" vs "network" vs "architecture"
- "training" vs "learning" vs "optimization"
- "sample" vs "example" vs "instance"

### Describe the Actual Contribution

Use verbs that accurately describe the work, including “combine,” “modify,” or “extend” when appropriate. Explain what is new with evidence; do not rename incremental work to imply stronger novelty.

---

## Mathematical Writing

### From Ethan Perez

**Unfold apostrophes** for clarity:
- Weak: "X's Y"
- Strong: "The Y of X"

Example: "the model's accuracy" → "the accuracy of the model"

### General Principles

1. **State all assumptions formally** before theorems
2. **Provide intuitive explanations** alongside proofs
3. **Use consistent notation** throughout the paper
4. **Define symbols at first use**

### Notation Conventions

```latex
% Scalars: lowercase italic
$x$, $y$, $\alpha$, $\beta$

% Vectors: lowercase bold
$\mathbf{x}$, $\mathbf{v}$

% Matrices: uppercase bold
$\mathbf{W}$, $\mathbf{X}$

% Sets: uppercase calligraphic
$\mathcal{X}$, $\mathcal{D}$

% Functions: roman for named functions
$\mathrm{softmax}$, $\mathrm{ReLU}$
```

---

## Figure Design

### From Neel Nanda

Figures should tell a coherent story even if the reader skips the text. Many readers DO skip the text initially.

### Design Principles

1. **Figure 1 is crucial**: Often the first thing readers examine after abstract
2. **Self-contained captions**: Reader should understand figure without main text
3. **Avoid redundant titles**: Use the caption when it supplies the same information; follow the actual venue instructions
4. **Export for the destination**: Prefer vector text/line art; choose raster resolution from final size and the target's requirements

### Accessibility Requirements

Make distinctions readable without relying on color alone; a named palette does not guarantee accessibility.

**Solutions**:
- Use colorblind-safe palettes: Okabe-Ito or Paul Tol
- Avoid red-green combinations
- Verify figures work in grayscale
- Use different line styles (solid, dashed, dotted) in addition to colors

### Tools

```python
import matplotlib.pyplot as plt

# Start with an installed style; tune for the target and inspect the output.
with plt.style.context("default"):
    fig, ax = plt.subplots(layout="constrained")
```

---

## Common Mistakes to Avoid

### Structure Mistakes

| Mistake | Solution |
|---------|----------|
| Introduction too long (>1.5 pages) | Move background to Related Work |
| Methods buried (after page 3) | Front-load contribution, cut intro |
| Missing contribution bullets | Add 2-4 specific, falsifiable claims |
| Experiments without explicit claims | State what each experiment tests |

### Writing Mistakes

| Mistake | Solution |
|---------|----------|
| Generic abstract opening | Start with your specific contribution |
| Inconsistent terminology | Choose one term per concept |
| Passive voice overuse | Use active voice: "We show" not "It is shown" |
| Hedging everywhere | Be confident unless genuinely uncertain |

### Figure Mistakes

| Mistake | Solution |
|---------|----------|
| Raster graphics for plots | Use vector (PDF/EPS) |
| Red-green color scheme | Use colorblind-safe palette |
| Title inside figure | Put title in caption |
| Captions require main text | Make captions self-contained |

### Citation Mistakes

| Mistake | Solution |
|---------|----------|
| Paper-by-paper Related Work | Organize methodologically |
| Missing relevant citations | Cite sources that support claims and identify the closest prior work |
| Unverified citations | Check the authoritative record and relevant source text |
| Inconsistent citation format | Preserve the template's bibliography system and existing keys |

---

## Pre-Submission Checklist

For a full-paper review, use the applicable prompts below; this is not required for a local edit:

**Narrative**:
- [ ] Can state contribution in one sentence
- [ ] Three pillars (What/Why/So What) clear in intro
- [ ] Every experiment supports a specific claim

**Structure**:
- [ ] Abstract states the contribution, approach, and supported result
- [ ] Introduction length and structure fit the paper
- [ ] Specific contributions and supporting methods are easy to find
- [ ] Limitations section present

**Writing**:
- [ ] Consistent terminology throughout
- [ ] No generic opening sentences
- [ ] Hedging removed unless necessary
- [ ] All figures have self-contained captions

**Technical**:
- [ ] Bibliographic records and cited claims verified against sources
- [ ] Suitable uncertainty reported with methodology where applicable
- [ ] Compute resources documented
- [ ] Code/data availability stated
