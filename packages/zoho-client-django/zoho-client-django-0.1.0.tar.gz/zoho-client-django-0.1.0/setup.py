from setuptools import setup, find_packages

setup(
    name="zoho-client-django",
    version="0.1.0",  # Update this for new versions
    description="Django client for the Zoho CRM API",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "Django>=4.2.3,<5.0",
        "requests>=2.31.0,<3.0",
    ],
)
