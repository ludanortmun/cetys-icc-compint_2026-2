import json
from pathlib import Path
import subprocess
import joblib
import numpy as np
from sklearn.datasets import load_iris


ROOT = Path(__file__).resolve().parents[1]


def test_other_runtime_loads_onnx_and_predicts():
    extra = ROOT / "extra_src"
    assert (ROOT / "models/iris.onnx").is_file(), "Run the optional export notebook first"
    assert (extra / "README.md").is_file()
    command = json.loads((extra / "command.json").read_text())
    assert isinstance(command, list) and command and all(isinstance(x, str) for x in command)
    bundle = joblib.load(ROOT / "models/iris.joblib")
    X = load_iris().data.astype(np.float32)[::-1]
    result = subprocess.run(command, cwd=extra, input=json.dumps(X.tolist()),
                            text=True, capture_output=True, timeout=60, check=True)
    names = json.loads(result.stdout)
    expected = [bundle["class_names"][int(c)] for c in bundle["model"].predict(X)]
    assert names == expected
