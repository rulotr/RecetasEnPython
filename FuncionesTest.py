import unittest

class Funciones(unittest.TestCase):
	def test_funciones_con_varios_argumentos(self):
		def avg(first, *rest):
			return (first + sum(rest)) / (1 + len(rest))

		self.assertEqual(avg(1,2),1.5)
		self.assertEqual(avg(1,2,3,4),2.5)

	def test_funciones_con_argumentos_de_llave(self):
		import html
		
		def make_element(name, value, **attrs):
			keyvals = [' %s="%s"' % item for item in attrs.items()]
			attr_str = ''.join(keyvals)
			element = '<{name}{attrs}>{value}</{name}>'.format(
					name=name,
					attrs=attr_str,
					value=html.escape(value))
			return element

		elemento = make_element('item', 'Albatross', size='large', quantity=6)
		#self.assertEqual(elemento,'<item quantity="6" size="large">Albatross</item>')

	def test_funciones_con_argumentos_llave_forzosos(self):
		def recv(maxsize, *, block):
			'Receives a message'
			pass

		with self.assertRaises(TypeError) as context:
			recv(1,True)

		recv(1,block = True)

	def test_funciones_con_argumentos_validados(self):
		def mininum(*values, clip=None):
			m = min(values)
			if clip is not None:
				m = clip if clip > m else m
			return m

		self.assertEqual(mininum(1,5,2,-5,10),-5)
		self.assertEqual(mininum(1,5,2,-5,10,clip=1),1)

	def test_informacion_sobre_argumentos(self):
		#def add(x:int, y:int) -> int:
		#	return x + y
		#help(add) 
		#add(x: int, y: int) -> int
		pass

	def test_retornar_multiples_valores(self):
		def miFuncion():
			return 1,2,3

		a,b,c = miFuncion()
		self.assertEqual(a,1)
		self.assertEqual(b,2)
		self.assertEqual(c,3)

	def test_funciones_con_argumentos_por_defecto(self):
		def spam(a,b=42):
			print(a,b)

		spam(1)   # a=1, b=42
		spam(1,2) # a=1, b=2
		
		x=42
		
		def spam2(b=x):
			return b
		self.assertEqual(spam2(),42)

		# x siempre vale 42
		x=23
		self.assertEqual(spam2(),42)

	def test_funciones_lambda(self):
		add = lambda x,y : x + y

		self.assertEqual(add(2,3),5)
		self.assertEqual(add('Hola','Mundo'),'HolaMundo')

		funcs = [lambda x, n=n: x+n for n in range(5)]
		for f in funcs:
			print(f(0))
			#0 1 2 3 4 5

	def test_funciones_parciales(self):
		import functools

		def lista_generica(funcion, cantidad):
			return [funcion(i) for i in range(cantidad)]

		# partial nos permite crear funciones mas especificas
		cadenas = functools.partial(lista_generica,(str))
		enteros = functools.partial(lista_generica,(int))

		self.assertEqual(cadenas(5),['0', '1', '2', '3', '4'])
		self.assertEqual(enteros(5),[0,1,2,3,4])

		suma_dos =functools.partial(lista_generica,(lambda x:x+2  ))
		self.assertEqual(suma_dos(5),[2,3,4,5,6])		






if __name__== "__main__":
	unittest.main()