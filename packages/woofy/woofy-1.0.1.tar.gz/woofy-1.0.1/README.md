# woofy

🐶 An unofficial [The Dog API](https://thedogapi.com) wrapper for Python

# 📦 Packages

## 🐍 PyPI

```sh
pip install woofy
```

# 🔎 Examples

[_examples/basic.py_](https://github.com/elaresai/woofy/blob/main/examples/basic.py)

```py
import woofy


client = woofy.Client()

# Let's search for 10 images at once
for _ in range(10):
    print(client.images.search())
```

# ✨ Links

[🐍 _PyPI_](https://pypi.org/project/woofy/)\
[🏠 _Homepage_](https://github.com/elaresai/woofy)\
[🐱 _Repository_](https://github.com/elaresai/woofy)
