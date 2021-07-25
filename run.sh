git pull

# Delete all `.Ds_Store`
find . -name ".DS_Store" -delete

# Delete all `.ipynb_checkpoints` folders
find . -name .ipynb_checkpoints -type d -exec rm -rf {} \;

# jupyter nbconvert --ExecutePreprocessor.timeout=-1 --to notebook --execute --inplace *.ipynb
# jupyter nbconvert --to script *.ipynb

ipython *.py

black *.py

git add --all && git commit -m "Update" && git push
