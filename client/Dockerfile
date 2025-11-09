# syntax=docker/dockerfile:1

FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
RUN npm ci

# Copy configuration files needed for development
COPY tsconfig.json .
COPY next.config.mjs .
COPY tailwind.config.ts .
COPY postcss.config.mjs .
COPY messages ./messages

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules

# Copy all client source files
COPY src ./src
COPY public ./public
COPY messages ./messages
COPY next.config.mjs .
COPY tsconfig.json .
COPY tailwind.config.ts .
COPY postcss.config.mjs .
COPY package.json .

# Set environment variables for build
ENV NEXT_TELEMETRY_DISABLED=1
# Note: NEXT_PUBLIC_API_URL should be set at runtime for browser requests
# Leaving it unset so it defaults to http://localhost:8000 in the browser

# Build the application (creates .next folder)
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application files from builder stage
# Copy public folder (static assets)
COPY --from=builder /app/public ./public

# Copy messages folder (i18n translations)
COPY --from=builder /app/messages ./messages

# Copy the standalone server (includes node_modules for production)
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./

# Copy the static files (.next/static for client-side JS and CSS)
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Note: The standalone build includes all necessary files to run Next.js
# The .next/standalone folder contains the minimal server + dependencies

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]

