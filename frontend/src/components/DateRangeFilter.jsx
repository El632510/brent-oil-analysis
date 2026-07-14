import { useState } from "react";

export default function DateRangeFilter({ onApply }) {
  const [startDate, setStartDate] = useState("2019-06-01");
  const [endDate, setEndDate] = useState("2020-12-31");

  function handleApply() {
    onApply(startDate, endDate);
  }

  return (
    <div className="filter-bar">
      <label>
        Start date
        <input
          type="date"
          value={startDate}
          onChange={(event) => setStartDate(event.target.value)}
        />
      </label>
      <label>
        End date
        <input
          type="date"
          value={endDate}
          onChange={(event) => setEndDate(event.target.value)}
        />
      </label>
      <button onClick={handleApply}>Apply range</button>
    </div>
  );
}
