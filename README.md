# Administrative Regions of Berlin / Lebensweltlich Orientierte Räume (LOR)

[![CC BY 3.0 DE](https://i.creativecommons.org/l/by/3.0/de/80x15.png)](https://creativecommons.org/licenses/by/3.0/de/)

The geo- and topojson files in this repository contain the geometries of Berlin's administrative regions on different levels of fidelity. These areas are commonly referred to when working with other data provided by the Berlin government. The amount of shapes in each file is as follows:

```
447 berlin-lor.planungsraeume.geojson
138 berlin-lor.bezirksregionen.geojson
60  berlin-lor.prognoseraeume.geojson
```

The files are automatically converted from the shapefiles found at [Lebensweltlich orientierte Räume (LOR) in Berlin](https://daten.berlin.de/datensaetze/lebensweltlich-orientierte-r%C3%A4ume-lor-berlin) by Berliner Datenportal, licensed under CC BY 3.0 DE. Further information on how to interpret the different data can be found when following the link.

The tools used for conversion are `gdal` (for converting shapefiles to geojson), `iconv` (for converting windows-1252 into utf-8) and `topojson` (for converting geojson to topojson).
