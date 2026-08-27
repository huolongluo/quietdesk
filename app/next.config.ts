import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  agentRules: false,
  turbopack: {
    root: path.join(__dirname),
  },
  async rewrites() {
    const agent = process.env.AGENT_URL || "http://127.0.0.1:8787";
    return [{ source: "/agent/:path*", destination: `${agent}/:path*` }];
  },
};

export default nextConfig;
