JobSuggest is an autocomplete component for French job titles.

It makes it super easy to integrate, in an HTML form, a text input where a user
can specify a job using auto-completion a.k.a. suggestions. It is OpenSource
and we welcome contributions both for the code and the data.

The data is hosted by [Algolia](https://www.algolia.com), so you can use any of
their client integration, especially the ones for
[Autocomplete](https://www.algolia.com/doc/search/auto-complete).

# Usage

Check out the code for our examples in the `examples` folder, or try it our
[live demo](https://cdn.rawgit.com/bayesimpact/french-job-suggest/master/examples/angular.html).

# Importing Data

This repository contains all the code that we use to generate the data. You can
use it to create your own Algolia base if you wish.

We download the ROME data from [Pôle Emploi](http://www.pole-emploi.org/informations/open-data-pole-emploi-@/view-category-25799.html) (click [here](https://api.emploi-store.fr/api/docs/romeopen/REF_ROME_CSV/1/RefRomeCsv.zip) to download the data), then clean it up and transform the
CSV to JSON before uploading it to Algolia.

To run it you will need the API key that has the following rights `addObject,
deleteObject, deleteIndex` on the existing Algolia index.

## Setup

* Install [Docker](https://docs.docker.com/engine/installation/).
* Build the Docker image that will manage the upload:
```
docker build -t bayesimpact/french-job-suggest .
```
* Run the Docker:
```
docker run -e "ALGOLIA_API_KEY=<the secret API>" bayesimpact/french-job-suggest
```

## Development

During development iterations, we recommend to mount the live files into the container so that you don't need to re-build the image each time:
```
docker run -e "ALGOLIA_API_KEY=<the secret API>" -v "$(pwd)/":/root/bin bayesimpact/french-job-suggest
```

## Test

To run tests, mount live files into the container so that you don't need to re-build the image each time:

```
docker run -v "$(pwd)/":/root/bin bayesimpact/french-job-suggest python bin/upload_test.py
docker run -v "$(pwd)/":/root/bin bayesimpact/french-job-suggest python bin/rome_genderization_test.py
```
