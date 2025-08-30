FROM node:latest AS build

# Install dependencies
WORKDIR /app
COPY *.js* ./
RUN npm install

# Copy app
COPY public/ public
COPY src/ src

# Package
RUN npm run build

# Host app
FROM nginx:latest
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
