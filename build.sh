#!/bin/sh

rm -rf build
rm -rf dist
pyinstaller --clean --onefile aidraw.py
