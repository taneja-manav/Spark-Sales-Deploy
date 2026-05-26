# PySpark Sales Analysis — Online Retail Dataset

A data engineering mini-project that analyzes the **UCI Online Retail** dataset using **PySpark**.

## Project Structure

```
cloudDEVOPS(final)/
├── data/
│   └── OnlineRetail.csv          # UCI Online Retail dataset
├── src/
│   └── sales_analysis.py         # PySpark analysis script
├── Jenkinsfile                   # CI/CD declarative pipeline
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## What It Does

1. **Loads** the Online Retail transactional dataset (~541K records)
2. **Cleans** column headers by removing spaces
3. **Calculates** Total Revenue (`Quantity × UnitPrice`) grouped by `Country`
4. **Displays** the top countries ranked by revenue

## Quick Start

### Prerequisites
- Python 3.8+
- Java 8 or 11 (required by Spark)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Analysis
```bash
python src/sales_analysis.py
```

Or with `spark-submit`:
```bash
spark-submit --master local[*] src/sales_analysis.py
```

## CI/CD Pipeline

The included `Jenkinsfile` defines three stages:

| Stage              | Description                                  |
|--------------------|----------------------------------------------|
| Environment Setup  | Creates a virtualenv and installs packages   |
| Linting            | Runs `flake8` on `src/`                      |
| Run Spark Job      | Executes the PySpark script via spark-submit |

## Dataset

- **Source:** [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)
- **Records:** ~541,909 transactions
- **Period:** Dec 2010 – Dec 2011
- **License:** CC BY 4.0
