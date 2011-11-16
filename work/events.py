# Copyright Dan Colish
# All rights reserved.
#
# This file is part of 'Work' and is distributed under the GPLv3 license.
# See LICENSE for more details.

# TODO:dc:
# Rethink using hashes as the dict keys, might be overkill
# How to speed up sync with file
# Should there be properties that alias dict keys

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
`active_event` key; a starting timestamp is placed into the `active_start_time`
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


class Event(dict):
    def __init__(self, name, dict_=None):
        if not dict_:
            self.update({
                    'cumulative_time': timedelta().total_seconds(),
                    'name': name,
                    'time_chunks': [],
                    })
        else:
            self.update(dict_)

    def __hash__(self):
        return hash(sha1(self['name']).hexdigest())

    def __str__(self):
        return ' '.join(
            (self['name'],
             str(timedelta(seconds=int(self['cumulative_time'])))))

    @classmethod
    def inflate(cls, dict_):
        name = dict_.get('name')
        if name:
            return Event(name, dict_)
        return dict_

    def stop(self, active_start_time):
        now = datetime.utcnow()
        active_datetime = datetime.strptime(
            active_start_time, '%Y-%m-%dT%H:%M:%S.%f')
        cumulative_time = timedelta(seconds=int(self['cumulative_time']))
        self['cumulative_time'] = (
            cumulative_time + (now - active_datetime)).total_seconds()
        self['time_chunks'].append((active_start_time, now.isoformat()))


default_data = {
    'active_start_time': None,
    'active_event_hash': None,
    'events': {},
    'previous_events': [],
    }


class EventManager(object):

    def __init__(self, storage_path):
        self.storage_path = abspath(storage_path)
        self._sync(dirty=False)

    def _reset_active(self):
        hash_ = self._data['active_event_hash']
        time_ = self._data['active_start_time']
        self._data['active_event_hash'] = None
        self._data['active_start_time'] = None
        return hash_, time_

    # XXX:dc: should this not be part of the event manager class?
    def _sync(self, dirty):
        if dirty:
            with open(self.storage_path, "w+") as f:
                dump(self._data, f)
                self._is_dirty = False
        else:
            if exists(self.storage_path):
                with open(self.storage_path, "r+") as f:
                    try:
                        self._data = load(f, object_hook=Event.inflate)
                    except ValueError:
                        self._data = default_data
            else:
                self._data = default_data

    def delete(self, name):
        ev_hash = sha1(name).hexdigest()
        if ev_hash == self._data['active_event_hash']:
            self._reset_active()
        del self._data['events'][ev_hash]
        self._sync(dirty=True)

    def list(self):
        for k, ev in self._data['events'].items():
            print ev

    def reset(self, name):
        ev_hash = sha1(name).hexdigest()
        ev = self._data['events'].get(ev_hash, Event(name))
        ev['cumulative_time'] = 0
        self._data['events'].update({ev_hash: ev})
        self._sync(dirty=True)

    def start(self, name=None):
        if self._data['active_event_hash']:
            self.stop()
        if not name:
            ev_hash = self._data.get('last_event')
        else:
            ev_hash = sha1(name).hexdigest()
        ev = self._data['events'].get(ev_hash, Event(name))
        ev_start = datetime.utcnow().isoformat()
        self._data['active_event_hash'] = ev_hash
        self._data['active_start_time'] = ev_start
        self._data['events'].update({ev_hash: ev})
        self._sync(dirty=True)

    def status(self):
        active_event_hash = self._data['active_event_hash']
        if active_event_hash:
            print self._data['events'][active_event_hash]
        else:
            print "Nothing active"

    def stop(self):
        active_event_hash, active_start_time = self._reset_active()
        ev = self._data['events'].get(active_event_hash)
        if not ev:
            return
        self._data['last_event'] = active_event_hash
        ev.stop(active_start_time)
        self._data['events'].update({active_event_hash: ev})
        self._sync(dirty=True)
        print ev
