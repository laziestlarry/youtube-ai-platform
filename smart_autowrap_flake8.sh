#!/bin/bash
# Aggressively auto-wrap long lines (E501) in app/ using autopep8, with multiple passes

set -e

MAX_PASSES=3
PASS=1

while [ $PASS -le $MAX_PASSES ]; do
  echo "Autopep8 pass $PASS/$MAX_PASSES: Wrapping long lines..."
  autopep8 --in-place --aggressive --aggressive --aggressive --max-line-length=79 --recursive app/
  PASS=$((PASS+1))

done

echo "Running flake8 to show any remaining issues:"
flake8 app/ | tee flake8_remaining.txt

REMAINING=$(grep -c 'E501' flake8_remaining.txt || true)
if [ "$REMAINING" -eq 0 ]; then
  echo "\nAll E501 (line too long) issues auto-wrapped!"
else
  echo "\n$REMAINING E501 (line too long) issues remain. Please review and wrap manually if needed."
fi 