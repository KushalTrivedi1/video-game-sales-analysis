
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Video Game Sales Analysis",
    page_icon="🎮",
    layout="wide"
)

# Project folder structure:
# vgsales/
# ├── results/
# │   ├── spark_genre_sales.csv
# │   ├── spark_platform_sales.csv
# │   ├── spark_region_sales.csv
# │   ├── spark_year_sales.csv
# │   ├── spark_top_games.csv
# │   └── spark_top_publishers.csv
# └── dashboard/
#     └── app.py

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_csv(filename):
    path = RESULTS_DIR / filename

    if not path.exists():
        return None

    try:
        return pd.read_csv(path)
    except (pd.errors.ParserError, UnicodeDecodeError, OSError):
        return None


genre_df = load_csv("spark_genre_sales.csv")
platform_df = load_csv("spark_platform_sales.csv")
region_df = load_csv("spark_region_sales.csv")
year_df = load_csv("spark_year_sales.csv")
games_df = load_csv("spark_top_games.csv")
publisher_df = load_csv("spark_top_publishers.csv")


# --------------------------------------------------
# VALIDATE DATA
# --------------------------------------------------

required_files = {
    "Genre sales": genre_df,
    "Platform sales": platform_df,
    "Regional sales": region_df,
    "Yearly sales": year_df,
    "Top games": games_df,
    "Top publishers": publisher_df,
}

missing_files = [
    name for name, dataframe in required_files.items()
    if dataframe is None
]

if missing_files:
    st.error(
        "Some required CSV files are missing or could not be read: "
        + ", ".join(missing_files)
    )
    st.info(
        "Check that the files exist inside the project's results folder "
        "and rerun the Spark notebook if necessary."
    )
    st.stop()


required_columns = {
    "Genre sales": (genre_df, ["genre", "sales"]),
    "Platform sales": (platform_df, ["platform", "sales"]),
    "Regional sales": (region_df, ["region", "sales"]),
    "Yearly sales": (year_df, ["year", "sales"]),
    "Top games": (games_df, ["game", "sales"]),
    "Top publishers": (publisher_df, ["publisher", "sales"]),
}

for name, (dataframe, columns) in required_columns.items():
    missing = [column for column in columns
               if column not in dataframe.columns]

    if missing:
        st.error(
            f"{name} CSV is missing required columns: "
            + ", ".join(missing)
        )
        st.stop()


# Convert sales to numeric values
for dataframe in [
    genre_df,
    platform_df,
    region_df,
    year_df,
    games_df,
    publisher_df,
]:
    dataframe["sales"] = pd.to_numeric(
        dataframe["sales"], errors="coerce"
    )

    dataframe.dropna(subset=["sales"], inplace=True)


# Convert years to numeric when possible
year_df["year"] = pd.to_numeric(
    year_df["year"], errors="coerce"
)

year_df.dropna(subset=["year"], inplace=True)
year_df["year"] = year_df["year"].astype(int)


# Sort datasets
genre_df = genre_df.sort_values("sales", ascending=False)
platform_df = platform_df.sort_values("sales", ascending=False)
region_df = region_df.sort_values("sales", ascending=False)
year_df = year_df.sort_values("year")
games_df = games_df.sort_values("sales", ascending=False)
publisher_df = publisher_df.sort_values("sales", ascending=False)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎮 Video Game Sales Analysis")

st.caption(
    "Explore video game sales by genre, publisher, platform, "
    "region, and release year using Apache Spark."
)

st.divider()


# --------------------------------------------------
# SUMMARY METRICS
# --------------------------------------------------

genre_total = genre_df["sales"].sum()

if not genre_df.empty:
    top_genre_row = genre_df.iloc[0]
    top_genre = str(top_genre_row["genre"])
    top_genre_sales = top_genre_row["sales"]
else:
    top_genre = "N/A"
    top_genre_sales = 0

if not publisher_df.empty:
    top_publisher_row = publisher_df.iloc[0]
    top_publisher = str(top_publisher_row["publisher"])
    top_publisher_sales = top_publisher_row["sales"]
else:
    top_publisher = "N/A"
    top_publisher_sales = 0

# This is the number of distinct game entries in the exported
# top-games CSV, not necessarily the full dataset size.
games_count = len(games_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Games in exported list",
    f"{games_count:,}"
)

col2.metric(
    "Genre sales total",
    f"{genre_total:,.2f} M"
)

