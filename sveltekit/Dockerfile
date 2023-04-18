FROM node:16-alpine
WORKDIR /app
EXPOSE 3000
COPY . .

RUN npm install

ENTRYPOINT ["npm", "run", "dev", "--", "--host"]