import arcpy
from arcpy import env
import time

start = time.time()
arcpy.env.overwriteOutput = True
# Set File workspace
file_workspace = 'B:\\Risk\\Risk.gdb'
env.workspace = file_workspace

# buffer set up
Holdings = 'B:\\Risk\\Risk.gdb\\Holdings\\Holdings_Join'
Holdings_clip = 'B:\\Risk\\Risk.gdb\\Holdings\\Holdings'
distances = [1000, 4000]
unit = "Meters"
# Make a feature layer from Holdings Layer#

arcpy.MakeFeatureLayer_management(Holdings, 'Holdings_Layer')
end = time.time()
print (end - start)
start = time.time()
#open Map Document
mxd = arcpy.mapping.MapDocument(
            'N:\\GIS\Projects\\AA_Leith_Hawkins_TestBed\\Search_Cursor\\Search_Cursor_mxd.mxd')
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
legend = arcpy.mapping.ListLayoutElements(
        mxd, "LEGEND_ELEMENT", "Legend")[0]
legend.autoAdd = False
end = time.time()
print (end - start)
# searchcursor for evey row in dataset to interrogate Holdings Ref nuber#
with arcpy.da.SearchCursor(Holdings, ['Holding_Reference_Number'])as Holdings_Ref_cursor:
    for row in Holdings_Ref_cursor:
<<<<<<< HEAD
        print row[0]
        query = "Holding_Reference_Number = " + str(row[0])
        print query
        File_output = file_workspace + '\\' 'Buffer_' + str(row[0])
        # print File_output

        # Select Feature using the reference number from holdings layer
        arcpy.SelectLayerByAttribute_management('Holdings_Layer', 'NEW_SELECTION',
                                                "Holding_Reference_Number = " + str(row[0]))
        start = time.time()
        # Export holding to geodatabase
        Holding_Boundary = file_workspace + '\\' 'Holding_' + str(row[0])
        arcpy.management.CopyFeatures('Holdings_Layer', Holding_Boundary)

        # Mutliple ring Buffer using Selected Features
        arcpy.MultipleRingBuffer_analysis(
            'Holdings_Layer', File_output, distances, unit, "", "ALL")
        arcpy.MakeFeatureLayer_management(File_output, 'Buffer_Layer')
        # arcpy.Buffer_analysis("Holdings_Layer", ofc, var_Buffer, "FULL", "ROUND", "ALL", "")

        # Clip Holdings Buffer

        # Intersect Features
        Intersect_out_features = file_workspace + \
            '\\' 'Intersect_' + str(row[0])
        arcpy.Intersect_analysis(
            [Holdings_clip, File_output], Intersect_out_features, "", "", "INPUT")
        Dissolved_output_intersect = file_workspace + \
            '\\' 'Intersect_Dissolve_' + str(row[0])

        # Dissolve Fields based on Holding name and Distance
        Dissolve_fields_intersect = ['Holding_Name', 'distance']

        arcpy.Dissolve_management(
            Intersect_out_features, Dissolved_output_intersect, Dissolve_fields_intersect)

        Clip_output = file_workspace + '\\' 'Clip_' + str(row[0])
        arcpy.Clip_analysis(Holdings_clip, File_output, Clip_output)
        Dissolve_fields = ['Holding_Name']
        Dissolved_output = file_workspace + '\\' 'Dissolve_' + str(row[0])
        # print Dissolved_output
        arcpy.Dissolve_management(
            Clip_output, Dissolved_output, Dissolve_fields)

=======
        start = time.time()
        refNumber = str(row[0])
        print 'Holding:' + refNumber

        # Select the holding (eg a definition query)
        arcpy.Select_analysis('Holdings_Layer', 'in_memory/holding', "Holding_Reference_Number = " + refNumber)

        arcpy.Buffer_analysis('in_memory/holding', 'in_memory/buffer1km', "1000 Meters", "FULL", "ROUND", "ALL")
        arcpy.AddField_management("in_memory/buffer1km", "distance", "SHORT")
        arcpy.CalculateField_management("in_memory/buffer1km", "distance", 1)

        arcpy.Buffer_analysis('in_memory/holding', 'in_memory/buffer4km', "4000 Meters", "FULL", "ROUND", "ALL")
        arcpy.AddField_management("in_memory/buffer4km", "distance", "SHORT")
        arcpy.CalculateField_management("in_memory/buffer4km", "distance", 4)

        arcpy.Merge_management(["in_memory/buffer1km", "in_memory/buffer4km"], "in_memory/buffer")


        arcpy.Intersect_analysis([Holdings_clip, 'in_memory/buffer'], 'in_memory/intersect', "", "", "INPUT")

        arcpy.Dissolve_management('in_memory/intersect', 'in_memory/intersectDissolved', ['Holding_Name', 'distance'])

        arcpy.Clip_analysis(Holdings_clip, 'in_memory/buffer', 'in_memory/clip')

        arcpy.Dissolve_management('in_memory/clip', 'in_memory/dissolvedOutput', ['Holding_Name'])
