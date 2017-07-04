{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}

-- the content concept of an event
-- core questions: when did this event happen? what happened before? what participants does the event have?
-- events are instantiated process portions with fields, objects, and networks as participants
-- an event collection is an event (in analogy to a feature collection being a feature)
-- (c) Werner Kuhn
-- latest change: Feb 6, 2016
-- To Do
-- compute event outcomes: central, but how to specify? do simple examples

module Event where

import Time

-- the class of all event types
-- Eq captures identity
-- events are bounded in time, but do not need an explicit boundary
{-
class Eq (event time) => EVENTS event time where
    bounds :: event time -> Interval time

data InstantEvent time = InstantEvent (Instant time) deriving (Eq, Show)

instance (Eq time, Ord time) => EVENTS InstantEvent time where
    bounds (InstantEvent (Instant t1 trs1)) = Interval (Instant t1 trs1) (Instant t1 trs1)

-- TESTS
ie1, ie2 :: InstantEvent Int
ie1 = InstantEvent i1
ie2 = InstantEvent i2
et1 = bounds ie1
    -}

class Eq event => EVENTS event where
    bounds :: event -> Period
    same :: event -> event -> Bool
    during :: event -> event -> Bool
    before :: event -> event -> Bool
    after :: event -> event -> Bool
    overlap :: event -> event -> Bool

data InstantEvent = InstantEvent Instant deriving (Eq, Show)

instance EVENTS InstantEvent where
    bounds (InstantEvent time) = (time, time)
    same e1 e2 = e1 == e2
    during (InstantEvent t1) (InstantEvent t2) = t1 == t2
    before (InstantEvent t1) (InstantEvent t2) = t1 < t2
    after (InstantEvent t1) (InstantEvent t2) = t1 > t2
    overlap = during -- just in the case of an instant event

data IntervalEvent = IntervalEvent Instant Instant deriving (Eq, Show)

instance EVENTS IntervalEvent where
    bounds (IntervalEvent s e) = (s, e)
    same e1 e2 = e1 == e2
    during (IntervalEvent s1 e1) (IntervalEvent s2 e2) = s1 > s2 && e1 < e2
    before (IntervalEvent s1 e1) (IntervalEvent s2 e2) = e1 <= s2
    after (IntervalEvent s1 e1) (IntervalEvent s2 e2) = e2 <= s1
    overlap (IntervalEvent s1 e1) (IntervalEvent s2 e2) = s2 <= e1 && e1 <= e2 || s1 <= e2 && e2 <= e1

e = IntervalEvent (timestamp (date 2017 07 03) (time 16 57 00)) (timestamp (date 2017 07 03) (time 18 00 00))

