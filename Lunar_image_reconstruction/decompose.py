import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import FactorAnalysis, PCA
import tensortools as tt
from tensortools.operations import unfold as tt_unfold, khatri_rao
import tensorly as tl
from tensorly import unfold as tl_unfold
from tensorly.decomposition import parafac
from utils import *

import cv2
 
img = cv2.imread('moon1.png')
img[36:46,10:25]=0
print(img.shape)
X, rank = img, 2

# Perform CP decompositon using TensorLy
factors_tl = parafac(X, rank=rank)

U = tt.cp_als(X, rank=rank, verbose=False)

factors_tt = U.factors.factors

# Reconstruct M, with the result of each library
# print(factors_tl[1],"*********")
M_tl = reconstruct(factors_tl[1])
# M_tt = reconstruct(factors_tt)
# print(img)
print(M_tl)
cv2.imshow("image",img)
cv2.waitKey(0)
# cv2.imshow("image",M_tl)
plt.imshow(M_tl/255)
plt.show()
# cv2.waitKey(0)
print(M_tl.shape)

def decompose_three_way(tensor, rank, max_iter=2, verbose=False):
    print(tensor.shape,"**********")
    # a = np.random.random((rank, tensor.shape[0]))
    b = np.random.random((rank, tensor.shape[1]))
    c = np.random.random((rank, tensor.shape[2]))

    for epoch in range(max_iter):
        # optimize a
        input_a = khatri_rao([b.T, c.T])
        target_a = tl.unfold(tensor, mode=0).T
        print(b.shape,c.shape,input_a.shape,target_a.shape)
        a = np.linalg.solve(input_a.T.dot(input_a), input_a.T.dot(target_a))

        # optimize b
        input_b = khatri_rao([a.T, c.T])
        target_b = tl.unfold(tensor, mode=1).T
        b = np.linalg.solve(input_b.T.dot(input_b), input_b.T.dot(target_b))

        # optimize c
        input_c = khatri_rao([a.T, b.T])
        target_c = tl.unfold(tensor, mode=2).T
        c = np.linalg.solve(input_c.T.dot(input_c), input_c.T.dot(target_c))

        if verbose and epoch % int(max_iter * .2) == 0:
            res_a = np.square(input_a.dot(a) - target_a)
            res_b = np.square(input_b.dot(b) - target_b)
            res_c = np.square(input_c.dot(c) - target_c)
            print("Epoch:", epoch, "| Loss (C):", res_a.mean(), "| Loss (B):", res_b.mean(), "| Loss (C):", res_c.mean())

    return a.T, b.T, c.T

factors_np = decompose_three_way(X[:128], rank)
# plot_factors(factors_tl[1])
# plot_factors(factors_tt)