#!/bin/bash

# source the env variables, since cronjob does not load them from .bashrc directly 
. $HOME/.bashrc

echo ">> moving to folder"

cd /root/Projects/abytob/python-daily-quiz

echo "Executing make..."

make setup_and_run

echo "Done!"
