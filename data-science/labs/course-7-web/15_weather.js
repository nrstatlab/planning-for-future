/* Experiment 15 — Fetch real-time weather from an open API and display it.
 *
 * The module is split in two on purpose:
 *
 *   summarise()    — pure. Takes a parsed response, returns display values.
 *                    Testable offline against weather-sample.json, which is a
 *                    real OpenWeatherMap response saved to disk.
 *   fetchWeather() — does the network call, then delegates to summarise().
 *                    fetchFn is injectable so the failure path can be tested
 *                    without a network or an API key.
 *
 * Separating the network call from the parsing is what makes the parsing
 * testable, and the parsing is where the bugs actually are.
 *
 * THREE THINGS TO SAY IN THE VIVA
 *
 *   1. fetch does NOT reject on a 404. An error status is still a successful
 *      HTTP transaction, so res.ok must be checked explicitly. Skip it and you
 *      call .json() on an HTML error page and get a confusing SyntaxError.
 *
 *   2. An API key in front-end JavaScript is visible to anyone who opens dev
 *      tools. Fine for a lab with a free key; in production the request goes
 *      through a server that holds the key.
 *
 *   3. CORS may block the request entirely. It is a BROWSER restriction — the
 *      same request from curl succeeds — and it cannot be worked around from
 *      the client. An API that forbids browser access needs a server proxy.
 */

const ENDPOINT = "https://api.openweathermap.org/data/2.5/weather";

export function summarise(json) {
  return {
    place:     json.name,
    country:   json.sys?.country ?? "",
    tempC:     Math.round(json.main.temp),
    feelsC:    Math.round(json.main.feels_like),
    humidity:  json.main.humidity,
    pressure:  json.main.pressure,
    condition: json.weather?.[0]?.description ?? "unknown",
    icon:      json.weather?.[0]?.icon ?? null,
    windMs:    json.wind?.speed ?? null,
    cloudPct:  json.clouds?.all ?? null
  };
}

/** Celsius to Fahrenheit, because the viva always asks. */
export const toF = c => +(c * 9 / 5 + 32).toFixed(1);

export function buildUrl(city, key, units = "metric") {
  const url = new URL(ENDPOINT);
  // URLSearchParams escapes the city name correctly — "New Delhi" becomes
  // "New+Delhi" without any manual encodeURIComponent.
  url.search = new URLSearchParams({ q: city, appid: key, units });
  return url;
}

export async function fetchWeather(city, key, fetchFn = fetch) {
  if (!key) throw new Error("An API key is required. Get a free one at openweathermap.org.");
  const res = await fetchFn(buildUrl(city, key));
  if (!res.ok) {
    if (res.status === 401) throw new Error("Invalid API key");
    if (res.status === 404) throw new Error(`City "${city}" not found`);
    throw new Error(`HTTP ${res.status} ${res.statusText}`);
  }
  return summarise(await res.json());
}
