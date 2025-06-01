# 1. Build stage
FROM node:20 AS builder
WORKDIR /frontend
COPY . .
RUN npm install
RUN npm run build

# 2. Serve stage
FROM nginx:alpine

# Копируем кастомный конфиг Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем статику
COPY --from=builder /frontend/dist /usr/share/nginx/html