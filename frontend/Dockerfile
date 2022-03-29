FROM node:16.14.2-alpine

# Create app directory
WORKDIR /app

COPY package.json ./
COPY yarn.lock ./

RUN yarn

COPY . .

CMD [ "yarn", "start" ]
