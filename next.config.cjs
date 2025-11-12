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
  images: {
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
        pathname: "/api/image/**",
      },
      {
        protocol: "http",
        hostname: "127.0.0.1",
        pathname: "/api/image/**",
      },
      {
        protocol: "http",
        hostname: "**",
        pathname: "/api/image/**",
      },
    ],
    unoptimized: process.env.NODE_ENV === "development",
  },
};
