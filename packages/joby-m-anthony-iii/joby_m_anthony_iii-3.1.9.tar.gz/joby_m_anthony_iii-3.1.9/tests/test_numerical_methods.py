import importlib.util
import logging
from joby_m_anthony_iii import numerical_methods as nm
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from random import random
import sympy as sp
import sys
from time import perf_counter

# create an external file that stores print outs
logfile = f"{os.getcwd()}/numerical_methods.log"
logger=logging.getLogger(__name__)
try: os.remove(logfile)
except FileNotFoundError:
	logging.basicConfig(filename=logfile, filemode="xt")
except PermissionError as e:
	logging.basicConfig(filename=logfile, filemode="at")
else:
	logging.basicConfig(filename=logfile, filemode="wt")
finally:
	logger.setLevel(logging.DEBUG)

#COUNT = 500000*3  # Change this value depending on the speed of your computer
COUNT = int((500000/5000)**2)  # Change this value depending on the speed of your computer
DATA = [(random() - 0.5) * 3 for _ in range(COUNT)]
rows = columns = int(np.floor(np.sqrt(len(DATA))))
COUNT = rows**columns  # Change this value depending on the speed of your computer
matrix = np.zeros((rows, columns))
for i in range(rows):
    for j in range(columns):
        matrix[i][j] = DATA[i + j]
DATA = matrix
DATA = np.reshape(DATA[:rows**columns], (rows, columns))

e = 2.7182818284590452353602874713527
pi = 3.141592653589793

def sinh(x):
	return (1 - (e ** (-2 * x))) / (2 * (e ** -x))

def cosh(x):
	return (1 + (e ** (-2 * x))) / (2 * (e ** -x))

def tanh(x):
	tanh_x = sinh(x) / cosh(x)
	return tanh_x

def build_matrix(x):
	s = 0
	rows, columns = np.shape(x)
	for i in range(rows):
		for j in range(columns):
			s += x[i][j]
	return s

def test(fn, x, name):
	start = perf_counter()
	result = fn(x)
	duration = perf_counter() - start
	print("{} took {:.3f} seconds".format(name, duration))

	#for d in result:
	#    assert -1 <= d <= 1, " incorrect values"

