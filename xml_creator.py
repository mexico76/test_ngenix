import aiofiles
import asyncio
from io import BytesIO
import os
import random
import string
import uuid
from xml.dom import minidom
from zipfile import ZipFile


class randomXmlCreator():
    """
    <root>
        <var name=’id’ value=’<случайное уникальное строковое значение>’/>
        <var name=’level’ value=’<случайное число от 1 до 100>’/>
        <objects>
            <object name=’<случайное строковое значение>’/>
            ... от 1 до 10 тегов object
            <object name=’<случайное строковое значение>’/>…
        </objects>
    </root>
    В тэге objects случайное число (от 1 до 10) вложенных тэгов object.
    """
    def _generate_random_str(self) -> str:
        random_n = random.randint(15, 20)
        return ''.join(random.choices(string.ascii_uppercase + string.digits,
                                      k=random_n))

    def _generate_random_int(self, start: int = 1, stop: int = 10) -> int:
        return random.randint(start, stop)

    def create_xml(self) -> minidom.Document:
        main_root = minidom.Document()
        root = main_root.createElement('root')
        main_root.appendChild(root)
        
        id = main_root.createElement('var')
        id.setAttribute('name', 'id')
        id.setAttribute('value', str(uuid.uuid4()))
        root.appendChild(id)
        
        level = main_root.createElement('var')
        level.setAttribute('name', 'level')
        level.setAttribute('value', f'{self._generate_random_int(1, 100)}')
        root.appendChild(level)
        
        objects = main_root.createElement('objects') 
        root.appendChild(objects)
        
        for i in range(self._generate_random_int()):
            object = main_root.createElement('object')
            object.setAttribute('name', self._generate_random_str())
            objects.appendChild(object)
        return main_root

    def create_n_xmls(self, count: int = 50) -> list[minidom.Document]:
        n_xmls = []
        for i in range(count):
            n_xmls.append(self.create_xml())
        return n_xmls


class archiver():
    '''
    save files to archive
    '''
    async def add_to_archive(self, data: list[minidom.Document],
                             zip_name: str = '1.zip') -> None:
        current_directory = os.getcwd()
        folder = 'temp'
        path = os.path.join(current_directory, folder)
        if not os.path.exists(path):
            os.mkdir(path)
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as myzip:
            for i, xml in enumerate(data): 
                myzip.writestr(f'{i}.xml', 
                               str.encode(xml.toprettyxml(indent ="\t")))
        async with aiofiles.open(os.path.join(path, zip_name), 'wb') as f:
            await f.write(zip_buffer.getvalue())
    
    async def add_n_archives(self, count: int = 100) -> None:
        xml_creator = randomXmlCreator()
        for i in range(count):
            await self.add_to_archive(xml_creator.create_n_xmls(), f"{i}.zip")
            
async def main():
    b = archiver()
    await b.add_n_archives()
       
    
if __name__ == '__main__':
    asyncio.run(main())
