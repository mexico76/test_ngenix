# test_ngenix

* before start
1. create virtualenvironment 
```
python3 -m venv .
```
2. activate it
```
source venv/bin/activate
```
3. install requirements
```
pip install -r requirements.txt
```
* to create archives 
```
python3 xml_creator.py 
```
* to create xmls
```
python3 xml_reader.py 
```



* 1. Создает 50 zip-архивов, в каждом 100 xml файлов со случайными данными следующей структуры:

<root><var name=’id’ value=’<случайное уникальное строковое значение>’/><var name=’level’ value=’<случайное число от 1 до 100>’/><objects><object name=’<случайное строковое значение>’/><object name=’<случайное строковое значение>’/>…</objects></root>

В тэге objects случайное число (от 1 до 10) вложенных тэгов object.

* 2. Обрабатывает директорию с полученными zip архивами, разбирает вложенные xml файлы и формирует 2 csv файла:Первый: id, level - по одной строке на каждый xml файлВторой: id, object_name - по отдельной строке для каждого тэга object (получится от 1 до 10 строк на каждый xml файл)

Очень желательно сделать так, чтобы задание 2 эффективно использовало ресурсы многоядерного процессора.
