## JMAG Tool

This document explains how the eMach component creation workflow is implemented for JSOL JMAG Designer.

### Background
The geometry creation workflow in eMach is as follows:

1. Draw a cross-section geometry.
2. Extrude or revolve the cross-section. eMach prvides the tool geometric coordinate `innerCoord` that is located somewhere within the cross-section. 
3. Assign materials.

The workflow for geometry creation in JMAG is listed below:
1. Draw a cross-section geometry.
2. Create regions.
3. If more than one region is created in Step 2, delete unnecessary regions.
4. Extrude the region.
5. Create a study.
6. Add the geometry to the study.
7. Assign materials.

The JMAG function to create regions simply converts any closed geometry (bounded by lines and arcs) into a region. For example, if the stator cross-section of a radial flux machine is drawn, JMAG creates two regions: `region 1`: a region consisting the stator teeth and yoke, and `region 2`: a region with the stator bore and slots. If this geometry is extruded, it will result in a solid cylinder. So, the unnecessary region (`region 2`) must be identified and deleted before extrusion.  

## Implementation in eMach
When working within JMAG Designer's GUI, one can select the unnecessary region and delete it manually. However, this is challenging to do programmatically because of the following reasons:

1. The `CreateRegions()` function in JMAG takes no arguments. So, there is no way to specify where to create JMAG geometry regions. All closed geometries are simply converted to JMAG geometry regions.
2. The `CreateRegions()` function does not return the name or any other information about the regions created. 

The eMach workflow provides a coordinate `innerCoord` inside every cross-section to be extruded. This `innerCoord` will be inside the geometry region that the user desires to retain. With this information, the following approach is used to create only the desired geometry region:

1. In the `prepareSection()` function, after drawing the cross-section, the number of geometry items in the JMAG drawing is obtained. This is done using the `NumItems()` function.
2. The JMAG geometry regions are created using the `CreateRegions()` function.
3. The number of geometry items after region creation is obtained by calling `NumItems()`.
4. The difference between the number of geometry items in Step 3 and Step 1 gives the total number of regions created in Step 2.
5. JMAG names regions in the format `region, region.2, region.3,......region.n` if there are `n` regions. So, knowing the number of regions created, an array of region names is populated.
6. The `innerCoord` is used with the `SelectAtCoordinateDlg()` function to select the desired region to be kept.
7. The `GetSelection()` function is used to get the name of the selected region which is to be retained.
8. The region name obtained in step 7 is compared with the array of region names populated in Step 5. All unnecessary regions created by JMAG are deleted.

The desired region is left behind and can then be extruded or revolved.

**Note:** The steps listed above to delete the undesired regions rely on JMAG's region naming convention. If future versions of JMAG update the naming of geometry regions, the JMAG implementation will need to be revised.

