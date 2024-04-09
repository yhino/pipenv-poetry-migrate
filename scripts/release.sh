#!/usr/bin/env bash

set -ue
set -x

git fetch --prune
NEW_VERSION=$(poetry run semantic-release --strict -v version --print-tag)
EXIT_CODE=$?
if [ ${EXIT_CODE} -eq 0 ]; then
	git ci --allow-empty --message=":bookmark: ${NEW_VERSION}"
fi
