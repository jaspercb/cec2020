import copy

import unittest
import drone
import brain
import parser

unscrambled, scrambled = parser.parse_file("../data/easy.txt")

class TestDrone(unittest.TestCase):
    def test_placing(self):
        stakk = copy.deepcopy(unscrambled)
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

class TestBrain(unittest.TestCase):
    def test_pathing(self):
        stakk = copy.deepcopy(unscrambled)
        mydrone = drone.Drone(stakk, 0, 0)
        mydrone.scan()
        mybrain = brain.Brain(mydrone, copy.deepcopy(scrambled))
        info, goodpath = mybrain.maxInformationPath((0, 0), (3, 3))
        self.assertEqual(info, 6)
        mybrain.travelPath(goodpath)
        info, goodpath = mybrain.maxInformationPath((3, 3,), (0, 0))
        self.assertEqual(info, 5)

class TestVoxelArray(unittest.TestCase):
    def test_gravity(self):
        unscrambled, scrambled = parser.parse_file("../data/overhang.txt")
        self.assertEqual(unscrambled[4][3][2], None)
        mydrone = drone.Drone(unscrambled, 4, 4)
        mydrone.pickup()
        self.assertNotEqual(unscrambled[4][3][2], None)
        # gravity better exist


if __name__ == '__main__':
    unittest.main()

