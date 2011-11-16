Work
====

Stupid simple time tracking

Tracking time for your agile work shouldn't be hard. Work is here to help keep
it that way. Starting tasks starts the timer. Starting another stops any which
are in progress. You can also manually stop. Listing shows a nice chart of what
you've done and gives me detail only when you ask for it.

Usage
=====

Eventually the recorded time spans will be shown to the user to give insite into
work habits. For now the cummulative is the only user facing data show and can
be reset to only track the most relevent time span for an event.


The command interface for work is terminal based. To start a task::

    $ work start mytask

To stop a task::
   
    $ work stop

This will stop the currently active task. To start that same task again::

    $ work start

To get the status on what job is currently running::
    
    $ work status

To see all the tasks with their cummulative time::

    $ work list

To reset the cummulative time, this will not delete all the recorded timespans::

    $ work reset


Availability
============

The git `work HEAD`_ can be installed via ``pip install work==dev``.

.. _work HEAD: https://github.com/dcolish/work/tarball/master#egg=work-dev

