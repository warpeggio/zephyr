# zephyr
Barebones API development pipeline using python/flask and AWS EKS

# Introduction
> Zephyr
>  1. A light wind from the west. 
>  2. Any light refreshing wind; **a gentle breeze.**

# Local usage / development
For now, you can run the local flask app by installing the pre-reqs and letting it rip:
0. make sure you've got python3 and pip3
1. pip3 install -r requirements.txt
2. python3 ./zephyr.py

# The test suite
To run the test suite, issue the following command from the top level of the project directory:
`~/.local/bin/pytest --no-header -vvv -rA *.py ; echo $?`
Any functions prefixed with `test_` will get called.

# Deploying to EKS
`#TODO`

# Cleanup
`#TODO`

