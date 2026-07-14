import { useEffect, useState } from "react";
import SummaryCards from "./components/SummaryCards.jsx";
import DateRangeFilter from "./components/DateRangeFilter.jsx";
import PriceChart from "./components/PriceChart.jsx";
import EventsList from "./components/EventsList.jsx";
import { getPrices, getChangePointResults, getEvents, getSummaryStats } from "./services/api.js";

export default function App() {
  const [prices, setPrices] = useState(null);
  const [summary, setSummary] = useState(null);
  const [changePoint, setChangePoint] = useState(null);
  const [events, setEvents] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  async function loadInitialData() {
    try {
      const [summaryData, changePointData, eventsData] = await Promise.all([
        getSummaryStats(),
        getChangePointResults(),
        getEvents(),
      ]);
      setSummary(summaryData);
      setChangePoint(changePointData);
      setEvents(eventsData.events);

      const priceData = await getPrices(
        changePointData.analysis_window_start,
        changePointData.analysis_window_end
      );
      setPrices(priceData.prices);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDateRangeApply(startDate, endDate) {
    try {
      const priceData = await getPrices(startDate, endDate);
      setPrices(priceData.prices);
    } catch (err) {
      setError(err.message);
    }
  }

  if (error) {
    return <div className="error-state">Failed to load dashboard: {error}</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">Birhan Energies</p>
          <h1>Brent Crude Change Point Dashboard</h1>
          <p>Bayesian structural break detection linked to geopolitical and economic events</p>
        </div>
      </header>

      <SummaryCards summary={summary} changePoint={changePoint} />

      <div className="main-grid">
        <div className="panel">
          <p className="panel-title">Price history</p>
          <p className="panel-subtitle">
            Detected change point and nearby researched events overlaid on daily Brent price
          </p>
          <DateRangeFilter onApply={handleDateRangeApply} />
          {prices ? (
            <PriceChart prices={prices} changePoint={changePoint} events={events} />
          ) : (
            <p className="loading-state">Loading price data...</p>
          )}
        </div>

        <div className="panel">
          <p className="panel-title">Researched events</p>
          <p className="panel-subtitle">Highlighted entries are closest to the detected change point</p>
          {events ? (
            <EventsList events={events} changePoint={changePoint} />
          ) : (
            <p className="loading-state">Loading events...</p>
          )}
        </div>
      </div>
    </div>
  );
}
