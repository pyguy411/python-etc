# flask app example of how to make multiple api calls within a view using threading

This code can be improved by making using the info from a first remote api call
to spawn the correct number of threads to get the remaining pages, instead 
of stepping through them synchronously.

## Install:

You can use a virtual environment (conda or venv):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file (recomended)
``` 
pip install -r requirements.txt
```

## Running the code

This example achieves the following: 
- Expose at least one RESTful endpoint that responds with a 
merged organization/team profile with data from both Github and Bitbucket 
- Provide a RESTful way for a client to provide the Github organization and 
Bitbucket team names to merge for the profile 
- The profile should include the following information (when available): 
    - Total number of public repos (separate by original repos vs forked repos) 
    - Total watcher/follower count 
    - A list/count of languages used across all public repos 
    - A list/count of repo topics

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests

```

curl -i "http://127.0.0.1:5000/health-check"
curl -i "http://127.0.0.1:5000/org-profile/<org>"  

```
where `<org>` in the url is replaced with the organization/team/individual name.
e.g.

    curl -i "http://127.0.0.1:5000/org-profile/pygame" 
    curl -i "http://127.0.0.1:5000/org-profile/mailchimp" 
    curl -i "http://127.0.0.1:5000/org-profile/microsoft" 
    curl -i "http://127.0.0.1:5000/org-profile/pyguy411" 
