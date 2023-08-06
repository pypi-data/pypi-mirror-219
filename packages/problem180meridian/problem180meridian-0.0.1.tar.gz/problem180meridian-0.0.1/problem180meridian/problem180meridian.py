import numpy as np
from osgeo import ogr


class GeometryHierarchyError(Exception):

    def __init__(self, *args, **kwargs):
        pass


# Arranges a set of polygons to find out which of them are within others
# If any of them is within others they are cut off while creating a new
# multipolygon
class GeometryHierarchy:

    def __init__(self, *geometries, main_geometry=None, level=0):

        assert (main_geometry is None) or isinstance(main_geometry, ogr.Geometry)

        self.main_geometry = main_geometry
        self.level = level
        self.geometries = []

        for geometry in geometries:
            self.joinGeometry(geometry)

    def __str__(self):

        if self.main_geometry is None:
            main_wkt = 'No main geometry'
        else:
            main_wkt = self.main_geometry.ExportToWkt()

        tab = '\n\t' + self.level*'\t'

        return tab.join([main_wkt] + [str(h) for h in self.geometries])

    def checkMainGeometry(self, geometry):

        if self.main_geometry is not None:

            if geometry.Within(self.main_geometry):
                # print('Geometry within')
                return 0

            elif self.main_geometry.Within(geometry):
                # print('Hierarchy within')
                return 2

            elif geometry.Intersects(self.main_geometry):
                raise GeometryHierarchyError('Unexpected intersection')

            else:
                # print('Out of main geometry')
                return 1

    def joinGeometry(self, geometry):

        assert isinstance(geometry, ogr.Geometry)

        main_geometry_check = self.checkMainGeometry(geometry)

        if main_geometry_check:
            return main_geometry_check

        new_hierarchy = GeometryHierarchy(main_geometry=geometry,
                                          level=self.level + 1)
        separate = True

        for i in range(len(self.geometries)-1, -1, -1):

            hierarchy = self.geometries[i]
            separate = self.geometries[i].joinGeometry(geometry)

            if separate == 0:
                # print('Joined hierarchy')
                return 0

            elif separate == 2:
                # Doesn't check if there're intersections within new_hierarchy
                # Need to fix if used for other polygons but raster footprints!
                new_hierarchy.geometries.append(self.geometries.pop(i))

            elif geometry.Intersects(hierarchy.main_geometry):
                raise GeometryHierarchyError('Unexpected intersection')

        if separate:
            self.geometries.append(new_hierarchy)
            return 0

        raise GeometryHierarchyError('Geometry not processed')

    def Multipolygon(self):

        if self.main_geometry is not None:
            multipolygon = self.main_geometry
            for hierarhy in self.geometries:
                multipolygon = multipolygon.Difference(hierarhy.Multipolygon())

        elif len(self.geometries) != 0:
            multipolygon = self.geometries[0].Multipolygon()
            for hierarhy in self.geometries[1:]:
                multipolygon = multipolygon.Union(hierarhy.Multipolygon())

        else:
            multipolygon = ogr.Geometry(6)

        return multipolygon


# Returns True if value is positive or zero and False if it is negative
def arrayNotNegative(array):
    return np.sign(np.sign(array) + 1).astype(bool)


# Checks if any segment in a pair of coordinates crosses 180th meridian
# It's considered so if abs(x2 - x1) > abs(x2_1 - x1_1) where
# xi_1 = xi + (xi < 0) * 360
# If any crossing is found a check_array is returned where crossing pairs
# are marked as True
def check180lon(coordinates):

    longitudes = np.array([p[0] for p in coordinates])
    signs = arrayNotNegative(longitudes)

    if list(np.unique(signs)) == [0, 1]:
        distances = abs(longitudes[1:] - longitudes[:-1])
        longitudes_fixed = longitudes + ((signs == 0) * 360)
        distances_fixed = abs(longitudes_fixed[1:] - longitudes_fixed[:-1])
        # Need to add small value below to avoid Python calculation errors
        check_array = arrayNotNegative(distances_fixed - distances + 0.000001)
        return True, check_array
    else:
        return False, None


# Creates coordinates for two points in a segment crossing 180th meridian
# Setting distance_from180lon one can separate them from each other and
# the meridian itself
def cross180lon(coord1, coord2, distance_from_180lon = 0):

    if coord1[0] > 0:
        assert coord2[0] < 0
        img_lon2 = coord2[0] + 360
        new_lon1 = 180 - abs(distance_from_180lon)
    else:
        assert coord2[0] >= 0
        img_lon2 = coord2[0] - 360
        new_lon1 = abs(distance_from_180lon) - 180

    if (img_lon2 - coord1[0]) == 0:
        angle_coef = 1
    else:
        angle_coef = (coord2[1] - coord1[1]) / (img_lon2 - coord1[0])

    new_lon2 = (-1) * new_lon1
    new_lat1 = coord1[1] + angle_coef * (new_lon1 - coord1[0])
    new_lat2 = coord2[1] + angle_coef * (new_lon2 - coord2[0])

    return (new_lon1, new_lat1), (- new_lon1, new_lat2)


# Split polygon geometry by the 180th meridian creating a multipolygon
def split180lon(coordinates, check, distance_from_180lon=0):

    assert len(coordinates) - 1 == len(check)
    assert coordinates[0] == coordinates[-1]
    chains=[[coordinates[0]]]

    for i in range(len(check)):

        if check[i]:
            chains[-1].append(coordinates[i+1])
        else:
            new_coord1, new_coord2 = cross180lon(*tuple(coordinates[i:i+2]),
                                    distance_from_180lon=distance_from_180lon)
            chains[-1].append(new_coord1)
            chains.append([new_coord2, coordinates[i+1]])

    # need to finish all the polygon chains to make correct wkt
    if len(chains) > 1:
        chains[0].extend(chains.pop())
        for chain in chains[1:]:
            chain.append(chain[0])

    wkt_list = ['MULTIPOLYGON (((%s)))' % ','.join(['%f %f' %
                (p[0], p[1]) for p in chain]) for chain in chains]

    polygons = [ogr.Geometry(wkt = wkt) for wkt in wkt_list]
    hierarchy = GeometryHierarchy(*polygons)
    multipolygon = hierarchy.Multipolygon()

    return multipolygon


# Split polygon/multipolygon geometry by the 180th meridian
def split180lonMultipolygon(coordinates, distance_from_180lon=0):

    hierarchy = GeometryHierarchy()

    for poly in coordinates:

        cross, check = check180lon(coordinates[0])

        if cross:
            hierarchy.joinGeometry(split180lon(poly, check,
                            distance_from_180lon=distance_from_180lon))
        else:
            hierarchy.joinGeometry(ogr.Geometry(wkt='MULTIPOLYGON (((%s)))' %
                            ','.join(['%f %f' % (p[0], p[1]) for p in poly])))

    return hierarchy.Multipolygon()
