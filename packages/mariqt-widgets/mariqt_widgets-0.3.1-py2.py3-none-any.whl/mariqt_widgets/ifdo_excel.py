import sys
#sys.path.insert(0, '/home/karl/Documents/HMC/mariqt/') # just for testing!
import pandas as pd
import os
from pprint import pprint

import mariqt.sources.ifdo as miqtf
import mariqt.files as miqtff
import mariqt.variables as miqtv
import mariqt.sources.ifdo as miqtiFDO
import mariqt.core as miqtc



def ifdo_export_to_excel(output_file:str, input_dir:str, ignore_sub_dirs:list, filter:dict, output_fields:list):
    """ export a set of header fields (outputFields) from iFDO file(s) to an Excel sheet so that the values can 
    be conveniently examined and potentially edited. 
    outputFile: output Excel file
    inputDir: directory will be recursively searched for iFDO files matching ```filter``` and excluding directories from ```ignoreSubDirs```
    ignoreSubDirs: list of folder names to ignore during search for iFDO files
    filter: dictionary to consider only those iFDO matching provided *image-set-header* field values of form ```{<header-field>:[<option1>,...]}``` set ```{}``` to ignore.
    outputFields: list of *image-set-header* fields to be exported as lines in Excel in the specified order. """
    
    # find iFOD files
    trunciFDODicts = []
    iFDOfiles = miqtff.browseForFiles(input_dir,['json'],ignoreSubDirs=ignore_sub_dirs)
    iFDOfiles.sort()

    i = 0
    for iFDOfile in iFDOfiles:
        
        print("reading",iFDOfile)
        iFDO_reader = miqtf.iFDO_Reader(iFDOfile)
        iFDO_Obj = iFDO_reader.ifdo

        if not filter is {}:
            skip = False
            for f in filter:
                if not iFDO_Obj['image-set-header'][f] in filter[f]:
                    skip = True
                    break
            if skip:
                print("skipped due to filter")
                continue

        trunciFDODict = {}
        for f in output_fields:
            if f in iFDO_Obj['image-set-header']:
                trunciFDODict[f] = iFDO_Obj['image-set-header'][f]
            else:
                trunciFDODict[f] = ""

        trunciFDODicts.append(trunciFDODict)
        i+=1
        
        print("done")

    df = pd.DataFrame(trunciFDODicts).transpose()
    print("imported",i,"iFDOs")

    # create field explanation sheet
    fieldExpl = []
    ifdo_fields = miqtv.ifdo_schema['$defs']['iFDO-fields']['properties']
    for field in output_fields:
        # if 'valid' in miqtv.ifdo_fields[field]:
        #     allow_values = str( miqtv.ifdo_fields[field]['valid'])
        # elif 'dataType' in miqtv.ifdo_fields[field]:
        #     allow_values = str( miqtv.ifdo_fields[field]['dataType']).replace('dataTypes.','')
        # else:
        #     allow_values = "text"

        allow_values = _get_allowed_values(ifdo_fields[field])

        fieldExpl.append([field,allow_values,ifdo_fields[field]['description']])
        #fieldExpl.append([field,allow_values,miqtv.ifdo_fields[field]['comment']])
    df_fieldExpl = pd.DataFrame(fieldExpl,columns=['iFDO fields','Allowed values','Explanation'])

    # create a excel writer object
    with pd.ExcelWriter(output_file) as writer:
        df.style.applymap(lambda _: 'vertical-align: top').to_excel(writer,header=False,sheet_name="Stations")
        df_fieldExpl.style.applymap(lambda _: 'vertical-align: top').to_excel(writer,sheet_name="Field Explanation",index=False)

    print("Wrote to",output_file)

def _get_allowed_values(obj:dict):
    type = obj['type']
    ret = type
    if type != 'object':
        for field in obj:
            if field != 'type' and field != 'description':
                if field == 'enum':
                    ret = str(obj[field])
                    break
                ret += ", " + field + ": " + str(obj[field])
    else:
        sub_ret = ""
        for sub_field in obj['properties']:
            sub_ret += sub_field + ": " + _get_allowed_values(obj['properties'][sub_field]) + ", "
        ret = 'dict {' + sub_ret + "}"
    return ret




