# dUMLe Language

![logo.png](logo.png)

Our language allows creating UML diagrams:
- class diagrams
- use case diagrams
- sequence diagrams


## Usage

Make sure you have internet connection. Clone this repository.

```
git clone https://gitlab.kis.agh.edu.pl/dpalka/komp22-dumle.git
cd komp22-dumle
```

To get your diagram in .png format run following commands:

```
pip install -r requirements.txt
python main.py [PATH TO .dml FILE]
```

The result png file will be created in the catalog results/

To test our examples use path to our code_examples file e.g. code_examples/classdiag.dml
