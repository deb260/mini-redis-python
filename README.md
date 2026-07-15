# Mini Redis

A Redis-compatible in-memory key-value server built from scratch in Python using only the Python standard library.

## Overview

Mini Redis is a simplified implementation of Redis that demonstrates how an in-memory database works internally. It supports TCP socket communication, the Redis Serialization Protocol (RESP), command dispatching, key expiration, and concurrent client handling using multithreading.

The project was built to understand the core concepts behind Redis rather than simply using an existing database.

## Features
TCP server accepting multiple client connections
RESP parser (client request parsing)
RESP serializer (server response generation)
In-memory key-value storage
Command dispatcher using a command-function mapping
Key expiration with TTL support
Multi-threaded client handling

## Supported commands:
  - `PING` — health check
  - `SET key value` — store a value
  - `GET key` — retrieve a value
  - `DEL key` — delete a key
  - `EXISTS key` — check if key exists
  - `INCR key` — increment a numeric value
  - `EXPIRE key seconds` — set expiration on a key
  - `TTL key` — check remaining time on a key

## Project Structure:
min_redis.py
    ├── RESP Parser
    ├── RESP Serializer
    ├── Command Functions
    ├── Dispatcher
    ├── TCP Server
    └── Multi-threaded Client Handling

test_client.py
    └── Test client for sending Redis commands

## How It Works:
Client
    │
    ▼
TCP Server
    │
    ▼
RESP Parser
    │
    ▼
Dispatcher
    │
    ▼
Command Function
    │
    ▼
RESP Serializer
    │
    ▼
Client Response


## Running the Server:
python min_redis.py


## The server starts on:
127.0.0.1:6379


## Testing:
python test_client.py

## What I learned:
- How TCP sockets work in Python
- How to parse and serialize the RESP protocol
- How Redis stores and expires keys
- How threading enables multiple simultaneous connections
- Why Redis is fast — everything lives in memory
