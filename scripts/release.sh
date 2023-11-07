#!/usr/bin/env bash

set -ue
set -x

NEW_VERSION=$(poetry run semantic-release print-version 2>/dev/null)
if [ -n "${NEW_VERSION}" ]; then
	git ci --allow-empty --message=":bookmark: ${NEW_VERSION}"
fi
