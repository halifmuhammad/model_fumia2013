all: prep fig3 fig4 

prep: 
	pytest -qs --pdb test_a.py

fig3: 
	pytest -qs --pdb test_b.py

fig4: 
	pytest -qs --pdb test_c.py

clean: 
	rm -f figure-* output-* chk-* *.pyx
