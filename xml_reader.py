import csv
import glob
from multiprocessing import Pool
import os
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

    @staticmethod
    def xml_reader(data: bytes) -> list:
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

    def save_data_to_csv(self, data: list, path: list) -> None:
        # path_1, path_2 = self.prepare_data(path)
        with open(path[0], "a+") as file_1:
            writer1 = csv.writer(file_1)
            writer1.writerow(data[0])
        with open(path[1], "a+") as file_2:
            writer2 = csv.writer(file_2)
            for object in data[1]:
                writer2.writerow([data[0][0], object])

    def prepare_data(self, path: str) -> list:
        name_1 = '1.csv'
        name_2 = '2.csv'
        path_1 = os.path.join(path, name_1)
        path_2 = os.path.join(path, name_2)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path_1, 'w'):
            pass
        with open(path_2, 'w'):
            pass
        return path_1, path_2


class unpacker():
    '''
    unpack archive
    '''
    def __init__(self) -> None:
        self.saver = csvWriter()

    def unpack_archive(self, save_paths: list[str],
                       source_path: str = os.path.join(os.getcwd(),
                                                       'temp/1.zip')) -> None:
        with ZipFile(source_path, 'r') as myzip:
            files = myzip.namelist()
            for file in files:
                if file.endswith('.xml'):
                    with myzip.open(file, 'r') as xml:
                        csv_data = xmlReader.xml_reader(xml.read())
                        self.saver.save_data_to_csv(csv_data, save_paths)

    def unpack_archives_in_folder(
            self,
            path: str = os.path.join(os.getcwd(), 'temp')
            ) -> None:
        save_path = os.path.join(os.getcwd(), 'res')
        paths = self.saver.prepare_data(save_path)
        zips = []
        for _, _, files in os.walk(path):
            for file in files:
                if file.endswith('.zip'):
                    zips.append((paths, os.path.join(path, file)))
        with Pool() as pool:
            pool.starmap(self.unpack_archive, zips)


if __name__ == '__main__':
    '''
    without multiprocessing execut 1000 archives = 18,75 sec
    with multiprocessing Pool = 4.9 sec
    '''
    a = unpacker()
    a.unpack_archives_in_folder()
