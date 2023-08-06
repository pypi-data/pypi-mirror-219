from setuptools import setup, Extension


setup(
    name='dequeai',
    version='0.000008234',
    description='Python Package for DEQUE AI Platform',
    author="The DEQUE AI Team",
    author_email='team@deque.app',
    packages=["dequeai"],
    url='https://dequeapp-deque.gitbook.io/deque-docs/getting-started/dequeai-experiment-tracking',
    keywords='dequeai client for deep learning',
    install_requires=[
          "coolname","requests","numpy","pillow","psutil","GPUtil","ipython","tabulate"
      ],
)