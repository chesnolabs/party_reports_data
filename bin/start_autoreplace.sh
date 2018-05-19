#!/bin/bash

source ~/CHESNO/chesnovenv/bin/activate
find .. -type f -name 5_donations.csv -exec python3 replace_names.py "{}" \;
find .. -type f -name 6_expenses.csv -exec python3 replace_names.py "{}" \;
deactivate