if __name__ == "__main__":
	# print("Running C++ extension benchmarks with COUNT = ({},{})".format(rows, columns))

	# test(lambda d: [[tanh(x) for x in r] for r in d], DATA, "[tanh(x) for x in d] (Python implementation)")

	# print("\nOnto 'numerical_methods'...\n")

	spec = importlib.util.spec_from_file_location("numerical_methods", r"..\src\joby_m_anthony_iii\numerical_methods.py")
	bar = importlib.util.module_from_spec(spec)

	# A = np.array([\
	# 	#[3, pi],
	# 	#[7, e]
	# 	# [-2, 2, -3],
	# 	# [-1, 1, 3],
	# 	# [2, 0, -1]
	# 	#[1, 1, 0],
	# 	#[1, 2, 1],
	# 	#[-1, 1, 2]
	# 	[-2, pi, 0],
	# 	[pi, 1, e],
	# 	[0, e, -1]
	# 	#[3, pi, 2, 1],\
	# 	#[4, 6, 5, 10],\
	# 	#[7, e, 9, 11],\
	# 	#[12, 13, 14, 15]
	# 	#[1, 2, 3, 4, 5, 6],
	# 	#[-2, 5, 5, 7, -1, 0],
	# 	#[1, 9, 10, 3, 0, 5],
	# 	#[-1, 11, -2, 2, 1, 4],
	# 	#[0, 19, 10, 13, -1, 4],
	# 	#[2, 2, 4, 3, -3, -2]
	# ])
	# B = np.array([\
	# 	#[3, pi],
	# 	#[7, e]
	# 	[-2, 2, -3],
	# 	[-1, 1, 3],
	# 	[2, 0, -1]
	# 	# [-2, pi, 0],
	# 	# [pi, 1, e],
	# 	# [0, e, -1]
	# 	#[3, pi, 2, 1],\
	# 	#[4, 6, 5, 10],\
	# 	#[7, e, 9, 11],\
	# 	#[12, 13, 14, 15]
	# 	#[1, 2, 3, 4, 5, 6],
	# 	#[-2, 5, 5, 7, -1, 0],
	# 	#[1, 9, 10, 3, 0, 5],
	# 	#[-1, 11, -2, 2, 1, 4],
	# 	#[0, 19, 10, 13, -1, 4],
	# 	#[2, 2, 4, 3, -3, -2]
	# ])

	# #test diagonality
	# print("Testing diagonality...")
	# print("nm.diagonality()", nm.diagonality(A))
	# # from extension import fast_diagonality
	# # print("C++", fast_diagonality(A))
	# sys.modules["diagonality"] = bar
	# spec.loader.exec_module(bar)
	# print("From path", bar.diagonality(A))

	# print("")

	# #test eigen_values
	# print("Testing eigen_values...")
	# print("nm.eigen_values()", nm.eigen_values(A))
	# # from extension import fast_eigen_values
	# # print("C++", fast_eigen_values(A))
	# sys.modules["eigen_values"] = bar
	# spec.loader.exec_module(bar)
	# print("From path", bar.eigen_values(A))

	# print("")

	# #test spectral_radius
	# print("Testing spectral_radius...")
	# print("nm.spectral_radius()", nm.spectral_radius(A))
	# #from extension import fast_spectral_radius
	# #print("C++", fast_spectral_radius(A))
	# sys.modules["spectral_radius"] = bar
	# spec.loader.exec_module(bar)
	# print("From path", bar.spectral_radius(A))

	# print("")

	# #test l_infinity
	# print("Testing l_infinity...")
	# #A = np.array([-0.38439942, 0.09028457, -0.67183719, 0.63989375])
	# #print("numpy", np.linalg.norm(A, "inf"))
	# print("nm.Norm().l_infinity()", nm.Norm(A, B).l_infinity())
	# #print("nm.Norm().l_infinity()", nm.Norm(A).l_infinity())
	# # from extension import fast_l_infinity
	# # print("C++", fast_l_infinity(A))
	# sys.modules["norms"] = bar
	# spec.loader.exec_module(bar)
	# print("From path", bar.Norm(A, B).l_infinity())

	# print("")

	# #test l_two
	# print("Testing l_two...")
	# print("nm.Norm().l_two()", nm.Norm(A, B).l_two())
	# #print("nm.Norm().l_infinity()", nm.Norm(A).l_infinity())
	# #from extension import fast_l_infinity
	# #print("C++", fast_l_infinity(A, B))
	# sys.modules["norms"] = bar
	# spec.loader.exec_module(bar)
	# print("From path", bar.Norm(A, B).l_two())
	# print("numpy", np.linalg.norm(A - B, 2))

	# # print("")

	# # #test determinant
	# # print("Testing determinant...")
	# # #sys.modules["diagonality"] = foo
	# # #spec.loader.exec_module(foo)
	# # #print("nm.diagonality()", nm.diagonality(A))
	# # from extension import fast_determinant
	# # print("C++", fast_determinant(A))
	# # #sys.modules["diagonality"] = bar
	# # #spec.loader.exec_module(bar)
	# # #print("From path", bar.diagonality(A))

	# print("")

	# #test condition_number
	# print("Testing condition_number...")
	# print("nm.condition_number()", nm.condition_number(A, "l_infinity"))
	# #from extension import condition_number
	# #print("C++", condition_number(A))
	# sys.modules["condition_number"] = bar
	# spec.loader.exec_module(bar)
	# print("From path", bar.condition_number(A, "l_infinity"))

	# print("")

	# #test symmetry
	# print("Testing symmetry...")
	# print("nm.symmetry()", nm.symmetry(A))
	# # from extension import fast_symmetry
	# # print("C++", fast_symmetry(A))
	# sys.modules["symmetry"] = bar
	# spec.loader.exec_module(bar)
	# print("From path", bar.symmetry(A))

	# print("")

	# #test tridiagonality
	# print("Testing tridiagonality...")
	# print("nm.tridiagonality()", nm.tridiagonality(A))
	# # from extension import fast_tridiagonality
	# # print("C++", fast_tridiagonality(A))
	# sys.modules["tridiagonality"] = bar
	# spec.loader.exec_module(bar)
	# print("From path", bar.tridiagonality(A))

	# # print("")

	# # #test parse_latex
	# # print("Testing parse_latex...")
	# # ltx_variable = r"x"
	# # cT = 2000 # K
	# # cP = 10e3 # MPa
	# # crho_0_300 = 3345 # kg/m3
	# # calpha_th = 3.5e-5 # 1/K
	# # cB_T0_300 = 1.29e5 # MPa
	# # cB_prime_T0 = 4.47
	# # cpartial_BT0_T = -1 # MPa/K
	# # r0 = crho_0_300 # kg/m3
	# # fB_T0 = cB_T0_300 + cpartial_BT0_T*(cT - 300)
	# # frho_0 = crho_0_300*(1 - calpha_th*(cT - 300))
	# # ltx_dict = {
	# # 	"cT": cT,
	# # 	r"c_{P}": cP,
	# # 	"crho_0_300": crho_0_300,
	# # 	r"calpha_th": calpha_th,
	# # 	"cB_T0_300": cB_T0_300,
	# # 	r"cB_prime_T0": cB_prime_T0,
	# # 	"cpartial_BT0_T": cpartial_BT0_T,
	# # 	r"r0": r0,
	# # 	"fB_T0": fB_T0,
	# # 	r"frho_0": frho_0
	# # }
	# # #lambda_expression = lambda x: f"{cP} - (3*{fB_T0}/2) * (({x}/{frho_0})^(7/3) - ({x}/{frho_0})^(5/3)* (1 + 3/4*({cB_prime_T0} - 4)*(({x}/{frho_0})^(2/3) - 1)))"
	# # #ltx_expression = lambda_expression#.encode("utf-8")#.decode("utf-8") # r"{}".format
	# # ltx_expression = r"c_{P} - (\frac{3}{2}*fB_T0) * ((\frac{x}{frho_0})^{\frac{7}{3}} - (\frac{x}{frho_0})^{\frac{5}{3}}*(1 + \frac{3}{4}*(cB_prime_T0 - 4)*((\frac{x}{frho_0})^{\frac{2}{3}} - 1)))"
	# # #lambda_expression = lambda x: cP - (3*fB_T0/2) * ((x/frho_0)**(7/3) - (x/frho_0)**(5/3)* (1 + 3/4*(cB_prime_T0 - 4)*((x/frho_0)**(2/3) - 1)))
	# # #print(lambda_expression(pi))
	# # from extension import fast_parse_latex
	# # parsed_string = fast_parse_latex(ltx_expression, ltx_dict)
	# # print("C++ (parse)", parsed_string)

	# # print("")

	# # #test eval_latex
	# # print("Testing eval_latex...")
	# # from extension import fast_eval_latex
	# # print(f"C++ parse({ltx_variable} = {pi})", fast_eval_latex(parsed_string, {"x": pi}))

	# # print("")

	# # #test derive_latex
	# # print("Testing derive_latex...")
	# # from extension import fast_derive_latex
	# # derived_string = fast_derive_latex(parsed_string, ltx_variable, degree=2)
	# # print("C++ (derive)", derived_string)
	# # print(f"C++ derive({ltx_variable} = {pi})", fast_eval_latex(derived_string, {"x": pi}))

	# print("")

	# #test SingleVariableIteration
	# print("Testing SingleVariableIteration...")
	# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7,7))
	# fig.suptitle("'SingleVariableIteration()' Methods")
	# ax2r = ax2.twinx()
	# ax2.get_yaxis().set_visible(False)
	# line_labels = []
	# cT = 2000 # K
	# cP = 10e3 # MPa
	# crho_0_300 = 3345 # kg/m3
	# calpha_th = 3.5e-5 # 1/K
	# cB_T0_300 = 1.29e5 # MPa
	# cB_prime_T0 = 4.47
	# cpartial_BT0_T = -1 # MPa/K
	# r0 = crho_0_300 # kg/m3
	# fB_T0 = cB_T0_300 + cpartial_BT0_T*(cT - 300)
	# frho_0 = crho_0_300*(1 - calpha_th*(cT - 300))
	# # ltx_dict = {
	# # 	"cT": cT,
	# # 	r"cP": cP,
	# # 	"crho_0_300": crho_0_300,
	# # 	r"calpha_th": calpha_th,
	# # 	"cB_T0_300": cB_T0_300,
	# # 	r"cB_prime_T0": cB_prime_T0,
	# # 	"cpartial_BT0_T": cpartial_BT0_T,
	# # 	r"r0": r0,
	# # 	"fB_T0": fB_T0,
	# # 	r"frho_0": frho_0
	# # }
	# # ltx_variable = "x"
	# # ltx_expression = r"cP - (3*fB_T0/2) * ((x/frho_0)^(7/3) - (x/frho_0)^(5/3)) * (1 + 3/4*(cB_prime_T0 - 4)*((x/frho_0)^(2/3) - 1))"
	# # from extension import fast_parse_latex
	# # parsed_string = fast_parse_latex(ltx_expression, ltx_dict)
	# # print("C++ (parse)", parsed_string)
	# parsed_string = lambda x: cP - (3*fB_T0/2) * ((x/frho_0)**(7/3) - (x/frho_0)**(5/3)) * (1 + 3/4*(cB_prime_T0 - 4)*((x/frho_0)**(2/3) - 1))
	# sys.modules["SingleVariableIteration"] = bar
	# spec.loader.exec_module(bar)
	# obj = bar.SingleVariableIteration(
	# 	parsed_string, 1e3, 6e3, iter_guess=1e3)
	# meth_bisect = obj.bisection()
	# bisect_approx, = ax1.semilogx(
	# 	meth_bisect["Iterations"].values,
	# 	meth_bisect["Approximations"].values,
	# 	label=f"Bisection (k={meth_bisect['Iterations'].values[-1]}): {meth_bisect['Approximations'].values[-1]:4.2f}"
	# )
	# bisect_error, = ax2r.plot(
	# 	meth_bisect["Iterations"].values,
	# 	meth_bisect["Errors"].values,
	# 	label=f"Bisection (k={meth_bisect['Iterations'].values[-1]}): {meth_bisect['Errors'].values[-1]:4.2f}"
	# )
	# line_labels.append(f"Bisection (k={meth_bisect['Iterations'].values[-1]}): {meth_bisect['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_bisect['Errors'].values):4.2f})")
	# meth_false_position = obj.false_position(1.5e3, 5.5e3)
	# falsepos_approx, = ax1.semilogx(
	# 	meth_false_position["Iterations"].values,
	# 	meth_false_position["Approximations"].values,
	# 	label=f"False Position (k={meth_false_position['Iterations'].values[-1]}): {meth_false_position['Approximations'].values[-1]:4.2f}"
	# )
	# falsepos_error, = ax2r.plot(
	# 	meth_false_position["Iterations"].values,
	# 	meth_false_position["Errors"].values,
	# 	label=f"False Position (k={meth_false_position['Iterations'].values[-1]}): {meth_false_position['Errors'].values[-1]:4.2f}"
	# )
	# line_labels.append(f"False Position (k={meth_false_position['Iterations'].values[-1]}): {meth_false_position['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_false_position['Errors'].values):4.2f})")
	# # meth_fixed_point = obj.fixed_point(3.3e3)
	# # fp_approx, = ax1.semilogx(
	# #    meth_fixed_point["Iterations"].values,
	# #    meth_fixed_point["Approximations"].values,
	# #    label=f"Fixed-Point (k={meth_fixed_point['Iterations'].values[-1]}): {meth_fixed_point['Approximations'].values[-1]:4.2f}"
	# # )
	# # fp_error, = ax2r.plot(
	# #    meth_fixed_point["Iterations"].values,
	# #    meth_fixed_point["Errors"].values,
	# #    label=f"Fixed-Point (k={meth_fixed_point['Iterations'].values[-1]}): {meth_fixed_point['Errors'].values[-1]:4.2f}"
	# # )
	# # line_labels.append(f"Fixed-Point (k={meth_fixed_point['Iterations'].values[-1]}): {meth_fixed_point['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_fixed_point['Errors'].values):4.2f})")
	# meth_newton_raphson = obj.newton_raphson(crho_0_300)
	# nr_approx, = ax1.semilogx(
	# 	meth_newton_raphson["Iterations"].values,
	# 	meth_newton_raphson["Approximations"].values,
	# 	label=f"Newton-Raphson (k={meth_newton_raphson['Iterations'].values[-1]}): {meth_newton_raphson['Approximations'].values[-1]:4.2f}",
	# )
	# nr_error, = ax2r.plot(
	# 	meth_newton_raphson["Iterations"].values,
	# 	meth_newton_raphson["Errors"].values,
	# 	label=f"Newton-Raphson (k={meth_newton_raphson['Iterations'].values[-1]}): {meth_newton_raphson['Errors'].values[-1]:4.2f}"
	# )
	# line_labels.append(f"Newton-Raphson (k={meth_newton_raphson['Iterations'].values[-1]}): {meth_newton_raphson['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_newton_raphson['Errors'].values):4.2f})")
	# meth_secant_method = obj.secant_method(1.5e3, 5.5e3)
	# secant_approx, = ax1.semilogx(
	# 	meth_secant_method["Iterations"].values,
	# 	meth_secant_method["Approximations"].values,    
	# 	label=f"Secant (k={meth_secant_method['Iterations'].values[-1]}): {meth_secant_method['Approximations'].values[-1]:4.2f}",
	# )
	# secant_error, = ax2r.plot(
	# 	meth_secant_method["Iterations"].values,
	# 	meth_secant_method["Errors"].values,    
	# 	label=f"Secant (k={meth_secant_method['Iterations'].values[-1]}): {meth_secant_method['Errors'].values[-1]:4.2f}"
	# )
	# line_labels.append(f"Secant (k={meth_secant_method['Iterations'].values[-1]}): {meth_secant_method['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_secant_method['Errors'].values):4.2f})")
	# ax1.set_title("Convergence of 'p'")
	# ax1.set_xlabel("Iterations")
	# ax1.set_ylabel("Value 'p'")
	# #ax1.legend(
	# #	handles=[bisect_approx, falsepos_approx, nr_approx, secant_approx],
	# #	bbox_to_anchor=(0, 1),
	# #	bbox_transform=fig.transFigure
	# #)
	# ax2r.set_title("Comparing Errors of Methods")
	# ax2.set_xlabel("Iterations")
	# ax2r.set_ylabel("Absolute Errors")
	# fig.legend([ax1, ax2], # The line objects
	# 	labels=line_labels, # The labels for each line
	# 	loc="lower center", # Position of legend
	# 	ncol=2,
	# 	fontsize="small",
	# 	mode="expand",
	# 	title="Legend", # Title for the legend
	# 	borderaxespad=0.1 # Small spacing around legend box
	# )
	# # Adjust the scaling factor to fit your legend text completely outside the plot
	# # (smaller value results in more space being made for the legend)
	# plt.subplots_adjust(bottom=0.175)
	# #plt.show()

	# print("")

	# # test MultiVariableIteration
	# print("Testing MultiVariableIteration...")
	# fig = plt.figure(figsize=(7,7))
	# fig.suptitle("'MultiVariableIteration()' Methods")
	# ax = fig.add_gridspec(4, 2)
	# ax1 = fig.add_subplot(ax[0, 0])
	# ax1.get_xaxis().set_visible(False)
	# ax2 = fig.add_subplot(ax[1, 0])
	# ax2.get_xaxis().set_visible(False)
	# ax3 = fig.add_subplot(ax[2, 0])
	# ax3.get_xaxis().set_visible(False)
	# ax4 = fig.add_subplot(ax[3, 0])
	# ax3.get_xaxis().set_visible(True)
	# ax5 = fig.add_subplot(ax[:, 1])
	# ax5r = ax5.twinx()
	# ax5.get_yaxis().set_visible(False)
	# line_labels = []
	# sys.modules["MultiVariableIteration"] = bar
	# spec.loader.exec_module(bar)
	# ## 		supplied parameters
	# # 4x4 matrix 
	# A = [\
	# 	[4., 0., -1., 1.],\
	# 	[1., 4., -1., -1.],\
	# 	[-1., -1., 5., 1.],\
	# 	[1., -1., 1., 3.]\
	# ]
	# # 4x1 vertical vector
	# b = [-2., -1., 0., 1.]
	# # initial guess, x vector
	# x0 = [0., 0., 0., 0.]
	# omega = 1.2
	# obj = bar.MultiVariableIteration(A, x0, b)
	# df_jacobi = obj.jacobi()
	# df_gauss = obj.gauss_seidel()
	# df_sr = obj.successive_relaxation(omega=omega)
	# dataframes = [df_jacobi, df_gauss, df_sr]
	# df_labels = ["Jacobi", "Gauss-Seidel", f"Successive Relaxation (w={omega})"]
	# k = 0
	# for df in dataframes:
	# 	ax1.semilogx(df["Iterations"].values, [df["Approximations"].values[i][0] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax2.semilogx(df["Iterations"].values, [df["Approximations"].values[i][1] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax3.semilogx(df["Iterations"].values, [df["Approximations"].values[i][2] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax4.semilogx(df["Iterations"].values, [df["Approximations"].values[i][3] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# ax5r.plot(df_jacobi["Iterations"].values, df_jacobi["Errors"].values, label=f"{df_labels[0]} (k={df_jacobi['Iterations'].values[-1]}): E={df_jacobi['Errors'].values[-1]:1.4f}")
	# line_labels.append(f"{df_labels[0]} (k={df_jacobi['Iterations'].values[-1]}): Error={np.sum(df_jacobi['Errors'].values):1.4f}")
	# ax5r.plot(df_gauss["Iterations"].values, df_gauss["Errors"].values, label=f"{df_labels[1]} (k={df_gauss['Iterations'].values[-1]}): E={df_gauss['Errors'].values[-1]:1.4f}")
	# line_labels.append(f"{df_labels[1]} (k={df_gauss['Iterations'].values[-1]}): Error={np.sum(df_gauss['Errors'].values):1.4f}")
	# ax5r.plot(df_sr["Iterations"].values, df_sr["Errors"].values, label=f"{df_labels[2]} (k={df_sr['Iterations'].values[-1]}): E={df_sr['Errors'].values[-1]:1.4f}")
	# line_labels.append(f"{df_labels[2]} (k={df_sr['Iterations'].values[-1]}): Error={np.sum(df_sr['Errors'].values):1.4f}")
	# ax1.set_ylabel(r"$x_{0}$")
	# #ax1.legend()
	# ax2.set_ylabel(r"$x_{1}$")
	# #ax2.legend()
	# ax3.set_ylabel(r"$x_{2}$")
	# #ax3.legend()
	# ax4.set_xlabel("Iterations")
	# ax4.set_ylabel(r"$x_{3}$")
	# #ax4.legend()
	# ax5.set_xlabel("Iterations")
	# ax5r.set_ylabel("Absolute Errors")
	# ax5r.set_title("Comparing Errors of Methods")
	# #ax5r.legend(bbox_to_anchor=(1, 1), bbox_transform=fig.transFigure)
	# fig.legend([ax1, ax2, ax3, ax4, ax5], # The line objects
	# 	labels=line_labels, # The labels for each line
	# 	loc="lower center", # Position of legend
	# 	ncol=3,
	# 	fontsize="x-small",
	# 	mode="expand",
	# 	title="Legend", # Title for the legend
	# 	borderaxespad=0.1 # Small spacing around legend box
	# )
	# # Adjust the scaling factor to fit your legend text completely outside the plot
	# # (smaller value results in more space being made for the legend)
	# plt.subplots_adjust(bottom=0.125)
	# #plt.show()

	# print("")

	# # test MultiVariableIteration.newton_raphson()
	# print("Testing MultiVariableIteration.newton_raphson()...")
	# fig = plt.figure(figsize=(7,7))
	# fig.suptitle("'MultiVariableIteration().newton_raphson()' Method")
	# ax = fig.add_gridspec(3, 2)
	# ax1 = fig.add_subplot(ax[0, 0])
	# ax1.get_xaxis().set_visible(False)
	# ax2 = fig.add_subplot(ax[1, 0])
	# ax2.get_xaxis().set_visible(False)
	# ax3 = fig.add_subplot(ax[2, 0])
	# ax3.get_xaxis().set_visible(True)
	# ax4 = fig.add_subplot(ax[:, 1])
	# ax4r = ax4.twinx()
	# ax4.get_yaxis().set_visible(False)
	# line_labels = []
	# sys.modules["MultiVariableIteration"] = bar
	# spec.loader.exec_module(bar)
	# ## 		supplied parameters
	# # 4x4 matrix 
	# A = [\
	# 	lambda x1, x2, x3: 3*x1 - sp.cos(x2*x3) - 1/2,
	# 	lambda x1, x2, x3: x1**2 - 81*(x2 + 0.1)**2 + sp.sin(x3) + 1.06,
	# 	lambda x1, x2, x3: sp.exp(-x1*x2) + 20*x3 + (10*math.pi - 3)/3
	# ]
	# # 4x1 vertical vector
	# b = [0, 0, 0]
	# # initial guess, x vector
	# x0 = [0.1, 0.1, -0.1]
	# symbols = ["x1", "x2", "x3"]
	# obj = bar.MultiVariableIteration(A, x0, b)
	# df_nr = obj.newton_raphson(symbols)
	# dataframes = [df_nr]
	# df_labels = ["Newton-Raphson"]
	# k = 0
	# for df in dataframes:
	# 	ax1.plot(df["Iterations"].values, [df["Approximations"].values[i][0] for i in df["Iterations"].values], label=f"{df['Approximations'].values[-1][0]:1.4f}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax2.plot(df["Iterations"].values, [df["Approximations"].values[i][1] for i in df["Iterations"].values], label=f"{df['Approximations'].values[-1][1]:1.4f}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax3.plot(df["Iterations"].values, [df["Approximations"].values[i][2] for i in df["Iterations"].values], label=f"{df['Approximations'].values[-1][2]:1.4f}")
	# 	k += 1
	# ax4r.plot(df_nr["Iterations"].values, df_nr["Errors"].values, label=f"{df_labels[0]} (k={df_nr['Iterations'].values[-1]}): E={df_nr['Errors'].values[-1]:1.4f}")
	# line_labels.append(f"{df_labels[0]} (k={df_nr['Iterations'].values[-1]}): Error={np.sum(df_nr['Errors'].values):1.4f}")
	# ax1.set_ylabel(r"$x_{0}$")
	# ax1.legend()
	# ax2.set_ylabel(r"$x_{1}$")
	# ax2.legend()
	# ax3.set_xlabel("Iterations")
	# ax3.set_ylabel(r"$x_{2}$")
	# ax3.legend()
	# ax4.set_xlabel("Iterations")
	# ax4r.set_ylabel("Absolute Errors")
	# ax4r.set_title("Comparing Errors of Methods")
	# #ax4r.legend(bbox_to_anchor=(1, 1), bbox_transform=fig.transFigure)
	# fig.legend([ax1, ax2, ax3, ax4], # The line objects
	# 	labels=line_labels, # The labels for each line
	# 	loc="lower center", # Position of legend
	# 	ncol=3,
	# 	fontsize="x-small",
	# 	mode="expand",
	# 	title="Legend", # Title for the legend
	# 	borderaxespad=0.1 # Small spacing around legend box
	# )
	# # Adjust the scaling factor to fit your legend text completely outside the plot
	# # (smaller value results in more space being made for the legend)
	# plt.subplots_adjust(bottom=0.125)
	# # plt.show()

	# print("")

	# # test cubic_spline
	# print("Testing cubic_spline...")
	# sys.modules["cubic_spline"] = bar
	# spec.loader.exec_module(bar)
	# ## 		supplied parameters
	# X = [0.0, 0.3, 0.5]
	# a, b = 0.0, 0.5
	# method = "Clamped"
	# # ltx_variable = "x"
	# # ltx_expression = r"\sin(3x)"
	# #ltx_expression = np.sin(3*np.array(X))
	# ltx_expression = lambda x: math.sin(3*x)
	# Y = [ltx_expression(x) for x in X]
	# #ltx_expression = [0, 0.7]
	# obj = bar.CubicSpline(X, Y)
	# if method == "Clamped":
	# 	Y, S = obj.clamped()
	# elif method == "Natural":
	# 	Y, S = obj.natural()
	# ### 		console outputs
	# # print('Interpolant Spline 1, $S_{0}$ = ', S_str[0])
	# # print('Interpolant Spline 2, $S_{1}$ = ', S_str[1])
	# #print('Clamped Cubic Spline, $s(x)$ = ','\n')
	# #print(spline,'\n')
	# ## 		output plots
	# plt.figure(figsize=(7,7))
	# plt.title(f"Cubic Spline ({method})")
	# plt.scatter(X,Y, color='r', label="Raw Data")
	# X1, Y1 = np.arange(a, X[1]+0.01, 0.01), []
	# for x in X1:
	# 	Y1.append(S[0](x))
	# plt.plot(X1,Y1, color='g', label=f"Interpolant 1")
	# X2, Y2 = np.arange(X[1], X[2]+0.01, 0.01), []
	# for x in X2:
	# 	Y2.append(S[1](x))
	# plt.plot(X2,Y2, color='b', label=f"Interpolant 2")
	# plt.xlabel("Real Domain [rad]")
	# plt.ylabel("Real Range [rad]")
	# plt.legend()
	# #plt.show()

	# print("")

	# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7,7))
	# fig.suptitle("Lagrangian and Hermetic Polynomials")
	# ax2r = ax2.twinx()
	# ax2.get_yaxis().set_visible(False)
	# # test lagrangian polynomials
	# print("Testing Lagrangian polynomials...")
	# sys.modules["lagrange"] = bar
	# spec.loader.exec_module(bar)
	# # sample time of study
	# D = [0, 5, 9, 12, 16, 23, 28] # days
	# # average mass on day in milligrams
	# samp_1 = [5, 14, 39, 34, 28, 26, 25] # mg
	# samp_2 = [5, 13, 15, 14, 12, 11, 10] # mg
	# #sym_x = sp.Symbol('x')
	# # first sample
	# # Lagrange polynomial and progressive error
	# Px1, Px1_err = bar.lagrange(D, samp_1, degree=4)
	# # second sample
	# # Lagrange polynomial and progressive error
	# Px2, Px2_err = bar.lagrange(D, samp_2, degree=4)
	# # substitute to time domain
	# dt = 1 # (days) time increment 
	# # time domain of study
	# time = np.arange(D[0], D[-1]+1, dt)
	# Y1 = []; Y2 = []        # initialize list
	# # buld curves from Lagrange polynomials
	# for t in time:
	# 	Y1.append(Px1(t))
	# 	Y2.append(Px2(t))
	# ## 		console outputs
	# # first sample results
	# print('**'*8, 'Sample 1 Results', '**'*8, sep=' ')
	# #print('Polynomial of Sample 1:\n', Px1("x"),end='\n')
	# print('Progressive Errors of First Sample: ', np.sum(Px1_err))
	# print('Maximum Value = ', int(np.amax(Y1)),' (mg)')
	# print('Minimum Value = ', int(np.amin(Y1)),' (mg)')
	# # second sample results
	# print('**'*8, 'Sample 2 Results', '**'*8, sep=' ')
	# #print('Polynomial of Sample 2:\n', sp.simplify(Px2(sym_x)),end='\n')
	# print('Progressive Errors of Second Sample: ', np.sum(Px2_err))
	# print('Maximum Value = ', int(np.amax(Y2)),' (mg)')
	# print('Minimum Value = ', int(np.amin(Y2)),' (mg)')
	# ## 		output plots
	# ax1.set_title("Lagrange")
	# # first data set and polynomial
	# ax1.plot(D,samp_1, color='r', label='Sample 1 (Raw)')
	# ax1.plot(time,Y1, color='g', label=f'Sample 1 (Y1) Error = {np.sum(Px1_err):4.4f}')
	# ax1.set_xlabel('Days')
	# ax1.set_ylabel('Average Weight [mg]')
	# # second data set and polynomial
	# ax1.plot(D,samp_2, color='b', label='Sample 2 (Raw)')
	# ax1.plot(time,Y2, color='k', label=f'Sample 2 (Y2) Error = {np.sum(Px2_err):4.4f}')
	# ax1.set_xlabel('Days')
	# ax1.set_ylabel('Average Weight [mg]')
	# ax1.legend()
	# #plt.show()

	# print("")

	# # test hermetic polynomials
	# print("Testing Hermetic polynomials...")
	# sys.modules["hermite"] = bar
	# spec.loader.exec_module(bar)
	# # sample time of study
	# D = [0, 5, 9, 12, 16, 23, 28] # days
	# # average mass on day in milligrams
	# samp_1 = [5, 14, 39, 34, 28, 26, 25] # mg
	# samp_2 = [5, 13, 15, 14, 12, 11, 10] # mg
	# # first sample
	# # Hermetic polynomial and progressive error
	# Px1 = bar.hermite(D, samp_1)
	# # substitute to time domain
	# dt = 1 # (days) time increment 
	# # time domain of study
	# time = np.arange(D[0], D[-1]+1, dt)
	# Y1 = []; Y2 = []        # initialize list
	# # buld curves from Hermitic polynomials
	# for t in time:
	# 	Y1.append(Px1(t))
	# 	Y2.append(Px2(t))
	# ## 		console outputs
	# # first sample results
	# print('**'*8, 'Sample 1 Results', '**'*8, sep=' ')
	# #print('Polynomial of Sample 1:\n', Px1("x"),end='\n')
	# #print('Progressive Errors of First Sample:\n',Px1_err, end='\n')
	# # print(poly_str)
	# print('Maximum Value = ', int(np.amax(Y1)),' (mg)')
	# print('Minimum Value = ', int(np.amin(Y1)),' (mg)')
	# # second sample results
	# # Hermetic polynomial and progressive error
	# Px2 = bar.hermite(D, samp_2)
	# Y1 = []; Y2 = []        # initialize list
	# # buld curves from Hermitic polynomials
	# for t in time:
	# 	Y1.append(Px1(t))
	# 	Y2.append(Px2(t))
	# print('**'*8, 'Sample 2 Results', '**'*8, sep=' ')
	# #print('Polynomial of Sample 2:\n', sp.simplify(Px2(sym_x)),end='\n')
	# #print('Progressive Errors of Second Sample:\n',Px2_err, end='\n')
	# # print(poly_str)
	# print('Maximum Value = ', int(np.amax(Y2)),' (mg)')
	# print('Minimum Value = ', int(np.amin(Y2)),' (mg)')
	# ## 		output plots
	# ax2r.set_title("Hermite")
	# # first data set and polynomial
	# ax2r.plot(D,samp_1, color='r', label='Sample 1 (Raw)')
	# ax2r.plot(time,Y1, color='g', label=f'Sample 1 (Y1)')
	# # second data set and polynomial
	# ax2r.plot(D,samp_2, color='b', label='Sample 2 (Raw)')
	# ax2r.plot(time,Y2, color='k', label=f'Sample 2 (Y2)')
	# ax2.set_xlabel('Days')
	# ax2r.set_ylabel('Average Weight [mg]')
	# ax2r.legend()
	# #plt.show()

	# print("")

	# # test least_squares
	# print("Testing least_squares...")
	# sys.modules["least_squares"] = bar
	# spec.loader.exec_module(bar)
	# plt.figure(figsize=(7,7))
	# plt.title("Raw Data versus Least Square Polynomial and Power Law")
	# ## 		supplied parameters
	# # x_i 
	# X_i = [0.01, 0.15, 0.31, 0.5, 0.6, 0.75]
	# # y_i 
	# Y_i = [1.0, 1.004, 1.031, 1.117, 1.223, 1.422]
	# degree = 2
	# obj = bar.LeastSquares(X_i, Y_i)
	# polynomial, error = obj.linear(degree)
	# plt.scatter(X_i,Y_i, color='r', label='Raw Data')
	# # build arrays to plot
	# dx = 0.01 			# distance between discrete elements
	# # X = discretize domain
	# # Y = empty list for range of domain, X
	# X, Y = np.arange(X_i[0],\
	# 	X_i[-1] + (X_i[-1] - X_i[-2]), dx), []
	# for x in X: 		# for each element in domain
	# 	# write to range, Y
	# 	Y.append(polynomial(x))
	# ## 		output plots
	# plt.plot(X,Y, color='g', label=f"Polynomial, n = {degree} (error = {error:1.4f})")
	# power_a, power_b, power_expression = obj.power()
	# # build arrays to plot
	# dx = 0.01 			# distance between discrete elements
	# # X = discretize domain
	# # Y = empty list for range of domain, X
	# X, Y = np.arange(X_i[0],\
	# 	X_i[-1] + (X_i[-1] - X_i[-2]), dx), []
	# for x in X: 		# for each element in domain
	# 	# write to range, Y
	# 	Y.append(power_expression(x))
	# ## 		output plots
	# plt.plot(X,Y, color='b', label=f'Power: {power_a:1.4f}x**{power_b:1.4f}')
	# plt.xlabel('Real Domain')
	# plt.ylabel('Real Range')
	# plt.legend()
	# #plt.show()

	# print("")

	# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7,7))
	# fig.suptitle("Applying Newton Difference Methods")
	# ax2r = ax2.twinx()
	# ax2.get_yaxis().set_visible(False)
	# # test newton_difference
	# print("Testing newton_difference...")
	# sys.modules["newton_difference"] = bar
	# spec.loader.exec_module(bar)
	# ## 		supplied parameters
	# X = [-1.2, -0.9, -0.6, -0.3, 0.0]
	# FX = [0.18232, -0.105083, -0.51036, -1.20397, -3.12145]
	# alpha = -1.0
	# ax1.set_title("Newton Difference")
	# ax1.scatter(X,FX, color='r', label='Raw Data')
	# polynomial = bar.newton_difference(X, FX, alpha)
	# # graph from discretized data
	# da = 0.1                                # increment 
	# A = np.arange(X[0], X[-1]+1, da)        # real domain
	# Y = []                                  # make empty list
	# for a in A:
	# 	Y.append(polynomial(a)) # store to list, Y
	# ## 		output plots
	# ax1.plot(A,Y, color='g', label=f"Forward: P(x={alpha}) = {polynomial(alpha):1.4f}")
	# alpha = -0.2
	# polynomial = bar.newton_difference(X, FX, alpha, direction="backward")
	# # graph from discretized data
	# da = 0.1                                # increment 
	# A = np.arange(X[0], X[-1]+1, da)        # real domain
	# Y = []                                  # make empty list
	# for a in A:
	# 	Y.append(polynomial(a)) # store to list, Y
	# ## 		output plots
	# ax1.plot(A,Y, color='b', label=f"Backward: P(x={alpha}) = {polynomial(alpha):1.4f}")
	# ax1.set_xlabel('Real Domain')
	# ax1.set_ylabel('Real Range')
	# ax1.legend()
	# #plt.show()

	# print("")

	# # test richard_extrapolation
	# print("Testing richard_extrapolation...")
	# sys.modules["richard_extrapolation"] = bar
	# spec.loader.exec_module(bar)
	# ## 		supplied parameters
	# x0, h, order = 1, 0.2, 4
	# # ltx_variable = "x"
	# # ltx_expression = r"\sin(x)*(2)^{x}"
	# # #ltx_expression = r"\cos(x)*((2)^{x}) + \sin(x)*((2)^{x})*\log(2)"
	# ltx_expression = lambda x: (2**x)*sp.sin(x)
	# X = []
	# for i in range(order): X.append(x0+h/(2**(order-i)))
	# ltx_diff = sp.diff(ltx_expression(sp.Symbol("x")), sp.Symbol("x"))
	# lambda_expression = sp.lambdify(sp.Symbol("x"), ltx_diff)
	# #print(ltx_diff)
	# raw = []
	# for x in X: raw.append(lambda_expression(x))
	# ## 		output plots
	# ax2r.set_title("Richardson's Extrapolation of Derivative")
	# ax2r.scatter(X,raw, color='r', label='Raw Data')
	# polynomial = bar.richard_extrapolation(ltx_expression, x0, h, order)
	# # graph from discretized data
	# da = h/100                                # increment 
	# A = np.arange(X[0]-1, X[-1]+X[0], da)        # real domain
	# Y = []                                  # make empty list
	# for a in A:
	# 	Y.append(polynomial(a)) # store to list, Y
	# ax2r.plot(A,Y, color='g', label=f"Forward: P(x={x0}) = {polynomial(x0):1.4f}")
	# polynomial = bar.richard_extrapolation(ltx_expression, X[-1], h, order, direction="backward")
	# # graph from discretized data
	# da = h/100                                # increment 
	# A = np.arange(X[0]-1, X[-1]+X[0], da)        # real domain
	# Y = []                                  # make empty list
	# for a in A:
	# 	Y.append(polynomial(a)) # store to list, Y
	# ax2r.plot(A,Y, color='b', label=f"Backward: P(x={X[-1]}) = {polynomial(X[-1]):1.4f}")
	# ax2.set_xlabel('Real Domain')
	# ax2r.set_ylabel('Real Range')
	# ax2r.legend()
	# #plt.show()

	# print("")

	# # test integrate
	# print("Testing integrate...")
	# sys.modules["integrate"] = bar
	# spec.loader.exec_module(bar)
	# ## 		supplied parameters
	# h, a, b = 0.25, 1, 2
	# # ltx_variable = "x"
	# # ltx_expression = r"\cos(x)*(x)^{2}"
	# lambda_expression = lambda x: math.cos(x)*x**2
	# X = np.arange(a, b+h, h)
	# Y = np.cos(X)*X**2
	# obj = bar.Integrate(lambda_expression, a=a, b=b, h=h, scheme="open")
	# # obj = bar.Integrate(lambda_expression, X, scheme="open")
	# # obj = bar.Integrate(Y, X, a=a, b=b, h=h, scheme="open")
	# # obj = bar.Integrate(Y, X, scheme="open")
	# domain, rng, area = obj.simpson()
	# print(f"Simpson, A = {area}")
	# domain, rng, area = obj.trapezoidal()
	# print(f"Trapezoidal, A = {area}")

	# print("")

	# # test EigenValues...
	# print("Testing EigenValues...")
	# sys.modules["EigenValues"] = bar
	# spec.loader.exec_module(bar)
	# fig = plt.figure(figsize=(7,7))
	# fig.suptitle(r"Finding Eigenvalues ($\lambda$) of Matrix")
	# ax = fig.add_gridspec(4, 2)
	# ax1 = fig.add_subplot(ax[0, 0])
	# ax1.get_xaxis().set_visible(False)
	# ax2 = fig.add_subplot(ax[1, 0])
	# ax2.get_xaxis().set_visible(False)
	# ax3 = fig.add_subplot(ax[2, 0])
	# ax3.get_xaxis().set_visible(False)
	# ax4 = fig.add_subplot(ax[3, 0])
	# ax4.get_xaxis().set_visible(True)
	# ax5 = fig.add_subplot(ax[:, 1])
	# ax5r = ax5.twinx()
	# ax5.get_yaxis().set_visible(False)
	# line_labels = []
	# A = [
	# 	[2, -1, 0, 0],
	# 	[-1, 2, 0, -1],
	# 	[0, 0, 4, -2],
	# 	[0, -1, -2, 4]
	# ]
	# tol, x = -10, np.transpose(np.matrix([1, 1, 1, 1]))
	# obj = bar.EigenValues(A, tol)
	# # power_method
	# df_power = obj.power_method(x)
	# print(f"Testing EigenValues().power_method()...{df_power['Lambdas'].values[-1].transpose()[0]*df_power['Mu'].values[-1]}")
	# # inverse_power_method
	# q = 3
	# df_inverse = obj.inverse_power_method(x, q)
	# print(f"Testing EigenValues().inverse_power_method()...{df_inverse['Lambdas'].values[-1].transpose()[0]*df_inverse['Mu'].values[-1]}")
	# # qr_algorithm
	# df_qr = obj.qr_algorithm()
	# print(f"Testing EigenValues().qr_algorithm()...{df_qr['Lambdas'].values[-1]}")
	# dataframes = [df_power, df_inverse, df_qr]
	# df_labels = ["Power", "Inverse Power", "QR", "Steepest Descent", "Conjugate Gradient"]
	# k = 0
	# for df in dataframes:
	# 	ax1.semilogx(df["Iterations"].values, [df["Lambdas"].values[i][0] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax2.semilogx(df["Iterations"].values, [df["Lambdas"].values[i][1] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax3.semilogx(df["Iterations"].values, [df["Lambdas"].values[i][2] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax4.semilogx(df["Iterations"].values, [df["Lambdas"].values[i][3] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# ax5r.plot(df_power["Iterations"].values, df_power["Errors"].values, label=f"{df_labels[0]} (k={df_power['Iterations'].values[-1]}): E={df_power['Errors'].values[-1]:1.4f}")
	# line_labels.append(f"{df_labels[0]} (k={df_power['Iterations'].values[-1]}): Error={np.sum(df_power['Errors'].values):1.4f}")
	# ax5r.plot(df_inverse["Iterations"].values, df_inverse["Errors"].values, label=f"{df_labels[1]} (k={df_inverse['Iterations'].values[-1]}): E={df_inverse['Errors'].values[-1]:1.4f}")
	# line_labels.append(f"{df_labels[1]} (k={df_inverse['Iterations'].values[-1]}): Error={np.sum(df_inverse['Errors'].values):1.4f}")
	# ax5r.plot(df_qr["Iterations"].values, df_qr["Errors"].values, label=f"{df_labels[2]} (k={df_qr['Iterations'].values[-1]}): E={df_qr['Errors'].values[-1]:1.4f}")
	# line_labels.append(f"{df_labels[2]} (k={df_qr['Iterations'].values[-1]}): Error={np.sum(df_qr['Errors'].values):1.4f}")
	# ax1.set_xlabel("Iterations")
	# ax1.set_ylabel(r"$x_{0}$")
	# #ax1.legend()
	# ax2.set_xlabel("Iterations")
	# ax2.set_ylabel(r"$x_{1}$")
	# #ax2.legend()
	# ax3.set_xlabel("Iterations")
	# ax3.set_ylabel(r"$x_{2}$")
	# #ax3.legend()
	# ax4.set_xlabel("Iterations")
	# ax4.set_ylabel(r"$x_{3}$")
	# #ax4.legend()
	# ax5r.set_title("Comparing Errors of Methods")
	# ax5.set_xlabel("Iterations")
	# ax5r.set_ylabel("Absolute Errors")
	# #ax5r.legend()
	# fig.legend([ax1, ax2, ax3, ax4, ax5], # The line objects
	# 	labels=line_labels, # The labels for each line
	# 	loc="lower center", # Position of legend
	# 	ncol=3,
	# 	fontsize="x-small",
	# 	mode="expand",
	# 	title="Legend", # Title for the legend
	# 	borderaxespad=0.1 # Small spacing around legend box
	# )
	# # Adjust the scaling factor to fit your legend text completely outside the plot
	# # (smaller value results in more space being made for the legend)
	# plt.subplots_adjust(bottom=0.175)
	# #plt.show()

	# print("")

	# # test SystemOfEquations...
	# print("Testing SystemOfEquations...")
	# sys.modules["SystemOfEquations"] = bar
	# spec.loader.exec_module(bar)
	# fig = plt.figure(figsize=(7,7))
	# fig.suptitle(r"Finding Solution System of Equations")
	# ax = fig.add_gridspec(5, 2)
	# ax1 = fig.add_subplot(ax[0, 0])
	# ax1.get_xaxis().set_visible(False)
	# ax2 = fig.add_subplot(ax[1, 0])
	# ax2.get_xaxis().set_visible(False)
	# ax3 = fig.add_subplot(ax[2, 0])
	# ax3.get_xaxis().set_visible(False)
	# ax4 = fig.add_subplot(ax[3, 0])
	# ax4.get_xaxis().set_visible(False)
	# ax5 = fig.add_subplot(ax[4, 0])
	# ax5.get_xaxis().set_visible(True)
	# ax6 = fig.add_subplot(ax[:, 1])
	# ax6r = ax6.twinx()
	# ax6.get_yaxis().set_visible(False)
	# line_labels = []
	# A = np.matrix([[4, 1, 1, 0, 1], [1, 3, 1, 1, 0], [1, 1, 5, -1, -1], [0, 1, -1, 4, 0], [1, 0, -1, 0, 4]])
	# x0 = np.array([1, 1, 1, 1, 1])
	# b = np.array([6, 6, 6, 6, 6])
	# # A = [
	# # 	[1, -1, 2, -1],
	# # 	[2, -2, 3, -3],
	# # 	[1, 1, 1, 0],
	# # 	[1, -1, 4, 3]
	# # ]
	# # x0 = [-7, 3, 2, 2]
	# # b = [-8, -20, -2, 4]
	# tol = -10
	# obj = bar.SystemOfEquations(A, b, tol)
	# # gaussian_elimination
	# df_gauss = obj.gaussian_elimination()
	# print(f"Testing EigenValues().gaussian_elimination()...{df_gauss}")
	# conj_ispos = bar.positive_definite(A)
	# if conj_ispos:
	# 	# conjugate_gradient
	# 	df_conj = obj.conjugate_gradient(x0, C=np.diag(np.diag(A)))
	# 	print(f"Testing EigenValues().conjugate_gradient()...{df_conj['Approximations'].values[-1]}")
	# df_steep = obj.steepest_descent(x0)
	# print(f"Testing EigenValues().steepest_descent()...{df_steep['Approximations'].values[-1]}")
	# if conj_ispos:
	# 	dataframes = [df_conj, df_steep]
	# 	df_labels = ["Conjugate Gradient", "Steepest Descent"]
	# else:
	# 	dataframes = [df_steep]
	# 	df_labels = ["Steepest Descent"]
	# k = 0
	# for df in dataframes:
	# 	ax1.semilogx(df["Iterations"].values, [df["Approximations"].values[i][0] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax2.semilogx(df["Iterations"].values, [df["Approximations"].values[i][1] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax3.semilogx(df["Iterations"].values, [df["Approximations"].values[i][2] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax4.semilogx(df["Iterations"].values, [df["Approximations"].values[i][3] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# k = 0
	# for df in dataframes:
	# 	ax5.semilogx(df["Iterations"].values, [df["Approximations"].values[i][4] for i in df["Iterations"].values], label=f"{df_labels[k]}")
	# 	k += 1
	# if conj_ispos:
	# 	ax6r.plot(df_conj["Iterations"].values, df_conj["Errors"].values, label=f"{df_labels[1]} (k={df_conj['Iterations'].values[-1]}): E={df_conj['Errors'].values[-1]:1.4f}")
	# 	line_labels.append(f"{df_labels[1]} (k={df_conj['Iterations'].values[-1]}): Error={np.sum(df_conj['Errors'].values):1.4f}")
	# ax6r.plot(df_steep["Iterations"].values, df_steep["Errors"].values, label=f"{df_labels[0]} (k={df_steep['Iterations'].values[-1]}): E={df_steep['Errors'].values[-1]:1.4f}")
	# line_labels.append(f"{df_labels[0]} (k={df_steep['Iterations'].values[-1]}): Error={np.sum(df_steep['Errors'].values):1.4f}")
	# ax1.set_xlabel("Iterations")
	# ax1.set_ylabel(r"$x_{0}$")
	# #ax1.legend()
	# ax2.set_xlabel("Iterations")
	# ax2.set_ylabel(r"$x_{1}$")
	# #ax2.legend()
	# ax3.set_xlabel("Iterations")
	# ax3.set_ylabel(r"$x_{2}$")
	# #ax3.legend()
	# ax4.set_xlabel("Iterations")
	# ax4.set_ylabel(r"$x_{3}$")
	# #ax4.legend()
	# ax5.set_xlabel("Iterations")
	# ax5.set_ylabel(r"$x_{4}$")
	# #ax5.legend()
	# ax6r.set_title("Comparing Errors of Methods")
	# ax6.set_xlabel("Iterations")
	# ax6r.set_ylabel("Absolute Errors")
	# #ax6r.legend()
	# fig.legend([ax1, ax2, ax3, ax4, ax5, ax6], # The line objects
	# 	labels=line_labels, # The labels for each line
	# 	loc="lower center", # Position of legend
	# 	ncol=3,
	# 	fontsize="x-small",
	# 	mode="expand",
	# 	title="Legend", # Title for the legend
	# 	borderaxespad=0.1 # Small spacing around legend box
	# )
	# # Adjust the scaling factor to fit your legend text completely outside the plot
	# # (smaller value results in more space being made for the legend)
	# plt.subplots_adjust(bottom=0.175)
	# #plt.show()

	# print("")

	# #test ivp
	# print("Testing ivp...")
	# sys.modules["ivp"] = bar
	# spec.loader.exec_module(bar)
	# fig = plt.figure(figsize=(7,7))
	# fig.suptitle("'IVP()' Methods")
	# ax = fig.add_gridspec(5, 2)
	# ax1 = fig.add_subplot(ax[0, 0])
	# ax2 = fig.add_subplot(ax[0, 1])
	# ax3 = fig.add_subplot(ax[1, 0])
	# ax4 = fig.add_subplot(ax[1, 1])
	# ax5 = fig.add_subplot(ax[2, 0])
	# ax6 = fig.add_subplot(ax[2, 1])
	# ax7 = fig.add_subplot(ax[3, 0])
	# ax8 = fig.add_subplot(ax[3, 1])
	# ax9 = fig.add_subplot(ax[4, 0])
	# ax10 = fig.add_subplot(ax[4, 1])
	# line_labels = []
	# n = 5 	# grain growth exponent
	# H_star = 10**5 	# activation enthalpy [J/mol]
	# k0 = 10**10 	# growth rate constant [micro-m-n/s]
	# R = 8.314462175 	# universal gas constant [J/K-mol]
	# T = 1000 	# absolute temperature [K]
	# d0 = 10 	# initial grain size [micro-m]
	# t = 10*60 	# total experiment time [s]
	# d_dot = lambda t, d: k0/(n*d**(n - 1))*math.exp(-H_star/R/T)
	# H = (10, 5, 1)
	# #ltx_expression = r"\frac{k}{nd^{n-1}}\exp(-\frac{H_star}{RT})"
	# #ltx_dict = {
	# #	"n": n,
	# #	"H_star": H_star,
	# #	"k0": k0,
	# #	"R": R,
	# #	"T": T,
	# #	"d0": d0,
	# #	"t": t
	# #}
	# def d_dot_analytical(t, d0, h):
	# 	domain, Y, increment = np.arange(h, t+h, h), [d0], [0]
	# 	d = lambda t, d0: (d0**n + k0*sp.exp(-H_star/R/T)*t)**(1/n)
	# 	for ti in domain:
	# 		Y.append(d(ti, d0))
	# 		increment.append(d(ti, d0) - d(ti - h, d0))
	# 	return pd.DataFrame(data={"Iterations": range(len(domain)+1), "Domain": np.arange(0, t+h, h), "Range": Y, "Increments": increment})
	# # forward_euler
	# print("Testing forward_euler...")
	# k = 1
	# for h in H:
	# 	obj = bar.IVP(d_dot, h, t, d0, steps=t/h)
	# 	df = obj.forward_euler()
	# 	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# 	ax1.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# 	ax2.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# 	line_labels.append(r"$\Delta t$" + f"={h:4.2f} s")
	# 	k += 1
	# df = d_dot_analytical(t, d0, h)
	# ax1.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# ax2.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# #plt.show()
	# # improved_euler
	# print("Testing improved_euler...")
	# k = 1
	# for h in H:
	# 	obj = bar.IVP(d_dot, h, t, d0, steps=t/h)
	# 	df = obj.modified_euler()
	# 	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# 	ax3.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# 	ax4.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# 	k += 1
	# df = d_dot_analytical(t, d0, h)
	# ax3.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# ax4.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# #plt.show()
	# # backward_euler
	# print("Testing backward_euler...")
	# k = 1
	# for h in H:
	# 	obj = bar.IVP(d_dot, h, t, d0, steps=t/h)
	# 	df = obj.backward_euler()
	# 	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# 	ax5.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# 	ax6.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# 	k += 1
	# df = d_dot_analytical(t, d0, h)
	# ax5.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# ax6.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# #plt.show()
	# # runge_kutta
	# print("Testing runge_kutta...")
	# k = 1
	# for h in H:
	# 	obj = bar.IVP(d_dot, h, t, d0, steps=t/h)
	# 	df = obj.runge_kutta()
	# 	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# 	ax7.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# 	ax8.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# 	k += 1
	# df = d_dot_analytical(t, d0, h)
	# ax7.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# ax8.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# #plt.show()
	# # trapezoidal
	# print("Testing trapezoidal...")
	# k = 1
	# for h in H:
	# 	obj = bar.IVP(d_dot, h, t, d0, steps=t/h)
	# 	df = obj.crank_nicholson()
	# 	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# 	ax9.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# 	ax10.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# 	k += 1
	# df = d_dot_analytical(t, d0, h)
	# ax9.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# ax10.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# line_labels.append("Analytical")
	# # ax1.set_xlabel("Time [s]")
	# ax1.set_ylabel("Forward Euler")
	# # ax1.legend()
	# # ax2.set_xlabel("Time [s]")
	# # ax2.set_ylabel(r"$\Delta\mu$")
	# # ax2.legend()
	# # ax3.set_xlabel("Time [s]")
	# ax3.set_ylabel("Improved Euler")
	# # ax3.legend()
	# # ax4.set_xlabel("Time [s]")
	# # ax4.set_ylabel(r"$\Delta\mu$")
	# # ax4.legend()
	# # ax5.set_xlabel("Time [s]")
	# ax5.set_ylabel("Backward Euler")
	# # ax5.legend()
	# # ax6.set_xlabel("Time [s]")
	# # ax6.set_ylabel(r"$\Delta\mu$")
	# # ax6.legend()
	# # ax7.set_xlabel("Time [s]")
	# ax7.set_ylabel("Runge-Kutta")
	# # ax7.legend()
	# # ax8.set_xlabel("Time [s]")
	# # ax8.set_ylabel(r"$\Delta\mu$")
	# # ax8.legend()
	# # ax9.set_xlabel("Time [s]")
	# ax9.set_ylabel("Trapezoidal")
	# # ax9.legend()
	# # ax10.set_xlabel("Time [s]")
	# # ax10.set_ylabel(r"$\Delta\mu$")
	# # ax10.legend()
	# fig.legend([ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10], # The line objects
	# 	labels=line_labels, # The labels for each line
	# 	loc="lower center", # Position of legend
	# 	ncol=4,
	# 	fontsize="small",
	# 	mode="expand",
	# 	title="Legend", # Title for the legend
	# 	borderaxespad=0.1 # Small spacing around legend box
	# )
	# # Adjust the scaling factor to fit your legend text completely outside the plot
	# # (smaller value results in more space being made for the legend)
	# plt.subplots_adjust(bottom=0.175)
	# #plt.show()

	# print("")

	# #test bvp
	# print("Testing bvp...")
	# sys.modules["bvp"] = bar
	# spec.loader.exec_module(bar)
	# fig = plt.figure(figsize=(7,7))
	# fig.suptitle(r"Comparing Boundary Value Problem Methods")
	# ax = fig.add_gridspec(3, 3)
	# ax1 = fig.add_subplot(ax[0, 0])
	# ax2 = fig.add_subplot(ax[1, 0])
	# ax3 = fig.add_subplot(ax[1, 1])
	# ax4 = fig.add_subplot(ax[2, 0])
	# ax5 = fig.add_subplot(ax[2, 1])
	# ax6 = fig.add_subplot(ax[2, 2])
	# a, b = 1, 2
	# alpha, beta = 0, 2
	# p = lambda x: -(2/x)
	# q = lambda x: 2/(x**2)
	# r = lambda x: -3*(x**2)
	# # alpha, beta = 1, 2
	# # p = lambda x: -(2/x)
	# # q = lambda x: 2/(x**2)
	# # r = lambda x: np.sin(np.log(x))/(x**2)
	# ypp = lambda y, yp, x: p(x)*yp + q(x)*y + r(x)
	# F = [p, q, r, ypp]
	# H = (0.2, 0.1, 0.05)
	# def y_analytical(a, b, alpha, beta, h):
	# 	N = int((b - a)/h)+1
	# 	domain, Y, increment = np.linspace(a, b, N+2), [], []
	# 	y = lambda x: -52/(21*x**2) - (x**4)/6 + 37*x/14
	# 	# c2 = (8 - 12*np.sin(np.log(2)) - 4*np.cos(np.log(2)))/70
	# 	# c1 = 11/10 - c2
	# 	# y = lambda x: c1*x + c2/(x**2) - 3/10*np.sin(np.log(x)) - 1/10*np.cos(np.log(x))
	# 	for x in domain:
	# 		Y.append(y(x))
	# 		increment.append(y(x) - y(x - h))
	# 	# Y.append(beta)
	# 	# increment.append(beta - y(b))
	# 	return pd.DataFrame(data={"Iterations": range(len(domain)), "Domain": np.linspace(a, b, N+2), "Range": Y, "Increments": increment})
	# k = 1
	# for h in H:
	# 	df = y_analytical(a, b, alpha, beta, h)
	# 	print(f"{k}, h = {h}: Max = {np.max(df['Range'].values)} in {df['Iterations'].values[-1]} steps.")
	# 	ax1.plot(df["Domain"].values, df["Range"].values, label=f"{h}")
	# 	k += 1
	# #plt.show()

	# print("Testing linear_shooting_method...")
	# ax3r = ax3.twinx()
	# ax3.get_yaxis().set_visible(False)
	# k = 1
	# # k, H = 1, [0.1]
	# for h in H:
	# 	N = int((b - a)/h)+1
	# 	domain = np.linspace(a, b, N+2)
	# 	df = bar.BVP(F, a, b, alpha, beta, h, steps=N).linear_shooting_method()
	# 	print(f"{k}, h = {h}: Max = {np.max(df['Range'].values)} in {df['Iterations'].values[-1]} steps.")
	# 	ax2.plot(df["Domain"].values, df["Range"].values, label=f"{h}")
	# 	df_analytical = y_analytical(a, b, alpha, beta, h)
	# 	error = np.abs((df["Range"].values - df_analytical["Range"].values)/df_analytical["Range"].values*100)
	# 	ax3.plot(domain, error, label=f"{h}")
	# 	k += 1
	# #plt.show()

	# print("Testing finite_difference_method...")
	# k = 1
	# def y_analytical(a, b, alpha, beta, h):
	# 	N = int((b - a)/h)+2
	# 	domain, Y, increment = np.linspace(a, b, N+2), [], []
	# 	y = lambda x: -52/(21*x**2) - (x**4)/6 + 37*x/14
	# 	# c2 = (8 - 12*np.sin(np.log(2)) - 4*np.cos(np.log(2)))/70
	# 	# c1 = 11/10 - c2
	# 	# y = lambda x: c1*x + c2/(x**2) - 3/10*np.sin(np.log(x)) - 1/10*np.cos(np.log(x))
	# 	for x in domain:
	# 		Y.append(y(x))
	# 		increment.append(y(x) - y(x - h))
	# 	# Y.append(beta)
	# 	# increment.append(beta - y(b))
	# 	return pd.DataFrame(data={"Iterations": range(len(domain)), "Domain": np.linspace(a, b, N+2), "Range": Y, "Increments": increment})
	# # k, H = 1, [0.1]
	# for h in H:
	# 	N = int((b - a)/h)+1
	# 	domain = np.linspace(a, b, N+3)
	# 	df, df_iter = bar.BVP(F, a, b, alpha, beta, h, steps=N).finite_difference_method()
	# 	print(f"{k}, h = {h}: Max = {np.max(df['Range'].values)} in {df['Iterations'].values[-1]} steps and {df_iter['Iterations'].values[-1]} iterations for total error = {np.sum(df_iter['Errors'].values[-1])}.")
	# 	ax4.plot(df["Domain"].values, df["Range"].values, label=f"{h}")
	# 	df_analytical = y_analytical(a, b, alpha, beta, h)
	# 	error = np.abs((df["Range"].values - df_analytical["Range"].values)/df_analytical["Range"].values*100)
	# 	ax5.plot(domain, error, label=f"{h}")
	# 	ax6.semilogx(df_iter["Iterations"].values, df_iter["Errors"].values, label=f"{h}")
	# 	k += 1
	# ax4.plot(df_analytical["Domain"].values, df_analytical["Range"].values, label=f"Analytical")
	# ax1.set_title("Analytical Form")
	# ax1.set_xlabel("Domain (x)")
	# ax1.set_ylabel("Range (y)")
	# ax1.legend()
	# ax2.plot(df_analytical["Domain"].values, df_analytical["Range"].values, label=f"Analytical")
	# ax2.set_title("Linear Shooting Method")
	# ax2.set_xlabel("Domain (x)")
	# ax2.set_ylabel("Range (y)")
	# ax2.legend()
	# ax3r.set_title("Comparing Errors of Step Size")
	# ax3.set_xlabel("Domain (x)")
	# ax3r.set_ylabel("Percent Error [%]")
	# ax3.legend()
	# ax4.set_title("Finite Difference Method")
	# ax4.set_xlabel("Domain (x)")
	# ax4.set_ylabel("Range (y)")
	# ax4.legend()
	# ax5.set_title("Comparing Errors of Step Size")
	# ax5.set_xlabel("Domain (x)")
	# ax5.set_ylabel("Percent Error [%]")
	# ax5.legend()
	# ax6.set_title("Comparing Iterative Errors of Step Size")
	# ax6.set_xlabel("Iterations")
	# ax6.set_ylabel("Method Error")
	# ax6.legend()
	# #plt.show()



	# A = DATA

	# #test diagonality
	# print("Testing diagonality...")
	# test(lambda d: [nm.diagonality(d)], DATA, "nm.diagonality(DATA) (Python implementation)")
	# # from extension import fast_diagonality
	# # test(lambda d: [fast_diagonality(d)], DATA, "fast_diagonality(DATA) (CPython C++ extension)")
	# sys.modules["diagonality"] = bar
	# spec.loader.exec_module(bar)
	# test(lambda d: [bar.diagonality(d)], DATA, "From path (Python implementation)")
	
	# # #print("")

	# # ##test eigen_values
	# # #print("Testing eigen_values...")
	# # #sys.modules["eigen_values"] = foo
	# # #spec.loader.exec_module(foo)
	# # ##test(lambda d: [foo.eigen_values(d)], DATA, "nm.eigen_values(DATA) (Python implementation)")
	# # #from extension import fast_eigen_values
	# # #test(lambda d: [fast_eigen_values(d)], DATA, "fast_eigen_values(DATA) (CPython C++ extension)")

	# # #print("")

	# # ##test spectral_radius
	# # #print("Testing spectral_radius...")
	# # #sys.modules["spectral_radius"] = foo
	# # #spec.loader.exec_module(foo)
	# # ##test(lambda d: [foo.spectral_radius(d)], DATA, "nm.spectral_radius(DATA) (Python implementation)")
	# # #sys.modules["spectral_radius"] = bar
	# # #spec.loader.exec_module(bar)
	# # ##test(lambda d: [bar.spectral_radius(d)], DATA, "cpp.spectral_radius(DATA) (CPython C++ extension)")

	# print("")

	# #test l_infinity
	# print("Testing l_infinity...")
	# #A = np.array([-0.38439942, 0.09028457, -0.67183719, 0.63989375])
	# #print("numpy", np.linalg.norm(A, "inf"))
	# test(lambda d: [nm.Norm(d).l_infinity()], DATA, "nm.Norm(DATA).l_infinity() (Python implementation)")
	# # from extension import fast_l_infinity
	# # test(lambda d: [fast_l_infinity(d)], DATA, "fast_l_infinity(DATA) (CPython C++ extension)")
	# sys.modules["norms"] = bar
	# spec.loader.exec_module(bar)
	# test(lambda d: [bar.Norm(d).l_infinity()], DATA, "From path (Python implementation)")

	# # #print("")

	# # ##test l_two
	# # #print("Testing l_two...")
	# # #sys.modules["norms.l_two"] = foo
	# # #spec.loader.exec_module(foo)
	# # #print("nm.Norm().l_two()", foo.norms(A).l_two())
	# # ##print("nm.Norm().l_infinity()", nm.Norm(A).l_infinity())
	# # ##from extension import fast_l_infinity
	# # ##print("C++", fast_l_infinity(A, B))
	# # #sys.modules["norms"] = bar
	# # #spec.loader.exec_module(bar)
	# # #print("From path", bar.Norm(A).l_two())
	# # #print("numpy", np.linalg.norm(A, 2))

	# # #print("")

	# # ##test determinant
	# # #print("Testing determinant...")
	# # ##sys.modules["diagonality"] = foo
	# # ##spec.loader.exec_module(foo)
	# # #test(lambda d: [foo.determinant(d)], DATA, "nm.determinant(DATA) (Python implementation)")
	# # #from extension import fast_determinant
	# # #test(lambda d: [fast_determinant(d)], DATA, "fast_determinant(DATA) (CPython C++ extension)")

	# # #print("")

	# # ##test condition_number
	# # #print("Testing condition_number...")
	# # #sys.modules["condition_number"] = foo
	# # #spec.loader.exec_module(foo)
	# # #print("nm.condition_number()", foo.condition_number(A, "l_infinity"))
	# # ##from extension import condition_number
	# # ##print("C++", condition_number(A))
	# # #sys.modules["condition_number"] = bar
	# # #spec.loader.exec_module(bar)
	# # #print("From path", bar.condition_number(A, "l_infinity"))

	# print("")

	# #test symmetry
	# print("Testing symmetry...")
	# test(lambda d: [nm.symmetry(d)], DATA, "nm.symmetry(DATA) (Python implementation)")
	# # from extension import fast_symmetry
	# # test(lambda d: [fast_symmetry(d)], DATA, "fast_symmetry(DATA) (CPython C++ extension)")
	# sys.modules["symmetry"] = bar
	# spec.loader.exec_module(bar)
	# test(lambda d: [bar.symmetry(d)], DATA, "From path (Python implementation)")

	# print("")

	# #test tridiagonality
	# print("Testing tridiagonality...")
	# test(lambda d: [nm.tridiagonality(d)], DATA, "nm.tridiagonality(DATA) (Python implementation)")
	# # from extension import fast_tridiagonality
	# # test(lambda d: [fast_tridiagonality(d)], DATA, "fast_tridiagonality(DATA) (CPython C++ extension)")
	# sys.modules["tridiagonality"] = bar
	# spec.loader.exec_module(bar)
	# test(lambda d: [bar.tridiagonality(d)], DATA, "From path (Python implementation)")

	# # #print("")

	# # ##test parse_latex
	# # #print("Testing parse_latex...")
	# # #ltx_variable = r"x"
	# # #cT = 2000 # K
	# # #cP = 10e3 # MPa
	# # #crho_0_300 = 3345 # kg/m3
	# # #calpha_th = 3.5e-5 # 1/K
	# # #cB_T0_300 = 1.29e5 # MPa
	# # #cB_prime_T0 = 4.47
	# # #cpartial_BT0_T = -1 # MPa/K
	# # #r0 = crho_0_300 # kg/m3
	# # #fB_T0 = cB_T0_300 + cpartial_BT0_T*(cT - 300)
	# # #frho_0 = crho_0_300*(1 - calpha_th*(cT - 300))
	# # #ltx_dict = {
	# # #	"cT": cT,
	# # #	r"c_{P}": cP,
	# # #	"crho_0_300": crho_0_300,
	# # #	r"calpha_th": calpha_th,
	# # #	"cB_T0_300": cB_T0_300,
	# # #	r"cB_prime_T0": cB_prime_T0,
	# # #	"cpartial_BT0_T": cpartial_BT0_T,
	# # #	r"r0": r0,
	# # #	"fB_T0": fB_T0,
	# # #	r"frho_0": frho_0
	# # #}
	# # ##lambda_expression = lambda x: f"{cP} - (3*{fB_T0}/2) * (({x}/{frho_0})^(7/3) - ({x}/{frho_0})^(5/3)* (1 + 3/4*({cB_prime_T0} - 4)*(({x}/{frho_0})^(2/3) - 1)))"
	# # ##ltx_expression = lambda_expression#.encode("utf-8")#.decode("utf-8") # r"{}".format
	# # #ltx_expression = r"c_{P} - (\frac{3}{2}*fB_T0) * ((\frac{x}{frho_0})^{\frac{7}{3}} - (\frac{x}{frho_0})^{\frac{5}{3}}*(1 + \frac{3}{4}*(cB_prime_T0 - 4)*((\frac{x}{frho_0})^{\frac{2}{3}} - 1)))"
	# # ##lambda_expression = lambda x: cP - (3*fB_T0/2) * ((x/frho_0)**(7/3) - (x/frho_0)**(5/3)* (1 + 3/4*(cB_prime_T0 - 4)*((x/frho_0)**(2/3) - 1)))
	# # ##print(lambda_expression(pi))
	# # #from extension import fast_parse_latex
	# # #parsed_string = fast_parse_latex(ltx_expression, ltx_dict)
	# # #print("C++ (parse)", parsed_string)

	# # #print("")

	# # ##test eval_latex
	# # #print("Testing eval_latex...")
	# # #from extension import fast_eval_latex
	# # #print(f"C++ parse({ltx_variable} = {pi})", fast_eval_latex(parsed_string, {"x": pi}))

	# # #print("")

	# # ##test derive_latex
	# # #print("Testing derive_latex...")
	# # #from extension import fast_derive_latex
	# # #derived_string = fast_derive_latex(parsed_string, ltx_variable, degree=2)
	# # #print("C++ (derive)", derived_string)
	# # #print(f"C++ derive({ltx_variable} = {pi})", fast_eval_latex(derived_string, {"x": pi}))

	# # #print("")

	# # ##test SingleVariableIteration
	# # #print("Testing SingleVariableIteration...")
	# # #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7,7))
	# # #fig.suptitle("'SingleVariableIteration()' Methods")
	# # #ax2r = ax2.twinx()
	# # #ax2.get_yaxis().set_visible(False)
	# # #line_labels = []
	# # #cT = 2000 # K
	# # #cP = 10e3 # MPa
	# # #crho_0_300 = 3345 # kg/m3
	# # #calpha_th = 3.5e-5 # 1/K
	# # #cB_T0_300 = 1.29e5 # MPa
	# # #cB_prime_T0 = 4.47
	# # #cpartial_BT0_T = -1 # MPa/K
	# # #r0 = crho_0_300 # kg/m3
	# # #fB_T0 = cB_T0_300 + cpartial_BT0_T*(cT - 300)
	# # #frho_0 = crho_0_300*(1 - calpha_th*(cT - 300))
	# # #ltx_dict = {
	# # #	"cT": cT,
	# # #	r"cP": cP,
	# # #	"crho_0_300": crho_0_300,
	# # #	r"calpha_th": calpha_th,
	# # #	"cB_T0_300": cB_T0_300,
	# # #	r"cB_prime_T0": cB_prime_T0,
	# # #	"cpartial_BT0_T": cpartial_BT0_T,
	# # #	r"r0": r0,
	# # #	"fB_T0": fB_T0,
	# # #	r"frho_0": frho_0
	# # #}
	# # #ltx_variable = "x"
	# # #ltx_expression = r"cP - (3*fB_T0/2) * ((x/frho_0)^(7/3) - (x/frho_0)^(5/3)) * (1 + 3/4*(cB_prime_T0 - 4)*((x/frho_0)^(2/3) - 1))"
	# # #from extension import fast_parse_latex
	# # #parsed_string = fast_parse_latex(ltx_expression, ltx_dict)
	# # #print("C++ (parse)", parsed_string)
	# # ##parsed_string = lambda x: cP - (3*fB_T0/2) * ((x/frho_0)**(7/3) - (x/frho_0)**(5/3)) * (1 + 3/4*(cB_prime_T0 - 4)*((x/frho_0)**(2/3) - 1))
	# # #sys.modules["SingleVariableIteration"] = bar
	# # #spec.loader.exec_module(bar)
	# # #obj = bar.SingleVariableIteration(
	# # #	parsed_string, 1e3, 6e3, variable=ltx_variable, iter_guess=True)
	# # #meth_bisect = obj.bisection()
	# # #bisect_approx, = ax1.semilogx(
	# # #	meth_bisect["Iterations"].values,
	# # #	meth_bisect["Approximations"].values,
	# # #	label=f"Bisection (k={meth_bisect['Iterations'].values[-1]}): {meth_bisect['Approximations'].values[-1]:4.2f}"
	# # #)
	# # #bisect_error, = ax2r.plot(
	# # #	meth_bisect["Iterations"].values,
	# # #	meth_bisect["Errors"].values,
	# # #	label=f"Bisection (k={meth_bisect['Iterations'].values[-1]}): {meth_bisect['Errors'].values[-1]:4.2f}"
	# # #)
	# # #line_labels.append(f"Bisection (k={meth_bisect['Iterations'].values[-1]}): {meth_bisect['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_bisect['Errors'].values):4.2f})")
	# # #meth_false_position = obj.false_position(1.5e3, 5.5e3)
	# # #falsepos_approx, = ax1.semilogx(
	# # #	meth_false_position["Iterations"].values,
	# # #	meth_false_position["Approximations"].values,
	# # #	label=f"False Position (k={meth_false_position['Iterations'].values[-1]}): {meth_false_position['Approximations'].values[-1]:4.2f}"
	# # #)
	# # #falsepos_error, = ax2r.plot(
	# # #	meth_false_position["Iterations"].values,
	# # #	meth_false_position["Errors"].values,
	# # #	label=f"False Position (k={meth_false_position['Iterations'].values[-1]}): {meth_false_position['Errors'].values[-1]:4.2f}"
	# # #)
	# # #line_labels.append(f"False Position (k={meth_false_position['Iterations'].values[-1]}): {meth_false_position['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_false_position['Errors'].values):4.2f})")
	# # ##meth_fixed_point = obj.fixed_point(3.3e3)
	# # ##plt.plot(
	# # ##    meth_fixed_point["Iterations"].values,
	# # ##    meth_fixed_point["Approximations"].values,
	# # ##    label=f"Fixed-Point (k={meth_fixed_point['Iterations'].values[-1]}): {meth_fixed_point['Approximations'].values[-1]}"
	# # ##)
	# # #meth_newton_raphson = obj.newton_raphson(crho_0_300)
	# # #nr_approx, = ax1.semilogx(
	# # #	meth_newton_raphson["Iterations"].values,
	# # #	meth_newton_raphson["Approximations"].values,
	# # #	label=f"Newton-Raphson (k={meth_newton_raphson['Iterations'].values[-1]}): {meth_newton_raphson['Approximations'].values[-1]:4.2f}",
	# # #)
	# # #nr_error, = ax2r.plot(
	# # #	meth_newton_raphson["Iterations"].values,
	# # #	meth_newton_raphson["Errors"].values,
	# # #	label=f"Newton-Raphson (k={meth_newton_raphson['Iterations'].values[-1]}): {meth_newton_raphson['Errors'].values[-1]:4.2f}"
	# # #)
	# # #line_labels.append(f"Newton-Raphson (k={meth_newton_raphson['Iterations'].values[-1]}): {meth_newton_raphson['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_newton_raphson['Errors'].values):4.2f})")
	# # #meth_secant_method = obj.secant_method(1.5e3, 5.5e3)
	# # #secant_approx, = ax1.semilogx(
	# # #	meth_secant_method["Iterations"].values,
	# # #	meth_secant_method["Approximations"].values,    
	# # #	label=f"Secant (k={meth_secant_method['Iterations'].values[-1]}): {meth_secant_method['Approximations'].values[-1]:4.2f}",
	# # #)
	# # #secant_error, = ax2r.plot(
	# # #	meth_secant_method["Iterations"].values,
	# # #	meth_secant_method["Errors"].values,    
	# # #	label=f"Secant (k={meth_secant_method['Iterations'].values[-1]}): {meth_secant_method['Errors'].values[-1]:4.2f}"
	# # #)
	# # #line_labels.append(f"Secant (k={meth_secant_method['Iterations'].values[-1]}): {meth_secant_method['Approximations'].values[-1]:4.2f} (Error={np.sum(meth_secant_method['Errors'].values):4.2f})")
	# # #ax1.set_title("Convergence of 'p'")
	# # #ax1.set_xlabel("Iterations")
	# # #ax1.set_ylabel("Value 'p'")
	# # ##ax1.legend(
	# # ##	handles=[bisect_approx, falsepos_approx, nr_approx, secant_approx],
	# # ##	bbox_to_anchor=(0, 1),
	# # ##	bbox_transform=fig.transFigure
	# # ##)
	# # #ax2r.set_title("Comparing Errors of Methods")
	# # #ax2.set_xlabel("Iterations")
	# # #ax2r.set_ylabel("Absolute Errors")
	# # #fig.legend([ax1, ax2], # The line objects
	# # #	labels=line_labels, # The labels for each line
	# # #	loc="lower center", # Position of legend
	# # #	ncol=2,
	# # #	fontsize="small",
	# # #	mode="expand",
	# # #	title="Legend", # Title for the legend
	# # #	borderaxespad=0.1 # Small spacing around legend box
	# # #)
	# # ## Adjust the scaling factor to fit your legend text completely outside the plot
	# # ## (smaller value results in more space being made for the legend)
	# # #plt.subplots_adjust(bottom=0.175)
	# # ##plt.show()

	# print("")

	# # test MultiVariableIteration
	# print("Testing MultiVariableIteration...")
	# ## 		supplied parameters
	# # 4x4 matrix
	# A = DATA
	# # 4x1 vertical vector
	# b = [(random() - 0.5) * 3 for _ in range(rows)]
	# # initial guess, x vector
	# x0 = np.zeros(rows)
	# omega = 1.2
	# # test(lambda d: [nm.MultiVariableIteration(d, x0, b).jacobi()], DATA, "nm.MultiVariableIteration(DATA).jacobi() (Python implementation)")
	# # test(lambda d: [nm.MultiVariableIteration(d, x0, b).gauss_seidel()], DATA, "nm.MultiVariableIteration(DATA).gauss_seidel() (Python implementation)")
	# # test(lambda d: [nm.MultiVariableIteration(d, x0, b).successive_relaxation(omega)], DATA, "nm.MultiVariableIteration(DATA).successive_relaxation() (Python implementation)")
	# sys.modules["MultiVariableIteration"] = bar
	# spec.loader.exec_module(bar)
	# test(lambda d: [bar.MultiVariableIteration(d, x0, b).jacobi()], DATA, "nm.MultiVariableIteration(DATA).jacobi() (CPython C++ extension)")
	# test(lambda d: [bar.MultiVariableIteration(d, x0, b).gauss_seidel()], DATA, "nm.MultiVariableIteration(DATA).gauss_seidel() (CPython C++ extension)")
	# test(lambda d: [bar.MultiVariableIteration(d, x0, b).successive_relaxation(omega)], DATA, "nm.MultiVariableIteration(DATA).successive_relaxation() (CPython C++ extension)")

	# # #print("")

	# # test cubic_spline
	# print("Testing cubic_spline...")
	# sys.modules["cubic_spline"] = bar
	# spec.loader.exec_module(bar)
	# ## 		supplied parameters
	# X = [0.0, 0.3, 0.5]
	# a, b = 0.0, 0.5
	# method = "Clamped"
	# # ltx_variable = "x"
	# # ltx_expression = r"\sin(3x)"
	# ltx_expression = np.sin(3*np.array(X))
	# #ltx_expression = lambda x: math.sin(3*x)
	# #ltx_expression = [0, 0.7]
	# obj = bar.CubicSpline(X, ltx_expression)
	# if method == "Clamped":
	# 	Y, S = obj.clamped()
	# elif method == "Natural":
	# 	Y, S = obj.natural()
	# ### 		console outputs
	# print('Interpolant Spline 1, $S_{0}$ = ', S[0](sp.Symbol("x")))
	# print('Interpolant Spline 2, $S_{1}$ = ', S[1](sp.Symbol("x")))
	# #print('Clamped Cubic Spline, $s(x)$ = ','\n')
	# #print(spline,'\n')
	# ## 		output plots
	# plt.figure(figsize=(7,7))
	# plt.title(f"Cubic Spline ({method})")
	# plt.scatter(X,Y, color='r', label="Raw Data")
	# X1, Y1 = np.arange(a, X[1]+0.01, 0.01), []
	# for x in X1:
	# 	Y1.append(S[0](x))
	# plt.plot(X1,Y1, color='g', label=f"Interpolant 1")
	# X2, Y2 = np.arange(X[1], X[2]+0.01, 0.01), []
	# for x in X2:
	# 	Y2.append(S[1](x))
	# plt.plot(X2,Y2, color='b', label=f"Interpolant 2")
	# plt.xlabel("Real Domain [rad]")
	# plt.ylabel("Real Range [rad]")
	# plt.legend()
	# #plt.show()

	# # #print("")

	# # #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7,7))
	# # #fig.suptitle("Lagrangian and Hermetic Polynomials")
	# # #ax2r = ax2.twinx()
	# # #ax2.get_yaxis().set_visible(False)
	# # ## test lagrangian polynomials
	# # #print("Testing Lagrangian polynomials...")
	# # #sys.modules["lagrange"] = bar
	# # #spec.loader.exec_module(bar)
	# # ## sample time of study
	# # #D = [0, 5, 9, 12, 16, 23, 28] # days
	# # ## average mass on day in milligrams
	# # #samp_1 = [5, 14, 39, 34, 28, 26, 25] # mg
	# # #samp_2 = [5, 13, 15, 14, 12, 11, 10] # mg
	# # ##sym_x = sp.Symbol('x')
	# # ## first sample
	# # ## Lagrange polynomial and progressive error
	# # #lst, Px1, prop, Px1_err = bar.lagrange(D, samp_1)
	# # ## second sample
	# # ## Lagrange polynomial and progressive error
	# # #lst, Px2, prop, Px2_err = bar.lagrange(D, samp_2)
	# # ## substitute to time domain
	# # #dt = 1 # (days) time increment 
	# # ## time domain of study
	# # #time = np.arange(D[0], D[-1]+1, dt)
	# # #Y1 = []; Y2 = []        # initialize list
	# # ## buld curves from Lagrange polynomials
	# # #for t in time:
	# # #	Y1.append(Px1(t))
	# # #	Y2.append(Px2(t))
	# # ### 		console outputs
	# # ## first sample results
	# # #print('**'*8, 'Sample 1 Results', '**'*8, sep=' ')
	# # ##print('Polynomial of Sample 1:\n', Px1("x"),end='\n')
	# # #print('Progressive Errors of First Sample: ', Px1_err)
	# # #print('Maximum Value = ', int(np.amax(Y1)),' (mg)')
	# # #print('Minimum Value = ', int(np.amin(Y1)),' (mg)')
	# # ## second sample results
	# # #print('**'*8, 'Sample 2 Results', '**'*8, sep=' ')
	# # ##print('Polynomial of Sample 2:\n', sp.simplify(Px2(sym_x)),end='\n')
	# # #print('Progressive Errors of Second Sample: ', Px2_err)
	# # #print('Maximum Value = ', int(np.amax(Y2)),' (mg)')
	# # #print('Minimum Value = ', int(np.amin(Y2)),' (mg)')
	# # ### 		output plots
	# # #ax1.set_title("Lagrange")
	# # ## first data set and polynomial
	# # #ax1.plot(D,samp_1, color='r', label='Sample 1 (Raw)')
	# # #ax1.plot(time,Y1, color='g', label=f'Sample 1 (Y1) Error = {Px1_err:4.4f}')
	# # #ax1.set_xlabel('Days')
	# # #ax1.set_ylabel('Average Weight [mg]')
	# # ## second data set and polynomial
	# # #ax1.plot(D,samp_2, color='b', label='Sample 2 (Raw)')
	# # #ax1.plot(time,Y2, color='k', label=f'Sample 2 (Y2) Error = {Px2_err:4.4f}')
	# # #ax1.set_xlabel('Days')
	# # #ax1.set_ylabel('Average Weight [mg]')
	# # #ax1.legend()
	# # ##plt.show()

	# # #print("")

	# # ## test hermetic polynomials
	# # #print("Testing Hermetic polynomials...")
	# # #sys.modules["hermite"] = bar
	# # #spec.loader.exec_module(bar)
	# # ## sample time of study
	# # #D = [0, 5, 9, 12, 16, 23, 28] # days
	# # ## average mass on day in milligrams
	# # #samp_1 = [5, 14, 39, 34, 28, 26, 25] # mg
	# # #samp_2 = [5, 13, 15, 14, 12, 11, 10] # mg
	# # ## first sample
	# # ## Hermetic polynomial and progressive error
	# # #Px1, poly_str = bar.hermite(D, samp_1)
	# # ## substitute to time domain
	# # #dt = 1 # (days) time increment 
	# # ## time domain of study
	# # #time = np.arange(D[0], D[-1]+1, dt)
	# # #Y1 = []; Y2 = []        # initialize list
	# # ## buld curves from Hermitic polynomials
	# # #for t in time:
	# # #	Y1.append(Px1(t))
	# # #	Y2.append(Px2(t))
	# # ### 		console outputs
	# # ## first sample results
	# # #print('**'*8, 'Sample 1 Results', '**'*8, sep=' ')
	# # ##print('Polynomial of Sample 1:\n', Px1("x"),end='\n')
	# # ##print('Progressive Errors of First Sample:\n',Px1_err, end='\n')
	# # #print(poly_str)
	# # #print('Maximum Value = ', int(np.amax(Y1)),' (mg)')
	# # #print('Minimum Value = ', int(np.amin(Y1)),' (mg)')
	# # ## second sample results
	# # ## Hermetic polynomial and progressive error
	# # #Px2, poly_str = bar.hermite(D, samp_2)
	# # #Y1 = []; Y2 = []        # initialize list
	# # ## buld curves from Hermitic polynomials
	# # #for t in time:
	# # #	Y1.append(Px1(t))
	# # #	Y2.append(Px2(t))
	# # #print('**'*8, 'Sample 2 Results', '**'*8, sep=' ')
	# # ##print('Polynomial of Sample 2:\n', sp.simplify(Px2(sym_x)),end='\n')
	# # ##print('Progressive Errors of Second Sample:\n',Px2_err, end='\n')
	# # #print(poly_str)
	# # #print('Maximum Value = ', int(np.amax(Y2)),' (mg)')
	# # #print('Minimum Value = ', int(np.amin(Y2)),' (mg)')
	# # ### 		output plots
	# # #ax2r.set_title("Hermite")
	# # ## first data set and polynomial
	# # #ax2r.plot(D,samp_1, color='r', label='Sample 1 (Raw)')
	# # #ax2r.plot(time,Y1, color='g', label=f'Sample 1 (Y1)')
	# # ## second data set and polynomial
	# # #ax2r.plot(D,samp_2, color='b', label='Sample 2 (Raw)')
	# # #ax2r.plot(time,Y2, color='k', label=f'Sample 2 (Y2)')
	# # #ax2.set_xlabel('Days')
	# # #ax2r.set_ylabel('Average Weight [mg]')
	# # #ax2r.legend()
	# # ##plt.show()

	# # #print("")

	# test least_squares
	print("Testing least_squares...")
	sys.modules["least_squares"] = bar
	spec.loader.exec_module(bar)
	plt.figure(figsize=(7,7))
	plt.title("Raw Data versus Least Square Polynomial and Power Law")
	## 		supplied parameters
	# x_i 
	X_i = [0.01, 0.15, 0.31, 0.5, 0.6, 0.75]
	# y_i 
	Y_i = [1.0, 1.004, 1.031, 1.117, 1.223, 1.422]
	degree = 2
	obj = bar.LeastSquares(X_i, Y_i)
	polynomial, error = obj.linear(degree)
	plt.scatter(X_i,Y_i, color='r', label='Raw Data')
	# build arrays to plot
	dx = 0.01 			# distance between discrete elements
	# X = discretize domain
	# Y = empty list for range of domain, X
	X, Y = np.arange(X_i[0],\
		X_i[-1] + (X_i[-1] - X_i[-2]), dx), []
	for x in X: 		# for each element in domain
		# write to range, Y
		Y.append(polynomial(x))
	## 		output plots
	plt.plot(X,Y, color='g', label=f"Polynomial, n = {degree} (error = {error:1.4f})")
	power_a, power_b, power_expression = obj.power()
	# build arrays to plot
	dx = 0.01 			# distance between discrete elements
	# X = discretize domain
	# Y = empty list for range of domain, X
	X, Y = np.arange(X_i[0],\
		X_i[-1] + (X_i[-1] - X_i[-2]), dx), []
	for x in X: 		# for each element in domain
		# write to range, Y
		Y.append(power_expression(x))
	## 		output plots
	plt.plot(X,Y, color='b', label=f'Power: {power_a:1.4f}x**{power_b:1.4f}')
	plt.xlabel('Real Domain')
	plt.ylabel('Real Range')
	plt.legend()
	#plt.show()

	# # #print("")

	# # #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7,7))
	# # #fig.suptitle("Applying Newton Difference Methods")
	# # #ax2r = ax2.twinx()
	# # #ax2.get_yaxis().set_visible(False)
	# # ## test newton_difference
	# # #print("Testing newton_difference...")
	# # #sys.modules["newton_difference"] = bar
	# # #spec.loader.exec_module(bar)
	# # ### 		supplied parameters
	# # #X = [-1.2, -0.9, -0.6, -0.3, 0.0]
	# # #FX = [0.18232, -0.105083, -0.51036, -1.20397, -3.12145]
	# # #alpha = -1.0
	# # #ax1.set_title("Newton Difference")
	# # #ax1.scatter(X,FX, color='r', label='Raw Data')
	# # #polynomial, px = bar.newton_difference(X, FX, alpha)
	# # ## graph from discretized data
	# # #da = 0.1                                # increment 
	# # #A = np.arange(X[0], X[-1]+1, da)        # real domain
	# # #Y = []                                  # make empty list
	# # #for a in A:
	# # #	Y.append(polynomial(a)) # store to list, Y
	# # ### 		output plots
	# # #ax1.plot(A,Y, color='g', label=f"Forward: P(x={alpha}) = {px:1.4f}")
	# # #alpha = -0.2
	# # #polynomial, px = bar.newton_difference(X, FX, alpha, direction="backward")
	# # ## graph from discretized data
	# # #da = 0.1                                # increment 
	# # #A = np.arange(X[0], X[-1]+1, da)        # real domain
	# # #Y = []                                  # make empty list
	# # #for a in A:
	# # #	Y.append(polynomial(a)) # store to list, Y
	# # ### 		output plots
	# # #ax1.plot(A,Y, color='b', label=f"Backward: P(x={alpha}) = {px:1.4f}")
	# # #ax1.set_xlabel('Real Domain')
	# # #ax1.set_ylabel('Real Range')
	# # #ax1.legend()
	# # ##plt.show()

	# # #print("")

	# # ## test richard_extrapolation
	# # #print("Testing richard_extrapolation...")
	# # #sys.modules["richard_extrapolation"] = bar
	# # #spec.loader.exec_module(bar)
	# # ### 		supplied parameters
	# # #x0, h, order = 1, 0.2, 4
	# # #ltx_variable = "x"
	# # #ltx_expression = r"\sin(x)*(2)^{x}"
	# # ##ltx_expression = r"\cos(x)*((2)^{x}) + \sin(x)*((2)^{x})*\log(2)"
	# # #X = []
	# # #for i in range(order): X.append(x0+h/(2**(order-i)))
	# # #ltx_diff = sp.diff("(2**(x))*sin(x)", ltx_variable)
	# # #lambda_expression = sp.lambdify(ltx_variable, ltx_diff)
	# # ##print(ltx_diff)
	# # #raw = []
	# # #for x in X: raw.append(lambda_expression(x))
	# # ### 		output plots
	# # #ax2r.set_title("Richardson's Extrapolation of Derivative")
	# # #ax2r.scatter(X,raw, color='r', label='Raw Data')
	# # #polynomial, px = bar.richard_extrapolation(ltx_expression, x0, h, order, variable=ltx_variable)
	# # ## graph from discretized data
	# # #da = h/100                                # increment 
	# # #A = np.arange(X[0]-1, X[-1]+X[0], da)        # real domain
	# # #Y = []                                  # make empty list
	# # #for a in A:
	# # #	Y.append(polynomial(a)) # store to list, Y
	# # #ax2r.plot(A,Y, color='g', label=f"Forward: P(x={x0}) = {px:1.4f}")
	# # #polynomial, px = bar.richard_extrapolation(ltx_expression, X[-1], h, order, direction="backward", variable=ltx_variable)
	# # ## graph from discretized data
	# # #da = h/100                                # increment 
	# # #A = np.arange(X[0]-1, X[-1]+X[0], da)        # real domain
	# # #Y = []                                  # make empty list
	# # #for a in A:
	# # #	Y.append(polynomial(a)) # store to list, Y
	# # #ax2r.plot(A,Y, color='b', label=f"Backward: P(x={X[-1]}) = {px:1.4f}")
	# # #ax2.set_xlabel('Real Domain')
	# # #ax2r.set_ylabel('Real Range')
	# # #ax2r.legend()
	# # ##plt.show()

	# # #print("")

	# # ## test integrate
	# # #print("Testing integrate...")
	# # #sys.modules["integrate"] = bar
	# # #spec.loader.exec_module(bar)
	# # ### 		supplied parameters
	# # #h, a, b = 0.25, 1, 2
	# # #ltx_variable = "x"
	# # #ltx_expression = r"\cos(x)*(x)^{2}"
	# # #lambda_expression = lambda x: math.cos(x)*x**2
	# # #X = np.arange(a, b+h, h)
	# # #Y = np.cos(X)*X**2
	# # #obj = bar.Integrate(lambda_expression, a=a, b=b, h=h, scheme="open")
	# # #domain, rng, area = obj.simpson()
	# # #print(f"Simpson, A = {area}")
	# # #domain, rng, area = obj.trapezoidal()
	# # #print(f"Trapezoidal, A = {area}")

	# print("")

	# # test EigenValues...
	# print("Testing EigenValues...")
	# A = DATA
	# x = np.ones(rows)
	# tol = -10
	# q = 3
	# b = [(random() - 0.5) * 3 for _ in range(rows)]
	# # test(lambda d: [nm.DirectSolver(d, tol).power_method(x)], DATA, "nm.DirectSolver(DATA).power_method() (Python implementation)")
	# # test(lambda d: [nm.DirectSolver(d, tol).inverse_power_method(x, q)], DATA, "nm.DirectSolver(DATA).inverse_power_method() (Python implementation)")
	# # test(lambda d: [nm.DirectSolver(d, tol).qr_algorithm(omega)], DATA, "nm.DirectSolver(DATA).qr_algorithm() (Python implementation)")
	# # test(lambda d: [nm.DirectSolver(d, tol).steepest_descent(x, b)], DATA, "nm.DirectSolver(DATA).steepest_descent() (Python implementation)")
	# # test(lambda d: [nm.DirectSolver(d, tol).conjugate_gradient(x, b, C=np.diag(np.diag(d)))], DATA, "nm.DirectSolver(DATA).conjugate_gradient() (Python implementation)")
	# sys.modules["EigenValues"] = bar
	# spec.loader.exec_module(bar)
	# test(lambda d: [bar.EigenValues(d, tol).power_method(x)], DATA, "nm.EigenValues(DATA).power_method() (CPython C++ extension)")
	# test(lambda d: [bar.EigenValues(d, tol).inverse_power_method(x, q)], DATA, "nm.EigenValues(DATA).inverse_power_method() (CPython C++ extension)")
	# test(lambda d: [bar.EigenValues(d, tol).qr_algorithm()], DATA, "nm.EigenValues(DATA).qr_algorithm() (CPython C++ extension)")

	# print("")

	# # test SystemOfEquations...
	# print("Testing SystemOfEquations...")
	# A = DATA
	# x = np.ones(rows)
	# tol = -10
	# b = [(random() - 0.5) * 3 for _ in range(rows)]
	# # test(lambda d: [nm.DirectSolver(d, tol).power_method(x)], DATA, "nm.DirectSolver(DATA).power_method() (Python implementation)")
	# # test(lambda d: [nm.DirectSolver(d, tol).inverse_power_method(x, q)], DATA, "nm.DirectSolver(DATA).inverse_power_method() (Python implementation)")
	# # test(lambda d: [nm.DirectSolver(d, tol).qr_algorithm(omega)], DATA, "nm.DirectSolver(DATA).qr_algorithm() (Python implementation)")
	# # test(lambda d: [nm.DirectSolver(d, tol).steepest_descent(x, b)], DATA, "nm.DirectSolver(DATA).steepest_descent() (Python implementation)")
	# # test(lambda d: [nm.DirectSolver(d, tol).conjugate_gradient(x, b, C=np.diag(np.diag(d)))], DATA, "nm.DirectSolver(DATA).conjugate_gradient() (Python implementation)")
	# sys.modules["SystemOfEquations"] = bar
	# spec.loader.exec_module(bar)
	# test(lambda d: [bar.SystemOfEquations(d, b, tol).gaussian_elimination()], DATA, "nm.SystemOfEquations(DATA).gaussian_elimination() (CPython C++ extension)")
	# if bar.positive_definite(DATA):
	# 	test(lambda d: [bar.SystemOfEquations(d, b, tol).conjugate_gradient(x)], DATA, "nm.SystemOfEquations(DATA).conjugate_gradient() (CPython C++ extension)")
	# test(lambda d: [bar.SystemOfEquations(d, b, tol).steepest_descent(x)], DATA, "nm.SystemOfEquations(DATA).steepest_descent() (CPython C++ extension)")

	# # #print("")

	# # ##test ivp
	# # #print("Testing ivp...")
	# # #sys.modules["ivp"] = bar
	# # #spec.loader.exec_module(bar)
	# # #fig = plt.figure(figsize=(7,7))
	# # #ax = fig.add_gridspec(5, 2)
	# # #ax1 = fig.add_subplot(ax[0, 0])
	# # #ax2 = fig.add_subplot(ax[0, 1])
	# # #ax3 = fig.add_subplot(ax[1, 0])
	# # #ax4 = fig.add_subplot(ax[1, 1])
	# # #ax5 = fig.add_subplot(ax[2, 0])
	# # #ax6 = fig.add_subplot(ax[2, 1])
	# # #ax7 = fig.add_subplot(ax[3, 0])
	# # #ax8 = fig.add_subplot(ax[3, 1])
	# # #ax9 = fig.add_subplot(ax[4, 0])
	# # #ax10 = fig.add_subplot(ax[4, 1])
	# # #n = 5 	# grain growth exponent
	# # #H_star = 10**5 	# activation enthalpy [J/mol]
	# # #k0 = 10**10 	# growth rate constant [micro-m-n/s]
	# # #R = 8.314462175 	# universal gas constant [J/K-mol]
	# # #T = 1000 	# absolute temperature [K]
	# # #d0 = 10 	# initial grain size [micro-m]
	# # #t = 10*60 	# total experiment time [s]
	# # #d_dot = lambda t, d: k0/(n*d**(n - 1))*sp.exp(-H_star/R/T)
	# # #H = (10, 5, 1)
	# # ##ltx_expression = r"\frac{k}{nd^{n-1}}\exp(-\frac{H_star}{RT})"
	# # ##ltx_dict = {
	# # ##	"n": n,
	# # ##	"H_star": H_star,
	# # ##	"k0": k0,
	# # ##	"R": R,
	# # ##	"T": T,
	# # ##	"d0": d0,
	# # ##	"t": t
	# # ##}
	# # #def d_dot_analytical(t, d0, h):
	# # #	domain, Y, increment = np.arange(h, t+h, h), [d0], [0]
	# # #	d = lambda t, d0: (d0**n + k0*sp.exp(-H_star/R/T)*t)**(1/n)
	# # #	for ti in domain:
	# # #		Y.append(d(ti, d0))
	# # #		increment.append(d(ti, d0) - d(ti - h, d0))
	# # #	return pd.DataFrame(data={"Iterations": range(len(domain)+1), "Domain": np.arange(0, t+h, h), "Range": Y, "Increments": increment})
	# # ## forward_euler
	# # #print("Testing forward_euler...")
	# # #k = 1
	# # #for h in H:
	# # #	obj = bar.IVP(d_dot, 0, t, d0, steps=t/h)
	# # #	df = obj.forward_euler()
	# # #	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# # #	ax1.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# # #	ax2.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# # #	k += 1
	# # #df = d_dot_analytical(t, d0, h)
	# # #ax1.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# # #ax2.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# # ##plt.show()
	# # ## improved_euler
	# # #print("Testing improved_euler...")
	# # #k = 1
	# # #for h in H:
	# # #	obj = bar.IVP(d_dot, 0, t, d0, steps=t/h)
	# # #	df = obj.improved_euler()
	# # #	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# # #	ax3.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# # #	ax4.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# # #	k += 1
	# # #df = d_dot_analytical(t, d0, h)
	# # #ax3.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# # #ax4.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# # ##plt.show()
	# # ## backward_euler
	# # #print("Testing backward_euler...")
	# # #k = 1
	# # #for h in H:
	# # #	obj = bar.IVP(d_dot, 0, t, d0, steps=t/h)
	# # #	df = obj.backward_euler()
	# # #	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# # #	ax5.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# # #	ax6.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# # #	k += 1
	# # #df = d_dot_analytical(t, d0, h)
	# # #ax5.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# # #ax6.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# # ##plt.show()
	# # ## runge_kutta
	# # #print("Testing runge_kutta...")
	# # #k = 1
	# # #for h in H:
	# # #	obj = bar.IVP(d_dot, 0, t, d0, steps=t/h)
	# # #	df = obj.runge_kutta()
	# # #	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# # #	ax7.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# # #	ax8.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# # #	k += 1
	# # #df = d_dot_analytical(t, d0, h)
	# # #ax7.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# # #ax8.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# # ##plt.show()
	# # ## trapezoidal
	# # #print("Testing trapezoidal...")
	# # #k = 1
	# # #for h in H:
	# # #	obj = bar.IVP(d_dot, 0, t, d0, steps=t/h)
	# # #	df = obj.trapezoidal()
	# # #	print(f"{k}, h = {h}s: d = {df['Range'].values[-1]} for total change = {np.sum(df['Increments'].values)} in {df['Iterations'].values[-1]} time steps.")
	# # #	ax9.plot(df["Domain"].values, df["Range"].values, label=f"{h} s")
	# # #	ax10.plot(df["Domain"].values, df["Increments"].values, label=f"{h} s")
	# # #	k += 1
	# # #df = d_dot_analytical(t, d0, h)
	# # #ax9.plot(df["Domain"].values, df["Range"].values, label=f"Analytical")
	# # #ax10.plot(df["Domain"].values, df["Increments"].values, label=f"Analytical")
	# # #ax1.set_xlabel("Time [s]")
	# # #ax1.set_ylabel(r"$\mu$")
	# # #ax1.legend()
	# # #ax2.set_xlabel("Time [s]")
	# # #ax2.set_ylabel(r"$\Delta\mu$")
	# # #ax2.legend()
	# # #ax3.set_xlabel("Time [s]")
	# # #ax3.set_ylabel(r"$\mu$")
	# # #ax3.legend()
	# # #ax4.set_xlabel("Time [s]")
	# # #ax4.set_ylabel(r"$\Delta\mu$")
	# # #ax4.legend()
	# # #ax5.set_xlabel("Time [s]")
	# # #ax5.set_ylabel(r"$\mu$")
	# # #ax5.legend()
	# # #ax6.set_xlabel("Time [s]")
	# # #ax6.set_ylabel(r"$\Delta\mu$")
	# # #ax6.legend()
	# # #ax7.set_xlabel("Time [s]")
	# # #ax7.set_ylabel(r"$\mu$")
	# # #ax7.legend()
	# # #ax8.set_xlabel("Time [s]")
	# # #ax8.set_ylabel(r"$\Delta\mu$")
	# # #ax8.legend()
	# # #ax9.set_xlabel("Time [s]")
	# # #ax9.set_ylabel(r"$\mu$")
	# # #ax9.legend()
	# # #ax10.set_xlabel("Time [s]")
	# # #ax10.set_ylabel(r"$\Delta\mu$")
	# # #ax10.legend()
	# # ##plt.show()

	# # #print("")

	# # ##test bvp
	# # #print("Testing bvp...")
	# # #sys.modules["bvp"] = bar
	# # #spec.loader.exec_module(bar)
	# # #fig = plt.figure(figsize=(7,7))
	# # #fig.suptitle(r"Comparing Boundary Value Problem Methods")
	# # #ax = fig.add_gridspec(3, 3)
	# # #ax1 = fig.add_subplot(ax[0, 0])
	# # #ax2 = fig.add_subplot(ax[1, 0])
	# # #ax3 = fig.add_subplot(ax[1, 1])
	# # #ax4 = fig.add_subplot(ax[2, 0])
	# # #ax5 = fig.add_subplot(ax[2, 1])
	# # #ax6 = fig.add_subplot(ax[2, 2])
	# # #a, b = 1, 2
	# # #alpha, beta = 0, 2
	# # #p = lambda x: -(2/x)
	# # #q = lambda x: 2/(x**2)
	# # #r = lambda x: -3*(x**2)
	# # ## alpha, beta = 1, 2
	# # ## p = lambda x: -(2/x)
	# # ## q = lambda x: 2/(x**2)
	# # ## r = lambda x: np.sin(np.log(x))/(x**2)
	# # #ypp = lambda y, yp, x: p(x)*yp + q(x)*y + r(x)
	# # #F = [p, q, r, ypp]
	# # #H = (0.2, 0.1, 0.05)
	# # #def y_analytical(a, b, alpha, beta, h):
	# # #	N = int((b - a)/h)+1
	# # #	domain, Y, increment = np.linspace(a, b, N+2), [], []
	# # #	y = lambda x: -52/(21*x**2) - (x**4)/6 + 37*x/14
	# # #	# c2 = (8 - 12*np.sin(np.log(2)) - 4*np.cos(np.log(2)))/70
	# # #	# c1 = 11/10 - c2
	# # #	# y = lambda x: c1*x + c2/(x**2) - 3/10*np.sin(np.log(x)) - 1/10*np.cos(np.log(x))
	# # #	for x in domain:
	# # #		Y.append(y(x))
	# # #		increment.append(y(x) - y(x - h))
	# # #	# Y.append(beta)
	# # #	# increment.append(beta - y(b))
	# # #	return pd.DataFrame(data={"Iterations": range(len(domain)), "Domain": np.linspace(a, b, N+2), "Range": Y, "Increments": increment})
	# # #k = 1
	# # #for h in H:
	# # #	df = y_analytical(a, b, alpha, beta, h)
	# # #	print(f"{k}, h = {h}: Max = {np.max(df['Range'].values)} in {df['Iterations'].values[-1]} steps.")
	# # #	ax1.plot(df["Domain"].values, df["Range"].values, label=f"{h}")
	# # #	k += 1
	# # ##plt.show()

	# # #print("Testing linear_shooting_method...")
	# # #ax3r = ax3.twinx()
	# # #ax3.get_yaxis().set_visible(False)
	# # #k = 1
	# # ## k, H = 1, [0.1]
	# # #for h in H:
	# # #	N = int((b - a)/h)+1
	# # #	domain = np.linspace(a, b, N+2)
	# # #	df = bar.BVP(F, a, b, alpha, beta, h, steps=N).linear_shooting_method()
	# # #	print(f"{k}, h = {h}: Max = {np.max(df['Range'].values)} in {df['Iterations'].values[-1]} steps.")
	# # #	ax2.plot(df["Domain"].values, df["Range"].values, label=f"{h}")
	# # #	df_analytical = y_analytical(a, b, alpha, beta, h)
	# # #	error = np.abs((df["Range"].values - df_analytical["Range"].values)/df_analytical["Range"].values*100)
	# # #	ax3.plot(domain, error, label=f"{h}")
	# # #	k += 1
	# # ##plt.show()

	# # #print("Testing finite_difference_method...")
	# # #k = 1
	# # #def y_analytical(a, b, alpha, beta, h):
	# # #	N = int((b - a)/h)+2
	# # #	domain, Y, increment = np.linspace(a, b, N+2), [], []
	# # #	y = lambda x: -52/(21*x**2) - (x**4)/6 + 37*x/14
	# # #	# c2 = (8 - 12*np.sin(np.log(2)) - 4*np.cos(np.log(2)))/70
	# # #	# c1 = 11/10 - c2
	# # #	# y = lambda x: c1*x + c2/(x**2) - 3/10*np.sin(np.log(x)) - 1/10*np.cos(np.log(x))
	# # #	for x in domain:
	# # #		Y.append(y(x))
	# # #		increment.append(y(x) - y(x - h))
	# # #	# Y.append(beta)
	# # #	# increment.append(beta - y(b))
	# # #	return pd.DataFrame(data={"Iterations": range(len(domain)), "Domain": np.linspace(a, b, N+2), "Range": Y, "Increments": increment})
	# # ## k, H = 1, [0.1]
	# # #for h in H:
	# # #	N = int((b - a)/h)+1
	# # #	domain = np.linspace(a, b, N+3)
	# # #	df, df_iter = bar.BVP(F, a, b, alpha, beta, h, steps=N).finite_difference_method()
	# # #	print(f"{k}, h = {h}: Max = {np.max(df['Range'].values)} in {df['Iterations'].values[-1]} steps and {df_iter['Iterations'].values[-1]} iterations for total error = {np.sum(df_iter['Errors'].values[-1])}.")
	# # #	ax4.plot(df["Domain"].values, df["Range"].values, label=f"{h}")
	# # #	df_analytical = y_analytical(a, b, alpha, beta, h)
	# # #	error = np.abs((df["Range"].values - df_analytical["Range"].values)/df_analytical["Range"].values*100)
	# # #	ax5.plot(domain, error, label=f"{h}")
	# # #	ax6.semilogx(df_iter["Iterations"].values, df_iter["Errors"].values, label=f"{h}")
	# # #	k += 1
	# # #ax4.plot(df_analytical["Domain"].values, df_analytical["Range"].values, label=f"Analytical")
	# # #ax1.set_title("Analytical Form")
	# # #ax1.set_xlabel("Domain (x)")
	# # #ax1.set_ylabel("Range (y)")
	# # #ax1.legend()
	# # #ax2.plot(df_analytical["Domain"].values, df_analytical["Range"].values, label=f"Analytical")
	# # #ax2.set_title("Linear Shooting Method")
	# # #ax2.set_xlabel("Domain (x)")
	# # #ax2.set_ylabel("Range (y)")
	# # #ax2.legend()
	# # #ax3r.set_title("Comparing Errors of Step Size")
	# # #ax3.set_xlabel("Domain (x)")
	# # #ax3r.set_ylabel("Percent Error [%]")
	# # #ax3.legend()
	# # #ax4.set_title("Finite Difference Method")
	# # #ax4.set_xlabel("Domain (x)")
	# # #ax4.set_ylabel("Range (y)")
	# # #ax4.legend()
	# # #ax5.set_title("Comparing Errors of Step Size")
	# # #ax5.set_xlabel("Domain (x)")
	# # #ax5.set_ylabel("Percent Error [%]")
	# # #ax5.legend()
	# # #ax6.set_title("Comparing Iterative Errors of Step Size")
	# # #ax6.set_xlabel("Iterations")
	# # #ax6.set_ylabel("Method Error")
	# # #ax6.legend()
	# # ##plt.show()



	plt.show()

logging.shutdown()