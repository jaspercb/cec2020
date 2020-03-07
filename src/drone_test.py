import copy

import unittest
import drone
import parser

class TestDrone(unittest.TestCase):
    unscrambled, scrambled = parser.parse_file("../data/easy.txt")

    def test_placing(self):
        stakk = copy.deepcopy(TestDrone.unscrambled)
        mydrone = drone.Drone(stakk, 0, 0)
        # import pdb; pdb.set_trace()
        self.assertEqual((0, (255, 0, 0)), mydrone.scan())

        mydrone.move(0, 1)
        self.assertEqual((0, (255, 0, 0)), mydrone.scan())

        mydrone.move(1, 0)
        self.assertEqual((1, (255, 165, 0)), mydrone.scan())

        mydrone.pickup()
        mydrone.dropoff((255, 165, 0), 1)
        self.assertEqual((1, (255, 165, 0)), mydrone.scan())

if __name__ == '__main__':
    unittest.main()

