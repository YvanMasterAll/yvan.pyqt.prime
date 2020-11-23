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
    packages=[
        'ZzClient.bloc',
        'ZzClient.common',
        'ZzClient.config',
        'ZzClient.db',
        'ZzClient.party',
        'ZzClient.view',
        'ZzClient.widget',
        'ZzClient.resources',
        'ZzClient.test'
    ],
    package_data={'resources': ['*.png']},
    entry_points={
        'console_scripts': [
            'ZzClient=ZzClient.__main__:start'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='com.zzzk.zzclient',
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='test',
    tests_require=test_requirements
)
