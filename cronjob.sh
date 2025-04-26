#!/bin/bash

# source the env variables, since cronjob does not load them from .bashrc directly 
. $HOME/.bashrc

echo ">> moving to folder"

cd ${$QUIZ_PROJECT_DIR} 

echo "Executing make..."

make setup_and_run

echo "Done!"
