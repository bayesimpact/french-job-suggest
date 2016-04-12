#!/bin/bash

mkdir -p data
  
# Download the latest ROME.
if [ ! -e "data/RefRomeCsv.zip" ]; then
	wget -P data 'https://api.emploi-store.fr/api/docs/romeopen/REF_ROME_CSV/1/RefRomeCsv.zip'
fi

mkdir -p data/rome

# Unzip the CSV files.
if [ -z "$(ls data/rome/unix_referentiel_appellation*.csv 2> /dev/null)" ]; then
  unzip data/RefRomeCsv.zip -d data/rome
fi

# Clean up the double single quotes.
sed -i -e "s/''/'/g" data/rome/*.csv

# Upload the names to Algolia.
DIR="$(dirname "${BASH_SOURCE[0]}")"
python "$DIR/upload.py" \
  data/rome/unix_referentiel_appellation_v*_utf8.csv \
  data/rome/unix_referentiel_code_rome_v*_utf8.csv
