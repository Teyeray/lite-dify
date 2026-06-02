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

const allowedDevOrigins = process.env.NEXT_ALLOWED_DEV_ORIGINS
  ? process.env.NEXT_ALLOWED_DEV_ORIGINS.split(',').map(origin => origin.trim()).filter(Boolean)
  : []

const nextConfig: NextConfig = {
  assetPrefix: getProxyAssetPrefix(),
  allowedDevOrigins,
}

export default nextConfig

