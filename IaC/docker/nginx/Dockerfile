FROM --platform=linux/amd64 nginx:1.25.3

COPY nginx.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/conf.d/site.conf
COPY upstream.conf /etc/nginx/conf.d/upstream.conf
RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 80