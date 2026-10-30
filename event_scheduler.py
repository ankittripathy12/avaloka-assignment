"""Event scheduler: overlap check, minimum rooms, and room assignment."""
import heapq
from typing import List, Tuple

Event = Tuple[int, int]


def can_attend_all(events: List[Event]) -> bool:
    """True if no two events overlap (end == start is NOT an overlap)."""
    ordered = sorted(events)
    for i in range(1, len(ordered)):
        if ordered[i][0] < ordered[i - 1][1]:
            return False
    return True


def min_rooms_required(events: List[Event]) -> int:
    """Minimum number of rooms so that every event gets one."""
    if not events:
        return 0
    ordered = sorted(events)
    end_times = []  # min-heap of end times of rooms in use
    max_rooms = 0
    for start, end in ordered:
        if end_times and end_times[0] <= start:
            heapq.heappop(end_times)  # reuse a room that has freed up
        heapq.heappush(end_times, end)
        max_rooms = max(max_rooms, len(end_times))
    return max_rooms


def room_name(rid: int) -> str:
    """0 -> 'Room A', 25 -> 'Room Z', 26 -> 'Room AA', ... (no upper limit)."""
    n, letters = rid + 1, ""
    while n:
        n, r = divmod(n - 1, 26)
        letters = chr(ord("A") + r) + letters
    return f"Room {letters}"


def assign_rooms(events: List[Event]) -> List[str]:
    """Assign a room name to each event (in original order) using the minimum rooms."""
    ordered = sorted(enumerate(events), key=lambda x: x[1])
    busy, free = [], []  # busy: (end_time, room_id); free: room_ids
    next_id = 0
    assignment = {}      # original index -> room name
    for idx, (start, end) in ordered:
        while busy and busy[0][0] <= start:
            _, rid = heapq.heappop(busy)
            heapq.heappush(free, rid)
        if free:
            rid = heapq.heappop(free)
        else:
            rid = next_id
            next_id += 1
        assignment[idx] = room_name(rid)
        heapq.heappush(busy, (end, rid))
    return [assignment[i] for i in range(len(events))]
