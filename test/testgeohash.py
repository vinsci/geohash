import sys

# import geohash

# Test the source tree, not an installed version.
sys.path.insert(0, "../Geohash")

if __name__ == "__main__":
    import doctest

    print("Testing tests in README.rst...")
    doctest.testfile("../README.rst")
