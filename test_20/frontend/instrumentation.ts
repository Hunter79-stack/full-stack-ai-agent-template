import { registerOTel } from "@vercel/otel";

export function register() {
  registerOTel({
    serviceName: "test_20-frontend",
  });
}
