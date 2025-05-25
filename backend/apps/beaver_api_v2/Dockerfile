FROM golang:1.24.1-alpine as builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -ldflags="-s -w" -o api cmd/beaver-api/main.go

FROM alpine:latest as api
WORKDIR /root/
COPY --from=builder /app/api .
EXPOSE 8000
CMD ["./api"]
