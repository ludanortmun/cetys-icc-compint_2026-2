# Optional ONNX application — replace this scaffold with your setup instructions

For the 10-point runtime extension, add your own project here. Document:

- Language/runtime and required versions; use an environment different from the
  Python/scikit-learn application (for example Node.js, Java, C#, or a browser).
- All dependency installation steps and any compilation/build commands.
- How to run it from a clean checkout, reading `../models/iris.onnx`.
- Input feature order, class mapping, and an example prediction.

Create `command.json` containing a JSON array of command arguments, such as
`["node", "predict.mjs"]`. The checker runs this command with this directory as
its working directory. It supplies a JSON matrix of measurements on stdin and
expects a JSON array of species names on stdout, with one name per input row.
Send diagnostic messages to stderr. Use the ONNX model for inference; do not
retrain, hardcode predictions, or call the Python/scikit-learn application.
The ONNX model metadata `class_names` contains the JSON-encoded species list
indexed by numeric label. Input is `float32` with shape `(n, 4)`.

This supplied README is a prompt, not completed documentation. Replace it with
your project's actual setup, dependencies, compilation (if needed), and run
instructions to receive credit. Do not commit installed dependencies or builds.
