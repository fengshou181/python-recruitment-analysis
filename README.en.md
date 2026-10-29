# Python Recruitment Data Analysis Platform

## 📋 Project Overview

This project is a Python-based recruitment data analysis platform. It crawls job information from recruitment websites such as Boss Zhipin, cleans, stores, and analyzes the data, and provides users with intuitive visualizations through a web interface. The platform offers core features such as job data analysis, salary prediction, and job matching, aiming to help job seekers understand the current IT job market and improve job hunting efficiency.

## 🚀 Core Features

- **Recruitment Data Analysis**: Multi-dimensional analysis of salary distribution, education requirements, work experience, skill requirements, etc., across different job categories.
- **Salary Prediction**: Predict possible salary ranges based on user-input conditions using machine learning models.
- **Job Matching**: Intelligent job matching based on user skills, preferred locations, and other criteria.
- **Regional Salary Map**: Visual display of salary levels and job distributions across different regions.
- **Job Detail Analysis**: In-depth analysis of specific jobs, including salary trends and skill requirements.

## 🔧 Tech Stack

### Frontend

- HTML5, CSS3, JavaScript
- jQuery, Bootstrap
- ECharts visualization library

### Backend

- Python 3.8+
- Flask web framework
- MySQL database
- Pandas, NumPy for data processing
- Scikit-learn for machine learning

## 📊 Data Pipeline

1. **Data Collection**: Using Python web crawlers to scrape job data from Boss Zhipin and other recruitment websites.
2. **Data Cleaning**: Deduplication, error correction, and format unification.
3. **Data Storage**: Storing the cleaned data in a MySQL database.
4. **Data Analysis**: Statistical analysis using tools like Pandas.
5. **Model Training**: Training salary prediction models based on historical data.
6. **Data Visualization**: Visualizing the analysis results using ECharts.

## 🗂️ Project Structure

```
Python-Recruitment-Analysis-Platform/
├── app.py                 # Flask application entry point
├── mysql.py               # Database operation module
├── match.py               # Job matching algorithm module
├── salary_model.py        # Salary prediction model
├── spider/                # Web crawler module
│   ├── boss_spider.py     # Boss Zhipin crawler
│   └── data_processor.py  # Data processing script
├── static/                # Static resources
│   ├── css/               # CSS files
│   ├── js/                # JavaScript files
│   ├── vendor/            # Third-party libraries
│   └── img/               # Image resources
├── templates/             # HTML templates
│   ├── index.html         # Homepage
│   ├── job-speculate.html # Job matching page
│   ├── job-match-result.html # Job matching result page
│   ├── salary-speculate.html # Salary prediction page
│   ├── speculate-result.html # Salary prediction result page
│   └── ...                # Other templates
├── models/                # Pre-trained models
├── data/                  # Data files
└── README.md              # Project documentation
```

## 💾 Database Design

### c_data Table (Job Data Table)

| Field Name | Data Type | Description           |
| ---------- | --------- | --------------------- |
| num        | int       | Primary Key ID        |
| name       | varchar   | Job Title             |
| province   | varchar   | Province              |
| city       | varchar   | City                  |
| area       | varchar   | Area                  |
| detail     | varchar   | Detailed Location     |
| company    | varchar   | Company Name          |
| scale      | varchar   | Company Size          |
| min_salary | float     | Minimum Salary        |
| max_salary | float     | Maximum Salary        |
| avg_salary | float     | Average Salary        |
| education  | varchar   | Education Requirement |
| experience | varchar   | Work Experience       |
| label      | varchar   | Company Labels        |
| skill      | varchar   | Skill Requirements    |
| welfare    | varchar   | Benefits              |

## 📈 Core Algorithms

### Job Matching Algorithm

The job matching algorithm calculates the matching score based on multiple factors, including:

- **Skill Matching**: Overlap between user skills and job requirements.
- **Location Matching**: Degree of alignment between user’s preferred location and job location.
- **Job Direction Matching**: Relevance between the user’s expected position and the actual job.
- **Salary Matching**: Whether the job salary meets user expectations.

The system dynamically adjusts the weights of each factor based on different priority strategies (comprehensive, skill-priority, location-priority, salary-priority).

### Salary Prediction Model

The machine learning model is trained using historical recruitment data and considers the following factors:

- Job Type
- Location
- Education
- Work Experience
- Skill Set
- Company Size

The model predicts the salary range under specific conditions based on the influence of these factors.

## 📊 Page Display

### Homepage

![Homepage](/images/home.png)

### Salary Heatmap

![Salary Heatmap](/images/map.png)

### Job Matching Result Page

![Job Matching Result](/images/post-result.png)

### Salary Prediction Page

![Salary Prediction](/images/salary-predict.png)

![Salary Prediction Result](/images/salary-result.png)

## 🔍 Big Data Technology Applications

This project applies various big data technologies, including:

1. **Data Collection**: Distributed crawling, IP proxy pool, request frequency control
2. **Data Processing**: Text normalization, keyword extraction, natural language processing
3. **Data Storage**: Relational database design, index optimization
4. **Data Analysis**: Statistical analysis, clustering analysis, correlation analysis
5. **Machine Learning**: Feature engineering, model training, hyperparameter tuning
6. **Data Visualization**: Interactive charts, geographic visualization

## 🛠️ Installation & Usage

### Requirements

- Python 3.8+
- MySQL 5.7+

### Installation Steps

1. Clone the repository

```bash
git clone https://github.com/yourusername/python-recruitment-analysis.git
cd python-recruitment-analysis
```

1. Install dependencies

```bash
pip install -r requirements.txt
```

1. Configure the database

```bash
# Import database structure
mysql -u username -p database_name < database/structure.sql
```

1. Run the application

```bash
python app.py
```

1. Access the application
    Visit `http://localhost:5000` in your browser.

## 🌟 Project Highlights

1. **Comprehensive Data Analysis**: Multi-dimensional analysis of recruitment market data to provide data-driven job search guidance.
2. **Accurate Job Matching**: Intelligent job recommendations based on user preferences and conditions.
3. **Scientific Salary Prediction**: Machine learning-based salary expectations.
4. **Intuitive Visualizations**: Rich chart visualizations for clear presentation of analysis results.
5. **Optimized User Experience**: Friendly interface and smooth interactions for improved usability.

## 📝 Future Development

1. **Algorithm Optimization**: Continuously improve job matching and salary prediction accuracy.
2. **Data Expansion**: Broaden data sources to cover more platforms and job categories.
3. **User Profiling**: Build a user profiling system for more personalized recommendations.
4. **Community Features**: Add user interaction and experience sharing features to create a job market community.
5. **Mobile Compatibility**: Develop mobile applications for better accessibility.

## 📄 License

This project is licensed under the [MIT License](https://chatgpt.com/c/LICENSE).

## 🙏 Acknowledgements

- Thanks to [Boss Zhipin](https://www.zhipin.com/) for providing data sources.
- Thanks to all teachers and classmates who supported and provided valuable suggestions for this project.