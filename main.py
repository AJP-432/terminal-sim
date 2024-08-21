import pygame
from game_map import Map
from navigation import ShortestPathFinder
from simulator import Simulator
from unit import * 
import time

obj = {
   "p2Units":[
      [
      ],
      [
         
      ],
      [
         [0, 14, 75, ""],
      ],
      [
         
      ],
      [
         
      ],
      [
         
      ],
      [
         
      ],
      [
         
      ]
   ],
   "turnInfo":[
      1,
      1,
      72,
      160
   ],
   "p1Stats":[
      40.0,
      17.0,
      8.8,
      1970
   ],
   "p1Units":[
      [
         
      ],
      [
         [1, 12, 30, ""]
      ],
      [
         
      ],
      [
        [0, 13, 12, ""],
        [0, 13, 12, ""],
        [0, 13, 12, ""],
      ],
      [
         
      ],
      [
         
      ],
      [
         
      ],
      [
         
      ]
   ],
   "p2Stats":[
      40.0,
      29.0,
      0.0,
      5
   ],
   "events":{
      "selfDestruct":[
         
      ],
      "breach":[
         
      ],
      "damage":[
         [
            [
               18,
               14
            ],
            15.0,
            5,
            "28",
            2
         ]
      ],
      "shield":[
         
      ],
      "move":[
         
      ],
      "spawn":[
         
      ],
      "death":[
         [
            [
               18,
               14
            ],
            5,
            "28",
            2,
            False
         ]
      ],
      "attack":[
         [
            [
               18,
               12
            ],
            [
               18,
               14
            ],
            15.0,
            2,
            "11",
            "28",
            1
         ]
      ],
      "melee":[
         
      ]
   }
}

def main():
    a = time.time()
    sim = Simulator(obj)
    sim.run()
    print(sim.summarize())
    b = time.time()
    print(f"Time: {b - a} s")

if __name__ == "__main__":
    main()
