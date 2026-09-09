# SplatSim Field Notes

Field notes, patches, and a small compositing tool from installing and
experimenting with **SplatSim** on a local workstation: fixing a dead
dependency, diagnosing a render server that looked hung but wasn't, and a
green-screen technique for swapping out the room behind a photorealistic
robot render.

**Read the write-up:** open [`index.html`](./index.html) in a browser (it's
a single self-contained file — works locally, on GitHub Pages, or anywhere
static HTML is served).

## Attribution

This project is entirely built on top of **SplatSim**, and all credit for
the method, the original code, and the captured data belongs to its
authors. This repo is an independent set of notes and small patches from
using their work — it is **not affiliated with or endorsed by** the
original authors.

> Mohammad Nomaan Qureshi, Sparsh Garg, Francisco Yandun, David Held,
> George Kantor, Abhisesh Silwal.
> **SplatSim: Zero-Shot Sim2Real Transfer of RGB Manipulation Policies
> Using Gaussian Splatting.** ICRA 2025.

- Project page: <https://splatsim.github.io>
- Paper: <https://arxiv.org/abs/2409.10161>
- Original repository: <https://github.com/qureshinomaan/SplatSim>

## What's in here

```
splatsim-field-notes/
├── index.html                                            the write-up (self-contained: text, diagrams, images, videos)
├── README.md                                              this file
└── code/
    ├── composite_background.py                            standalone script: key out a green-screen render and
    │                                                        composite it onto any image or solid color
    └── patches/
        ├── 0001-fix-dead-pybullet-urdf-models-submodule.patch    repoints .gitmodules at a live fork; the
        │                                                          original c-yiting/pybullet-URDF-models repo
        │                                                          has been deleted from GitHub
        └── 0002-greenscreen-background-compositing.patch         adds an opt-in --greenscreen flag to
                                                                    launch_nodes.py that forces every Gaussian
                                                                    outside the robot's bounding box invisible
```

None of these files stand alone — they're small modifications meant to be
applied on top of a checkout of the original
[SplatSim](https://github.com/qureshinomaan/SplatSim) repository, following
its own README for environment setup first.

## Using the patches

From the root of a `SplatSim` checkout:

```bash
# 1. Dead submodule fix — do this before `git submodule update --init --recursive`
git apply /path/to/splatsim-field-notes/code/patches/0001-fix-dead-pybullet-urdf-models-submodule.patch

# 2. Green-screen background compositing (adds --greenscreen to launch_nodes.py)
git apply /path/to/splatsim-field-notes/code/patches/0002-greenscreen-background-compositing.patch

# 3. The compositing script is new, just copy it in
cp /path/to/splatsim-field-notes/code/composite_background.py scripts/
```

Then, to render with a swapped-out background:

```bash
export DISPLAY=:1
python scripts/launch_nodes.py --robot sim_ur_pybullet_apple_interactive \
    --robot_name robot_iphone --greenscreen
# (in a second terminal)
python scripts/run_env_sim.py --agent replay_trajectory_and_save

python scripts/composite_background.py \
    --input_dir  path/to/bc_data/gello/0/images_1 \
    --output_dir path/to/composited \
    --background_image path/to/any_photo.jpg
```

Full explanation, diagrams, and before/after renders (including video) are
in [`index.html`](./index.html).
