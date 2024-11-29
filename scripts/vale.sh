#!/bin/sh
git ls-files '*.md' | xargs vale
