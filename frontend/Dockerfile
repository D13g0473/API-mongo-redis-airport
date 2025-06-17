FROM node:20.12.2

WORKDIR /app



# Copiar el resto del código
COPY . .

# Instalar dependencias del Quasar Project
RUN npm install

# Instalar Quasar CLI
RUN npm install -g @quasar/cli

EXPOSE 9000

CMD ["quasar", "dev"]
