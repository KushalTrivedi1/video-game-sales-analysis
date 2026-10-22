
# Video Game Sales Analysis Using Apache Spark

## Project Overview
This project analyzes video game sales data using Apache Spark and PySpark RDDs. It identifies sales trends across genres, gaming platforms, regions, release years, games, and publishers.

## Objectives
- Analyze global video game sales by genre.
- Compare sales across gaming platforms.
- Study sales across different regions.
- Analyze sales trends by release year.
- Identify top-selling video games.
- Find publishers with the highest total sales.

## Technologies Used
- **Python** – Programming language
- **Apache Spark** – Big data processing
- **PySpark RDD** – Data processing and aggregation
- **Pandas** – Organizing and exporting results
- **Matplotlib** – Creating charts and visualizations
- **Jupyter Notebook** – Executing the analysis

## Dataset
The project uses `vgsales.csv`, which contains video game information, including:
- Rank
- Name
- Platform
- Year
- Genre
- Publisher
- North America sales
- Europe sales
- Japan sales
- Other region sales
- Global sales

The dataset contains approximately 16,598 records and 11 columns. Sales figures are measured in millions of copies.

## Project Structure
```text
vgsales/
├── dashboard/
├── results/
├── vgsales.csv
├── VGSales_Spark_Analysis.ipynb
└── README.md
```

- `dashboard/` – Dashboard-related files, if used.
- `results/` – Generated CSV summaries and charts.
- `vgsales.csv` – Input dataset.
- `VGSales_Spark_Analysis.ipynb` – Main analysis notebook.
- `README.md` – Project documentation.

## Analysis Workflow
1. Load the video game sales dataset.
2. Parse and validate the CSV records.
3. Process the data using Spark RDDs.
4. Aggregate sales using operations such as `map()` and `reduceByKey()`.
5. Export summary results as CSV files.
6. Generate charts using Matplotlib.
7. Save the output files for further use.

## Expected Outputs
- Genre-wise sales analysis
- Platform-wise sales analysis
- Regional sales analysis
- Year-wise sales analysis
- Top-selling games
- Top publishers
- CSV summary files and visualization charts

## How to Run
1. Install Python and Java.
2. Install the required Python packages:

   ```bash
   pip install pyspark pandas matplotlib
   ```

3. Open the Jupyter Notebook.
4. Place `vgsales.csv` in the notebook's working directory.
5. Run the notebook cells in order.

## Conclusion
This project demonstrates how Apache Spark can process and aggregate video game sales data to discover meaningful patterns and present results through tables and visualizations.

## Author
Kushal Trivedi  
Varad Kawtikwar
