# 📊 Sales Analytics Dashboard

Interactive sales analytics dashboard built with Python, Streamlit, Plotly, Pandas, and MySQL.

The application provides real-time sales insights through interactive charts, KPI metrics, filters, and formatted financial data visualization.

![Tela inicial.](https://raw.githubusercontent.com/rensilver/image-repo-github/main/prin-sales-analytics-dashboard.png "This is a sample image.")

---

# 🚀 Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- MySQL
- SQLAlchemy
- PyMySQL

---

# ✨ Features

- 📈 Revenue analysis over time
- 🛒 Top-selling products visualization
- 💳 Filter by payment method
- 📅 Date range filtering
- 🌙 Dark/Light mode toggle
- ⚡ Cached database connections and queries
- 💰 Brazilian currency formatting (R$)
- 📊 KPI cards:
  - Total Revenue
  - Orders
  - Average Ticket
- 🧾 Interactive data table

---

# 📂 Project Structure

```bash
project/
│
├── sales.py
├── requirements.txt
├── .streamlit/
│   └── secrets.toml
└── README.md
```

---

# ⚙️ Installation

Clone the repository:
```
git clone <repository-url>
```
Enter the project folder:
```
cd sales-analytics-dashboard
```
Create virtual environment:
```
python -m venv venv
```
Activate virtual environment:
Windows
```
venv\Scripts\activate
```
Linux / Mac
```
source venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```

---

# 🔐 Streamlit Secrets Configuration

Create the file:
```
.streamlit/secrets.toml
```
Example:
```
[mysql]
host = "localhost"
port = 3306
database = "your_database"
user = "your_user"
password = "your_password"
```

---

▶️ Run the Application
```
streamlit run sales.py
```

---

# 📊 Dashboard Preview

Features included in the dashboard:

- Revenue over time analysis
- Product sales ranking
- Interactive filters
- Responsive layout
- Dark mode support

---

# 🧠 Key Learnings

This project helped reinforce concepts such as:

- Building data-driven applications with Streamlit
- Database integration using SQLAlchemy
- Data transformation with Pandas
- Interactive visualization with Plotly
- Performance optimization using caching
- Dashboard UI customization with CSS
- Data formatting and presentation best practices

---

# 📌 Future Improvements
- Docker support
- Authentication/Login
- Deployment on Streamlit Cloud or AWS
- Export reports to PDF/Excel
- Real-time database updates
- Advanced analytics and forecasting

---

# 👨‍💻 Author

Renato Silveira

Software Engineer transitioning into AI Engineering, Machine Learning, and Data Science.
