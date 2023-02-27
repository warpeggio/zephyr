# zephyr
Barebones API development pipeline using python/flask and AWS EKS

# Introduction
> Zephyr
>  1. A light wind from the west. 
>  2. Any light refreshing wind; **a gentle breeze.**

## Pre-requisites
### For the local instance
1. Install docker - On ubuntu, verify that your user is in the `docker` group. Restart any login sessions as necessary.
2. Download the repository, and while CWD'd to your local copy, run `docker build -t zephyr .` to create the image for use on your workstation.
### For the Infastructure-as-Code
1. Install pulumi. Download the binaries to your workstation and put them in a directory in your $PATH
2. Install awscli and configure your credentials:
    `aws configure`
3. You'll need python3
4. awscli must be at least v 1.24
	pip3 install --upgrade awscli
See "Deploying to EKS" below for more information.

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
1. From the `pulumi` directory, issue `pip3 install -r requirements.txt`
2. then you can `pulumi up`
3. This automatically creates an EKS stack, builds an image from the Dockerfile, and runs that image on the EKS cluster.
4. After you make changes to the application, you can run `pulumi up` from the `pulumi` directory to upload a new image to the cluster.
## Cleanup
`pulumi destroy` from the pulumi dir will get it done.

# Contributing
1. Open an issue to describe the work [Write some test cases?]
2. Create a branch from `development` that references your issue
3. Do neat stuff
4. Run the test suite to validate safety, reliability, and suitabilty
5. Open a pull request to merge your code with the `development` branch
6. Smoke test by deploying the development branch
7. Merge the `development` branch into `main`
8. Deploy to production
