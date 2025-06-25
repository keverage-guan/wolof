<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: Train new language model from cadet and inception data

This project template lets you train a part-of-speech tagger, morphologizer and dependency parser from your cadet and inception data.

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[Weasel documentation](https://github.com/explosion/weasel).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `prepare` | Convert .conllu files to spaCy .spacy format with expected filenames |
| `debug` | Assess data for training using spaCy's debug data |
| `train` | Train wolof |
| `evaluate` | Evaluate on the test data and save the metrics |
| `package` | Package the trained model so it can be installed |
| `document` | Generate project documentation |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `prepare` &rarr; `debug` &rarr; `train` &rarr; `evaluate` &rarr; `package` &rarr; `document` |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->