col3.metric(
    "Top genre",
    top_genre,
    help=f"Sales: {top_genre_sales:,.2f} million"
)

col4.metric(
    "Top publisher",
    top_publisher,
    help=f"Sales: {top_publisher_sales:,.2f} million"
)

st.divider()


# --------------------------------------------------
# DASHBOARD TABS
# Machine Learning tab intentionally removed
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Genres",
    "Publishers",
    "Platforms and Regions",
    "Years",
    "Top Games"
])


# --------------------------------------------------
# TAB 1: GENRE ANALYSIS
# --------------------------------------------------

with tab1:
    st.header("Video Game Sales by Genre")

    if genre_df.empty:
        st.warning("No genre sales data is available.")
    else:
        st.bar_chart(
            genre_df.set_index("genre")[["sales"]],
            horizontal=True
        )

        st.subheader("Genre Sales Data")

        st.dataframe(
            genre_df.reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Genre Sales CSV",
            data=genre_df.to_csv(index=False).encode("utf-8"),
            file_name="spark_genre_sales.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# TAB 2: PUBLISHER ANALYSIS
# --------------------------------------------------

with tab2:
    st.header("Video Game Sales by Publisher")

    if publisher_df.empty:
        st.warning("No publisher sales data is available.")
    else:
        top_n = st.slider(
            "Number of publishers to display",
            min_value=1,
            max_value=max(1, min(20, len(publisher_df))),
            value=min(10, len(publisher_df)),
            key="publisher_top_n"
        )

        displayed_publishers = publisher_df.head(top_n)

        st.bar_chart(
            displayed_publishers.set_index("publisher")[["sales"]],
            horizontal=True
        )

        st.subheader("Publisher Sales Data")

        st.dataframe(
            publisher_df.reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Publisher Sales CSV",
            data=publisher_df.to_csv(index=False).encode("utf-8"),
            file_name="spark_top_publishers.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# TAB 3: PLATFORM AND REGIONAL ANALYSIS
# --------------------------------------------------

with tab3:
    st.header("Platform Sales")

    if platform_df.empty:
        st.warning("No platform sales data is available.")
    else:
        st.bar_chart(
            platform_df.set_index("platform")[["sales"]],
            horizontal=True
        )

        st.dataframe(
            platform_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Platform Sales CSV",
            data=platform_df.to_csv(index=False).encode("utf-8"),
            file_name="spark_platform_sales.csv",
            mime="text/csv"
        )

    st.divider()

    st.header("Regional Sales Distribution")

    if region_df.empty:
        st.warning("No regional sales data is available.")
    else:
        chart_col, table_col = st.columns([3, 2])

        with chart_col:
            st.bar_chart(
                region_df.set_index("region")[["sales"]],
                horizontal=True
            )

        with table_col:
            st.dataframe(
                region_df,
                use_container_width=True,
                hide_index=True
            )

        st.download_button(
            "Download Regional Sales CSV",
            data=region_df.to_csv(index=False).encode("utf-8"),
            file_name="spark_region_sales.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# TAB 4: YEARLY SALES ANALYSIS
# --------------------------------------------------

with tab4:
    st.header("Global Video Game Sales by Release Year")

    if year_df.empty:
        st.warning("No yearly sales data is available.")
    else:
        st.line_chart(
            year_df.set_index("year")[["sales"]]
        )

        st.subheader("Yearly Sales Data")

        st.dataframe(
            year_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Yearly Sales CSV",
            data=year_df.to_csv(index=False).encode("utf-8"),
            file_name="spark_year_sales.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# TAB 5: TOP-SELLING GAMES
# --------------------------------------------------

with tab5:
    st.header("Top-Selling Video Games")

    if games_df.empty:
        st.warning("No top-game data is available.")
    else:
        top_n_games = st.slider(
            "Number of games to display",
            min_value=1,
            max_value=max(1, min(20, len(games_df))),
            value=min(10, len(games_df)),
            key="games_top_n"
        )

        displayed_games = games_df.head(top_n_games)

        st.bar_chart(
            displayed_games.set_index("game")[["sales"]],
            horizontal=True
        )

        st.subheader("Top Games Data")

        st.dataframe(
            games_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Top Games CSV",
            data=games_df.to_csv(index=False).encode("utf-8"),
            file_name="spark_top_games.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Video Game Sales Analysis | Data processed using Apache Spark "
    "and visualized with Streamlit."
)
