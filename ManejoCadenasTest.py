import unittest

class TestCadenas_y_Texto(unittest.TestCase):
	def test_separar_cadena_usando_varios_delimitadores(self):
		cadena  = 'asdf fjdk; afed, fjek,asdf, foo'
		import re
		# separamos la cadena cuando existan ciertos caractes y cualquier espacio extra
		# el patron de la expresion regular debe de ir entre corchetes []
		separacion = re.split(r'[;,\s]\s*', cadena)
		self.assertEqual(separacion,['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo'])

	def test_revisar_principio_y_final_de_una_Cadena(self):
		filename = 'spam.txt'
		self.assertTrue(filename.endswith('.txt'))
		self.assertTrue(filename.startswith('spam'))

		# revisar de una lista cuales cadenas cumplen con una condicion
		lista_archivos = ['foto.jpg','archivo.txt','tesis.txt','tu.mp3','libro.doc']
		
		documentos = [nombre for nombre in lista_archivos if nombre.endswith(('.txt','.doc'))]
		self.assertEqual(documentos, ['archivo.txt', 'tesis.txt', 'libro.doc'])
		
		hay_musica = any(nombre.endswith('.mp3') for nombre in lista_archivos)
		self.assertEqual(hay_musica,True)

		# startswith y endswith aceptan cadenas o tupas
		choices = ['http:', 'ftp:']
		url = 'http://www.python.org'
		#Si usamos listas marcara un error
		with self.assertRaises(TypeError) as context:
			url.startswith(choices)
		#Asi que lo convertimos a tuplas	
		url.startswith(tuple(choices))

	def test_buscando_dentro_de_un_texto_usando_patrones(self):
		from fnmatch import fnmatch, fnmatchcase
		# buscamos dentro de un texto muy parecido a como la hacemos desde la terminal de linux
		self.assertEqual(fnmatch('foo.txt', '*.txt') ,True)
		self.assertEqual(fnmatch('foo.txt', '?oo.txt') ,True)
		self.assertEqual(fnmatch('Dat45.csvt', 'Dat[0-9]*') ,True)

		names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
		archivos_csv = [name for name in names if fnmatch(name, 'Dat*.csv')]
		self.assertEqual(archivos_csv, ['Dat1.csv', 'Dat2.csv'])
		
		# Si queremos distinguir mayusculas y minusculas se usa fnmatchcase
		self.assertEqual(fnmatch('foo.txt', '*.TXT') ,True)
		self.assertEqual(fnmatchcase('foo.txt', '*.TXT') ,False)

	def test_buscando_dentro_de_un_texti_usando_expresiones_regulares(self):
		import re
		es_formato_fecha = re.match(r'\d+/\d+/\d+', '11/27/2012')
		self.assertIsNotNone(es_formato_fecha)
		no_es_formato_fecha =  re.match(r'\d+/\d+/\d+', 'Nov 27, 2012')
		self.assertIsNone(no_es_formato_fecha)
		
		#Si vamos a utilizar la misma expresion en varios lugares podemos precompilarla

		patron = re.compile(r'\d+/\d+/\d+')
		es_formato_fecha = patron.match('11/27/2012')

		# match() siempre busca desde el inicio de la cadena
		# para buscar en cualquier parte de la cadena se usa findall()
		text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
		fechas_encontradas = patron.findall(text)
		self.assertEqual(fechas_encontradas,['11/27/2012', '3/13/2013'])

		# Es posible agrupar los datos que encontremos
		patron_agrupado = re.compile(r'(\d+)/(\d+)/(\d+)')
		m = patron_agrupado.match('11/27/2012')
		self.assertEqual(m.groups(),('11', '27', '2012'))


		self.assertIsNotNone(patron_agrupado.match('11/27/2012abcdef'))
		#Si queremos que coincide excatamente el patron debemos agregar el $ al final
		patron_excacto = re.compile(r'(\d+)/(\d+)/(\d+)$')		
		
		self.assertIsNone(patron_excacto.match('11/27/2012abcdef'))
		self.assertIsNotNone(patron_excacto.match('11/27/2012'))

	def test_buscar_y_remplazar_cadenas(self):
		text = 'yeah, but no, but yeah, but no, but yeah'
		nueva = text.replace('yeah','yep')
		self.assertEqual(nueva,'yep, but no, but yep, but no, but yep')

		# si queremos usar expresiones regulares se usara el comando sub()
		text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
		import re
		# El primer argumento de sub es la expresion regular
		# El segundo argumento es el cambio de posision de los elemento '\3-\1-\2' 
		nueva = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
		self.assertEqual(nueva,'Today is 2012-11-27. PyCon starts 2013-3-13.')

		# Se puede pasar una funcion a sub
		from calendar import month_abbr
		
		def formato_fecha(m):
			lista_meses = month_abbr
			num_mes = int(m.group(1))
			mes = month_abbr[num_mes]
			return '{} {} {}'.format(m.group(2), mes, m.group(3))
		
		datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
		con_formato = datepat.sub(formato_fecha, text)
		self.assertEqual(con_formato,'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.')

		# Si queremos saber cuantas sustituciones se haran
		con_formato, n = datepat.subn(r'\3-\1-\2', text)
		self.assertEqual(n,2)

	def test_buscar_y_remplazar_cadenas_con_mayusculas_minusculas(self):
		import re
		text = 'UPPER PYTHON, lower python, Mixed Python'
		# Para buscar o remplazar sin importar si es mayuscula o minuscuka se usa re.IGNORECASE
		# tambien se usa con el comando sub
		encotrados =re.findall('python', text, flags=re.IGNORECASE)
		nuevo =re.sub('python','snake' ,text, flags=re.IGNORECASE)
		self.assertEqual(nuevo,'UPPER snake, lower snake, Mixed snake')

		#Si queremos que respete si es mayuscula,minuscula o capital
		def matchcase(word):
			def replace(m):
				text = m.group()
				if text.isupper():
					return word.upper()
				elif text.islower():
					return word.lower()
				elif text[0].isupper():
					return word.capitalize()
				else:
					return word
			return replace

		nueva = re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
		self.assertEqual(nueva,'UPPER SNAKE, lower snake, Mixed Snake')

	def test_usar_expresiones_regulares_cortas(self):
		import re
		str_pat = re.compile(r'\"(.*)\"')
		text1 = 'Computer says "no."'
		
		encontrado = str_pat.findall(text1)
		self.assertEqual(encontrado,['no.'])
		text2 = 'Computer says "no." Phone says "yes."'
		
		# Encuentra toda la cadena no solo los que tienen .
		encontrado=str_pat.findall(text2)
		self.assertEqual(encontrado,['no." Phone says "yes.'])

		# ? Coincide con el elemento anterior una o mas veces
		str_pat = re.compile(r'\"(.*?)\"')
		encontrado = str_pat.findall(text2)
		self.assertEqual(encontrado,['no.', 'yes.'])

	def test_expresiones_regulares_en_cadenas_multilinea(self):
		import re
		comment = re.compile(r'/\*(.*?)\*/')
		text1 = '/* this is a comment */'
		encontrado = comment.findall(text1)
		self.assertEqual(encontrado,[' this is a comment '])

		text2 = '''/* this is a 
		multiline comment */ 
				'''
		encontrado = comment.findall(text2)
		self.assertEqual(encontrado,[])

		# Para tomar en cuenta los saltos de linea usamos (?:.|\n)
		comment = re.compile(r'/\*((?:.|\n)*?)\*/')
		encontrado = comment.findall(text2)
		self.assertEqual(encontrado,[' this is a \n\t\tmultiline comment '])

	def test_usando_texto_unicode(self):
		# Jalapeño en dos distintos formatos, uno tiene la ñ como un caracter y el otro separa la n~ 
		s1 = 'Spicy Jalape\u00f1o'
		s2 = 'Spicy Jalapen\u0303o'
		self.assertNotEqual(s1,s2)

		#Para poder compararlo es necesario normalizar los caracteres unicode
		import unicodedata
		t1 = unicodedata.normalize('NFC',s1)
		t2 = unicodedata.normalize('NFC', s2)
		self.assertEqual(t1,t2)		
		# Si queremos quitar los caracteres unicode
		t1 = unicodedata.normalize('NFD', s1)
		sin_unicode = ''.join(c for c in t1 if not unicodedata.combining(c))
		self.assertEqual(sin_unicode,'Spicy Jalapeno')

	def test_manejo_diferentes_tipos_numeros(self):
		import re
		# Nuestra expresion evalua cualquier tipo de digito
		num = re.compile('\d+')
		# Numeros ASCII
		self.assertIsNotNone(num.match('123'))
		# Numeros Arabes 123 = ١٢٣ 		
		self.assertIsNotNone(num.match('\u0661\u0662\u0663'))
		# para cosas mas complejas es mejor usar la libreria regex 

	def test_eliminar_espacios_en_una_cadena(self):
		s = '    hola mundo \n'
		self.assertEqual(s.strip(), 'hola mundo')
		self.assertEqual(s.lstrip(), 'hola mundo \n')		
		self.assertEqual(s.rstrip(), '    hola mundo')

		t = '----hola===='
		self.assertEqual(t.lstrip('-'),'hola====')
		self.assertEqual(t.strip('-='),'hola')

		# Para eliminar carcteres que se encuentran enmedio
		s = '    hola   mundo     \n'
		import re
		espacio = re.sub('\s+',' ',s)
		self.assertEqual(espacio,' hola mundo ')

	def test_agregar_espacios_en_una_cadena(self):
		text = "hola mundo"
		self.assertEqual(text.rjust(20),'          hola mundo')
		self.assertEqual(text.rjust(20,'='),'==========hola mundo')
		self.assertEqual(text.ljust(20),'hola mundo          ')
		self.assertEqual(text.center(20),'     hola mundo     ')

		# Para mas flexibilidad podemos usar format
		self.assertEqual(format(text,'>20'),'          hola mundo')
		self.assertEqual(format(text,'*>20s'),'**********hola mundo')
		self.assertEqual(format(text,'<20'),'hola mundo          ')
		self.assertEqual(format(text,'^20'),'     hola mundo     ')

		# con format podemos usarlo con multiples valores
		formato_multiple ='{:>10s} {:>10s}'.format('Hola', 'Mundo')
		self.assertEqual(formato_multiple,'      Hola      Mundo')

		#Tambien podemos darle formato a los numeros
		x = 1.2345
		self.assertEqual(format(x, '>10'),'    1.2345')
		self.assertEqual(format(x, '^10.2f'),'   1.23   ')

	def test_concatenacion_de_cadenas(self):
		# union de una lista en una sola cadena
		parts = ['Is', 'Chicago', 'Not', 'Chicago?']
		self.assertEqual(','.join(parts), 'Is,Chicago,Not,Chicago?')

		# Usando el operador + y format
		a = 'Is Chicago'
		b = 'Not Chicago?'
		c = 'ok'
		
		concatenacion = a+ ' ' + b
		self.assertEqual(concatenacion,'Is Chicago Not Chicago?')

		con_format = '{} {}'.format(a,b)
		self.assertEqual(con_format,'Is Chicago Not Chicago?')

		# Concatenar cadenas usando + es mas ineficiente cuando imprimimos
		print(a + ':' + b + ':' + c)
		# Es mejor
		print(a,b,c, sep= ':')

	def test_concatenar_cadenas_usando_nombres_de_variables(self):
		s = '{name} has {n} messages.'
		con_variables = s.format(name='Guido',n=37)		
		self.assertEqual(con_variables,'Guido has 37 messages.')

		# Otra forma
		name = 'Guido'
		n = 33
		con_variables = s.format_map(vars())
		self.assertEqual(con_variables,'Guido has 33 messages.')

		# Tambien podemos pasar una clase
		class Info:
			def __init__(self,name,n=None):
				self.name = name
				self.n = n

		clase = Info('Guido',30)
		con_clase = s.format_map(vars(clase))
		self.assertEqual(con_clase,'Guido has 30 messages.')

		# Si no se le pasa alguna de las variable marcara error
		# para evitar esto podemos usar una clase que tenga el metodo __missing__

		class ConcatenacionSegura(dict):
			def __missing__(self,key):
				return '{' + key + '}'

		# Quitamos la variable n
		del n		
		con_clase2 = s.format_map(ConcatenacionSegura(vars()))
		self.assertEqual(con_clase2,'Guido has {n} messages.')

	def test_formateando_texto_en_cadenas_largas(self):
		s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

		import textwrap
		mas_corta = textwrap.fill(s, 40)
		print(mas_corta)
		self.assertEqual(mas_corta,mas_corta)

		# si queremos agregarle un espacio al inicio
		print(textwrap.fill(s, 40, initial_indent=' '))
		# un espacio despues de la primera linea
		print(textwrap.fill(s, 40, subsequent_indent=' '))


if __name__ == '__main__':
	unittest.main()