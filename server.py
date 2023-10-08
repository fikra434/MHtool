from flask import Flask, request, jsonify,  make_response
import xmltodict
import json
from xmlschema import XMLSchema
from io import BytesIO, StringIO
from lxml import etree
import lxml
from flask_cors import CORS
import xmlschema
import subprocess
# import  webservice as webservices


app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'})

    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'})

    # convert the xml file to a dictionary using the xmltodict library
    xml_dict = xmltodict.parse(file)

    # convert the dictionary to JSON and return it as the response
    # 
    response = jsonify(xml_dict)
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'

    return response



@app.route('/validate_xml', methods=['POST'])
def validate_xml():
    xml_file = request.files['xml_file']
    xsd_file = request.files['xsd_file']

    xml_string = xml_file.read()
    xsd_string = xsd_file.read()

    schema = xmlschema.XMLSchema(xsd_string)

    if schema.is_valid(xml_string):
        return 'XML file is valid against XSD file'
    else:
        return 'XML file is not valid against XSD file'

@app.route('/validate_dtd', methods=['POST'])
def validate_dtd():
    xml_file = request.files['xml_filee']
    dtd_file = request.files['dtd_file']
    # f = open(dtd_file,"rb")
    dtd_string = dtd_file.read()
    dtd_string = dtd_string.decode('utf-8')
    dtd = etree.DTD(StringIO(dtd_string))

    xml_string = xml_file.read()
    root = etree.XML(xml_string)

    # print(dtd.validate(root))
    if dtd.validate(root):
        return 'XML file is valid against DTD file'
    else:
        return 'XML file is not valid against DTD'



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'dtdd_file' not in request.files:
        return 'No file uploaded.'

    file = request.files['dtdd_file']

    # Save the file to a temporary location
    # file.save('C:\\Users\\Asus ROG\\Desktop\\file.txt')
    file.save('.\\static\\file.txt')


    # Execute the Perl script, passing the file as an argument
    # with open('C:\\Users\\Asus ROG\\Desktop\\filee.txt', "w+") as ff:
    with open('.\\static\\filee.txt', "w+") as ff:
        subprocess.run(['perl', 'dtdTOxsd.pl', '.\\static\\file.txt'],stdout=ff)
    

    
    with open('.\\static\\filee.txt', "r") as file:
        lines = file.readlines()


    for i in range(len(lines)):

        if '<' in lines[i]:
            index = lines[i].index('<')
            if '/' in lines[i] and lines[i].index('/') == index+1:
                lines[i] = lines[i][:(index+2)] + "xsd:" + lines[i][(index+2):]
            else :
                lines[i] = lines[i][:(index+1)] + "xsd:" + lines[i][(index+1):]
        

    with open('.\\static\\filee.txt', 'w') as file:
        file.writelines(lines)


    # f = open('C:\\Users\\Asus ROG\\Desktop\\filee.txt','r')
    with open('.\\static\\filee.txt', "r") as f:
        a = f.read()
    # output = subprocess.run(['perl', 'dtdTOxsd.pl', 'C:\\Users\\Asus ROG\\Desktop\\file.txt'],capture_output=True)
    # subprocess.run(['perl', 'dtdTOxsd.pl', 'C:\\Users\\Asus ROG\\Desktop\\file.txt'])
    return a

@app.route("/download",methods=['GET'])
def download():
  # Open the file in binary read-only mode
  with open(".\\static\\filee.txt", "rb") as f:
    # Read the file content
    data = f.read()

  # Set the response headers
  response = make_response(data)
  response.headers["Content-Type"] = "application/zip"
  response.headers["Content-Disposition"] = "attachment; filename=file.zip"

  # Return the response with the file data
  return response

if __name__ == '__main__':
    app.run()
