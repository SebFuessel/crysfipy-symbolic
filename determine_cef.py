import sympy
from sympy import pprint
import numpy as np
from matplotlib import pyplot as plt

from cef_hamiltonian import CEF_Hamiltonian, Hamiltonian
# import mikibox as ms

from timeit import default_timer as timer


# Dont forget to edit these fields
# Jval = 2.5
# lattice='tetragonal_2'
# Ex.1 interesting set of 4D matrices
# Jval = 12
# lattice='hexagonal_2'
# Ex.2 5D matrix
# Jval = 12
# lattice='hexagonal_2'

# calculate_eigenvectors = False

# diagonalizeH = False
# investigateSubspaces = False

# exportLatex = False
# exportSympy = False

hline = '--------------------------------------------------------------------------------------'

Jval = 1
lattice='trigonal_2'
determine_eigenvectors = True

Jmax=5
Symmetries=['tetragonal_1', 'tetragonal_2', 'trigonal_1', 'trigonal_2', 'hexagonal_1', 'hexagonal_2'] #monoclinic takes ages to calculate, cubic ones are out of range so they aren't implemented
calc_results=[]
Symmetries_Eigenvectors=['tetragonal_1_Vec', 'tetragonal_2_Vec', 'trigonal_1_Vec', 'trigonal_2_Vec', 'hexagonal_1_Vec', 'hexagonal_2_Vec']
colours=['b', 'g', 'r', 'c', 'm', 'y', 'b--', 'g--', 'r--', 'c--', 'm--', 'y--','k--']

for symmetry in Symmetries:
    lattice=symmetry
    if determine_eigenvectors:
        determine_eigenvectors_b=True
    for j in np.arange(1,Jmax,0.5):
        print(j)
        delta=0
        delta2=0
        H = CEF_Hamiltonian(symmetry=lattice, Jval=j)   
        start_time = timer()

        H.make_block_form()

        H.determine_eigenvalues()
        eigenvalues_timer = timer()
        delta = eigenvalues_timer-start_time
        
        print(f'# Determining eigenvalues = {eigenvalues_timer-start_time:4f} s')

        if delta>10:
            break

        if determine_eigenvectors_b:
            vector_start=timer()
            H.determine_eigenvectors()
            eigenvectors_timer = timer()
            delta2=eigenvectors_timer-vector_start
            print(f'# Determining eigenvectors = {eigenvectors_timer-vector_start:4f} s')
            if delta2>10 or (symmetry=='trigonal_1' and (j+0.5)>2.5) or ((symmetry=='tetragonal_1' or 'tetragonal_2') and j+0.5>4) or (symmetry=='trigonal_2' and (j+0.5)>3):
                determine_eigenvectors_b=False

        calc_results.append([delta, j, symmetry, delta2])

plt.title('Calculation Time for Eigenvalues depending on Jval')
plt.xlabel('Jval')
plt.ylabel('Calculation Time in seconds')
plt.grid(True)
plt.yscale("log")
for x, symmetry in enumerate (Symmetries):
    diay=[]
    diax=[]
    diax_vec=[]
    diay_vec=[]
    for entry in calc_results:
        if entry[2]==symmetry:
            diay.append(entry[0])
            diax.append(entry[1])
            if entry[3]>0:
                diax_vec.append(entry[1])
                diay_vec.append(entry[3])
    plt.plot(diax, diay, colours[x], label=symmetry)
    plt.plot(diax_vec, diay_vec, colours[x+6], label=Symmetries_Eigenvectors[x])
            
plt.legend()
plt.savefig('EigenVals_logscale.png', dpi=300)
plt.show()
# # Evaluations
# sqrt  = np.emath.sqrt
# I = 1j

# CePdAl3
# Bij_names = ['B20', 'B22', 'B40', 'B42', 'B44', 'B60', 'B62', 'B64', 'B66']
# Bij_values = [1.203, -0.3   , -0.001, -1.1182781e-02,  0.244, 1, 0.01, 0.3, -0.001]    # orth

# Bij = ms.crysfipy.CEFpars('C4', [1.203, -0.001, 0.244], 'meV')
# Ce_4mm = ms.crysfipy.CEFion(ms.crysfipy.Ion('Ce'), (0,0,0), Bij)

# print(Ce_4mm)

# PrOs4Sb12
# doi.org/10.1103/PhysRevLett.93.157003
# Bij_names = ['B40','B60','B66']
# Bij_values = [0.2e-2, 0.11e-3, -0.9e-3]    # orth

# Bij_subs = {key:val for key, val in zip(Bij_names, Bij_values)}

# def cal_symbolic(Elevels, Bij_names, Bij_values):
#     e_symbolic = []

#     for E in Elevels:
#         E = str(E)
#         for Bij_name, Bij_value in zip(Bij_names, Bij_values):
#             E = E.replace(Bij_name, f'({Bij_value})')

#         e = eval(E)
#         if np.abs(np.imag(e))>1e10:
#             e = np.real(e)

#         e_symbolic.append(e)

#     return np.array(e_symbolic)-min(e_symbolic)

###
# Calculations

# H = CEF_Hamiltonian(symmetry=lattice, Jval=Jval)

# H.save_latex('./Symbolic-output/test.tex')

# print(H)
# H.make_block_form()
# for Hsub in H.subs:
#     print(Hsub)
#     # print(Hsub.print_latex())

# print('Main eigenvalues')
# print(H.determine_eigenvalues())
# print(H.determine_eigenvectors())

# print(hline)

# for Hsub in H.subs:
#     print(Hsub)
#     print(Hsub.eigenvalues)
#     print(Hsub.eigenvectors)

    # if Hsub.matrix.shape[0] < 4:
    #     print('Look into eigenvectors of this Hsub')
    #     Hsub.determine_eigenvectors()
    #     print(Hsub.eigenvectors)

# print(H.Neval_eigenvalues(Bij_subs, precision=5))


# print(hline)
# for Hsub in H.make_block_form():
#     print(Hsub)
#     eigenvalues = Hsub.determine_eigenvalues()
#     eigenvectors = Hsub.determine_eigenvectors()

#     print(eigenvalues)
#     print(eigenvectors)

#     print(Hsub.Neval_eigenvectors(Bij_subs, normalize=True))
#     evals_reformat = [formula for formula, _ in eigenvalues]
#     print(cal_symbolic(evals_reformat, Bij_names, Bij_values))
        
# N = 100
# print('Time numerical')
# test = timeit.Timer(lambda: Hsub.Neval_eigenvalues(Bij_subs)) 
# print (test.timeit(N))

# print(hline)
#################################
# Test Hamiltonian
# h = Hamiltonian(base=['1', '0', '-1'], matrix=sympy.eye(3))

# print(h)

# eigenvalues = h.determine_eigenvalues()
# eigenvectors = h.determine_eigenvectors()

# print(eigenvalues)
# print(eigenvectors)
