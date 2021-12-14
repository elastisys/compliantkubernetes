FROM node:14-alpine

WORKDIR /home/node/app

COPY package*.json ./
RUN npm install

COPY . ./

# We use a numeric ID here to avoid Kubernetes throwing the error: 'container has runAsNonRoot and image has
# non-numeric user (node), cannot verify user is non-root'
USER 1000
EXPOSE 3000
CMD npm start
