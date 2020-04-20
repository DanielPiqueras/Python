FROM node:10.15.1-alpine
LABEL maintainer="jason.gass@sewan.es"

RUN mkdir -p /var/app
WORKDIR /var/app

COPY ebiblio-front /var/app/

RUN cd /var/app 
RUN npm install --global --unsafe-perm serve
RUN npm install

CMD ["sh", "-c", "npm run build; serve -s build"]