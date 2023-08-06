from setuptools import setup

setup(
    name='lqq_tool_weekreport',
    version='1.0.1',
    description='周报自动生成工具',
    author='lqq',
    author_email='linqingf@sina.com',
    url='https://gitee.com/linqingf/py_tool_weekreport',
    packages=['com.lqq.tool.report'],
    install_requires=[
        "pandas",
        "openpyxl",
        "vika"
    ],
)