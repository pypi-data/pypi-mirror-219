# a simple test, where most of the calls are made using juliacall

from hmatrices import hmatrices_jl, Point3D
from juliacall import Main as jl

m, n = 1000, 1000

X = jl.rand(Point3D, m)
Y = jl.rand(Point3D, n)

G_str = """
function G(x,y)
    d = norm(x-y)
    1/d
end
"""
G = jl.seval(G_str)
K = jl.KernelMatrix(G, X, Y)

H = hmatrices_jl.assemble_hmat(K)

x = jl.rand(n)
y = jl.zeros(n)

A = jl.Matrix(H)

jl.mul_b(y, H, x, threads=True)

# TODO: compare this to the exact value for a given index
