# pyquadim
[![CI](https://github.com/Widecss/pyquadim/actions/workflows/ci.yml/badge.svg)](https://github.com/Widecss/pyquadim/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/pyquadim.svg)](https://badge.fury.io/py/pyquadim)

简单移植 quadim 到 Python 中。（~~用于 qq bot 的涩图防和谐~~）

## 安装
使用 pip
~~~
pip install pyquadim
~~~

编译安装（需要 [Rust](https://www.rust-lang.org/) 环境）
~~~
pip install -r requirements.txt

# 直接安装
python setup.py install

# 或者打包 wheel
python setup.py sdist bdist_wheel
~~~

## 用法
~~~ python
from PIL import Image
import pyquadim

img = Image.open("./test.jpg")
img = img.convert("RGBA")  # Quadim 项目目前仅支持 RGBA

w, h = img.size
data = img.getdata()

result = pyquadim.render(data, w, h, shape="yr-add", thres_ay=10, stroke_width=6)

img.putdata(result)
img.show()
~~~


## 问题
- ~~能力不足，linux 用户请自行编译~~


## 致谢
- [Quadim](https://github.com/eternal-io/quadim)
- [PyO3](https://github.com/PyO3/pyo3)
