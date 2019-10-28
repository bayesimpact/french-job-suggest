all: data/rome data/passage_fap2009_romev3.txt

data/RefRomeCsv.zip:
	wget -P "$(@D)" 'https://api.emploi-store.fr/api/docs/romeopen/REF_ROME_CSV/1/RefRomeCsv.zip'

data/rome: data/RefRomeCsv.zip
	unzip "$<" -d "$@"
	sed -i -e "s/''/'/g" "$@"/csv/*.csv
	# TODO: Get rid of this once the ROME has been cleaned up.
	sed -i -e 's/2 D/2D/g;s/3 D/3D/g;s/\([^,"]\)"\([^,"]\|, \)/\1""\2/g' "$@"/csv/*.csv

data/passage_fap2009_romev3.txt:
	wget -P "$(@D)" 'http://dares.travail-emploi.gouv.fr/IMG/txt/passage_fap2009_romev3.txt'
