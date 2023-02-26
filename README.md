# zephyr
Barebones API development pipeline using python/flask and AWS EKS

# Introduction
> Zephyr
>  1. A light wind from the west. 
>  2. Any light refreshing wind; **a gentle breeze.**

## Pre-requisites
1. Install docker - On ubuntu, verify that your user is in the `docker` group. Restart any login sessions as necessary.
2. Download the repository, and while CWD'd to your local copy, run `docker build -t zephyr .` to create the image for use on your workstation.

# Local usage / development
## Run the server locally
0. Build the image with `docker build -t zephyr .`
1. docker run -p 5000:5000 -t zephyr
2. You can now access the application via web browser at http://localhost:5000
## The test suite
0. Build the image with `docker build -t zephyr .`
1. `docker run -t zephyr -m pytest --no-header -vvv -rA *.py`
Any functions in zephyr.py prefixed with `test_` will get called by pytest.
In a perfect world, the test suite must pass for code to be deployed in production.

# Deploying to EKS
`#TODO`

# Cleanup
`#TODO`

