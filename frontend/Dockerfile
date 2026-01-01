# Этап 1: Сборка
FROM node:20-slim AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап 2: Production (Nginx)
FROM nginx:stable-alpine AS production-stage
# Копируем наш конфиг
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Копируем собранные файлы фронтенда из предыдущего этапа
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
