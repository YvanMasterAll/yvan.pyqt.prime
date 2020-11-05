from setuptools import setup

requirements = [
    # TODO: put your package requirements here
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-faulthandler',
    'pytest-mock',
    'pytest-qt',
    'pytest-xvfb',
]

setup(
    name='ZzClient',
    version='0.0.1',
    description="ZzClient",
    author="yvan ",
    author_email='1136838669@qq.com',
    url='https://github.com/masteryvanall/yvan.pyqt.prime',
    packages=['ZzClient', 'ZzClient.resource',
              'ZzClient.test'],
    package_data={'ZzClient.resource': ['*.png']},
    entry_points={
        'console_scripts': [
            'ZzClient=ZzClient.ZzClient:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='yvan.pyqt.prime',
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='test',
    tests_require=test_requirements
)
