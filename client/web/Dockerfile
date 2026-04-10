FROM node:20-slim

WORKDIR /app

COPY pnpm-lock.yaml pnpm-workspace.yaml ./
COPY client/web/package.json ./client/web/package.json

RUN npm install -g pnpm@10.32.0 && pnpm install --filter @do4ai/client-web-template...

COPY . .

WORKDIR /app/client/web

EXPOSE 3001

CMD ["pnpm", "dev", "--host", "0.0.0.0", "--port", "3001"]
