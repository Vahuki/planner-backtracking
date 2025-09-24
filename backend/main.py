from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# Cho phép frontend truy cập API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import Optional

class Section(BaseModel):
    id: str
    teacher: str
    group: str
    duration: int
    students: int
    preferred: Optional[List[str]] = None 



class InputData(BaseModel):
    timeslots: List[str]
    sections: List[Section]
    teachers: Dict[str, Dict[str, List[str]]] = {}
    groups: Optional[Dict[str, Dict[str, List[str]]]] = {}
    rooms: Dict[str, Dict] = {}


def backtrack(idx, sections, timeslots, teachers, groups, rooms, schedule, used):
    if idx == len(sections):
        return True

    sec = sections[idx]
    for t in timeslots:
        slot_idx = timeslots.index(t)
        if slot_idx + sec.duration > len(timeslots):
            continue
        slots = timeslots[slot_idx:slot_idx+sec.duration]

        if any(s in teachers.get(sec.teacher, {}).get("unavailable", []) for s in slots):
            continue
        if any(s in groups.get(sec.group, {}).get("unavailable", []) for s in slots):
            continue

        conflict = False
        for s in slots:
            if sec.teacher in used.get(s, {}).get("teachers", []):
                conflict = True
                break
            if sec.group in used.get(s, {}).get("groups", []):
                conflict = True
                break
        if conflict:
            continue

        room_assigned = None
        for rname, rdata in rooms.items():
            if sec.students <= rdata.get("capacity", 9999) and all(s not in rdata.get("unavailable", []) for s in slots):
                if all(rname not in used.get(s, {}).get("rooms", []) for s in slots):
                    room_assigned = rname
                    break
        if not room_assigned:
            continue

        for s in slots:
            if s not in used:
                used[s] = {"teachers": [], "groups": [], "rooms": []}
            used[s]["teachers"].append(sec.teacher)
            used[s]["groups"].append(sec.group)
            used[s]["rooms"].append(room_assigned)

        schedule[sec.id] = {"slots": slots, "room": room_assigned}

        if backtrack(idx+1, sections, timeslots, teachers, groups, rooms, schedule, used):
            return True

        for s in slots:
            used[s]["teachers"].remove(sec.teacher)
            used[s]["groups"].remove(sec.group)
            used[s]["rooms"].remove(room_assigned)
        del schedule[sec.id]

    return False

@app.post("/solve")
def solve(data: InputData):
    rooms = data.rooms if data.rooms else {"R1": {"capacity": 9999, "unavailable": []}}

    schedule = {}
    used = {}
    success = backtrack(
        0, data.sections, data.timeslots, data.teachers, data.groups, rooms, schedule, used
    )
    if success:
        return {"ok": True, "schedule": schedule}
    else:
        return {"ok": False, "message": "No valid schedule found"}

