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
3. It will fail trying to do the loadbalancer stuff; wait a moment for `pulumi refresh`, and then run `pulumi up` again
4. ???? It still doesn't work because the loadbalancer configuration is wrong. It's not able to parse the ingress stuff, or the loadbalancer module is incompatible with the kubernetes version. Not sure.
5. Update the local kubernetes config:
    `pulumi stack output kubeconfig > ~/.kube/config`
6. From the `kubernetes` directory, we can now apply a handful of yamls to effect a deployment:
    `kubectl apply -f namespace.yaml`
    `kubectl apply -f service.yaml`
    `kubectl apply -f deployment.yaml`
    `kubectl apply -f ingress.yaml -n zephyr-webapp`

# Cleanup
`pulumi destroy` from the pulumi dir will get it done.

