import numpy as np
import math

def calcCusto(custoObj, direcao_basica):
	c = custoObj.dot( direcao_basica.transpose() )
	return c


def vetorSolucao(vec, var_bas, direcao, tamanho):
	vec_sol = np.zeros(shape=(tamanho))

	
	for j in range(len(var_bas)):
		vec_sol[var_bas[j]] = vec[j]

	if( direcao != -1 ):
		vec_sol[direcao] = 1

	return vec_sol


def calcTheta(x, d):
	theta = np.zeros(shape=len(x))
	#theta_pos = 10000000000

	for i in range(len(x)):
		if( d[i] < 0 ):
			theta[i] = -x[i]/d[i]

			valido = 0
			theta_pos = i
			for j in range(len(x)):
				if( x[j] + theta[i]*d[j] >= 0 ):
					valido +=1
						
			if( valido == len(x) ):
				return(theta_pos, theta[theta_pos])

	return(-1, -1)



def solucionar(A, b, custoObj, VB, VNB):
	B = np.zeros(shape=(len(VB), len(A)))
	tamanhoA = len(A[1, :])
	iter = 0

	for i in range(len(VB)):
		B[:, i] = A[:, VB[i]]
	
	x_bas = np.linalg.inv(B).dot( b )
	x_bas = vetorSolucao(x_bas, VB, -1, tamanhoA)

	while(True):
		iter += 1
		B = np.zeros(shape=(len(VB), len(A)))

		for i in range(len(VB)):
			B[:, i] = A[:, VB[i]]

		custo = np.zeros(tamanhoA)
		VB_passado = np.array([])

		for j in range(len(VNB)):
			dir_bas = -np.linalg.inv(B).dot( A[:, VNB[j]].transpose() )
			dir_bas = vetorSolucao(dir_bas, VB, VNB[j], tamanhoA)
			custo[j] = calcCusto(custoObj, dir_bas)


			# Checar direção basica
			pos = 0
			for k in range(len(dir_bas)):
				if( dir_bas[k] >= 0 ):
					pos += 1


			if( pos == len(dir_bas) ):
				# Temos d >= 0, logo z -> -inf
				print("Temos d >= 0 logo z -> -inf.")


			if(iter > 10 ):
				print("Erro. Mais que 1000 iterações. Saindo...")
				exit()

			
			if( custo[j] >= 0 ):
				# Verifica se o vetor custo é maior que zero
				# Se todo o vetor custo for >0 temos uma 
				# solução ótima
				if( j == (len(VNB)-1) ):
					otimo = True
					for p in range(len(custo)):
						if( custo[p] < 0 ):
							otimo = False

					if(otimo == True):
						print("Vetor custo c >= 0 logo a solução é ", x_bas)
						exit()

			elif( custo[j] < 0 ):
				# Se o custo é <0 devemos calcular o theta possível 
				# para movermos nessa direção
				theta_pos, theta = calcTheta(x_bas, dir_bas)
				theta_dir_bas = np.multiply(theta, dir_bas)
				x_bas = np.sum((x_bas, theta_dir_bas), axis=0)

				# Agora usamos a posição do theta (theta_pos) para 
				# remover a variável == theta_pos da base.
				# Ainda insere-se a variável em j na base.
				VB_passado = np.concatenate((VB_passado, VB))
				entra_base = VNB[j]
				sai_base   = VB[VB == theta_pos]
				VB[VB == theta_pos] = entra_base
				VNB[VNB == entra_base] = sai_base

				break