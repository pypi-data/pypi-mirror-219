from setuptools import setup,find_packages

setup(name='gd32graphing',
      version='0.0.3',
      description='Several no-fuss methods for creating plots with plotly by microsoft',
      author='GeorgeDong32',
      author_email='GeorgeDong32@outlook.com',
      requires= ['numpy','typing','pandas','plotly',], # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      )