FROM node
WORKDIR /App
ADD . /App
RUN npm install
RUN chmod 755 /App/wait-for-it.sh
ENV PORT 3000
ENV IP "127.0.0.1"
CMD ["./wait-for-it.sh"]