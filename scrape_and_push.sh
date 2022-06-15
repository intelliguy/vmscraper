#!/usr/bin/bash

PICKLE=vmhistory.pickle

cd /home/siim/bithumb/
./scrape_1m_data_for_day.py ${PICKLE}
cp ${PICKLE} ${PICKLE}.backup
rm ${PICKLE}.tz
tar cvzf ${PICKLE}.tz  *-${PICKLE}
git add ${PICKLE}.tz

log=$(git log -1 | head -n 5 | tail -n 1)
prefix_commit="BOT: scraped data at "
if [[ "$log" == *"$prefix_commit"* ]]
then 
  echo "--- Update privious commit"
  git commit --amend -m "$prefix_commit at $(date) by bithumb_96-250"
  git push --force
else
  echo "--- Push the new commit"
  git commit -m "$prefix_commit at $(date) by bithumb_96-250"
  git push
fi

