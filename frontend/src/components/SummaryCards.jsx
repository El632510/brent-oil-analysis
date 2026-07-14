function formatUsd(value) {
  return `$${Number(value).toFixed(2)}`;
}

export default function SummaryCards({ summary, changePoint }) {
  if (!summary || !changePoint) return null;

  const priceChangeIsDecline = changePoint.price_pct_change < 0;

  return (
    <div className="summary-grid">
      <div className="panel summary-card">
        <p className="label">Date range</p>
        <p className="value" style={{ fontSize: 16 }}>
          {summary.date_range_start} - {summary.date_range_end}
        </p>
      </div>

      <div className="panel summary-card">
        <p className="label">Average price</p>
        <p className="value">{formatUsd(summary.avg_price)}</p>
      </div>

      <div className="panel summary-card">
        <p className="label">Detected change point</p>
        <p className="value" style={{ fontSize: 16 }}>{changePoint.change_point_date}</p>
      </div>

      <div className="panel summary-card">
        <p className="label">Price shift at change point</p>
        <p className={`value ${priceChangeIsDecline ? "decline" : "incline"}`}>
          {priceChangeIsDecline ? "" : "+"}
          {changePoint.price_pct_change}%
        </p>
      </div>
    </div>
  );
}
