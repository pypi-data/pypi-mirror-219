from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("multimcts.mcts", ["multimcts/mcts.pyx"]),
    Extension("multimcts.gamestate", ["multimcts/gamestate.pyx"]),
]

setup(
    name="multimcts",
    version="0.1",
    author="Taylor Vance",
    description="Monte Carlo Tree Search for multiple teams",
    license="MIT",
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
