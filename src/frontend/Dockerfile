# 1. Build stage
FROM node:18 AS build

WORKDIR /app

# Copy package.json và package-lock.json
COPY package*.json ./

# Cài dependencies
RUN npm install

# Copy toàn bộ code frontend
COPY . ./

# Build app cho production
RUN npm run build

# 2. Serve stage
FROM nginx:alpine

# Copy build output sang thư mục của nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copy config nginx nếu muốn custom (optional)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]