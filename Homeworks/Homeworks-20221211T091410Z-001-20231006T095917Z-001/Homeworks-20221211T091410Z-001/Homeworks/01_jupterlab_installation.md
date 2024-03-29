```
conda create --name lab-dev python=3.7
conda activate lab-dev
pip install jupyterlab pandas scikit-learn mlflow
ipython kernel install --user --name=lab-dev
jupyter lab --ip 0.0.0.0 --port 8991
```


