FROM node:20

WORKDIR /app

# Copiar solo package.json y lock primero para cacheo de dependencias
COPY frontend/package*.json ./

# Instalar dependencias del Quasar Project
RUN npm install

# Copiar el resto del código
COPY frontend/ .

# Instalar Quasar CLI
RUN npm install -g @quasar/cli

EXPOSE 9000

CMD ["quasar", "dev"]
