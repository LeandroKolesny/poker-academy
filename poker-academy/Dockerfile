# Multi-stage build para React
# Estágio 1: Build da aplicação
FROM node:18-alpine AS builder

# Definir diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências (incluindo dev dependencies para build)
RUN npm ci

# Copiar código fonte
COPY . .

# Definir variável de ambiente para produção
ENV NODE_ENV=production
ENV REACT_APP_ENV=production

# Build da aplicação para produção
RUN npm run build

# Estágio 2: Servir com NGINX
FROM nginx:alpine

# Remover configuração padrão do NGINX
RUN rm /etc/nginx/conf.d/default.conf

# Copiar configuração customizada do NGINX
COPY nginx.conf /etc/nginx/conf.d/

# Copiar arquivos buildados do estágio anterior
COPY --from=builder /app/build /usr/share/nginx/html

# Ajustar permissões (usuário nginx já existe na imagem base)
RUN chown -R nginx:nginx /usr/share/nginx/html

# Expor porta
EXPOSE 80

# Comando para iniciar NGINX
CMD ["nginx", "-g", "daemon off;"]
