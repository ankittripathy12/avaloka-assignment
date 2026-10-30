import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from event_scheduler import can_attend_all, min_rooms_required, assign_rooms, room_name


def test_can_attend_all_true():
    assert can_attend_all([(9, 10), (10, 11), (11, 12)]) is True


def test_can_attend_all_false():
    assert can_attend_all([(9, 11), (10, 12)]) is False


def test_can_attend_all_empty():
    assert can_attend_all([]) is True


def test_can_attend_all_unsorted_input():
    assert can_attend_all([(11, 12), (9, 10), (10, 11)]) is True


def test_min_rooms_adjacent_events():
    assert min_rooms_required([(9, 10), (10, 11)]) == 1


def test_min_rooms_overlap():
    assert min_rooms_required([(9, 12), (10, 11), (11, 13)]) == 2


def test_min_rooms_empty():
    assert min_rooms_required([]) == 0


def test_min_rooms_all_identical():
    assert min_rooms_required([(0, 10)] * 5) == 5


def test_assign_rooms_matches_min_rooms():
    events = [(9, 12), (10, 11), (11, 13)]
    rooms = assign_rooms(events)
    assert len(set(rooms)) == min_rooms_required(events)


def test_assign_rooms_no_double_booking():
    events = [(9, 12), (10, 11), (11, 13), (9, 10), (12, 14)]
    rooms = assign_rooms(events)
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            if rooms[i] == rooms[j]:
                a, b = events[i], events[j]
                assert a[1] <= b[0] or b[1] <= a[0]


def test_room_names_beyond_26():
    many = [(0, 10)] * 30
    assert len(set(assign_rooms(many))) == 30
    assert room_name(0) == "Room A"
    assert room_name(25) == "Room Z"
    assert room_name(26) == "Room AA"
    assert room_name(27) == "Room AB"
