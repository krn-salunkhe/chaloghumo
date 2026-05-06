# External API Landscape & Signal Sources

This document categorizes real-world data sources that can be integrated into the ChaloGhumo "Understanding Engine." APIs are sorted by budget accessibility, with a priority on free and developer-friendly tiers.

## 1. Weather & Environmental Signals

*Foundational signals for the Environmental Domain.*

| API | Category | Budget | Official Link |
| :--- | :--- | :--- | :--- |
| **Open-Meteo** | Weather / Air Quality | **Free** (Non-commercial) | [open-meteo.com](https://open-meteo.com) |
| **OpenAQ** | Air Quality | **Free** (Open Source) | [openaq.org](https://openaq.org) |
| **OpenWeatherMap** | Weather | **Freemium** (1k calls/day) | [openweathermap.org](https://openweathermap.org) |
| **IQAir (AirVisual)** | Air Quality | **Freemium** (Limited calls) | [iqair.com](https://www.iqair.com) |
| **Tomorrow.io** | Weather / Hazards | **Premium** | [tomorrow.io](https://www.tomorrow.io) |

## 2. Destination & Geospatial Metadata

*Foundational data for the Geographic Domain.*

| API | Category | Budget | Official Link |
| :--- | :--- | :--- | :--- |
| **Teleport** | Urban Quality of Life | **Free** | [teleport.org](https://teleport.org) |
| **Trueway Places** | POI / Metadata | **Freemium** (Free tier) | [trueway.com](https://www.trueway.com) |
| **Google Places** | Search / Details | **Budget** ($200 monthly credit) | [mapsplatform.google.com](https://mapsplatform.google.com) |
| **Foursquare** | POI / Vibe | **Premium** | [foursquare.com](https://location.foursquare.com) |

## 3. Travel & Transportation Signals

*Real-time accessibility for the Societal Domain.*

| API | Category | Budget | Official Link |
| :--- | :--- | :--- | :--- |
| **TransitFeeds** | Bus / Train (GTFS) | **Free** (Community) | [transitfeeds.com](https://transitfeeds.com) |
| **OpenSky Network** | Flight Tracking | **Free** (Non-commercial) | [opensky-network.org](https://opensky-network.org) |
| **Amadeus** | Flights / Hotels | **Freemium** (Dev tier) | [developers.amadeus.com](https://developers.amadeus.com) |
| **Aviationstack** | Flight Status | **Freemium** (Limited calls) | [aviationstack.com](https://aviationstack.com) |
| **Skyscanner** | Flight Prices | **Premium** (Partner only) | [skyscanner.net](https://www.skyscanner.net) |

## 4. Social, Events & Crowd Density

*Human constraints for the Societal Domain.*

| API | Category | Budget | Official Link |
| :--- | :--- | :--- | :--- |
| **Eventbrite** | Local Events | **Freemium** (Public events) | [eventbrite.com](https://www.eventbrite.com/platform/api) |
| **Ticketmaster** | Major Events | **Freemium** (Discovery API) | [developer.ticketmaster.com](https://developer.ticketmaster.com) |
| **PredictHQ** | Crowds / Events | **Premium** | [predicthq.com](https://www.predicthq.com) |

---

## 🛠️ Integration Strategy

1. **Caching**: All external signals must be cached in **Redis** with a TTL (Time-To-Live) based on their velocity (e.g., 15 mins for weather, 24h for events).
2. **Weighted Truth**: If multiple APIs are used (e.g., Open-Meteo and OpenWeather), the system favors the source with the highest historical confidence for the specific region.
3. **Graceful Degradation**: If an external API is down, the system must fall back to "Historical Seasonal Averages" stored in PostgreSQL.
