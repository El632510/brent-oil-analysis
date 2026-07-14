import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
} from "recharts";

export default function PriceChart({ prices, changePoint, events }) {
  if (!prices || prices.length === 0) {
    return <p className="loading-state">No price data in this range.</p>;
  }

  const changePointInRange =
    changePoint &&
    prices.some((row) => row.Date === changePoint.change_point_date);

  const eventsInRange = (events || []).filter((event) =>
    prices.some((row) => row.Date === event.event_date)
  );

  return (
    <div>
      <ResponsiveContainer width="100%" height={380}>
        <LineChart data={prices} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid stroke="#262b35" strokeDasharray="3 3" />
          <XAxis
            dataKey="Date"
            tick={{ fill: "#8b93a1", fontSize: 11 }}
            minTickGap={40}
          />
          <YAxis
            tick={{ fill: "#8b93a1", fontSize: 11 }}
            domain={["auto", "auto"]}
            width={50}
          />
          <Tooltip
            contentStyle={{
              background: "#1a1e26",
              border: "1px solid #262b35",
              borderRadius: 6,
              fontSize: 12,
            }}
            labelStyle={{ color: "#c98a3b" }}
          />
          <Line
            type="monotone"
            dataKey="Price"
            stroke="#c98a3b"
            dot={false}
            strokeWidth={1.6}
          />

          {changePointInRange && (
            <ReferenceLine
              x={changePoint.change_point_date}
              stroke="#e8e6df"
              strokeDasharray="4 4"
              label={{
                value: "Structural break",
                position: "insideTopLeft",
                fill: "#e8e6df",
                fontSize: 11,
              }}
            />
          )}

          {eventsInRange.map((event) => (
            <ReferenceLine
              key={event.event_name}
              x={event.event_date}
              stroke="#6fa287"
              strokeDasharray="2 2"
            />
          ))}
        </LineChart>
      </ResponsiveContainer>

      {changePointInRange && (
        <div className="change-point-callout">
          The Bayesian change point model detects a structural break on{" "}
          <strong>{changePoint.change_point_date}</strong>. Average daily
          price shifted from <strong>${changePoint.avg_price_before}</strong>{" "}
          to <strong>${changePoint.avg_price_after}</strong>, a{" "}
          <strong>{changePoint.price_pct_change}%</strong> change, with{" "}
          {Math.round(changePoint.prob_mean_increased * 100)}% posterior
          probability that the mean daily return increased afterward.
        </div>
      )}
    </div>
  );
}
