import numpy as np
import simplex as sp

# O PPL deve estar na forma padrão
# 			  min z = cx 
# sujeito a		Ax = b
# 				x >= 0
#
# Os indices iniciam no 0, logo temos as varaiáveis 
# x_0, x_1, ..., x_{m-1} ao invés de x_1, x_2, ..., x_m


####### Exemplo
# 	max z = x_1 + x_2
# s.a. x_1 + 2x_2 >= 4
#	   x_1 + x_2  <= 1
#      x_1, x_2 >= 0
####
# Na forma padrão tem-se
# 	min -z = - x_1 - x_2
# s.a.  x_1 + 2x_2 + x_3 = 4
#       x_1 + x_2  - x_4 = 1
#		x_1, x_2, x_3, x_4 >= 0
#
####
# Transformando para a aplicação do algoritmo
# 	min -z = - x_0 - x_1
# s.a.  x_0 + 2x_1 + x_2 = 4
#       x_0 + x_1  - x_3 = 1
#		x_0, x_1, x_2, x_3, >= 0


# Entrada da matriz "A" 
A = np.array([[1, 2, 1, 0], 
			  [1, 1, 0, -1]])

# Entrada dos valores de "b" como vetores *COLUNAS*
b = np.array([[4], 
			  [1]])

# Entrada do vetor *LINHA* custo na forma padrão
c = np.array([-1, -1, 0, 0])

# Definição das variáveis básicas e não básicas
# Obs.: cuidado com os indices
VB = np.array([1, 2])
VNB = np.array([0, 3])

sp.solucionar(A, b, c, VB, VNB)
