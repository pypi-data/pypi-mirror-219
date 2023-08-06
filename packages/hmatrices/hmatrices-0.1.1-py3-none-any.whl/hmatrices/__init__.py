from juliacall import Main as jl

# cmd = 'import Pkg;' + 'Pkg.add(name="HMatrices",rev="main");' + 'using HMatrices;' + 'using LinearAlgebra;'

cmd = 'import Pkg;' + 'Pkg.develop(path="/Users/lfaria/Research/WaveProp/HMatrices");' + \
    'using HMatrices;' + 'using LinearAlgebra;' + 'BLAS.set_num_threads(1);'
jl.seval(cmd)

hmatrices_jl = jl.HMatrices

Point3D = hmatrices_jl.SVector[3, jl.Float64]
