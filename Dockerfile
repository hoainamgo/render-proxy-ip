FROM alpine:3.19

# Cài đặt curl, ca-certificates, bash và nginx
RUN apk add --no-cache curl ca-certificates bash nginx \
    && curl -L -o /usr/local/bin/gost.gz https://github.com/ginuerzh/gost/releases/download/v2.11.5/gost-linux-amd64-2.11.5.gz \
    && gzip -d /usr/local/bin/gost.gz \
    && chmod +x /usr/local/bin/gost \
    && mkdir -p /run/nginx

WORKDIR /app

COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PORT=10000
ENV PROXY_USER=ksmart
ENV PROXY_PASS=98427189427194817294817294817294

EXPOSE 10000

CMD ["/app/entrypoint.sh"]
