#!/usr/bin/bash

cd /home/siim/bithumb/
./scrape_1m_data_for_day.py vmhistory.pickle
cp vmhistory.pickle vmhistory.pickle.backup
rm vmhistory.pickle.backup.gz
gzip vmhistory.pickle.backup
git add vmhistory.pickle.backup.gz

dd=$(date)
log=$(git log -1 | head -n 5 | tail -n 1)
prefix_commit="BOT: scraped data at "
if [[ "$log" == *"$prefix_commit"* ]]
then 
  echo "--- Update privious commit"
  git commit --amend -m "$prefix_commit at $dd by bithumb_96-250"
  git push --force
else
  echo "--- Push the new commit"
  git commit -m "$prefix_commit at $dd by bithumb_96-250"
  git push
fi

