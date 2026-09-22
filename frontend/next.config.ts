import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  poweredByHeader: false,
  experimental: {
    // Mantem o build em threads, inclusive a checagem pela API do TypeScript.
    cpus: 2,
    workerThreads: true,
    useTypeScriptCli: false,
  },
};

export default nextConfig;
