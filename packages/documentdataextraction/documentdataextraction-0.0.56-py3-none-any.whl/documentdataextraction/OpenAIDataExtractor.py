import requests, json, traceback, openai
import os
from invoice2data import extract_data
from flask import request
import loggerutility as logger
from PIL import Image
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path
import cv2
import pytesseract
import yaml
from .GenerateExtractTemplate import GenerateExtractTemplate
import pdfplumber
import pdftotext
import datetime
import docx2txt
import pandas as pd
import pathlib
from striprtf.striprtf import rtf_to_text
import unicodedata
import tiktoken
 
class OpenAIDataExtractor:

    mainPg_Instruction    =  ""
    otherPg_Instruction   =  ""

    def pytesseract_ocr(self,PDF_file):
        image_file_list = []
        dict = {}
        with TemporaryDirectory() as tempdir:
            pdf_pages = convert_from_path(PDF_file, 500)
            for page_enumeration, page in enumerate(pdf_pages, start=1):
                filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
                page.save(filename, "JPEG")
                image_file_list.append(filename)

            for page_no,image_file in enumerate(image_file_list):
                text = cv2.imread(image_file)
                image_file = self.resizing(text, 50)
                dict[str(page_no+1)] = str(((pytesseract.image_to_string(image_file)))).strip()

            logger.log(f"pytesseract for image ::::: 61 {dict}","0")
            return dict
        
    def pdfplumber_ocr(self,PDF_file):
        OCR_lst = []
        ocr_text_final = ""
        dict = {}
        
        file = pdfplumber.open(PDF_file)
        ocr_text = file.pages
        logger.log(f"file.pages::: {file.pages}", "0")
        for page_no in range (len(ocr_text)):
            ocr_text_final = ocr_text[page_no].extract_text()
            dict[str(page_no+1)] = ocr_text_final.strip()
            # OCR_lst.append(ocr_text_final)
        # print(len(dict.values()))
        return dict
    
    def pdftotext_ocr(self,PDF_file):
        with open(PDF_file, "rb") as f:
            pdf = pdftotext.PDF(f)

        OCR_Text = "\n\n".join(pdf)
        return OCR_Text
    
    def gaussianBlur(self,img,blur_value):
        logger.log(f"gaussianBlur::::54> {blur_value}","0")
        img = cv2.GaussianBlur(img, (blur_value, blur_value),cv2.BORDER_DEFAULT)
        return img

    def grayscale(self,img):
        logger.log(f"grayscale::::59","0")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def resizing(self,img,scale_percent):
        logger.log(f"resizing::::64> {scale_percent}","0")
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_LANCZOS4)
        return img

    def thresholding(self,img,thresholding_value):
        logger.log(f"thresholding::::72> {thresholding_value}","0")
        mean_value = img.mean()
        threshold_value = mean_value * thresholding_value
        _, img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)
        return img

    def OpenAIDataExtract(self,file_path : str, jsonData : str, templates : str):
        try:
            
            ent_code = ""
            ent_name = ""
            mandatory = []
            enhancement_parameters = ""
            # enhancement_parameters =    {   
            #     '1': {'Blur': 3},
            #     '2': {'Gray': 1},
            #     '3': {'Resizing': 84},
            #     '4': {'Thresholding': 0.9}
            #                             }

            logger.log(f"json data   ::::: 61 {jsonData}","0")
            logger.log(f"OpenAIDataExtract all Parameters::  \n{locals()}\n","0")
            
            if 'ai_proc_templ' in jsonData.keys():
                ai_proc_templ = jsonData['ai_proc_templ']
            
            if 'proc_api_key' in jsonData.keys():
                proc_api_key = jsonData['proc_api_key']

            if 'userId' in jsonData.keys():
                userId = jsonData['userId']
                
            if 'objName' in jsonData.keys():
                objName = jsonData['objName']

            if 'ent_code' in jsonData.keys():
                ent_code = jsonData['ent_code']

            if 'ent_name' in jsonData.keys():
                ent_name = jsonData['ent_name']
 
            if 'IS_OCR_EXIST' in jsonData.keys():
                IS_OCR_EXIST = jsonData['IS_OCR_EXIST']

            if 'ai_proc_variables' in jsonData.keys():
                ai_proc_variables = jsonData['ai_proc_variables']

            if 'enhancement_parameters' in jsonData.keys():
                enhancement_parameters = jsonData['enhancement_parameters']
                if enhancement_parameters:
                    enhancement_parameters = json.loads(enhancement_parameters)

            if isinstance(ai_proc_variables, str):
                ai_proc_variables = json.loads(ai_proc_variables)

            if ai_proc_variables:
                for val in ai_proc_variables["Details"]:
                    if val['mandatory'] == 'true':
                        mandatory.append(val['name'])
                
            logger.log(f"ai_proc_variables::::88> {ai_proc_variables}","0")
            
            if 'proc_mtd' in jsonData.keys():
                proc_mtd = jsonData['proc_mtd']
                proc_mtd_value = proc_mtd.split("-")
           
            OCR_Text = ""
            finalResult = ""
            self.result = {}
            df = None
            fileExtension = (pathlib.Path(file_path).suffix)
            logger.log(f"\nfileExtention::::> {fileExtension}","0")
            fileExtension_lower = fileExtension.lower()
            logger.log(f"\nfileExtention_lower()::::> {fileExtension_lower}","0")

            if IS_OCR_EXIST == 'false':
                logger.log(f"OCR Start !!!!!!!!!!!!!!!!!102","0")  
                dict = {}          
                if '.PDF' in fileExtension_lower or '.pdf' in fileExtension_lower:

                    if 'PP' in proc_mtd_value[0]:
                        OCR_Text=self.pdfplumber_ocr(file_path)

                    elif 'PT' in proc_mtd_value[0]:
                        OCR_Text=self.pdftotext_ocr(file_path)

                    elif 'PO' in proc_mtd_value[0]:
                        OCR_Text=self.pytesseract_ocr(file_path)
                    
                    # if len((OCR_Text).strip()) == 0: 
                    keys_with_blank_values = [key for key, value in OCR_Text.items() if not value]
                    if len(keys_with_blank_values) != 0:      
                        OCR_Text=self.pytesseract_ocr(file_path)

                    logger.log(f"OpenAI pdf ocr ::::: {OCR_Text}","0")
                
                elif '.docx' in fileExtension_lower or '.DOCX' in fileExtension_lower:
                    dict[str(1)] = docx2txt.process(file_path)
                    OCR_Text = dict
                    logger.log(f"OpenAI DOCX ocr ::::: {OCR_Text}","0")

                # Added by SwapnilB for handling xls case on 28-Mar-23 [START]
                elif ".xls" in fileExtension_lower or ".xlsx" in fileExtension_lower:
                    logger.log(f"inside .xls condition","0")
                    df = pd.read_excel(file_path)
                    xls_ocr = df.to_csv()
                    dict[str(1)] = xls_ocr.replace(","," ").strip()
                    OCR_Text = dict
                    logger.log(f"\nxls_ocr type ::::: \t{type(OCR_Text)}","0")
                    logger.log(f"\nxls_ocr ::::: \n{OCR_Text}\n","0")
                    
                elif ".csv" == fileExtension_lower :
                    logger.log(f"inside .csv condition","0")
                    df = pd.read_csv(file_path)
                    csv_ocr = df.to_csv()           # to handle multiple spaces between columns
                    dict[str(1)] = csv_ocr.replace(","," ")
                    OCR_Text = dict
                    logger.log(f"\ncsv_ocr type ::::: \t{type(OCR_Text)}","0")
                    logger.log(f"\ncsv_ocr ::::: \n{OCR_Text}\n","0")
                
                elif ".rtf" == fileExtension_lower :
                    logger.log(f"inside .rtf condition","0")
                    with open(file_path) as infile:
                        content = infile.read()
                        dict[str(1)] = rtf_to_text(content, errors="ignore")  # to handle encoding error
                    OCR_Text = dict
                    logger.log(f"\nrtf_ocr type ::::: \t{type(OCR_Text)}","0")
                    logger.log(f"\nrtf_ocr ::::: \n{OCR_Text}\n","0")
                
                # Added by SwapnilB for handling xls case on 28-Mar-23 [END]

                else:
                    path = file_path
                    image = cv2.imread(path)
                    if enhancement_parameters:
                        if '1' in enhancement_parameters.keys():
                            image = self.gaussianBlur(image,enhancement_parameters['1']['Blur'])
                        
                        if '2' in enhancement_parameters.keys():
                            image = self.grayscale(image)

                        if '3' in enhancement_parameters.keys():
                            image = self.resizing(image,enhancement_parameters['3']['Resizing'])
                        
                        if '4' in enhancement_parameters.keys():
                            image = self.thresholding(image,enhancement_parameters['4']['Thresholding'])


                    dict[str(1)] = pytesseract.image_to_string(image)
                    logger.log(f"{dict}","0")
                    OCR_Text = dict
                
                keys_with_blank_values = [key for key, value in OCR_Text.items() if not value]
                if len(keys_with_blank_values) != 0: 
                    logger.log(f'\n In getCompletionEndpoint exception stacktrace : ', "1")
                    trace = str('Contact System Administrator')
                    descr = str('OCR is not available')
                    returnErr = self.getErrorXml(descr, trace)
                    logger.log(f'\n Print exception returnSring inside OCR : {returnErr}', "0")
                    return str(returnErr)
                
                logger.log(f"OCR End !!!!!!!!!!!!!!!!!156","0")
                if not ent_code and not ent_name:
                    logger.log(f"INSIDE entcode and entname not blank","0")
                    try:
                        if proc_mtd_value[0] == 'PT':
                            from invoice2data.input import pdftotext
                            input_module = pdftotext

                        elif proc_mtd_value[0] == 'PP':
                            # from invoice2data.input import pdfplumber
                            # input_module = pdfplumber
                            logger.log(f"PP !!!!!!!!!!!! 175","0")
                            from invoice2data.input import pdftotext
                            input_module = pdftotext

                        elif proc_mtd_value[0] == 'PO':
                            from invoice2data.input import tesseract
                            input_module =  tesseract
                    
                        logger.log(f"Template Extraction call Start !!!!!!!!!!!!!!!!!183","0")
                        resultdata = extract_data(invoicefile=file_path,templates=templates,input_module=input_module)
                        # resultdata = dict(resultdata)
                        logger.log(f"Template Extraction call End !!!!!!!!!!!!!!!!!111","0")
                        logger.log(f"Template extracted data  ::::: 186 {resultdata}","0")
                        logger.log(f"resultdata type  ::::: 187 {type(resultdata)}","0")

                        if isinstance(resultdata, bool) and len(mandatory)>0:
                            logger.log(f"resultdata type  ::::: 283 {type(OCR_Text)}","0")
                            self.result['OCR_DATA']=OCR_Text
                            self.result['isMandatoryExtracted']='false'
                            return self.result
                            # resultdata = {}
                        elif isinstance(resultdata, bool):
                            resultdata = {}

                        resultdata['isTemplateExtracted']='true'
                        self.result['isMandatoryExtracted']='true'

                        if mandatory:
                            for valuesOfmandatory in mandatory:
                                if valuesOfmandatory in resultdata:
                                    if not resultdata[valuesOfmandatory]:  
                                        self.result['OCR_DATA']=OCR_Text
                                        self.result["EXTRACT_TEMPLATE_DATA"] = resultdata
                                        self.result['isMandatoryExtracted']='false'
                                        return self.result
                                    
                        
                        for valuesOfmandatory in resultdata.keys():
                            if type(resultdata[valuesOfmandatory]) == list and resultdata[valuesOfmandatory] != []:
                                resultdata[valuesOfmandatory] = resultdata[valuesOfmandatory][0]
                            elif resultdata[valuesOfmandatory] == []:
                                resultdata[valuesOfmandatory] = ""

                        # resultdata['isTemplateExtracted']='true'
                        if 'ent_code' in resultdata.keys():
                            self.result["EXTRACT_TEMPLATE_DATA"] = resultdata
                            self.result['OCR_DATA']=OCR_Text
                            return self.result
                            
                        
                    except Exception as e:
                        logger.log(f'\n Exception : {e}', "1")

            else:
                if 'OCR_DATA' in jsonData.keys():
                    OCR_Text = jsonData['OCR_DATA']

            if ai_proc_templ:
                if 'AID' in proc_mtd_value[1]:
                    logger.log(f"AID !!!!!!!!!!!! 204","0")
                    finalResult = self.extractdatausing_davinci(proc_api_key=proc_api_key, OCR_Text=OCR_Text, ai_proc_templ=ai_proc_templ,ai_proc_variables=ai_proc_variables)
                    

                elif 'AIT' in proc_mtd_value[1]:
                    finalResult = self.extractdatausing_turbo(proc_api_key = proc_api_key, ai_proc_templ=ai_proc_templ,ai_proc_variables=ai_proc_variables, OCR_Text = OCR_Text)
                
                self.result["EXTRACT_LAYOUT_DATA"] = finalResult
                self.result['OCR_DATA']=OCR_Text
            
            logger.log(f"Response Return !!!!!!!!!!!! 142","0")
            return self.result
            
        
        except Exception as e:
            logger.log(f'\n In getCompletionEndpoint exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str(e)
            returnErr = self.getErrorXml(descr, trace)
            logger.log(f'\n Print exception returnSring inside getCompletionEndpoint : {returnErr}', "0")
            return str(returnErr)
        
    def getErrorXml(self, descr, trace):
        errorXml = '''<Root>
                            <Header>
                                <editFlag>null</editFlag>
                            </Header>
                            <Errors>
                                <error type="E">
                                    <message><![CDATA['''+descr+''']]></message>
                                    <trace><![CDATA['''+trace+''']]></trace>
                                    <type>E</type>
                                </error>
                            </Errors>
                        </Root>'''

        return errorXml


    def getlayouttextaidata(self):
        try:
            result = {}
            final_result = {}
            mandatory = []
            finalResult = ""
            proc_api_key = ""
            ai_proc_templ = ""
            ent_name = ""
            ent_code = ""
            ent_type = ""
            OCR_Text = ""
            ai_proc_variables = ""
            
            jsonData = request.get_data('jsonData', None)
            jsonData = json.loads(jsonData[9:])
            logger.log(f"jsonData API openAI class::: !!!!!269 {jsonData}","0")

            if 'extract_templ' in jsonData.keys():
                given_temp_path = jsonData['extract_templ']
            
            if 'ent_code' in jsonData.keys():
                ent_code = jsonData['ent_code']
            
            if 'ent_type' in jsonData.keys():
                ent_type = jsonData['ent_type']

            if 'ent_name' in jsonData.keys():
                ent_name = jsonData['ent_name']

            if 'ai_proc_templ' in jsonData.keys():
                ai_proc_templ = jsonData['ai_proc_templ']

            if 'ai_proc_variables' in jsonData.keys():
                ai_proc_variables = jsonData['ai_proc_variables']

            if 'proc_api_key' in jsonData.keys():
                proc_api_key   = jsonData['proc_api_key']

            if 'userId' in jsonData.keys():
                userId = jsonData['userId']

            if 'objName' in jsonData.keys():
                objName = jsonData['objName']
            
            if 'proc_mtd' in jsonData.keys():
                proc_mtd = jsonData['proc_mtd']
                proc_mtd_value = proc_mtd.split("-")
            
            if 'OCR_DATA' in jsonData.keys():
                OCR_Text = jsonData['OCR_DATA']
            logger.log(f'\n\n  OCR_Text line 406: \n{OCR_Text}\n{type({OCR_Text})}\n{len({OCR_Text})}\n', "0")


            if ai_proc_templ:
                if 'AID' in proc_mtd_value[1]:
                    finalResult = self.extractdatausing_davinci(proc_api_key=proc_api_key, OCR_Text=OCR_Text, ai_proc_templ=ai_proc_templ,ai_proc_variables=ai_proc_variables)

                elif 'AIT' in proc_mtd_value[1]:
                    finalResult = self.extractdatausing_turbo(proc_api_key = proc_api_key, ai_proc_templ=ai_proc_templ,ai_proc_variables=ai_proc_variables, OCR_Text = OCR_Text)
                
                ymlfilepath = "/"+(given_temp_path)+"/"+str(ent_name).strip().replace(" ","_").replace(".","").replace("/","")+".yml"
                
                if os.path.exists(ymlfilepath) == True:
                    os.remove(ymlfilepath)

                if ent_name.strip() and ent_code.strip():
                    logger.log(f'\n[ Template creation Start time  305  :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                    templatecreation = GenerateExtractTemplate()
                    templatecreation.generateHeaderTemplate(ymlfilepath,ent_name,ent_code,ent_type,ai_proc_variables,OCR_Text)
                    logger.log(f'\n[ Template creation End time  308  :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")

                temp_file_path = "/"+(given_temp_path)+"/"+'.yml'
                if os.path.exists(temp_file_path) == True:
                    os.remove(temp_file_path)
                    final_result['status'] = 0
                    final_result['error'] = str('Ent Code or Ent Name is not present, mention required details properly')
                    logger.log(f'\n[ Blank Template Remove :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                
                elif os.path.exists(ymlfilepath) == True:
                    result["EXTRACT_LAYOUT_DATA"] = finalResult
                    final_result['status'] = 1
                    final_result['result'] = result
                else:
                    final_result['status'] = 0
                    final_result['error'] = str('Template not created, Mention the Required details properly')

        except Exception as ex:
            final_result['status'] = 0
            final_result['error'] = str(ex)
        logger.log(f"Return result value !!!!!!!!! 203 {final_result}","0")
        return final_result
    
    def extractdatausing_davinci(self,proc_api_key : str, OCR_Text : str , ai_proc_templ : str, ai_proc_variables : str):

        logger.log(f'\n[ Open ai starting time 131 :        {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
        openai.api_key = proc_api_key
        logger.log(f"\nai_proc_variables::::\n {ai_proc_variables}\n{type(ai_proc_variables)}","0")
        logger.log(f"\nai_proc_templ::::\n {ai_proc_templ}\n{type(ai_proc_templ)}","0")       
        logger.log(f"TYPE OF ai_proc_variables {type(ai_proc_variables)}","0")

        if isinstance(ai_proc_variables, str):
            ai_proc_variables = json.loads(ai_proc_variables)

        if ai_proc_variables:
            for val in ai_proc_variables["Details"]:
                if "<"+val["name"]+">" in ai_proc_templ:
                    ai_proc_templ = ai_proc_templ.replace("<"+val["name"]+">", val['defaultValue'])

        if '<DOCUMENT_DATA>' in ai_proc_templ:
            print(type(ai_proc_templ))
            ai_proc_templ = ai_proc_templ.replace('<DOCUMENT_DATA>',OCR_Text)
            logger.log(f'\n[ Open ai " model " Value              :      "text-davinci-003" ]', "0")
            logger.log(f'\n[ Open ai " prompt " Value             :      "{ai_proc_templ}" ]', "0")
            logger.log(f'\n[ Open ai " temperature " Value        :      "0" ]', "0")
            logger.log(f'\n[ Open ai " max_tokens " Value         :      "1800" ]', "0")
            logger.log(f'\n[ Open ai " top_p " Value              :      "1" ]', "0")
            logger.log(f'\n[ Open ai " frequency_penalty " Value  :      "0" ]', "0")
            logger.log(f'\n[ Open ai " presence_penalty " Value   :      "0" ]', "0")
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt= ai_proc_templ,
            temperature=0,
            max_tokens=1800,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )

        else:

            logger.log(f'\n[ Open ai " model " Value              :      "text-davinci-003" ]', "0")
            logger.log(f'\n[ Open ai " prompt " Value             :      "{OCR_Text+ai_proc_templ}" ]', "0")
            logger.log(f'\n[ Open ai " temperature " Value        :      "0" ]', "0")
            logger.log(f'\n[ Open ai " max_tokens " Value         :      "1800" ]', "0")
            logger.log(f'\n[ Open ai " top_p " Value              :      "1" ]', "0")
            logger.log(f'\n[ Open ai " frequency_penalty " Value  :      "0" ]', "0")
            logger.log(f'\n[ Open ai " presence_penalty " Value   :      "0" ]', "0")
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt= OCR_Text+'\n'+ai_proc_templ,
            temperature=0,
            max_tokens=1800,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        logger.log(f"Response openAI completion endpoint::::: {response}","0")
        finalResult=str(response["choices"][0]["text"])
        logger.log(f'\n [ Open ai completion time 171 :      {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
        logger.log(f"OpenAI completion endpoint finalResult ::::: {finalResult}","0")
        return finalResult


    def extractdatausing_turbo(self,proc_api_key: str, ai_proc_templ : str, ai_proc_variables : str, OCR_Text : str):
        logger.log(f"\proc_api_key::::\n {proc_api_key}\n{type(proc_api_key)}","0")
        logger.log(f"\nai_proc_variables::::\n {ai_proc_variables}\n{type(ai_proc_variables)}","0")
        logger.log(f"\nai_proc_templ::::\n {ai_proc_templ}\n{type(ai_proc_templ)}","0")
        logger.log(f"\nai_OCR_Text::::  516\n {OCR_Text}\n{type(OCR_Text)}","0")
        OCR_List            = []
        response_lst        = []
        token_limit         = 4096
        max_response_tokens = 1800
        messageTokenLength  = None
        start               = ""
        end                 = ""
        
        if isinstance(ai_proc_variables, str):
            ai_proc_variables = json.loads(ai_proc_variables)

        
        if isinstance(OCR_Text, str):
            OCR_Text = json.loads(OCR_Text.strip())
        
        
        if isinstance(OCR_Text, dict):
            for val in OCR_Text.values():
                OCR_List.append(val)
            OCR_Text = OCR_List

        if isinstance(ai_proc_templ, list):
            ai_proc_templ = json.dumps(ai_proc_templ)

        if ai_proc_variables:
            for val in ai_proc_variables["Details"]:
                if "<"+val["name"]+">" in ai_proc_templ:
                    ai_proc_templ = ai_proc_templ.replace("<"+val["name"]+">", val['defaultValue'].strip())

                if val["name"] == "start_index":
                    start = val['defaultValue']
                    logger.log(f"\n\n start_index ::: {start} \n\n","0")    

                if val["name"] == "end_index":
                    end = val['defaultValue']
                    logger.log(f"\n\n end_index ::: {end} \n\n","0")    

        # Creating substring from OCR Data
        subStringOcrList=[]
        if start != "" and end != "" :
            for page_no in range(len(OCR_Text)):
                if start.strip() in OCR_Text[page_no] and end.strip() in OCR_Text[page_no]:   # if start and  end present in ocr 
                    logger.log(f"\n\n if condition line 561  \n\n","0")
                    OCR_TableStartIndex = OCR_Text[page_no].find(start)  
                    OCR_TableEndIndex = OCR_Text[page_no].find(end)
                    
                    subStringOcrList.append(OCR_Text[page_no][OCR_TableStartIndex : OCR_TableEndIndex])
                else:
                    logger.log(f"\n\n start_index ::: {start} and end_index ::: {end} not found in OCR page no. {page_no} \n\n","0")
            if len(subStringOcrList) > 0:
                logger.log(f"\n\n if condition line 569  subStringOcrList::{subStringOcrList} length :::{len(subStringOcrList)}\n\n","0")
                OCR_Text =  subStringOcrList


        openai.api_key = proc_api_key
        ai_proc_templ_updated = self.replaceWithExtractInstruction(ai_proc_temp=ai_proc_templ, OCR_Text = OCR_Text, ai_proc_variables = ai_proc_variables )

        # Overview call or Template creation call ai_proc_templ variable type is list and while uploading it's variable type is string
        if isinstance(ai_proc_templ_updated, str):       
            ai_proc_templ_updated = ai_proc_templ_updated.replace('\n'," ") 
            ai_proc_templ_updated = json.loads(ai_proc_templ_updated)

        logger.log(f"\n\n ai_proc_templ_updated LINE 531     ::: {type(ai_proc_templ_updated)} \n\n","0")
        logger.log(f"\n\nOCR_Text 533     ::: {type(OCR_Text)} \t {len(OCR_Text)}\n\n","0")
        
        useGPT4  = False
        for i in range(len(ai_proc_templ_updated)):
                clean_string = ''.join(c for c in ai_proc_templ_updated[i] if unicodedata.category(c)[0] != 'C')
                message = json.loads(clean_string.replace("\\",'\/'))
                
                # to calculate token
                conv_history_tokens = self.num_tokens_from_messages(message)   
                logger.log(f"conv_history_tokens:::{conv_history_tokens}","0")    
                messageTokenLength = conv_history_tokens + max_response_tokens 
                logger.log(f"\n\n MessageTokenLength is :::{messageTokenLength}\n","0")
                
                if messageTokenLength <= token_limit:
                    logger.log(f"\n\n--- Using GPT-3.5-TURBO Model ---\t for Page-{i}\t as messageTokenLength is :::{messageTokenLength}\n","0")
                    completion = openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",
                                    messages=message,
                                    temperature=0,
                                    max_tokens=max_response_tokens,
                                    top_p=0.5,
                                    frequency_penalty=0,
                                    presence_penalty=0,
                                )
                    response_lst.append(completion['choices'][0]['message']['content'])
                
                else:
                    logger.log(f"\n--- messageTokenLength:::{messageTokenLength} ---\n","0")
                    useGPT4 = True
                    break
            
        if useGPT4 :
            response_lst.clear()
            
            ai_proc_templ_GPT4 = ai_proc_templ
            logger.log(f"\n\ai_proc_templ_GPT4::::{ai_proc_templ_GPT4}{type(ai_proc_templ_GPT4)}\n\n","0")
            
            OCR_Text_str = " ".join(OCR_Text)
            logger.log(f"\n\OCR_Text_str::::{OCR_Text_str}{type(OCR_Text_str)}\n\n","0")
            
            ai_proc_templ_GPT4 = (ai_proc_templ_GPT4.replace("<EXTRACT_INSTRUCTIONS>", self.mainPg_Instruction)).replace("<DOCUMENT_DATA>", OCR_Text_str.replace('"',' ').replace("\\",'\/')).strip()
            logger.log(f"\n\ai_proc_templ_GPT4::::{ai_proc_templ_GPT4}{type(ai_proc_templ_GPT4)}\n\n","0")
        
            
            clean_string = ''.join(c for c in ai_proc_templ_GPT4 if unicodedata.category(c)[0] != 'C')

            message = json.loads(clean_string.replace("\\",'\/'))
                
            logger.log(f"\n\n--- Using GPT-4 Model ---\t as messageTokenLength is:::{messageTokenLength} \n\n","0")
            
            completion = openai.ChatCompletion.create(
                        model="gpt-4",    
                        messages=message,
                        temperature=0,
                        top_p=0.5,
                        frequency_penalty=0,
                        presence_penalty=0,
                                )
            response_lst.append(completion['choices'][0]['message']['content'])
            
        logger.log(f"OpenAI response_lst  :::\n\n{response_lst}\n\n","0")  
        finalResponseStr = self.concatFinalResponse(returnedResponseList = response_lst)
        logger.log(f"OpenAI FINAL ResponseStr  :::\n\n{finalResponseStr}\n\n","0")  
        return finalResponseStr

    def replaceWithExtractInstruction(self, ai_proc_temp: str, OCR_Text: list, ai_proc_variables : str):
        logger.log(f"\n\niNSIDE replaceWithExtractInstruction()\n\n","0")
        logger.log(f"\n\nOCR_Text line 637::::{OCR_Text}{type(OCR_Text)}\n\n","0")
        logger.log(f"\n\nai_proc_temp::::{ai_proc_temp}{type(ai_proc_temp)}\n\n","0")
        
        if isinstance(ai_proc_variables, str):
            ai_proc_variables = json.loads(ai_proc_variables)

        for key in ai_proc_variables["Details"]:
            if key["name"] == "main_page":
                self.mainPg_Instruction = key['defaultValue']
        logger.log(f"mainPg_Instruction:::\n\n{self.mainPg_Instruction}\n","0")

        for key in ai_proc_variables["Details"]:
            if key["name"] == "other_pages":
                self.otherPg_Instruction = key['defaultValue']
        logger.log(f"otherPg_Instruction:::\n\n{self.otherPg_Instruction}\n","0")
        
        FinalInstruction_lst = []
        ai_proc_temp_main = (ai_proc_temp.replace("<EXTRACT_INSTRUCTIONS>", self.mainPg_Instruction)).replace("<DOCUMENT_DATA>", OCR_Text[0].replace('"',' ').replace("\\",'\/')).strip()
        logger.log(f"\n\ai_proc_temp_main::::{ai_proc_temp_main}{type(ai_proc_temp_main)}\n\n","0")
        FinalInstruction_lst.append(ai_proc_temp_main)
        # other Page OCR

        if len(OCR_Text) > 1:
            for i in range(1, len(OCR_Text)):
                ai_proc_temp_other = (ai_proc_temp.replace("<EXTRACT_INSTRUCTIONS>", self.otherPg_Instruction)).replace("<DOCUMENT_DATA>", OCR_Text[i].replace('"',' ').replace("\\",'\/')).strip()
                FinalInstruction_lst.append(ai_proc_temp_other)
        logger.log(f"\n\FinalInstruction_lst line 647::::{FinalInstruction_lst}\n\n","0")
        return FinalInstruction_lst

    def concatFinalResponse(self, returnedResponseList : list):
        finalResponse=[]
        for i in range(len(returnedResponseList)):
            if i == 0:
                finalResponse.append(returnedResponseList[i])
            else:
                fromSizeVar = returnedResponseList[i]
                if "Size" in fromSizeVar:
                    pageCSV = fromSizeVar[fromSizeVar.find("Size")+4:]
                pageCSV = "\n" + returnedResponseList[i] if returnedResponseList[i] != "\n" else pageCSV
                finalResponse.append(pageCSV)
                
        return (" ".join(finalResponse))

    
    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
    
        return num_tokens






