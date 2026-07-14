const BASE_URL = "/api";

async function fetchJson(path) {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request to ${path} failed with status ${response.status}`);
  }
  return response.json();
}

export function getPrices(startDate, endDate) {
  const params = new URLSearchParams();
  if (startDate) params.set("start_date", startDate);
  if (endDate) params.set("end_date", endDate);
  const query = params.toString() ? `?${params.toString()}` : "";
  return fetchJson(`/prices${query}`);
}

export function getChangePointResults() {
  return fetchJson("/change-points");
}

export function getEvents() {
  return fetchJson("/events");
}

export function getSummaryStats() {
  return fetchJson("/summary");
}