>>>>>>> 3ec4552a5b239db1bbb35c9eefdb8d2998c6b84b
        # Export to Excel
        # Make Feature Layer Based on Disoveled Output Intersect and Dissolved
        # Layer

        arcpy.MakeFeatureLayer_management(
            Dissolved_output_intersect, 'Intersect_Layer')
        arcpy.MakeFeatureLayer_management(Dissolved_output, 'Dissolve_layer')

        Intersect_Selection_Excel = 'distance = 1000'
        # export selected records to excel
        arcpy.SelectLayerByAttribute_management(
            'Intersect_Layer', 'NEW_SELECTION', Intersect_Selection_Excel)
        Excel_Output = 'B:\\Risk\\Map_Output\\Map_output_2\\'
        Excel_Location = Excel_Output + '\\' + str(row[0]) + '.xls'
        # print Excel_Location
        arcpy.TableToExcel_conversion('Intersect_Layer', Excel_Location)
        # arcpy.SelectLayerByAttribute_management('Intersect_Layer', 'CLEAR_SELECTION')
        print 'Geoprocessing Complete'
        end = time.time()
        print (end - start)
        # start = time.time()
        # add Layers to the Map
        # mxd = arcpy.mapping.MapDocument(
        #     'N:\\GIS\Projects\\AA_Leith_Hawkins_TestBed\\Search_Cursor\\Search_Cursor_mxd.mxd')
        # df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
        # legend = arcpy.mapping.ListLayoutElements(
        #     mxd, "LEGEND_ELEMENT", "Legend")[0]
        # print legend
        # legend.autoAdd = False
        # end = time.time()
        # print (end - start)
        start = time.time()
        addLayer3 = arcpy.mapping.Layer(Dissolved_output)
        arcpy.ApplySymbologyFromLayer_management(addLayer3,
                                                 'C:\\Database_connections\\assesment_Model_lyr\\Intersect_3.lyr')
        addLayer3.showLabels = True
        arcpy.mapping.AddLayer(df, addLayer3, 'TOP')

        legend.autoAdd = True
        addLayer = arcpy.mapping.Layer(File_output)
        arcpy.ApplySymbologyFromLayer_management(
            addLayer, 'C:\\Database_connections\\assesment_Model_lyr\\Buffer.lyr')
        arcpy.mapping.AddLayer(df, addLayer, "TOP")

        addLayer2 = arcpy.mapping.Layer(Holding_Boundary)
        arcpy.ApplySymbologyFromLayer_management(addLayer2,
                                                 'C:\\Database_connections\\assesment_Model_lyr\\Holding.lyr')
        arcpy.mapping.AddLayer(df, addLayer2, "TOP")

        legend.autoAdd = False
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()

        # zoom to layer

        # print df
        lyr = arcpy.mapping.ListLayers(mxd, '', df)[1]
        # print lyr.name
        extent = lyr.getExtent()
        # print extent
        df.extent = extent

        # Adding Title to MXD
        Map_title = "Holding Reference Number : " + ' ' + str(row[0])
        titleItem = arcpy.mapping.ListLayoutElements(
            mxd, 'TEXT_ELEMENT', '')[0]
        titleItem.text = Map_title

        # Export Map to PNG File
<<<<<<< HEAD
        Png_output = 'B:\\Risk\\Map_Output\\Map_output_2\\' + \
            str(row[0]) + '.png'
        arcpy.mapping.ExportToPNG(mxd, Png_output)
        # print 'Map Created'
        del mxd
        end = time.time()
        print (end - start)
        f = open('B:\\Risk\\Risk.txt', "a")
        f.write(datetime.datetime.now().ctime())  # openlogfile
        f.write('Holding_Reference_Number = ' + ' ' + str(row[0]) + '\n')
        f.close()
        print "Moving to Next Row"
# end = time.time()
# print (end - start)
=======
        arcpy.mapping.ExportToPNG(mxd, baseDirectory + '\\' + refNumber + '.png')
        print('Time: ' + str(time.time() - start))
>>>>>>> 3ec4552a5b239db1bbb35c9eefdb8d2998c6b84b
