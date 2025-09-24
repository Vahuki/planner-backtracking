import React, { useState } from "react";
import ScheduleGrid from "./component/ScheduleGrid";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [tab, setTab] = useState("input");
  const [sections, setSections] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [schedule, setSchedule] = useState(null);

  const timeslots = [
    "Mon-1", "Mon-2", "Mon-3", "Mon-4", "Mon-5",
    "Tue-1", "Tue-2", "Tue-3", "Tue-4", "Tue-5",
    "Wed-1", "Wed-2", "Wed-3", "Wed-4", "Wed-5",
    "Thu-1", "Thu-2", "Thu-3", "Thu-4", "Thu-5",
    "Fri-1", "Fri-2", "Fri-3", "Fri-4", "Fri-5"
  ];

  const [form, setForm] = useState({
    id: "",
    teacher: "",
    group: "",
    students: "",
    duration: 1,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const addSection = (e) => {
    e.preventDefault();
    if (!form.id || !form.teacher || !form.group) {
      alert(" Vui lòng nhập đủ thông tin lớp");
      return;
    }
    setSections([
      ...sections,
      {
        id: form.id,
        teacher: form.teacher,
        group: form.group,
        students: parseInt(form.students) || 0,
        duration: parseInt(form.duration) || 1,
      },
    ]);
    setForm({ id: "", teacher: "", group: "", students: "", duration: 1 });
  };

  const solveSchedule = async () => {
  const payload = { 
    timeslots, 
    sections, 
    teachers: {},   
    groups: {}, 
    rooms: {}       
  };

  try {
    const res = await fetch("http://localhost:8000/solve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.ok) {
      setSchedule(data.schedule);
      setTab("result");
    } else {
      alert(data.message || "Không thể sắp lịch");
    }
  } catch (err) {
    alert("Lỗi kết nối backend");
  }
};


  return (
    <div className="container py-4">
      <h1 className="text-center text-primary fw-bold mb-4">
        Planner Lịch Học
      </h1>

      <div className="d-flex justify-content-center mb-4">
        <div className="btn-group">
          <button
            className={`btn ${tab === "input" ? "btn-primary" : "btn-outline-primary"}`}
            onClick={() => setTab("input")}
          >
            Nhập dữ liệu
          </button>
          <button
            className={`btn ${tab === "result" ? "btn-primary" : "btn-outline-primary"}`}
            onClick={() => setTab("result")}
            disabled={!schedule}
          >
            Kết quả
          </button>
        </div>
      </div>

      {tab === "input" && (
        <div className="card shadow">
          <div className="card-body">
            <h4 className="card-title mb-3"> Thêm lớp/môn</h4>
            <form onSubmit={addSection} className="row g-3">
              <div className="col-md-2">
                <input
                  type="text"
                  name="id"
                  placeholder="Mã lớp"
                  value={form.id}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
              <div className="col-md-2">
                <input
                  type="text"
                  name="teacher"
                  placeholder="Giáo viên"
                  value={form.teacher}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
              <div className="col-md-2">
                <input
                  type="text"
                  name="group"
                  placeholder="Nhóm"
                  value={form.group}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
              <div className="col-md-2">
                <input
                  type="number"
                  name="students"
                  placeholder="Số SV"
                  value={form.students}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
              <div className="col-md-2">
                <input
                  type="number"
                  name="duration"
                  placeholder="Tiết"
                  min="1"
                  value={form.duration}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
              <div className="col-md-2 d-grid">
                <button type="submit" className="btn btn-success">
                  Thêm lớp
                </button>
              </div>
            </form>

            {sections.length > 0 && (
              <div className="table-responsive mt-4">
                <table className="table table-bordered table-hover align-middle text-center">
                  <thead className="table-light">
                    <tr>
                      <th scope="col">Mã lớp</th>
                      <th scope="col">Giáo viên</th>
                      <th scope="col">Nhóm</th>
                      <th scope="col">Số SV</th>
                      <th scope="col">Tiết</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sections.map((s, i) => (
                      <tr key={i}>
                        <td>{s.id}</td>
                        <td>{s.teacher}</td>
                        <td>{s.group}</td>
                        <td>{s.students}</td>
                        <td>{s.duration}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {sections.length > 0 && (
              <div className="text-center mt-3">
                <button
                  onClick={solveSchedule}
                  className="btn btn-primary px-4"
                >
                  Solve lịch
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {tab === "result" && schedule && (
        <div className="card shadow mt-4">
          <div className="card-body">
            <h4 className="card-title mb-3"> Kết quả sắp lịch</h4>
            <ScheduleGrid timeslots={timeslots} schedule={schedule} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
