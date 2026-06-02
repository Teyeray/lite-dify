import type { NextConfig } from 'next'

function getProxyAssetPrefix() {
  const publicWebUrl = process.env.PUBLIC_WEB_URL
  if (!publicWebUrl)
    return undefined

  try {
    const url = new URL(publicWebUrl)
    return url.pathname === '/' ? undefined : publicWebUrl.replace(/\/$/, '')
  }
  catch {
    return undefined
  }
}

const configuredAllowedDevOrigins = process.env.NEXT_ALLOWED_DEV_ORIGINS
  ? process.env.NEXT_ALLOWED_DEV_ORIGINS.split(',').map(origin => origin.trim()).filter(Boolean)
  : []

const allowedDevOrigins = Array.from(new Set([
  'http://localhost:13080',
  'http://127.0.0.1:13080',
  'localhost:13080',
  '127.0.0.1:13080',
  ...configuredAllowedDevOrigins,
]))

const nextConfig: NextConfig = {
  assetPrefix: getProxyAssetPrefix(),
  allowedDevOrigins,
}

export default nextConfig
