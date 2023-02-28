# zephyr

Barebones API development pipeline using python/flask and AWS EKS

# Introduction

> Zephyr
>  1. A light wind from the west. 
>  2. Any light refreshing wind; **a gentle breeze.**

## Pre-requisites

Development is currently based around a Vagrant image for convenience. You will need Virtualbox and Vagrant on your workstation.

If you can `vagrant up`, the resulting environment will have all pre-requisites installed.

# Local usage / development

1. You've already downloaded the repository. Run `vagrant up` to provision your workspace.
2. Log into the vagrant environment with `vagrant ssh`

## Local server

0. Build the image with `docker build -t zephyr .`
1. Run the resulting image with `docker run -p 5000:5000 -t zephyr`
2. You can now access the application via web browser at http://localhost:5000

## The test suite

0. Build the image with `docker build -t zephyr .`
1. `docker run -t zephyr -m pytest --no-header -vvv -rA *.py`

Any functions in zephyr.py prefixed with `test_` will get called by pytest.

In a perfect world, the test suite must pass for code to be deployed in production.

# Cloud Development

The EKS deployments are also managed from within the Vagrant environment, so as before, 

1. `vagrant up`
2. `vagrant ssh`

## Deploying to AWS EKS

1. Configure your aws credentials with `aws configure`
2. Next, "login" locally to pulumi (to store state) with `pulumi login --local`
3. then you can `pulumi up`
4. This automatically creates an EKS stack, builds an image from the Dockerfile, and runs that image on the EKS cluster.
5. The output will include an appUrl, which you can use to access the application.

If and when you make changes to the application, you can run `pulumi up` from the `pulumi` directory to upload a new image to the cluster.

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
