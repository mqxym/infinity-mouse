from setuptools import setup, find_packages

setup(
    name='infinity-mouse',
    version='0.2.1',
    author='mqxym',
    author_email='maxim@omg.lol',
    description='Mouse infinity movement after timeout.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mqxym/infinity-mouse',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.10',
    platforms=["MacOS"],
    install_requires=[
        'pyobjc-framework-Quartz',
        'pyautogui',
        'screeninfo',
    ],
    py_modules=['run'],
    entry_points={
        'console_scripts': [
            'infinity-mouse=run:infinity_movement',
        ],
    },
)