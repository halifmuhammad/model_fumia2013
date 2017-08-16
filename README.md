### Fumia network 

The model_fumia2013 reproduces the CRC model described in (Fumiã et al., 2013). Run with following commands: 

```bash 
# preprocessing for model network 
pytest -qs test_a.py

# figure 3 in (Fumiã et al., 2013)
pytest -qs test_b.py

# figure 4 in (Fumiã et al., 2013)
pytest -qs test_c.py
```

#### Dependencies 

```
git clone git@github.com:jehoons/BooleanSim.git
cd BooleanSim 
python setup.py install 
```

#### Reference 
Fumiã, Herman F., and Marcelo L. Martins. 2013. “Boolean Network Model for Cancer Pathways: Predicting Carcinogenesis and Targeted Therapy Outcomes.” PLOS ONE 8 (7): e69008. doi:10.1371/journal.pone.0069008.

