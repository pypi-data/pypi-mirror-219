League Ranker
=============

|Build Status|

Given a collection of entrants and their scores, sort them and return their
ranked points.

The mechanism used to allocate the ranked points is a generalised form of that
used for the `Student Robotics <https://www.studentrobotics.org>`__ league
points (quote from the SR
`rulebook <https://www.studentrobotics.org/docs/rules>`__):

    The team with the **most** game points will be awarded 8 points
    towards the competition league. The team with the second most will
    be awarded 6. The team with the third most will be awarded 4 points,
    and the team with the fewest game points will be awarded 2 points.
    Teams whose robot was not entered into the round, or who were
    disqualified from the round, will be awarded no points.

    Tied robots will be awarded the average of the points that their
    combined positions would be awarded. Thus, three robots tied for
    first place would receive 6 points each (since this is
    ``(8+6+4)/3``).

The ranker supports an arbitrary number of entrants and zones (as long as there
are fewer entrants than zones) and will return points which follow the pattern
described above.

The points for the winning team will be 2 × the number of zones, points for
subsequent places reduce by 2 points per place. Ties are resolved as described
and as a result of the points per place reducing by two, the points for any
entrant will always be an integer.

It supports Python 3.7+.

Tests
~~~~~

Tests can be run for the current interpreter by running ``./run-tests`` or for
all supported available interpreters by running ``tox``.

.. |Build Status| image:: https://circleci.com/gh/PeterJCLaw/ranker.svg?style=svg
   :target: https://circleci.com/gh/PeterJCLaw/ranker
