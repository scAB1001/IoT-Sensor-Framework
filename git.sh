#!/bin/bash

# Create symbolic link `ln -s git.sh git` to run as just ./git

git st
cd ~/github-projects/uni/comp3211/
git add .; git ci; git push origin dev
# Set vim.basic as default with:
# sudo update-alternatives --config editor
