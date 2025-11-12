module.exports = {
  /** @type {import('next').NextConfig} */
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: "50mb",
    },
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },
};
