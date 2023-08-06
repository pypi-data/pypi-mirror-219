import pyximport; 
pyximport.install()
import utils
#
### test verify_lat_lng_py
#assert utils.verify_lat_lng_py(40, -105) == (40, -105)
#assert utils.verify_lat_lng_py(-91, -181) == (-85.05112878, -180.0)
#
#
## test geo_to_web_mecator_tile_py 
#assert utils.geo_to_web_mecator_tile_py(40, 105, 7) == (101, 48)
#assert utils.geo_to_web_mecator_tile_py(40, -105, 7) == (26, 48)
#assert utils.geo_to_web_mecator_tile_py(-90, -180, 1) == (0,1)
#assert utils.geo_to_web_mecator_tile_py(90, 180, 1) == (1,0)

#for i in range(1,23):
#    print(utils.geo_to_web_mecator_tile_py(40, 105, i), i)
#print(utils.web_mecator_tile_to_geo_py(1747626, 3175752, 23))

print(
    utils.tile_to_corner_py(
        *utils.geo_to_tile_py(40, 105, 22),
        22,
        0
    ),
    utils.tile_to_corner_py(
        *utils.geo_to_tile_py(40, 105, 22),
        22,
        1
    ),
    utils.tile_to_corner_py(
        *utils.geo_to_tile_py(40, 105, 22),
        22,
        2
    ),
    utils.tile_to_corner_py(
        *utils.geo_to_tile_py(40, 105, 22),
        22,
        3
    )
)
#print(utils.web_mercator_tile_to_quadkey_py(
#    utils.geo_to_web_mecator_tile_py(40, 105, 22)[0], 
#    utils.geo_to_web_mecator_tile_py(40, 105, 22)[1],
#    22
#)
#)
#
#print( utils.quadkey_to_web_mercator_tile_py(
#        utils.web_mercator_tile_to_quadkey_py(
#        utils.geo_to_web_mecator_tile_py(40, 105, 22)[0], 
#        utils.geo_to_web_mecator_tile_py(40, 105, 22)[1],
#        22
#    )
#    )
#)


