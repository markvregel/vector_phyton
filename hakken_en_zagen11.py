# Hakken en zagen
# Mark ten Vregelaar and Jos Goris
# 18 January 2016

## Loading packages

from osgeo import ogr, osr
import os,os.path,mapnik

## set the workspace

workingdirect = '/media/user/Elements/geoscripting/python/lesson1' # should have data(with data) and fig folder
os.chdir(workingdirect)
print os.getcwd()
os.chdir('data')

## define driver
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )

## name shapefile and layer
fn = "some_cities.shp"
layername = "capitals"

## Create shape file
ds = drv.CreateDataSource(fn)

# Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')


## Create Layer
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)

## Create a list of points Amsterdam, Wageningen, Brussels, Berlin
pointslist = [[4.88969000, 52.3740300],[5.66667005, 51.9700000,],[4.3487800, 50.8504500],[13.4105300, 52.5243700]] 

## for loop to create layer with all points
for point_cor in pointslist:
  point = ogr.Geometry(ogr.wkbPoint)

  ## SetPoint(self, int point, double x, double y, double z = 0)
  point.SetPoint(0, point_cor[0], point_cor[1]) 
  
  ## Export to KML
  point.ExportToKML()
  
  ## define feature
  layerDefinition = layer.GetLayerDefn()
  feature = ogr.Feature(layerDefinition)

  ## add the point to the feature
  feature.SetGeometry(point)

  ## Lets store the feature in a layer
  layer.CreateFeature(feature)

## get the extent  
extent=layer.GetExtent() 
extent = [extent[0]-0.2, extent[2]-0.2, extent[1]+0.2, extent[3]+0.2] # change ton (minx, miny, maxx, maxy)xmin,

ds.Destroy()

## load into QGIS

##qgis.utils.iface.addVectorLayer(fn, layername, "ogr") 
##aLayer = qgis.utils.iface.activeLayer()
##print aLayer.name()

os.chdir(workingdirect)

#file with symbol for point
file_symbol=os.path.join("figs","arrow.png")

#First we create a map
map = mapnik.Map(800, 400) #This is the image final image size

#Lets put some sort of background color in the map
map.background = mapnik.Color("steelblue") # steelblue == #4682B4 

#Create the rule and style obj
r = mapnik.Rule()
s = mapnik.Style()

polyStyle= mapnik.PolygonSymbolizer(mapnik.Color("red"))
pointStyle = mapnik.PointSymbolizer(mapnik.PathExpression(file_symbol))
r.symbols.append(polyStyle)
r.symbols.append(pointStyle)

s.rules.append(r)
map.append_style("mapStyle", s)

# Adding point layer
layerPoint = mapnik.Layer("pointLayer")
layerPoint.datasource = mapnik.Shapefile(file=os.path.join("data",
                                        fn))

layerPoint.styles.append("mapStyle")

#adding polygon
layerPoly = mapnik.Layer("polyLayer")
layerPoly.datasource = mapnik.Shapefile(file=os.path.join("data",
                                        "ne_110m_land.shp"))
layerPoly.styles.append("mapStyle")

#Add layers to map
map.layers.append(layerPoly)
map.layers.append(layerPoint)

#Set boundaries 
boundsLL = (extent) #(minx, miny, maxx, maxy)
map.zoom_to_box(mapnik.Box2d(*boundsLL)) # zoom to bbox

mapnik.render_to_file(map, os.path.join("figs",
                                        "map3.png"), "png")
print "All done - check content"
