#!/usr/bin/env zsh
# approximate the functionality of pre-commit hooks,
# without the attitude or lack of useful docs

declare -a arr=(
    "check"
    "run pytest"
    "run mypy bwyd"
    "run pylint bwyd"
)

set -e

for i in "${arr[@]}"
do
    cmd="poetry $i"
    echo $cmd
    eval $cmd
done
