#!/usr/bin/env bash

# deploy this code using rsync to a remove ssh host
# just use
#   ./deploy.sh
# to incrementally deploy
# use
#  ./deploy.sh complete
# to DELETE EVERYTHING first and then redeploy

deploy_user_host="pi@mollyvision"
# relative to home directory unless preceded by a slash,
# WARNING: watch out not to delete the whole thing when using:
#   deploy.sh complete
deployment_folder="deployment"



d="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "x${1:-}" == "xcomplete" ]; then
    echo "Deleting previous deployment:"
    ssh "$deploy_user_host" "test -n "\$HOME" && rm -rv '$deployment_folder'"
fi
rsync -avz --exclude-from="$d"/.gitignore --exclude .git "$d" $deploy_user_host:deployment
