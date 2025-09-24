from typing import List, Dict, Optional, Set, Tuple

def contiguous_next(timeslots: List[str]) -> Dict[str, Optional[str]]:
    """Return next slot mapping for contiguous check. timeslots must be in order."""
    nxt = {}
    for i, t in enumerate(timeslots):
        nxt[t] = timeslots[i+1] if i+1 < len(timeslots) else None
    return nxt

def backtrack_schedule(
    sections: List[Dict],
    timeslots: List[str],
    teachers: Dict[str, Dict],
    groups: Dict[str, Dict],
    rooms: Optional[Dict[str, Dict]] = None,
    preassign: Optional[Dict[str, Tuple[str, Optional[str]]]] = None,
) -> Optional[Dict[str, Tuple[str, Optional[str]]]]:
    """
    Returns assignment: section_id -> (start_timeslot, room_id or None)
    sections: [{'id','teacher','group','duration'(int, default=1), 'preferred': []}]
    timeslots: ordered list e.g. ['Mon-1','Mon-2','Tue-1',...']
    teachers/groups: {id: {'unavailable': set(...) }}
    rooms: {room_id: {'capacity': int, 'unavailable': set(...)}} or None
    preassign: {section_id: (start_slot, room_id_or_null)}  # locked
    """

    if preassign is None:
        preassign = {}
    if rooms is None:
        rooms = {}

    for t in teachers.values():
        t.setdefault('unavailable', set())
    for g in groups.values():
        g.setdefault('unavailable', set())
    for r in rooms.values():
        r.setdefault('unavailable', set())

    sec_map = {s['id']: dict(s) for s in sections}
    for s in sec_map.values():
        s.setdefault('duration', 1)
        s.setdefault('preferred', [])

    nextmap = contiguous_next(timeslots)
    def slots_for(start: str, duration: int) -> Optional[List[str]]:
        out = []
        cur = start
        for _ in range(duration):
            if cur is None:
                return None
            out.append(cur)
            cur = nextmap[cur]
        return out

    for sid, (start, room) in preassign.items():
        if sid not in sec_map:
            return None
        s = sec_map[sid]
        need = s['duration']
        sls = slots_for(start, need)
        if sls is None:
            return None
        if any(t in teachers.get(s['teacher'], {}).get('unavailable', set()) for t in sls):
            return None
        if any(t in groups.get(s['group'], {}).get('unavailable', set()) for t in sls):
            return None
        if room:
            if any(t in rooms.get(room, {}).get('unavailable', set()) for t in sls):
                return None
            if 'students' in s and 'capacity' in rooms.get(room, {}):
                if rooms[room]['capacity'] < s['students']:
                    return None

    domains: Dict[str, List[Tuple[str, Optional[str]]]] = {}
    for sid, s in sec_map.items():
        possibilities = []
        for start in timeslots:
            sls = slots_for(start, s['duration'])
            if sls is None:
                continue
            if any(t in teachers.get(s['teacher'], {}).get('unavailable', set()) for t in sls):
                continue
            if any(t in groups.get(s['group'], {}).get('unavailable', set()) for t in sls):
                continue
            if rooms:
                for rid, rmeta in rooms.items():
                    if any(t in rmeta.get('unavailable', set()) for t in sls):
                        continue
                    if 'students' in s and 'capacity' in rmeta and rmeta['capacity'] < s['students']:
                        continue
                    possibilities.append((start, rid))
            else:
                possibilities.append((start, None))
        if sid in preassign:
            domains[sid] = [preassign[sid]]
        else:
            domains[sid] = possibilities
        if not domains[sid]:
            return None

    def mrv_key(sid):
        return (len(domains[sid]), -sec_map[sid].get('duration', 1))
    order = sorted(list(sec_map.keys()), key=mrv_key)

    assigned: Dict[str, Tuple[str, Optional[str]]] = {}
    occ_teacher: Dict[str, Set[str]] = {t: set() for t in timeslots}
    occ_group: Dict[str, Set[str]] = {t: set() for t in timeslots}
    occ_room: Dict[str, Set[str]] = {t: set() for t in timeslots}

    for sid, pair in preassign.items():
        start, rid = pair
        sls = slots_for(start, sec_map[sid]['duration'])
        assigned[sid] = pair
        for t in sls:
            occ_teacher[t].add(sec_map[sid]['teacher'])
            occ_group[t].add(sec_map[sid]['group'])
            if rid:
                occ_room[t].add(rid)

    def consistent_place(sid: str, start: str, rid: Optional[str]) -> bool:
        s = sec_map[sid]
        sls = slots_for(start, s['duration'])
        if sls is None:
            return False
        for t in sls:
            if s['teacher'] in occ_teacher[t]:
                return False
            if s['group'] in occ_group[t]:
                return False
            if rid and rid in occ_room[t]:
                return False
        return True

    def place(sid: str, start: str, rid: Optional[str]):
        s = sec_map[sid]
        sls = slots_for(start, s['duration'])
        assigned[sid] = (start, rid)
        for t in sls:
            occ_teacher[t].add(s['teacher'])
            occ_group[t].add(s['group'])
            if rid:
                occ_room[t].add(rid)

    def unplace(sid: str):
        start, rid = assigned[sid]
        s = sec_map[sid]
        sls = slots_for(start, s['duration'])
        for t in sls:
            occ_teacher[t].remove(s['teacher'])
            occ_group[t].remove(s['group'])
            if rid:
                occ_room[t].remove(rid)
        del assigned[sid]

    def dfs(idx: int) -> bool:
        if idx >= len(order):
            return True
        sid = order[idx]
        if sid in assigned:
            return dfs(idx + 1)

        dom = sorted(domains[sid], key=lambda pr: (0 if pr[0] in sec_map[sid].get('preferred', []) else 1))
        for start, rid in dom:
            if not consistent_place(sid, start, rid):
                continue
            # tentative place
            place(sid, start, rid)
            ok = True
            for other_sid in order[idx+1:]:
                if other_sid in assigned:
                    continue
                has_val = False
                for st2, r2 in domains[other_sid]:
                    if all(
                        (sec_map[other_sid]['teacher'] not in occ_teacher[t]) and
                        (sec_map[other_sid]['group'] not in occ_group[t]) and
                        (r2 is None or r2 not in occ_room[t])
                        for t in slots_for(st2, sec_map[other_sid]['duration'])
                    ):
                        has_val = True
                        break
                if not has_val:
                    ok = False
                    break
            if ok and dfs(idx + 1):
                return True
            unplace(sid)
        return False

    success = dfs(0)
    return assigned if success else None
