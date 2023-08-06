#!/bin/bash

EXIT_SUCCESS=0
EXIT_FAILURE=1


echo 'Deploying to Python Package Index...';
echo;
grep "name" pyproject.toml | grep --invert-match "{name";
grep "version" pyproject.toml;
echo;
echo -n "Press 'Y' to continue... "
if ! read -n1 -t30
then
    echo
    echo 'Operation aborted.';
    exit $EXIT_FAILURE;
fi;
echo

if [ "$REPLY" != 'y' ] && [ "$REPLY" != 'Y' ]
then
    echo 'Operation aborted.';
    exit $EXIT_FAILURE;
fi;

status="$(git status --porcelain)"
if (( ${#status} > 0 ))
then
    echo 'Git pending.';
    exit $EXIT_FAILURE;
fi;

source bin/activate;

python3 -m pip install --upgrade build;
python3 -m pip install --upgrade twine;
python3 -m build;
python3 -m twine upload dist/* 

echo 'Done.';
exit $EXIT_SUCCESS;
