from io import StringIO, BytesIO
import os
import random
import string
import xml.etree.ElementTree as ET
from zipfile import ZipFile


class xmlReader():
    '''
    Обрабатывает директорию с полученными zip архивами, 
    разбирает вложенные xml файлы и формирует 2 csv файла:
        Первый: id, level - по одной строке на каждый xml файл
        Второй: id, object_name - 
            по отдельной строке для каждого тэга object 
            (получится от 1 до 10 строк на каждый xml файл)
    '''
    def xml_reader(self, data):
        data = data.decode('utf-8')
        root = ET.fromstring(data)
        id = root[0].get('value')
        level = root[1].get('value')
        csv1_data = [id, level]
        csv2_data = []
        for option in root[2]:
            csv2_data.append(option.get('name'))
        return csv1_data, csv2_data


class csvWriter():
    '''
    write data to csv file
    ''' 
    
class unpacker():
    '''
    unpack archive
    '''   
    def unpack_archive(self, file):
        with ZipFile(file, 'r') as myzip:
            files = myzip.namelist()
            for file in files:
                with myzip.open(file, 'r') as xml:
                    reader = xmlReader()
                    csv1_data, csv2_data = reader.xml_reader(xml.read())


if __name__ == '__main__':
    a = unpacker()
    a.unpack_archive('/home/mexico76/Desktop/Projects/test_ngenix/temp/0.zip')