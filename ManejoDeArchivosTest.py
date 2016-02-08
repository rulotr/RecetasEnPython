import unittest

class TestAchivosIO(unittest.TestCase):
	def test_escribir_texto_de_un_archivo(self):
		# wt es el la opcion para el modo de escritura
		text1 = "hola mundo"
		text2 = "como estas?"
		with open('ejemplo.txt','wt') as f:
			f.write(text1)
			f.write(text2)

		# o imprimir directamente

		with open('ejemplo.txt','wt') as f:
			print(text1, file=f)
			print(text2, file=f)

	def test_leer_texto_en_un_archivo(self):
		# rt es el la opcion para el modo de lectura
		with open('ejemplo.txt','rt') as f:
			datos = f.read()
		self.assertEqual(datos,'hola mundo\ncomo estas?\n')

		# podemos leer linea a linea
		with open('ejemplo.txt','rt') as f:
			for line in f:
				print(line)

		# leer un archivo sin usar el with, siempre se debe de cerrar al final.
		f = open('ejemplo.txt','rt')
		data = f.read()
		f.close() 

	def test_obtener_encoding(self):
		import sys
		enc = sys.getdefaultencoding()
		self.assertEqual(enc,'utf-8')
		#Si queremos usar otro encoding al abrir el archivo
		with open('ejemplo.txt','rt', encoding= 'latin-1') as f:
			datos = f.read()
		self.assertEqual(datos,'hola mundo\ncomo estas?\n')

	def test_imprimir_una_tupla_en_forma_de_cadena(self):		
		print('ACME',50,91.5) # ACME 50 91.5
		print('ACME', 50, 91.5, sep=',') # ACME,50,91.5
		print('ACME', 50, 91.5, sep=',', end='!!\n') # ACME,50,91.5!!
		# esta forma concatena letras y numeros 
		# si usaramos join tenemos que convertir los numeros a cadena

	def test_escribir_archivos_binarios(self):
		# wt es para escritura de archivos binarios
		with open('ejemplo.bin', 'wb') as f:
				f.write(b'Hola mundo')

	def test_leer_archivos_binarios(self):
		# rb es para lectura de archivos binarios
		with open('ejemplo.bin', 'rb') as f:
			data = f.read()

		pos0 = data[0]
		#Cuando es una cadena binaria nos retorna valor en numero
		# 72 = H
		self.assertEqual(pos0,72)

		# para declarar una cadena como binaria 
		b = b'Hola Mundo'
		self.assertEqual(b[1],111)

		# para leer un binario en formato texto 
		with open('ejemplo.bin', 'rb') as f:
			data = f.read(16)
			text = data.decode('utf-8')
		self.assertEqual(text,'Hola mundo')

	def test_excribir_en_un_archivo_solo_si_no_existe(self):
		# con xt solo escribe si no existe el archivo
		with self.assertRaises(FileExistsError) as context:
			with open('ejemplo.txt','xt') as f:
				f.write('hola\n')

	def test_consultar_si_existe_un_archivo(self):
		import os
		existe = os.path.exists('ejemplo.txt')
		self.assertTrue(existe)

	def test_usar_un_objeto_tipo_archivo(self):
		# Estos tipos de objetos nos sirven cuando trabajamos en pruebas unitarias
		# para no crear un archivo real.
		import io
		s = io.StringIO()
		s.write('Hello World\n')
		print('This is a test', file=s)

		valor = s.getvalue()
		self.assertEqual(valor,'Hello World\nThis is a test\n')

		# Crear el objeto con una cadena por defecto		
		s = io.StringIO('Hello\nWorld')
		parte = s.read(5)
		self.assertEqual(parte,'Hello')

		# Si queremos un objeto de tipo binario
		s = io.BytesIO()
		s.write(b'binary data')
		valor = s.getvalue()
		self.assertEqual(valor,b'binary data')

	def test_comprimir_archivos(self):
		# podemos usar gzip o bz2
		import gzip
		with gzip.open('ejemplo.gz','wt') as f:
			f.write('hola mundo desde gzip')

		import bz2
		with bz2.open('ejemplo.bz2','wt') as f:
			f.write('hola mundo desde bz2')

	def test_leer_archivos_comprimidos(self):
		# podemos usar gzip o bz2
		import gzip
		with gzip.open('ejemplo.gz','rt') as f:
			texto = f.read()

		self.assertEqual(texto,'hola mundo desde gzip')

		import bz2
		with bz2.open('ejemplo.bz2','rt') as f:
			texto = f.read()

		self.assertEqual(texto,'hola mundo desde bz2')
		# Podemos cambiar el nivel de compresion con compresslevel
		# with gzip.open('ejemplo.gz', 'wt', compresslevel=5)

	def test_leer_un_archivo_en_un_buffer(self):
		import os.path
		
		def read_into_buffer(filename):
			buf = bytearray(os.path.getsize(filename))
			with open(filename, 'rb') as f:
				f.readinto(buf)
			return buf

		buf = read_into_buffer('ejemplo.txt')
		self.assertEqual(buf[0:4],bytearray(b'hola'))

		with open('nuevo.bin', 'wb') as f:
			f.write(buf)

	def test_manipular_rutas(self):
		import os
		path = '/Users/RAUL.TORRES/Documents/Cursos/Python/RecetasEnPython/ejemplo.txt'

		ultimo_valor = os.path.basename(path)
		self.assertEqual(ultimo_valor,'ejemplo.txt')

		directorio = os.path.dirname(path)
		self.assertEqual(directorio,'/Users/RAUL.TORRES/Documents/Cursos/Python/RecetasEnPython')

		unir = os.path.join('tmp', 'data', os.path.basename(path))
		self.assertEqual(unir,'tmp\data\ejemplo.txt')

		agregar ='~/Nuevo/texto.txt'
		agregar = os.path.expanduser(agregar)
		self.assertEqual(agregar, 'C:\\Users\RAUL.TORRES/Nuevo/texto.txt')

		cortar = os.path.splitext(agregar)
		self.assertEqual(cortar, ('C:\\Users\\RAUL.TORRES/Nuevo/texto', '.txt'))

	def test_consultar_si_existe_un_directorio_o_archivo(self):
		import os
		self.assertTrue(os.path.isfile('ejemplo.txt'))
		self.assertFalse(os.path.isdir('ejemplo.txt'))
		
		# Para ver enalces simbolicos y su ruta real
		#os.path.islink('/usr/local/bin/python3')
		#os.path.realpath('/usr/local/bin/python3')

	def test_listar_directorio(self):
		import os
		names = os.listdir('Ejemplo')
		self.assertEqual(names, ['SoyUnDirectorio', 'soy_un_archivo.txt'])

		# Podemos usar isfile o isdir para filtrar
		archivos = [name for name in os.listdir('Ejemplo') 
					if os.path.isfile(os.path.join('Ejemplo',name))]
		self.assertEqual(archivos,['soy_un_archivo.txt'])
		# o startwith o endwith

		# para busquedas especificas se puede usar glob
		import glob
		binfiles = glob.glob('*.bin')
		self.assertEqual(binfiles, ['ejemplo.bin', 'nuevo.bin'])

	def test_archivos_y_directorios_temporales(self):
		from tempfile import TemporaryFile
	
		with TemporaryFile('w+t') as f:
			# Read/write to the file
			f.write('Hello World\n')
			f.write('Testing\n')
			# Seek back to beginning and read the data
			f.seek(0)
			data = f.read()
		# Temporary file is destroyed






if __name__ == "__main__":
	unittest.main()