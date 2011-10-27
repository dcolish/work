"""
Data struct for storing timed events

{
  active_event: hash,
  active_start_time: timestamp
  paused events: [hash],
  events: { hash:
                {
                  cumulative_time: calculated_timedelta
                  name: "Local name for event"
                  timed_things: [
                                  [start_time<timestamp>, end_time<timestamp>],
                                ],
                 }
          }
}

Managing an Event
-----------------

When an `event` is started, the description is hashed and placed into the
`active_event` key; a starting timestamp is placed into the `active_starttime`
key. The event is also placed into the events key with a `cumulative_time` of 0.

When another event is stopped, the event's hash is moved from `active_event` key
to the `paused_events` list. The `active_starttime` is moved to the event's
record and stored with the ending timestamp. A timedelta is also calculated for
these and placed into the `cumulatimve_time` for the event's record.

The paused_events queue should be sorted by the last event stopped
"""
from datetime import datetime, timedelta
from hashlib import sha1


def event(name):
    return {
        'cumulative_time': timedelta(),
        'name': name,
        'time_chunks': [],
        }


def start_event(name):
    hash_ = sha1(name)
    start_time = datetime.utcnow()
    ev = event(name)
    return hash_, start_time, ev


def stop_event(ev, active_start_time):
    now = datetime.utcnow()
    ev['cumulative_time'] = now - active_start_time
    ev['time_chunks'].append(active_start_time, now)
