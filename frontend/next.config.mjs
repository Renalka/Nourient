/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  // The existing codebase has legacy lint violations. Keep production builds
  // deployable while lint cleanup is tracked as a separate maintenance task.
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
