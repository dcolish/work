# Copyright Dan Colish
# All rights reserved.
#
# This file is part of 'Work' and is distributed under the GPLv3 license.
# See LICENSE for more details.

"""
Data struct for storing timed events

{
  active_event: hash,
  active_start_time: timestamp
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

When an event is stopped, the event's hash is removed from `active_event`. The
`active_starttime` is moved to the event's record and stored with the ending
timestamp. A timedelta is also calculated for these and placed into the
`cumulatimve_time` for the event's record.

The paused_events queue should be sorted by the last event stopped
"""
from datetime import datetime, timedelta
from hashlib import sha1
from json import dump, load
from os.path import abspath, exists


#TODO:dc: Make events into a class, probably should inherit from dict
def new_event(name):
    return {
        'cumulative_time': timedelta().total_seconds(),
        'name': name,
        'time_chunks': [],
        }


def format_event(ev):
    return ' '.join(
        (ev['name'], str(timedelta(seconds=int(ev['cumulative_time'])))))


def stop_event(ev, active_start_time):
    now = datetime.utcnow()
    active_datetime = datetime.strptime(
        active_start_time, '%Y-%m-%dT%H:%M:%S.%f')
    cumulative_time = timedelta(seconds=int(ev['cumulative_time']))
    ev['cumulative_time'] = (
        cumulative_time + (now - active_datetime)).total_seconds()
    ev['time_chunks'].append((active_start_time, now.isoformat()))
    return ev


default_data = {
    'active_start_time': None,
    'active_event_hash': None,
    'events': {},
    }


class EventManager(object):

    def __init__(self, storage_path):
        self.storage_path = abspath(storage_path)
        self._sync(dirty=False)

    def _sync(self, dirty):
        if dirty:
            with open(self.storage_path, "w+") as f:
                dump(self._data, f)
                self._is_dirty = False
        else:
            if exists(self.storage_path):
                with open(self.storage_path, "r+") as f:
                    try:
                        self._data = load(f)
                    except ValueError:
                        self._data = default_data
            else:
                self._data = default_data

    def start(self, name):
        self.stop()
        ev_hash = sha1(name).hexdigest()
        ev = self._data['events'].get(ev_hash, new_event(name))
        ev_start = datetime.utcnow().isoformat()
        self._data['active_event_hash'] = ev_hash
        self._data['active_start_time'] = ev_start
        self._data['events'].update({ev_hash: ev})
        self._sync(dirty=True)

    def list(self):
        for k, ev in self._data['events'].items():
            print format_event(ev)

    def stop(self):
        active_event_hash = self._data['active_event_hash']
        active_start_time = self._data['active_start_time']
        ev = self._data['events'].get(active_event_hash)
        if not ev:
            return
        stopped_ev = stop_event(ev, active_start_time)
        self._data['active_event_hash'] = None
        self._data['active_start_time'] = None
        self._data['events'].update({active_event_hash: stopped_ev})
        self._sync(dirty=True)
        print format_event(stopped_ev)
