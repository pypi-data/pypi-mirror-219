from setuptools import setup, find_packages

setup(name="pyISBO",
      version="1.0.1",
      author="Liu Xiangting and Zhu Zesheng",
      author_email="liu-xt22@mails.tsinghua.edu.cn",
      packages = find_packages(),
      description="An integrated Surrogate-Base Optimization Toolbox",
      package_dir={"pyISBO":"pyISBO"},
      package_data={"pyISBO":['pyISBO/OperationData.xlsx']},
      url="https://github.com/Shawn1eo/pyISBO",
      python_require=">=3.7",
      install_require = [
            "numpy >= 1.19.0",
            "pandas >= 1.3.0",
            "PuLP >= 2.7.0",
            "tensorflow >= 2.11.0",
            "scikit-learn >= 1.0.2",
            "sklearn-contrib-py-earth >= 0.1.0"]
      )