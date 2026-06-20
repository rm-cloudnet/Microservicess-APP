FROM nginx:alpine

# Remove default nginx configurations and static assets
RUN rm -rf /usr/share/nginx/html/*
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom nginx network config
COPY nginx.conf /etc/nginx/conf.d/

# Copy static webpage code
COPY index.html /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
