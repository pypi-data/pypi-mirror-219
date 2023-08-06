# meowy

🐱 An unofficial [_The Cat API_](https://thecatapi.com/) wrapper for Python

# 📦 Packages

## 🐍 PyPI

```sh
pip install meowy
```

# 🔎 Examples
[_examples/basic.py_](https://github.com/elaresai/meowy/blob/main/examples/basic.py)
```py
import meowy


client = meowy.Client()

# Let's search for 10 images at once
for _ in range(10):
    print(client.images.search())
```

# ✨ Links

[🐍 _PyPi_](https://pypi.org/project/meowy/)\
[🏠 _Homepage_](https://github.com/elaresai/meowy)\
[🐱 _Repository_](https://github.com/elaresai/meowy)
