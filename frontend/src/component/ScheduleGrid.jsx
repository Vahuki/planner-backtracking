import React from "react";

function ScheduleGrid({ timeslots, schedule }) {
  // Lấy danh sách ngày (Mon, Tue, …)
  const days = [...new Set(timeslots.map(t => t.split("-")[0]))];
  // Lấy danh sách tiết (1,2,3…)
  const periods = [...new Set(timeslots.map(t => t.split("-")[1]))];

  return (
    <div className="table-responsive">
      <table className="table table-bordered text-center">
        <thead className="table-light">
          <tr>
            <th>Tiết</th>
            {days.map(day => (
              <th key={day}>{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {periods.map(period => (
            <tr key={period}>
              <td><strong>{period}</strong></td>
              {days.map(day => {
                const slot = `${day}-${period}`;
                const found = Object.entries(schedule).find(([id, info]) =>
                  info.slots.includes(slot)
                );
                return (
                  <td key={day}>
                    {found ? (
                      <div>
                        <div><b>{found[0]}</b></div>
                        <div className="text-muted">{found[1].room}</div>
                      </div>
                    ) : (
                      "-"
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ScheduleGrid;
