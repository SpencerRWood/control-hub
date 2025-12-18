import { useEffect, useState } from "react";
import { getHealth } from "../lib/api";

export function BackendStatus() {
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getHealth()
      .then((data) => {
        setStatus(data.status);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

  return <p>Backend status: {status}</p>;
}
