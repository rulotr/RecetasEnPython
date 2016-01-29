import unittest

class TestEstructurasDeDatos(unittest.TestCase):
	def test_pasar_elementos_de_una_tupla_a_variables_individuales(self):
		p = (4,5)
		x,y = p
		self.assertEqual(x,4)
		self.assertEqual(y,5)

		data = ['ACME',50,91.1,(2012,12,21)]
		name,shares,price,(year,mont,day)= data
		self.assertEqual(name,"ACME")
		self.assertEqual(shares,50)
		self.assertEqual(price,91.1)
		self.assertEqual(year,2012)
		self.assertEqual(mont,12)
		self.assertEqual(day,21)

		# Funciona con cualquier objeto iterable no solo con tuplas
		# Si queremos ignorar alguna palabra usamos _
		s = 'Hola'
		_,b,_,d = s
		self.assertEqual(b,"o")		
		self.assertEqual(d,"a")

	def test_pasar_elemento_de_una_tupla_a_menor_numero_de_variables(self):
		record = ('Dave','dave@example.com','123-456-789','987-654-321')
		name,email,*phone_numbers=record
		self.assertEqual(phone_numbers,['123-456-789','987-654-321'])

		*trailing,current = [10,8,7,1,9,5,10,3]
		self.assertEqual(trailing,[10,8,7,1,9,5,10])
		self.assertEqual(current,3)

	def test_mantener_solo_n_cantidad_de_numeros_agregados(self):
		from collections import deque
		q = deque(maxlen=3)
		q.append(1)
		q.append(2)
		q.append(3)
		self.assertEqual(q,deque([1,2,3],maxlen=3))
		
		q.append(5)
		self.assertEqual(q,deque([2,3,5],maxlen=3))

		q.appendleft(6)
		self.assertEqual(q,deque([6,2,3],maxlen=3))

		ultimo=q.pop()
		self.assertEqual(ultimo,3)

		primero=q.popleft()
		self.assertEqual(primero,6)
		#La lista solo tiene el valor 2
		self.assertEqual(q,deque([2],maxlen=3))

	def test_buscar_el_mayor_y_menor_valor_de_una_lista(self):
		import heapq
		nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]

		tres_mayores = heapq.nlargest(3,nums) 
		self.assertEqual(tres_mayores,[42,37,23])
		tres_menores = heapq.nsmallest(3,nums)
		self.assertEqual(tres_menores,[-4,1,2])

		mayor = max(nums)
		menor = min(nums)
		self.assertEqual(mayor ,42)
		self.assertEqual(menor ,-4)

		heap = list(nums)
		#Pone el primer elemento en la posicion 0
		heapq.heapify(heap)
		self.assertEqual(heap,[-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8])

		#heappop saca el primer elemento, y lo sustituye por el menor de la lista
		# asi heappop siempre sacara el elemento mas pequeño
		menor =heapq.heappop(heap)
		self.assertEqual(menor,-4)
		menor =heapq.heappop(heap)
		self.assertEqual(menor, 1)	

	def test_buscar_el_mayor_y_menor_valor_de_un_diccionario(self):
		import heapq
		portfolio = [
			{'articulo': 'IBM',  'precio': 91.1},
			{'articulo': 'AAPL',  'precio': 543.22},
			{'articulo': 'FB',  'precio': 21.09},
			{'articulo': 'HPQ', 'precio': 31.75},
			{'articulo': 'YHOO',  'precio': 16.35},
			{'articulo': 'ACME',  'precio': 115.65}
		]
		

		dos_mas_baratos = heapq.nsmallest(2, portfolio, key=lambda s: s['precio'])
		el_mas_caro = heapq.nlargest(1, portfolio, key=lambda s: s['precio'])
		self.assertEqual(dos_mas_baratos,[{'articulo': 'YHOO',  'precio': 16.35},{'articulo': 'FB',  'precio': 21.09}])
		self.assertEqual(el_mas_caro,[{'articulo': 'AAPL',  'precio': 543.22}])

		from operator import itemgetter
		menor = min(portfolio, key=itemgetter('precio'))
		self.assertEqual(menor,{'articulo': 'YHOO',  'precio': 16.35})

	def test_prioridad_en_las_colas_queue(self):
		from MisClases import Item
		a = (1,Item('foo'))
		b = (5,Item('bar'))
		c = (1,Item('grook'))	

		#Cuando se compara una tupla, se compara el primer elemento	
		self.assertTrue(a<b)	
		
		#Si los primero valores son iguales, compara el segundo
		#El segundo valor en este caso es una clase, por eso marca error la comparacion
		with self.assertRaises(TypeError) as context:
			a<c

	    # Usamos un indice extra cuando el primer valor es igual
		a = (1,1,Item('foo'))
		b = (5,2,Item('bar'))
		c = (1,2,Item('grook'))	
		self.assertTrue(a<b)
		self.assertTrue(a<c)

	def test_matener_diccionarios_ordenados(self):
		from collections import OrderedDict
		# Un diccionario {} no mantiene el orden de inserccion
		# Si queremos mantener el orden de un diccionario se debe usar OrderedDict
		d= OrderedDict()
		d['foo'] = 1
		d['bar'] = 2
		d['spam'] = 3
		d['grok'] = 4
		# Es muy util cuando despues de serializarlo a un json queremos que mantenga el mismo orden.
		import json
		archivo = json.dumps(d)
		self.assertEqual(archivo,'{"foo": 1, "bar": 2, "spam": 3, "grok": 4}')
		#** Un OrderedDict es dos veces mas grande que un diccionario normal, hay que tener cuidado.

	def test_calculos_usando_diccionarios(self):
		lista_precios = {'ACME': 45.23,
			'AAPL': 612.78,
			'IBM': 205.55,
			'HPQ': 37.20,
			'FB': 10.75
		}

		# Las funciones min y max toman en cuenta el primer elemento del diccionario
		minimo = min(lista_precios)
		maximo = max(lista_precios)
		self.assertEqual(minimo,'AAPL')
		self.assertEqual(maximo,'IBM')

		# Podemos especificar que tome los valores y no la llave
		minimo = min(lista_precios.values())
		self.assertEqual(minimo,10.75)
		
		# O Podemos usar el metodo zip para cambiar las posiciones
		# y obtener los datos completos para el valor minimo
		minimo = min(zip(lista_precios.values(),lista_precios.keys()))
		self.assertEqual(minimo,(10.75,'FB'))

		# Si solo quiero obtener el nombre de quien tiene el precio minimo
		minimo = min(lista_precios, key=lambda k: lista_precios[k])
		self.assertEqual(minimo,'FB')

	def test_teoria_de_conjuntos_usando_diccionarios(self):
		a = {'x':1  , 'y':2,  'z':3}
		b = {'w': 10, 'x': 11, 'y': 2}

		# Union usando llaves
		self.assertEqual(a.keys() & b.keys(), {'x','y'})

		# left join usando llaves
		self.assertEqual(a.keys() - b.keys(), {'z'})

		# Union usando llave y Valor
		self.assertEqual(a.items() & b.items(), {('y',2)})

	def test_eliminar_duplicados(self):
		a = [1, 5, 2, 1, 9, 1, 5, 10]
		
		# set() nos permite crear un conjunto vacio.
		# Si le pasamos datos eliminara los duplicados.
		b= set(a)
		self.assertEqual(b,{1,2,10,5,9})

	def test_tomando_valores_de_una_cadena(self):
		record = '....................100          .......513.25  ..........'
		cost = int(record[20:32]) * float(record[40:48])
		self.assertEqual(cost,51325.00)
		#slice(inicio,fin,saltos) nos permite crear rangos reutilizables

		shares = slice(20,32) # Crea un slice del tipo (20,30, None)
		price =  slice(40,48)
		self.assertEqual(int(record[shares]),100)		
		self.assertEqual(int(record[shares])* float(record[price]),51325)
		
	def test_contar_elementos_repetidos_en_una_lista(self):
		words = [
			'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
			'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
			'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
			'my', 'eyes', "you're", 'under'
		]
		
		from collections import Counter
		

		word_counts = Counter(words)
		self.assertEqual(word_counts['eyes'],8)
		
		top_three = word_counts.most_common(3)
		self.assertEqual(top_three,[('eyes', 8), ('the', 5), ('look', 4)])

		morewords = ['why','are','you','not','looking','in','my','eyes']
		contador2 = Counter(morewords)

		contador_union = word_counts + contador2
		self.assertEqual(contador_union['eyes'], 9)

		contador_resta = word_counts - contador2
		self.assertEqual(contador_resta['eyes'], 7)

	def test_ordenar_diccionarios_por_una_llave_especifica(self):
		rows = [
			{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
			{'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
			{'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
			{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
		]

		from operator import itemgetter

		llave = itemgetter('uid')
		mapeo = map(llave, rows)
		#Obtenemos el listado solo de los valores del uid
		self.assertEqual(list(mapeo),[1003, 1002, 1001, 1004])

		llave = itemgetter('lname','fname')
		mapeo = map(llave, rows)
		self.assertEqual(list(mapeo),[('Jones', 'Brian'), ('Beazley', 'David'), ('Cleese', 'John'), ('Jones', 'Big')])

		rows_by_uid = sorted(rows, key=itemgetter('uid'))
		self.assertEqual(rows_by_uid[0],{'fname': 'John', 'lname': 'Cleese', 'uid': 1001})

		rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
		self.assertEqual(rows_by_lfname[3],{'fname': 'Brian', 'uid': 1003, 'lname': 'Jones'})

	def test_ordenar_objetos_creados_por_nosotros(self):
		from operator import attrgetter
		from MisClases import User


		users =[User(23), User(3), User(99)]
		#self.assertEqual(users,[User(23), User(3), User(99)])
		lista_orden = sorted(users, key= attrgetter('user_id'))
		self.assertEqual(lista_orden[0].user_id,User(3).user_id,User)
		# attrgetter puede aceptar varias columnas para el orden

	def test_agrupar_datos_de_lista_de_diccionarios(self):
		rows = [
			{'producto': 'Manzanas', 'fecha': '07/01/2012'},
			{'producto': 'Manzanas', 'fecha': '07/04/2012'},
			{'producto': 'Peras', 'fecha': '07/02/2012'},
			{'producto': 'Manzanas', 'fecha': '07/03/2012'},
			{'producto': 'Sandias', 'fecha': '07/02/2012'},
			{'producto': 'Melones', 'fecha': '07/02/2012'},
			{'producto': 'Zanahorias', 'fecha': '07/01/2012'},
			{'producto': 'Melones', 'fecha': '07/04/2012'},
		]

		from operator import itemgetter
		from itertools import groupby

		# Ordenamos la lista primero 
		# porque el operador groupby agrupa solo los elemento que se encuentran juntos
		rows.sort(key=itemgetter('fecha'))
		for fecha, items in groupby(rows, key=itemgetter('fecha')):
			print(fecha)
			for i in items:
				print(' ', i)
		
		# Si no tenemos problemas de memoria es mas rapido de la siguiente manera:
		from collections import defaultdict
		rows_by_date = defaultdict(list)
		for row in rows:
			rows_by_date[row['fecha']].append(row)
		
		# Asi podemos obtener los agrupados por una determinada fecha
		for r in rows_by_date['07/01/2012']:
			print(r)

	def test_filtrar_elementos_de_una_lista(self):
		mylist = [1, 4, -5, 10, -7, 2, 3, -1]
		mayores_cero = [n for n in mylist if n >0]
		self.assertEqual(mayores_cero,[1,4,10,2,3])

		menores_cero = [n for n in mylist if n <0]
		self.assertEqual(menores_cero,[-5,-7,-1])

		#Podemos usar un generador si la lista es muy larga
		generador = (n for n in mylist if n>0)
		for x in generador:
			print(x)

		# tambien es posible usar una funcion
		values = ['1', '2', '-3', '-', '4', 'N/A', '5']
		def es_entero(valor):
			try:
				x=int(valor)
				return True
			except ValueError:
				return False


		enteros = list(filter(es_entero,values))
		self.assertEqual(enteros,['1', '2', '-3', '4', '5'])

		# Es posible realizar operaciones sobre cada numero tambien
		import math
		# Aplicamos la raiz cuadrada a cada numero mayor a cero
		raiz = [math.sqrt(n) for n in mylist if n > 0]
		self.assertEqual(raiz,[1.0, 2.0, 3.1622776601683795, 1.4142135623730951, 1.73205080756887721])

		#Tambien podemos aplicar condicionales en el valor 
		clip_neg = [n if n > 0 else 0 for n in mylist]
		self.assertEqual(clip_neg,[1, 4, 0, 10, 0, 2, 3, 0])

	def test_relacionar_dos_lista_aplicar_condicion_y_comprimirlas(self):
		addresses = [
			'5412 N CLARK',
			'5148 N CLARK',
			'5800 E 58TH',
			'2122 N CLARK',
			'5645 N RAVENSWOOD',
			'1060 W ADDISON',
			'4801 N BROADWAY',
			'1039 W GRANVILLE',
		]

		counts = [ 0, 3, 10, 4, 1, 7, 6, 1]
		from itertools import compress
		more5 = [n > 5 for n in counts]
		self.assertEqual(more5,[False, False, True, False, False, True, True, False])
		#el operador compress toma los valores de una lista si en su misma posicion de otra lista tienen un valor True
		#compres retorna un iterador por eso lo convertimos a una lista
		solo_verdaderos = list(compress(addresses, more5))		
		self.assertEqual(solo_verdaderos,['5800 E 58TH', '1060 W ADDISON', '4801 N BROADWAY'])

	def test_condicionales_sobre_diccionarios(self):
		prices = {
			'ACME': 45.23,
			'AAPL': 612.78,
			'IBM': 205.55,
			'HPQ': 37.20,
			'FB': 10.75
		}
		
		p1 = { key:value for key, value in prices.items() if value > 200 }
		self.assertEqual(p1, {'AAPL': 612.78, 'IBM': 205.55})

		tech_names = { 'AAPL', 'IBM', 'HPQ', 'MSFT' }
		p2 = { key:value for key,value in prices.items() if key in tech_names}
		self.assertEqual(p2,{'AAPL': 612.78, 'HPQ': 37.2, 'IBM': 205.55})

	def test_transformar_y_reducir_datos_en_un_solo_paso(self):
		nums = [1, 2, 3, 4, 5]
		s = sum(x * x for x in nums)
		self.assertEqual(55,55)

		s = ('ACME', 50, 123.45)
		union = (','.join(str(x) for x in s))
		self.assertEqual(union, 'ACME,50,123.45')

		portfolio = [
			{'name':'GOOG', 'shares': 50},
			{'name':'YHOO', 'shares': 75},
			{'name':'AOL', 'shares': 20},
			{'name':'SCOX', 'shares': 65}
		]
		min_shares = min(s['shares'] for s in portfolio)
		self.assertEqual(min_shares,20)

		min_shares = min(portfolio, key=lambda s: s['shares'])
		self.assertEqual(min_shares,{'name': 'AOL', 'shares': 20})

if __name__ == '__main__':
	unittest.main()