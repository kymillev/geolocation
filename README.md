# Automatic Georeferencing of Topographic Raster Maps

Supplementary code for the IJDAR submission: Automatic Georeferencing of Topographic Raster Maps

Note to editors: The code is not final and may be reformatted or cleaned.

## Datasets

### TOP50Raster

Full dataset can be downloaded [here](https://www.pdok.nl/downloads/-/article/dataset-basisregistratie-topografie-brt-topraster). Following map sheets were used: 31O, 32W, 32O, 38O, 39W, 39O, 44O, 45W, and 45O. The maps are in the GeoTif format, WGS84 coordinates of the corner points can be found with the functions described in **get_wgs84.py**. 

### M834 topographic raster maps of Belgium

These 16 maps are subject to copyright and can therefore not be shared publicly. They can be viewed online in [Cartesius](https://www.cartesius.be/CartesiusPortal/), you can search for each of the map's titles. Example for [Lebbeke-Merchtem](http://www.cartesius.be/arcgis/home/webmap/viewer.html?basemapUrl=http://www.ngi.be/tiles/arcgis/rest/services/25k__{C9BA3B31-8EDB-44DA-9F5A-D9884096433D}__default__404000/MapServer&lang=en) and its [metadata](https://www.cartesius.be/geoportal/catalog/search/resource/details.page?uuid=%7B84E5BEFF-D865-43F4-9165-1E6730680249%7D), you might have to use Internet Explorer. 

A full list of the maps used is given below:
* Aalter-Nevele
* Bassevelde-Zelzate
* Dendermonde-Puurs
* Dentergem-Deinze
* Evergem-Lochristi
* Gavere-Oosterzele
* Gent-Melle
* Knesselare-Zomergem
* Langelede-Stekene
* Lebbeke-Merchtem
* Maldegem-Eeklo
* Oordegem-Aalst
* Sint-Gillis-Waas-Beveren
* Sint-Niklaas-Temse
* Wetteren-Zele
* Zeveneken-Lokeren