def ifdo_update_from_excel(input_excel_file:str, ifdo_file:str, sheet_name:str):
    """ Updates iFDO's header fields from an Excel sheet.
    input_excel_file: input Excel file (generate with *iFDO_exportToExcel.ipynb* and edit)
    ifdo_file: iFDO file to be updated
    sheet_name: name of the sheet in the input Excel file containing the respective data """

    print("Using mariqt version",miqtv.version)

    excel_data_df = pd.read_excel(input_excel_file, sheet_name, header=None,dtype = str)
    
    # remove uncool chars
    excel_data_df = excel_data_df.replace({'‘':'\'','’':'\''},regex=True)
    excel_data_df_dict = excel_data_df.to_dict(orient='index')

    # find 'image-set-name' and create index -> image-set-name dict
    imageSetsIndices = {}
    setUpdates = {}
    for index in excel_data_df_dict:
        if excel_data_df_dict[index][0] == 'image-set-name':
            for id in excel_data_df_dict[index]:
                if id != 0:
                    setName = excel_data_df_dict[index][id]
                    imageSetsIndices[id] = setName
                    if setName in setUpdates:
                        raise Exception("image-set-name exists multiple times in Excel sheet: " + setName)
                    setUpdates[setName] = {}
            break

    # parse data
    for imageSetIndex, value in excel_data_df_dict.items():
        fieldName = value[0]
        if fieldName != 'image-set-name' and  fieldName[0:6] == 'image-':
            miqtc.recursiveEval(value)
            for fieldIndex, val in value.items():
                if fieldIndex != 0:
                    if str(val).lower() == "nan" or str(val).strip() == "":
                        val = ""
                    setUpdates[imageSetsIndices[fieldIndex]][fieldName] = val

    #pprint(setUpdates)
    
    # create iFDO object
    iFDO = miqtiFDO.iFDOFromFile(ifdo_file, ignore_image_files=True)

    #pprint(iFDO.ifdo_tmp)

    if iFDO.findTmpField('image-set-name') not in setUpdates:
        raise Exception("Could not find image set in Excel: " + iFDO.findTmpField('image-set-name'))

    iFDO.update_ifdo_header_fields(setUpdates[iFDO.findTmpField('image-set-name')])
    iFDO.update_fields()
    iFDO.write_ifdo_file()


def excel_to_markdown(input_excel_file:str, sheet_name:str=None, output_file:str=None, overwrite=False):
    """ Convert Excel file to markdown table """
    if sheet_name is None:
        df = pd.read_excel(input_excel_file)
    else:
        df = pd.read_excel(input_excel_file,sheet_name=sheet_name)
    df.columns = df.columns.str.strip()
    md_table = df.to_markdown(index=False)
    md_table = md_table.replace('nan','')
    
    if output_file is None:
        output_file = miqtff.changeFileExtension(input_excel_file,'md')
    if not overwrite and os.path.isfile(output_file):
        raise Exception("File exists: " + output_file)
    with open(output_file,'w') as file:
        file.write(md_table)
    return output_file


def markdown_to_excel(input_md_file:str, sheet_name:str="Sheet1", output_file:str=None, overwrite=False):
    """ Convert markdown file to Excel file.  """
    # Read a markdown file, getting the header from the first row and idnex from the second column
    df = pd.read_table(input_md_file, sep="|", 
                       header=None, 
                       index_col=1, skipinitialspace=True)

    # Drop the left-most and right-most null columns 
    df = df.dropna(axis=1, how='all')

    # Drop the header underline row
    df = df.drop(df.index[1])

    if output_file is None:
        output_file = miqtff.changeFileExtension(input_md_file,'xlsx')
    if not overwrite and os.path.isfile(output_file):
        raise Exception("File exists: " + output_file)
    with pd.ExcelWriter(output_file) as writer:
        df.style.applymap(lambda _: 'vertical-align: top').to_excel(writer,header=False,sheet_name="Stations")

    return output_file