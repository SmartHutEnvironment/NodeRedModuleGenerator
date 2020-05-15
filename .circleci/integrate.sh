#!/bin/bash
set -e
FEATURE_BRANCH=$CIRCLE_BRANCH

git fetch origin master $FEATURE_BRANCH
git diff origin/$FEATURE_BRANCH...origin/master --exit-code # This exits with 1 if the master is not fast forwardable
git checkout master
git reset --hard origin/master
git config user.name "CircleCI Agent"
git config user.email circleci@stdio.work
git merge --no-edit --no-ff origin/$FEATURE_BRANCH
git push origin master
git push -d origin $FEATURE_BRANCH
