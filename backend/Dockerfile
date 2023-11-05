
FROM python:3.12-bookworm

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# when running docker image, bind ports 5000:5000 (host port 5000 bind to container port 5000)
# Jetbrains docker run configuration should already be found in .idea/runConfigurations