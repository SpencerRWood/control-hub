const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type HealthResponse = {
  status: string;
};

export async function getHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE_URL}/health`);
  if (!res.ok) throw new Error(`Backend error: ${res.status}`);
  return res.json();
}
