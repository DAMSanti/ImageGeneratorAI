FROM node:18-alpine

# Instalar Python y dependencias del sistema
RUN apk add --no-cache python3 py3-pip build-base python3-dev

WORKDIR /app

# Copiar package.json
COPY package*.json ./

# Instalar dependencias Node
RUN npm install

# Copiar código frontend
COPY app ./app
COPY components ./components
COPY hooks ./hooks
COPY types ./types
COPY lib ./lib
COPY public ./public
COPY *.js *.json *.css ./

# Build Next.js
RUN npm run build

# Copiar requirements Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar backend
COPY backend ./backend

# Exponer puertos
EXPOSE 3000 8000

# Crear comando para iniciar ambos servicios
RUN echo '#!/bin/sh\nnpm run dev & \npython -m uvicorn backend.main:app --host 0.0.0.0 --port 8000\nwait' > /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
