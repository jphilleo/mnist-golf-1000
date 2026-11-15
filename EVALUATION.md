# Final official MNIST test evaluation

November 15, 2026.

**993 bytes. 99.25% official MNIST test accuracy.**

| Metric | Result |
| --- | ---: |
| Correct predictions | 9,925 / 10,000 |
| Errors | 75 |
| Accuracy | 99.25% |
| 95% Wilson interval | 99.061%–99.401% |
| Compressed artifact | 993 bytes |
| Decompressed Python source | 1,571 bytes |
| Timed inference | 16.448 seconds |

The exact existing block-185 artifact was frozen before official-test acquisition. Its SHA-256 is `924fc897db1f4faa0e29b2cde0b1d87b280575fc64e40818156dda36395f0b86`. The evaluation slot was consumed before downloading the two original MNIST test archives. Their known MD5 checksums, SHA-256 hashes, IDX headers, payload lengths, and label ranges were verified.

One CPU float32 pass evaluated every test image once, using one thread and batches of 256. Warmup used synthetic zeros only. No test examples were removed, and no per-image feedback, confusion matrix, alternate finalist or retry was produced. The previously recorded development score was 99.15%; this is a separate official-test result.

The 993-byte gzip archive includes the custom model reconstruction and inference code and all model data. Python 3.9.6 and PyTorch 2.6.0 are supplied separately; NumPy 2.0.2 is used by the evaluation harness. The model reconstructs float32 weights, so compact storage is not a claim of integer-only inference or a 993-byte standalone executable.

The Wilson interval describes binomial sampling uncertainty; it is not a guarantee of accuracy on other handwriting distributions. This is a one-shot evaluation of one selected model, not a replication across independently trained models or an independently reproduced world record. Any subsequent tuning using this result must treat the official test set as exposed.

Evidence: [aggregate evaluation result](results/official-test-result.json), [model](model/model.py.gz), and [model manifest](model/manifest.json).
