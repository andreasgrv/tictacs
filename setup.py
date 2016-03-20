from setuptools import setup

setup(
        name='tictacs',
        packages=['tictacs'],
        version='0.0.3',
        author='Andreas Grivas',
        author_email='andreasgrv@gmail.com',
        description='Machine learning pipeline creation from config files',
        url='https://github.com/andreasgrv/tictacs',
        download_url='https://github.com/andreasgrv/tictacs/tarball/0.0.3',
        license='BSD',
        keywords=['machine learning', 'pipeline', 'config'],
        classifiers=[],
        install_requires=[
            'pyyaml',
            ],
        setup_requires=['pytest-runner'],
        test_requires=['pytest']
        )
