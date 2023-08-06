from setuptools import setup, find_packages

setup(
    name='LangChainAgentFactory',
    version='0.2',
    description='A wrapper for LangChain to create AI Agents with existing LLMs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='http://github.com/yourusername/LangChainAgentFactory',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'langchain',
        # etc.
    ],
)