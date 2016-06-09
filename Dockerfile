FROM tailordev/pandas:0.17.1

RUN apt-get update -qqy && apt-get install -qqy unzip && \
  pip install algoliasearch

ENV ALGOLIA_APP_ID K6ACI9BKKT
# You will also need to set ALGOLIA_API_KEY.

WORKDIR /root

COPY generate.sh rome_genderization.py upload.py Makefile bin/
COPY jobs_frequency.json data/

CMD ["bin/generate.sh"]
