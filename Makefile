
install:
	pip install -e .
	python -m swi_kernel.install

clean:
	pip uninstall swi_kernel
	jupyter kernelspec remove swi_kernel
