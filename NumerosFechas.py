import unittest

class TestNumeros_y_Fechas(unittest.TestCase):
	def test_redondear_valores(self):
		# Menor a 5 deja el numero, mayor a 5 sube al siguiente numero
		self.assertEqual(round(1.23,1),   1.2)		
		self.assertEqual(round(1.27,1),   1.3)
		self.assertEqual(round(1.25361,3),   1.254)

		# Si solo queremos tomar el valor con cierto numero de decimales sin redondearlo
		# es mejor usar format
		self.assertEqual(format(1.23,'0.2f'),   '1.23')	

	def test_manejo_numeros_decimales(self):
		a = 4.2
		b = 2.1
		suma = a + b 
		self.assertTrue(suma != 6.3 )

		from decimal import Decimal
		a = Decimal('4.2')
		b = Decimal('2.1')
		suma = a + b
		self.assertTrue(suma == Decimal('6.3') )
		self.assertTrue(suma == Decimal('6.300') )

		# podemos usar with con la funcion localcontext, para especificar los decimales para todo el bloque with
		from decimal import localcontext
		a = Decimal('1.3')
		b = Decimal('1.7')

		with localcontext() as ctx:
			ctx.prec = 3
			con_contexto = (a/b)
			self.assertEqual(con_contexto,Decimal('0.765'))

	def test_aplicar_formato_en_numeros(self):
		x = 1234.56789

		self.assertEqual(format(x,'0.2f'), '1234.57')
		self.assertEqual(format(x,'>10.1f'), '    1234.6')
		self.assertEqual(format(x,'<10.1f'), '1234.6    ')
		self.assertEqual(format(x,'^10.1f'), '  1234.6  ')

		# Separador de decimales
		self.assertEqual(format(x,','), '1,234.56789')
		self.assertEqual(format(x,'0,.1f'), '1,234.6')

		# Usando notacion exponencial
		self.assertEqual(format(x,'e'),'1.234568e+03')
		self.assertEqual(format(x,'0.2E'),'1.23E+03')

		# Tambien lo podemos usar una cadena
		con_formato ='The value is {:0,.2f}'.format(x)
		self.assertEqual(con_formato,'The value is 1,234.57')

		# Poner un negativo en el formato
		self.assertEqual(format(-x, '0.1f'),'-1234.6')

	def test_manejo_de_binario_octal_hexadecimal(self):
		decimal = 1234
		binario = bin(decimal) # '0b10011010010'
		octal = oct(decimal)   # '0o2322'
		hexa  = hex(decimal)   # '0x4d2'

		# tambien podemos usar format
		self.assertEqual(format(decimal,'b'),'10011010010')
		self.assertEqual(format(decimal,'o'),'2322')
		self.assertEqual(format(decimal,'x'),'4d2')

		# Para usar numero complejos existe una libreria llamada cmath

	def test_calculos_con_fracciones(self):
		from fractions import Fraction
		a = Fraction(5,4)
		b = Fraction(7,16)
		self.assertEqual(a+b,27/16)
		self.assertEqual(float(a+b),1.6875)

		# Obtener numerador y denominador
		self.assertEqual(a.numerator,5)
		self.assertEqual(a.denominator,4)

		# Convertir un decimal en fraccion
		x = 3.75
		y = Fraction(*x.as_integer_ratio())
		self.assertEqual(y,15/4)

	def test_generar_numeros_aleatorios(self):
		import random
		valores = [1,2,3,4,5,6]
		# Obtenemos un valor aleatorio
		numero = random.choice(valores)

		# Obtener dos valores aleatorios
		numeros = random.sample(valores,2) # Ejemplo [3,5]

		# Poner la lista en un orden aleatorio
		lista = random.shuffle(valores) # Ejemplos [2,4,6,5,1,3]

		# Generar un numero entero del 0 -10
		numero = random.randint(0,10)

	def test_manejo_de_fechas_horas(self):		
		from datetime import timedelta,datetime

		# podemos manejar dias y horas por separado
		a = timedelta(days=2 ,hours=6)
		b = timedelta(hours=4.5)
		sumar = a + b
		self.assertEqual(sumar.days,2)
		self.assertEqual(sumar.seconds,37800)

		# o podemos manejar una fecha completa
		fecha =datetime(2012,9,23)
		dias = timedelta(days=10)
		sumar_dias = fecha + dias
		self.assertEqual(sumar_dias,datetime(2012, 10, 3, 0, 0))

		fecha2 = datetime(2012,12,21)
		resta_fecha = fecha2 - fecha
		self.assertEqual(resta_fecha.days,89)

		#para obtener la fecha actual
		now = datetime.today()

		# si sumamos meses nos dara error
		with self.assertRaises(TypeError) as context:			
			mas_meses = fecha + timedelta(months =1)

		# para sumar meses u operaciones mas complejas se usa la libreria dateutil
		from dateutil.relativedelta import relativedelta
		mas_meses = fecha + relativedelta(months=+1)
		self.assertEqual(mas_meses,datetime(2012, 10, 23, 0, 0))

		# diferencia entre dos fechas
		diferencia = relativedelta(fecha2,fecha)
		self.assertEqual(diferencia, relativedelta(months=+2, days=+28))
		self.assertEqual(diferencia.days,28)
		self.assertEqual(diferencia.months,2)

if __name__ == '__main__':
	unittest.main()
