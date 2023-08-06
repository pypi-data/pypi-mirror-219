# Stage 1: Building the code
FROM rust:1.66 as builder

WORKDIR /usr/src/myapp

# Copy your source code
COPY . .
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      protobuf-compiler

WORKDIR /usr/src/myapp/experiments/toolchain/prompt-graph-exec
RUN cargo install cargo-build-dependencies
RUN cargo build-dependencies

WORKDIR /usr/src/myapp
# This step will build the binary
RUN cargo install --path ./experiments/toolchain/prompt-graph-exec

# Stage 2: Running the binary
FROM debian:buster-slim

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      libssl-dev \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/*
# Copy the binary from the builder stage
COPY --from=builder /usr/src/myapp/experiments/toolchain/target/release/prompt-graph-exec /usr/local/bin/myapp

CMD ["myapp"]
