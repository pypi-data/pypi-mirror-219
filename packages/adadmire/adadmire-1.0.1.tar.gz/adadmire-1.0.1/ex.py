from adadmire import impute
import numpy as np

# load data containing missing values in continuous
X = np.load('data/Higuera_et_al/data_na_scaled.npy')
# as well as in discrete features
D = np.load('data/Higuera_et_al/pheno_na.npy')

print(np.sum(np.isnan(X)))
print(np.sum(np.isnan(D)))

levels = np.load('data/Higuera_et_al/levels.npy') # levels of discrete variables

# define Lambda sequence
lam_zero = np.sqrt(np.log(X.shape[1] + D.shape[1]/2)/X.shape[0])
lam_seq = np.array([-1.75,-2.0,-2.25])
lam = [pow(2, x) for x in lam_seq]
lam = np.array(lam)
lam = lam_zero * lam

# now impute with ADMIRE
X_imp, D_imp,lam_o = impute(X,D,levels,lam)

print(np.sum(np.isnan(X_imp)))
print(np.sum(np.isnan(D_imp)))