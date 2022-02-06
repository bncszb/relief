#!/bin/bash

NOW=$(date +"%Y-%m-%d %H:%M:%S")
NOW_FILE=$(date +"%Y-%m-%d_%H-%M-%S")

RUN_LOGS="data/logs/run_logs.log"
CURRENT_LOGS="data/logs/$NOW_FILE.log"

echo $NOW >> $RUN_LOGS

/usr/local/bin/docker-compose up \
--abort-on-container-exit \
--exit-code-from search

/usr/local/bin/docker-compose logs > $CURRENT_LOGS

/usr/local/bin/docker-compose down