from shapely.geometry import Point, Polygon

# the plane (or a finite square of it)
R = Polygon([(-3, -3), (-3, 5), (5, 5), (5, -3)])

# center points for some basic regions
centers = [(1, 2), (0, 0), (2, 0), (3, 2), (1, 1), (1.75, 0.85)]

# specify six basic regions
A1 = Point(centers[0]).buffer(2)
A2 = Point(centers[1]).buffer(2)
A3 = Point(centers[2]).buffer(2)
A4 = Point(centers[3]).buffer(1.5)
A5 = Point(centers[4]).buffer(0.3)
A6 = Point(centers[5]).buffer(2.2)

basic_regions = {A1, A2, A3, A4, A5, A6}
