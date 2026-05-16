from setuptools import setup, find_packages

setup(
    name='infinity-mouse',
    version='0.3.0',
    author='mqxym',
    author_email='maxim@omg.lol',
    description='Mouse infinity movement after timeout.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mqxym/infinity-mouse',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.9',
    platforms=['MacOS', 'Windows', 'Linux'],
    install_requires=[
        "pyobjc-framework-Quartz; platform_system == 'Darwin'",
        "python-xlib; platform_system == 'Linux'",
        'pyautogui',
    ],
    py_modules=['run'],
    entry_points={
        'console_scripts': [
            'infinity-mouse=run:infinity_movement',
        ],
    },
)

## Versioning Names:
# 1.0.0a1 (Alpha release)
# 1.0.0b1 (Beta release)
# 1.0.0rc1 (Release candidate)