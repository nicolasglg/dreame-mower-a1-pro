## Contributing

This repository is maintained exclusively for the Dreame A1 Pro
(`dreame.mower.g2422`). Bug reports and pull requests must be reproducible and
validated on that model.

Changes dedicated to other Dreame or MOVA mowers are outside this repository's
scope. Please continue those in a community fork.

To submit an A1 Pro change, fork the repository and open a pull request against
the `main` branch. Include the Home Assistant version, integration version, A1
Pro firmware version, and relevant debug logs with secrets removed.

### Tests

Add tests for your change under `tests/`. They run automatically on every pull
request. To run them locally, put only the `dreame` package on the import path
(the integration's `select.py` would otherwise shadow the standard library
module):

```bash
pip install pytest numpy pillow pybase64 pycryptodome cryptography paho-mqtt requests
mkdir -p /tmp/dreame-path && ln -sfn "$PWD/custom_components/dreame_mower/dreame" /tmp/dreame-path/dreame
PYTHONPATH=/tmp/dreame-path python -m pytest -q tests
```
