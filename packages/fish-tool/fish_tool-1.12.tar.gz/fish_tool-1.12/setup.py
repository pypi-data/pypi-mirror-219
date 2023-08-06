from setuptools import setup, find_packages

setup(
    name="fish_tool",
    version="1.12",
    author="aifish",
    url="https://gitee.com/laowangzi/fish_tool",
    author_email="ofyu@163.com",
    description="some tool code",
    packages=find_packages(),
    install_requires=[
        'pyyaml>=6.0',
        'tqdm>=4.36.1',
        'requests>=2.22.0',
        'httpx>=0.18.1',
        "fastapi>=0.90.0",
        "uvicorn>=0.20.0",
    ],
    extras_require={
        'AI': [
            "torch>=1.0"
        ],
        'db': [
            "pymysql>=1.0.2"
        ],
    },
    python_requires='>=3.6',
)

"""
build代码
python setup.py sdist

上传到PyPi
(pip install twine)
twine upload dist/*
"""
"""
更新内容
1.1 2023.03.22 db/sqlite_tool.py 增加字段功能

1.11 2023年3月27日 db/sqlite_tool.py 增加scroll功能
1.12 2023年7月18日 ai/torch_tool.py 增加load_model(model, path, device=None)
"""
