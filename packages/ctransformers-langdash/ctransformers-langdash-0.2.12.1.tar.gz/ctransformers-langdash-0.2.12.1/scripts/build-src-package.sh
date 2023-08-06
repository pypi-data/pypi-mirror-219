#!/bin/bash

clean() {
    rm -r build dist *.egg-info || true
    rm -r _skbuild MANIFEST.in || true
}

clean
python -m build --sdist
