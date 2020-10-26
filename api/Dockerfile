FROM golang:alpine as builder

WORKDIR /workspace

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a

FROM alpine AS final

WORKDIR /

COPY --from=builder /workspace/pricecheck-api .

CMD ["./pricecheck-api"]

EXPOSE 8000