# Temporal Delay Neural Network (TDNN)

A biologically-inspired **time-delay neural network** for temporal pattern and speech
recognition. The model learns the *transmission delays* between spiking units — not just
synaptic weights — so that information arriving along different paths can be aligned in
time and integrated at a downstream neuron. This makes the network naturally suited to
problems where the **temporal structure of a signal** carries the information, such as
phoneme and consonant recognition from spectrograms.

Presented as a poster at the **New York Academy of Sciences (NYAS), 2016**
([`NYAS-2016-POSTER.pdf`](NYAS-2016-POSTER.pdf)).

## Idea

Classic artificial neurons sum weighted inputs instantaneously. Real axons impose
**conduction delays**, and a growing body of work (gamma models, polychronization,
delay-tuned coincidence detection) shows that *learnable delays* are a powerful
computational primitive for temporal coding.

This project implements a feed-forward network of integrate-and-fire neurons in which each
connection carries a **learnable delay distribution**. Three families of delay functions are
implemented and compared:

- **Masquelier** — fixed delay lines (baseline)
- **Single-Beta** — one beta-distributed delay kernel per connection
- **Beta-Mixture** — a mixture of beta kernels, allowing multi-modal delay tuning

Delays and thresholds adapt online as patterns are presented, so the network learns to fire
selectively for the *temporal signature* of a class (e.g. a particular consonant) rather than
its instantaneous amplitude.

## What's here

| Path | Contents |
|------|----------|
| `py/` | Core Python implementation — networks, neurons, delay functions, update rules, and simulation drivers |
| `py/Networks/` | Feed-forward network construction |
| `py/Neurons/` | Input, integrate-and-fire, and base neuron models |
| `py/DelayFunctions/` | Masquelier / single-beta / beta-mixture delay kernels + their update rules |
| `py/Updates/` | Online threshold and variable adaptation |
| `py/simulation_script_*.py` | Reproducible experiment drivers (consonants, simple images, long streams, with/without noise) |
| `network-3.0/` | A cleaner, pickled rewrite of the core engine |
| `matlab/` | Stimulus generation and analysis — spectrograms, beta-mixture fitting, weight/potential visualization (`generateStream*.m`, `myspectrogram.m`, `calc_*`, `graphics_*`) |
| `figures/` | Result figures — training/test weight and membrane-potential meshes, per-stimulus responses across SNR levels |

## Method, briefly

1. **Stimuli** — speech tokens (consonants) and simple visual patterns are converted to
   time–frequency representations (`myspectrogram.m`) and streamed to the network as
   per-channel spike trains.
2. **Encoding** — input neurons emit spikes; each connection delays them according to its
   current delay kernel.
3. **Learning** — coincidence at a target neuron reinforces the contributing delays
   (delay/weight update rules in `DelayFunctions/` and `Updates/`); thresholds adapt to
   keep firing selective.
4. **Evaluation** — the network is tested across delay-function families, delay ranges
   (e.g. 250–300 ms), distribution counts, and signal-to-noise ratios; figures report
   train-vs-test separability of the learned delay/weight structure.

## Running

The Python simulations are driven by the `simulation_script_*.py` files; set the project
path and dataset/category at the top of a script and run it. The MATLAB side generates the
stimulus streams and the analysis figures. (Note: the large generated datasets and raw
simulation outputs are not committed — regenerate them with the `generateStream*.m` /
`buildDataSet*.m` scripts and the simulation drivers.)

## Background

The design draws on gamma networks for automatic speech recognition, spike-timing-dependent
plasticity, Izhikevich spiking-neuron dynamics, and delay-learning models (Masquelier;
Legenstein, Naeger & Maass). See the NYAS poster for the consolidated references and results.

---

*Author: Shady El Damaty. Research project on temporal coding and delay learning for
speech / temporal pattern recognition.*
