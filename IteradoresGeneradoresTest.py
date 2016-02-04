import unittest 

class IteradoresGeneradores(unittest.TestCase):
	def test_recorrer_lista_sin_loop(self):
		items = [1,2,3]

		it = iter(items)

		self.assertEqual(next(it),1)
		self.assertEqual(next(it),2)
		self.assertEqual(next(it),3)
		# Si sacamos mas elemento de los que hay lanzara un error
		with self.assertRaises(StopIteration) as context:	
			next(it)

	def test_delegando_iteradores(self):
		class Node:
			def __init__(self, value):
				self._value = value
				self._children = []
			
			def __repr__(self):
				return 'Node({!r})'.format(self._value)
			
			def add_child(self, node):
				self._children.append(node)
			
			#__iter__ nos permite tener un objeto iterador 
			def __iter__(self):
				return iter(self._children)
		root   = Node(0)
		child1 = Node(1)
		child2 = Node(2)
		root.add_child(child1)
		root.add_child(child2)
		it = iter(root)
		print(next(it))

		for ch in root:
			print(ch)
		# Outputs Node(1), Node(2)

	def test_creando_generadores(self):
		
		def generar_rango(inicia, termina, incremento):
			x = inicia
			while x < termina:
				yield x
				x += incremento

		for n in generar_rango(0,4,0.5):
			print(n)

		lista = list(generar_rango(0,1,0.125))
		self.assertEqual(lista,[0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])


		def countdown(n):
			print('Starting to count from', n)
			while n > 0:
				yield n
				n -= 1
			print('Termino!')

		c = countdown(3)
		#'Starting to count from'
		self.assertEqual(next(c),3)
		self.assertEqual(next(c),2)
		self.assertEqual(next(c),1)
	
		with self.assertRaises(StopIteration) as context:	
			next(c)
		#Termino!

	def test_iterar_a_profundidad(self):
		class Node:
			def __init__(self, value):
				self._value = value
				self._children = []
		
			def __repr__(self):
				return 'Node({!r})'.format(self._value)
			
			def add_child(self, node):
				self._children.append(node)
			
			def __iter__(self):
				return iter(self._children)

			def depth_first(self):
				yield self
				for c in self:
					yield from c.depth_first()

		root = Node(0)
		child1 = Node(1)
		child2 = Node(2)
		root.add_child(child1)
		root.add_child(child2)
		child1.add_child(Node(3))
		child1.add_child(Node(4))
		child2.add_child(Node(5))
		for ch in root.depth_first():
			print(ch)
			# Outputs Node(0), Node(1), Node(3), Node(4), Node(2), Node(5)

	def test_iterar_a_la_inversa(self):
		a = [1,2,3,4]

		for x in reversed(a):
			print(x)
		#4,3,2,1
		#Solo se puen recorrer inversamente listas, sino es lista la podemos convertir con list

	def test_iteradores_de_rango(self):
		import itertools
		def count(n):
			while True:
				yield n
				n += 1
		c = count(0)

		for x in itertools.islice(c, 10, 20):
			print(x)
		#10...20

	def test_conbinar_lists_con_iteradores(self):
		items = ['a','b','c']
		from itertools import permutations
		for p in permutations(items):
			print(p)
			#('a', 'b', 'c')
			#('a', 'c', 'b')
			#('b', 'a', 'c')
			#('b', 'c', 'a')
			#('c', 'a', 'b')
			#('c', 'b', 'a')

	def test_mostrar_indices_con_iteradores(self):
		lista= ['a','b','c']
		for idx, val in enumerate(lista):
			print(idx, val)
			#1 a
			#2 b
			#3 c
	def test_iterando_sobre_multiples_listas(self):
		xpts = [1, 5, 4, 2, 10, 7]
		ypts = [101, 78, 37, 15, 62, 99]
		# Usamos zip para unir las dos listas
		for x, y in zip(xpts, ypts):
			print(x,y)
			#1 101
			#5 78

		# Si la queremos en tuplas
		for i in zip(xpts,ypts):
			print(i)
		# (1,101)
		# (5,78)

		# Si las listas no tienen el mismo tamaño podemos usar zip_longest()

	def test_iterar_y_ordenar_listas(self):
		import heapq
		a = [1, 4, 7, 10]
		b = [2, 5, 6, 11]

		for c in heapq.merge(a, b):
			print(c)
		#1 2 4 5 6 7 10 11





if __name__ == '__main__':
	unittest.main()
