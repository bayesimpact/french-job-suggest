#!/bin/bash

DIR="$(dirname "${BASH_SOURCE[0]}")"
make -f "$DIR/Makefile"

# Upload the names to Algolia.
python "$DIR/upload.py" \
  data/rome/unix_referentiel_appellation_v*_utf8.csv \
  data/rome/unix_referentiel_code_rome_v*_utf8.csv \
  data/passage_fap2009_romev3.txt \
  data/jobs_frequency.json
