from setuptools import setup, find_packages

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

setup(
    name='py_go_goose',
    author='wangjianzhou',
    version='1.2',
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'bdist_wheel': bdist_wheel},
)