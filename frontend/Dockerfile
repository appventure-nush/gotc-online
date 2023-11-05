FROM httpd:latest

# remember to npm run build before making the docker image
# when running docker image, bind ports 8080:80 (host port 8080 bind to container port 80)
# Jetbrains docker run configuration should already be found in .idea/runConfigurations

COPY ./dist/ /usr/local/apache2/htdocs/