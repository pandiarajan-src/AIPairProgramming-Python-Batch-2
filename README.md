# AI Pair Programming Python Batch 2 🐍

A comprehensive Python learning repository featuring three major projects and various algorithm implementations for AI/ML education and practice.

## 📋 Table of Contents

- [Major Projects](#major-projects)
- [Algorithm Implementations](#algorithm-implementations)
- [Data Analysis Scripts](#data-analysis-scripts)
- [Testing](#testing)
- [Prerequisites](#prerequisites)
- [Contributing](#contributing)

---

## 🚀 Major Projects

### 1. BookBloom 🌸 - E-commerce Book Platform

**"Books Reborn, Knowledge Renewed"**

A full-stack e-commerce application for browsing and purchasing books.

**Features:**
- 📚 Book catalog with search functionality
- 👤 User registration and JWT authentication
- 🛒 Shopping cart management
- 💳 Checkout process
- 📱 Responsive web design

**Tech Stack:** FastAPI, SQLite, Vanilla JavaScript

**Quick Start:**
```bash
cd book_bloom
./start.sh
# Access at: http://127.0.0.1:8000
```

📖 **[Full Documentation](book_bloom/README.md)**

---

### 2. Log Analyzer 📊 - Server Log Processing Tool

A Python CLI tool to analyze server logs and count requests per IP address.

**Features:**
- Process CSV or plain text log files
- Count requests per IP address
- Export results to CSV format
- Support for large log files

**Quick Start:**
```bash
cd log_analyzer
python3 log_analyzer.py --input app_logs.csv --output results.csv --top 5
```

📖 **[Full Documentation](log_analyzer/README.md)**

---

### 3. Movie Recommender 🎬 - Content-Based Recommendation System

A CLI-based movie recommendation system that suggests top-rated movies by genre.

**Features:**
- Genre-based movie filtering
- Rating-based recommendations
- CSV data processing
- Interactive CLI interface

**Quick Start:**
```bash
cd movie_recommender
python movie_recommender.py --csv movies.csv --limit 5
```

📖 **[Full Documentation](movie_recommender/README.md)**

---

## 🧮 Algorithm Implementations

### Core Algorithm Scripts

Run these Python scripts directly from the repository root:

#### 1. FizzBuzz Implementation
```bash
python fizzbuzz.py
```
Classic FizzBuzz algorithm with performance timing.

#### 2. Number Algorithms Collection
```bash
python number_algorithms.py
```
**Includes:**
- Factor finding algorithms
- String comparison functions  
- Character frequency analysis
- Vowel counting
- Divisibility checkers
- Factorial calculation (recursive & iterative)

#### 3. String Algorithms Collection
```bash
python strings_algorithms.py
```
**Includes:**
- Palindrome number detection
- Pangram sentence verification
- Anagram string comparison
- Character frequency analysis
- Armstrong number identification

---

## 📈 Data Analysis Scripts

### Machine Learning & Data Science

#### 1. Mall Customer Analysis
```bash
python mall_customer_analysis.py
```
**Features:**
- KMeans clustering analysis
- Customer segmentation
- Data visualization with matplotlib/seaborn
- Cluster analysis and insights

#### 2. Pima Indians Diabetes Analysis
```bash
python pima_knn_analysis.py
```
**Features:**
- KNN classification model
- Medical dataset analysis
- Comprehensive data visualization
- Model accuracy evaluation
- Statistical insights

#### 3. Synthetic Data Generator
```bash
python synthetic_data.py
```
**Features:**
- Generate synthetic CSV datasets
- Mixed data types (strings and integers)
- Configurable rows and columns
- CSV reading and validation

---

## 🧪 Testing

All major components include comprehensive test suites:

### Run All Tests
```bash
# Run all test files
python -m pytest test_*.py -v

# Or run individual test files
python test_fizzbuzz.py
python test_number_algorithms.py
python test_strings_algorithms.py
python test_mall_customer_analysis.py
python test_pima_knn_analysis.py
python test_synthetic_data.py
python test_book_bloom.py
```

### Project-Specific Tests
```bash
# Log Analyzer tests
cd log_analyzer
python -m pytest tests/ -v

# Movie Recommender tests  
cd movie_recommender
python -m pytest test_movie_recommender.py -v
```

---

## 📋 Prerequisites

### System Requirements
- **Python 3.9+** (Python 3.12+ recommended for BookBloom)
- pip or uv package manager

### Common Dependencies
Most scripts use standard library modules, but some require additional packages:

```bash
# For data analysis scripts
pip install pandas numpy matplotlib seaborn scikit-learn

# For BookBloom (handled automatically)
cd book_bloom/bookbloom && uv sync

# For Movie Recommender
cd movie_recommender && pip install pandas pyarrow pytest pylint
```

---

## 📁 Repository Structure

```
AIPairProgramming-Python-Batch-2/
├── book_bloom/                    # 🌸 E-commerce platform
│   ├── bookbloom/                # FastAPI backend & frontend
│   ├── README.md                 # BookBloom documentation
│   └── start.sh                  # Quick startup script
├── log_analyzer/                 # 📊 Log processing tool
│   ├── log_analyzer.py          # Main CLI script
│   ├── app_logs.csv             # Sample data
│   └── README.md                # Log analyzer documentation
├── movie_recommender/            # 🎬 Movie recommendation system
│   ├── movie_recommender.py     # Main CLI script
│   ├── movies.csv               # Sample movie data
│   └── README.md                # Movie recommender documentation
├── fizzbuzz.py                   # Classic FizzBuzz algorithm
├── number_algorithms.py          # Number manipulation algorithms
├── strings_algorithms.py         # String processing algorithms
├── mall_customer_analysis.py     # Customer clustering analysis
├── pima_knn_analysis.py         # Medical data KNN classification
├── synthetic_data.py            # Synthetic dataset generator
├── test_*.py                    # Comprehensive test suites
└── README.md                    # This file
```

---

## 🤝 Contributing

This repository serves as a learning resource for Python programming, algorithms, and machine learning concepts. Each script includes detailed documentation and examples for educational purposes.

### Key Learning Areas Covered:
- **Web Development**: FastAPI, REST APIs, Authentication
- **Data Science**: Pandas, NumPy, Scikit-learn
- **Algorithms**: String processing, number theory, sorting
- **Machine Learning**: Classification, clustering, data visualization
- **Software Engineering**: Testing, modular design, CLI tools

---

## 📞 Support

For questions about specific projects, refer to their individual README files:
- [BookBloom Documentation](book_bloom/README.md)
- [Log Analyzer Documentation](log_analyzer/README.md)  
- [Movie Recommender Documentation](movie_recommender/README.md)

Happy Learning! 🎓✨