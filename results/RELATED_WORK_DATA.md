# Accuracy and size comparison data

Selected primary-source results checked November 15, 2026. External results are source-reported, not independently reproduced. The plot uses official-test scores only; our historical development scores are separate.

| Work | Reported size | Test accuracy | Byte accounting |
| --- | ---: | ---: | --- |
| [MNIST Golf](../results/official-test-result.json) | 993 B | 99.25% | Code + model data |
| [MIRACLE](https://arxiv.org/pdf/1810.00440) | 1.52 kB | 99.04% | Model/weight payload |
| [MIRACLE](https://arxiv.org/pdf/1810.00440) | 3.03 kB | 99.31% | Model/weight payload |
| [Scaling Discovery](https://arxiv.org/html/2609.21032v1) | 1,957 B | 99.41% | Code + model data |
| [tiny_MNIST reproduction](https://arxiv.org/html/2609.21032v1) | 2,461 B | 99.40% | Code + model data |
| [Kilobyte Models](https://arxiv.org/html/2608.00860v1) | 524 B | 96.41% | Model/weight payload |
| [Kilobyte Models](https://arxiv.org/html/2608.00860v1) | 1,036 B | 97.94% | Model/weight payload |
| [Kilobyte Models](https://arxiv.org/html/2608.00860v1) | 2,060 B | 98.60% | Model/weight payload |
| [ATtiny85 RNN](https://www.reddit.com/r/computervision/comments/1rk4va4/computer_vision_in_512_bytes/) | 472 B | 95.10% | Model/weight payload |
| [BitNetPDK](https://cpldcpu.github.io/2024/05/02/machine-learning-mnist-inference-on-the-3-cent-microcontroller/) | 3,392 bits | 90.07% | Model/weight payload |
| [Deep Compression](https://arxiv.org/pdf/1510.00149) | 44 KB | 99.26% | Model/weight payload |

The figure shows only results with accuracy **>96%** and reported size **≤3,000 bytes**: seven of the eleven rows. MIRACLE’s 3.03 kB configuration, ATtiny85 RNN, BitNetPDK and Deep Compression remain in this full source table.

The figure uses one graph with linear axes: 0–3,000 bytes and 96–100% accuracy. The label **“Seed + learned code”** refers to Sahil Rajesh Dhayalkar’s *Kilobyte Models: Neural Networks as a Seed and a Quantized Latent*, represented by the three CNN2 configurations below.

## Notes

**MNIST Golf (993 B):** One frozen artifact, one official-test evaluation; Python/PyTorch excluded.

**MIRACLE (1.52 kB):** Table 1: 0.96% test error; rounded kB size, plotted using 1 kB = 1000 bytes.

**MIRACLE (3.03 kB):** Table 1: 0.69% test error; rounded kB size, plotted using 1 kB = 1000 bytes.

**Scaling Discovery (1,957 B):** Sections 3.3.2 and A.5; gzipped tar submission including code; runtime excluded.

**tiny_MNIST reproduction (2,461 B):** Reproduction by the Scaling Discovery authors, not an upstream artifact-size claim; same tar/gzip contract.

**Kilobyte Models (524 B):** Tables 2–3: CNN2, SLVT, d=1024, int4 QAT. Seed/latent/scale payload; inference and regeneration code excluded. These are the three 4-bit SLVT CNN2 budgets, not every configuration in the paper.

**Kilobyte Models (1,036 B):** Tables 2–3: CNN2, SLVT, d=2048, int4 QAT. Seed/latent/scale payload; inference and regeneration code excluded. These are the three 4-bit SLVT CNN2 budgets, not every configuration in the paper.

**Kilobyte Models (2,060 B):** Tables 2–3: CNN2, SLVT, d=4096, int4 QAT. Seed/latent/scale payload; inference and regeneration code excluded. These are the three 4-bit SLVT CNN2 budgets, not every configuration in the paper.

**ATtiny85 RNN (472 B):** Author reports 472 int8 parameters and 95.10% test accuracy. Firmware/library excluded. Code: https://github.com/GiorgosXou/ATTiny85-MNIST-RNN-EEPROM

**BitNetPDK (3,392 bits):** Weight payload: 3392/8 = 424 bytes. Inputs downsampled to 8×8; firmware excluded.

**Deep Compression (44 KB):** Original paper Table 1: 0.74% test error. Use this primary result, rather than the rounded 0.8% error quoted in MIRACLE. Rounded KB plotted using 1000 bytes.

Exact byte or bit figures retained. Rounded kB/KB figures plotted at 1000 bytes per kB; these positions are approximate, not exact file measurements.

## Results without comparable coordinates

- **Rohrer leaderboard:** 1,398 parameters, 99% category; no verified deployed-byte size.
- **Grimov minimal model:** 1,936 parameters, 99.1%; no verified deployed-byte size.
- **Weightless:** Reported byte sizes concern selected layers; no verified complete-model size for this comparison.
- **PAC-Bayes subspace compression:** 0.38 KB reported, but a matching measured test accuracy for that encoding has not been established here; generalization bounds are not test accuracy.
- **Bayesian Compression:** Primary paper gives compression ratios; 2.3 kB comes from a later comparison. Omitted pending consistent primary-source absolute-size accounting.

## Prior reported frontier

The faint line excludes MNIST Golf. A prior point is on this plotted frontier when no other included prior point is both no larger and at least as accurate, with at least one strict improvement. The connected points are 524 B / 96.41%, 1,036 B / 97.94%, approximately 1,520 B / 99.04%, and 1,957 B / 99.41%. Straight segments are a visual guide, not measured intermediate models. Accounting and runtime differences remain as stated above.
