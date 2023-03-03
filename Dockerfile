FROM python:3.7-slim-buster
RUN apt-get update -y

ARG stackName

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENV stackName=$stackName
RUN if [ "$stackName" = "prod" ] ; then python -m pytest --no-header -vvv -rA *.py ; fi

EXPOSE 5000
#ENTRYPOINT python
#CMD zephyr.py test
CMD python zephyr.py $stackName
#CMD ["zephyr.py"]
