export default function EventsList({ events, changePoint }) {
  if (!events || events.length === 0) {
    return <p className="loading-state">No events loaded.</p>;
  }

  const associatedDates = new Set(
    (changePoint?.associated_events || []).map((event) => event.event_date.slice(0, 10))
  );

  const sortedEvents = [...events].sort((a, b) =>
    a.event_date < b.event_date ? 1 : -1
  );

  return (
    <ul className="event-list">
      {sortedEvents.map((event) => (
        <li
          key={event.event_name}
          className={`event-item ${associatedDates.has(event.event_date) ? "highlighted" : ""}`}
        >
          <p className="event-date">{event.event_date}</p>
          <p className="event-name">{event.event_name}</p>
          <p className="event-description">{event.description}</p>
          <span className="event-category">{event.category.replace(/_/g, " ")}</span>
        </li>
      ))}
    </ul>
  );
}
