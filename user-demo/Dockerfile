FROM node:14

WORKDIR /home/node/app

COPY package*.json ./
RUN npm install

COPY . ./

USER 1000  # User "node". Putting a numeric ID here to avoid Kubernetes throwing the error: 'container has runAsNonRoot and image has non-numeric user (node), cannot verify user is non-root'
EXPOSE 3000
CMD ./bin/www
