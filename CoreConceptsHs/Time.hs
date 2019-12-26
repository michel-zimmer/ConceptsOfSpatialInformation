-- basic time values and operations for core concepts
-- (c) Werner Kuhn
-- latest change: October 7, 2016

-- TO DO

module Time where

import Data.Time  -- Haskell's time library, see http://two-wrongs.com/haskell-time-library-tutorial   

type Instant = UTCTime
ts = (read "2016-07-01 19:16 UTC") :: Instant -- an arbitrary time stamp

type Duration = DiffTime

type Period = (Instant, Instant)

type Date = Day

instantIn :: Instant -> Period -> Bool
instantIn i p = (fst p) <= i && (snd p) >= i

-- Returns a date with input format year month day
date :: Integer -> Int -> Int -> Date
date y m d = let dt = fromGregorianValid y m d in
    case dt of
    Just t -> t
    Nothing -> error "No valid gregorian date."

-- Returns the time (input hour minute second) as a duration from midnight
time :: Integer -> Integer -> Integer -> Duration 
time h m s = secondsToDiffTime (h*60*60 + m*60 + s)

-- Returns a certain point in time
timestamp :: Date -> Duration -> Instant
timestamp d t = UTCTime d t
       
