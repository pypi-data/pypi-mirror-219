import quadkey
lat = 47.641268
lng = -122.125679
zoom = 15

# Convert lat lng to quadkey
qk = quadkey.geo_to_quadkey(lat, lng, zoom)

# Convert quadkey to lat lng
## get top left corner
lat, lng = quadkey.quadkey_to_geo(qk, corner=0)
## get bottom right corner
lat, lng = quadkey.quadkey_to_geo(qk, corner=2)

# Convert quadkey to bbox
bbox = quadkey.quadkey_to_bbox(qk)

# Convert quadkey to Tile
tl = quadkey.quadkey_to_tile(qk)

# Conver quadkey to quadint
qi = quadkey.quadkey_to_quadint(qk)

# Convert lat lng to quadint
qi = quadkey.geo_to_quadint(lat, lng, zoom)

# get parent quadkey
parent = quadkey.quadkey_to_parent(qk)


print(
    qk,
    lat, lng,
    bbox,
    tl,
    qi
)