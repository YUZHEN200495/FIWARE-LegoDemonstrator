FROM node:18.10
 
WORKDIR /usr/src/app
 
COPY ./frontend/package*.json ./
 
RUN npm install
 
COPY ./frontend .
 
EXPOSE 8000
 
#TODO: change from dev to build when in event
CMD [ "npm", "run", "dev","--", "--host", "--port", "8000" ]
