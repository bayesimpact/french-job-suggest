all: data/rome data/passage_fap2009_romev3.txt

data/RefRomeCsv.zip:
	wget -P "$(@D)" 'https://api.emploi-store.fr/api/docs/romeopen/REF_ROME_CSV/1/RefRomeCsv.zip'

data/rome: data/RefRomeCsv.zip
	unzip "$<" -d "$@"
	sed -i -e "s/''/'/g" "$@"/*.csv

data/passage_fap2009_romev3.txt:
	wget -P "$(@D)" 'http://dares.travail-emploi.gouv.fr/IMG/txt/passage_fap2009_romev3.txt'
