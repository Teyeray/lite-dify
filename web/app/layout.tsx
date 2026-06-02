import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Lite Dify',
  description: 'A lightweight workflow and agent app builder',
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

