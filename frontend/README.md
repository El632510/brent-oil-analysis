# Frontend (React Dashboard)

Interactive dashboard for exploring Brent oil prices, the detected
Bayesian change point, and associated events.

## Setup

```bash
cd frontend
npm install
```

## Running (development)

Make sure the backend is running first on port 5000 (see
`backend/README.md`) - Vite proxies `/api` requests to it.

```bash
npm run dev
```

Open http://localhost:5173.

## Building for production

```bash
npm run build
npm run preview
```

## Features

- **Summary cards**: date range, average price, detected change point
  date, and the price shift at that change point
- **Price chart** (Recharts): daily price line with a dashed marker at
  the detected change point and dotted markers at nearby researched
  events, plus a plain-language callout explaining the shift
- **Date range filter**: refetches price data for any custom window
- **Events list**: all researched events, with the ones nearest the
  detected change point highlighted

## Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── SummaryCards.jsx
│   │   ├── DateRangeFilter.jsx
│   │   ├── PriceChart.jsx
│   │   └── EventsList.jsx
│   ├── services/
│   │   └── api.js          # fetch wrappers for the Flask API
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── vite.config.js
└── package.json
```
