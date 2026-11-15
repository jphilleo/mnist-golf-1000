"""Verify the frozen download and run a synthetic-input smoke check."""
from pathlib import Path
import gzip
import hashlib
import json
import torch

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "model/manifest.json").read_text())
packed = (root / "model/model.py.gz").read_bytes()
assert len(packed) == manifest["compressed_bytes"] == 993
assert hashlib.sha256(packed).hexdigest() == manifest["artifact_sha256"]
source = gzip.decompress(packed)
assert len(source) == manifest["source_bytes"] == 1571
assert hashlib.sha256(source).hexdigest() == manifest["source_sha256"]
assert source == (root / "model/model.py").read_bytes()
namespace = {}
exec(compile(source, "model/model.py", "exec"), namespace)
torch.set_num_threads(1)
with torch.inference_mode():
    images = torch.zeros(2, 1, 28, 28)
    logits = namespace["logits"](images)
    labels = namespace["predict"](images)
assert logits.shape == (2, 10) and torch.isfinite(logits).all()
assert labels.shape == (2,) and ((labels >= 0) & (labels <= 9)).all()
print("Verified: 993 bytes, expected SHA-256, matching source, valid inference.")
print("Synthetic inputs only; no MNIST test evaluation was run.")
