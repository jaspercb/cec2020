import sys

import parser
import brain
import drone

def main(filename):
    [unscrambled, scrambled] = parser.parse_file(filename)
    d = drone.Drone(scrambled, 0, 0)
    b = brain.Brain(d, unscrambled)
    b.mainloop()

if __name__ == '__main__':
    main(sys.argv[1])
