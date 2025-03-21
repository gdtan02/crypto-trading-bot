# from setuptools import setup, find_packages
#
# setup(
#     name="crypto-trading-bot",
#     version="1.0.0",
#     description="Self-Learning Cryptocurrency Trading System",
#     author="gdtan02",
#     author_email="gdtan021115@gmail.com",
#     packages=find_packages(),
#     include_package_data=True,
#     python_requires=">=3.8",
#     install_requires=[
#         # API and Web Framework
#         "fastapi>=0.68.0",
#         "uvicorn>=0.15.0",
#         "requests==2.32.0",
#
#         # Data Processing
#         "pandas>=1.3.0",
#         "numpy>=1.21.0",
#
#         # Machine Learning
#         "scikit-learn>=1.0.0",
#         "tensorflow>=2.8.0",
#         "keras>=2.8.0",
#
#         # Database
#         "sqlalchemy>=1.4.0",
#         "psycopg2-binary>=2.9.1",  # PostgreSQL
#         "pymongo>=4.0.0",  # MongoDB
#
#         # Data providers
#         "cybotrade>=1.5.0"
#
#         # Environment variables
#         "python-dotenv>=0.19.0",
#
#         # Background Jobs
#         "apscheduler>=3.8.0",
#
#         # Logging
#         "loguru>=0.5.3",
#
#         # Testing
#         "pytest>=6.2.5",
#
#         # Utilities
#         "pydantic>=1.8.2",
#     ],
#     extras_require={
#         "dev": [
#             "black>=21.9b0",
#             "isort>=5.9.3",
#             "flake8>=3.9.2",
#             "mypy>=0.910",
#             "jupyter>=1.0.0",
#             "pytest-cov>=2.12.1",
#         ],
#     },
#     entry_points={
#         "console_scripts": [
#             "crypto-trading-ml=app.main:main",
#         ],
#     },
# )