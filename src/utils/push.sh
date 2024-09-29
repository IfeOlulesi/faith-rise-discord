#!/bin/bash
if [ "$1" == "all" ]; then
    git push origin dev
    git push origin main
    git push origin prod

    git push deploy-origin dev
    git push deploy-origin main
    git push deploy-origin prod
elif [[ "$1" == "dev" || "$1" == "main" || "$1" == "prod" ]]; then
    git push origin "$1"
    git push deploy-origin "$1"
else
    echo "Error: Unrecognized command '$1'. Use 'all', 'dev', 'main', or 'prod'."
fi