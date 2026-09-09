# Can a world model generate synthetic training episodes for a real pick-and-place task?

A Kinova Jaco2 arm with a spoon taped to its gripper scoops pasta from a container and transfers it to a plate. We have 37 real recorded episodes of this. The goal: use NVIDIA's Cosmos3 world model to generate *more* synthetic episodes — either to train a diffusion/ACT policy directly, or to stress-test whether video world models are a viable synthetic-data source for real robot manipulation at all.

**[Read the full writeup with embedded videos →](index.html)** (or open `index.html` locally / via GitHub Pages)

## TL;DR

- Action-conditioned generation (feed the model an exact 6-DoF trajectory) works well for short clips (~1s) but **degrades badly when chained into longer rollouts** — quality collapses into artifact noise within ~10 seconds, and giving the model *more* self-generated context to condition on made this **worse**, not better.
- **Text-prompt-only generation** (one real photo + one sentence describing the task, no trajectory at all) was the strongest result: a single ~30-second call produced a coherent clip where the arm correctly scoops pasta and drops it in the plate — no chaining, no drift.
- That generated video was **relabeled end-to-end** with Depth Anything (metric depth) + FoundationPose (6-DoF tracking) — closing the loop from "photo + sentence" to "validated action labels" with no ground truth in between.
- Found and fixed a real bug in our own label-extraction pipeline along the way: FoundationPose's periodic re-registration was silently producing physically-impossible 58cm phantom jumps in 35+ of 37 real episodes, at predictable frame boundaries.

## Repo layout

```
writeup/
├── index.html            the full writeup, with every video embedded inline
├── assets/
│   ├── videos/            8 generated clips referenced in the writeup (~2.7MB total)
│   └── images/            comparison stills + video poster frames
└── code/                  every script written during this project, with notes
    └── README.md          what each script does and why
```

## Environment (for reproducing)

- [NVIDIA Cosmos3](https://github.com/NVIDIA/Cosmos) / [cosmos-framework](https://github.com/NVIDIA/cosmos-framework), `Cosmos3-Edge` (4B) checkpoint
- [FoundationPose](https://github.com/NVlabs/FoundationPose) for 6-DoF tool tracking
- [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) (metric, indoor) for monocular depth
- Both run in separate Docker containers on a single machine with 2× RTX A6000; see `code/README.md` for the specific host-compatibility fixes this required.

## License / attribution

Code here is provided as-is, adapted from the above upstream projects (each under its own license — see the respective repos). No claim of novelty on the underlying models; this is an applied experiment log.
