#!/bin/bash

# source the env variables, since cronjob does not source .bashrc
. $HOME/.bashrc

echo ">> Current date" $(date)
echo ">> moving to folder"

cd $QUIZ_PROJECT_DIR

echo ">> Executing make..."

make setup_and_run

echo ">> Done!"
