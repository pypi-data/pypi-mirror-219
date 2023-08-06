import setuptools
import hertz


if __name__ == '__main__':
    setuptools.setup(
        name="hertz",
        version=hertz.__version__,
        author="Andrew Blomenberg",
        author_email="andrewBlomen@gmail.com",
        description="A simple, standard, and handy way to represent Hertz, kHz, GHz, etc",
        install_requires=[],
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
        ],
        url='https://github.com/Yook74/hertz',
        python_requires='>=3.6',
    )
