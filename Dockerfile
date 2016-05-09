FROM tailordev/pandas:0.17.1

RUN apt-get update -qqy && apt-get install -qqy unzip && \
  pip install algoliasearch

ENV ALGOLIA_APP_ID K6ACI9BKKT
# You will also need to set ALGOLIA_API_KEY.

WORKDIR /root

COPY generate.sh upload.py Makefile jobs_frequency.json bin/

CMD ["bin/generate.sh"]
