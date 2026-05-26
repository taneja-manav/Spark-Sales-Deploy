import streamlit as st
import plotly.express as px
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, round as spark_round, count

# Reuse your bulletproof session logic
def get_spark():
    java_opts = (
        "-Djava.security.manager=allow "
        "-Djava.net.preferIPv4Stack=true "
        "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED "
        "--add-opens=java.base/java.lang=ALL-UNNAMED "
        "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED "
        "--add-opens=java.base/java.io=ALL-UNNAMED "
        "--add-opens=java.base/java.util=ALL-UNNAMED "
        "--add-opens=java.base/java.net=ALL-UNNAMED "
        "--add-opens=java.base/java.nio=ALL-UNNAMED "
        "--add-opens=java.base/sun.security.ssl=ALL-UNNAMED "
        "--add-opens=java.base/sun.security.action=ALL-UNNAMED "
        "--add-opens=java.base/sun.net.util=ALL-UNNAMED"
    )
    return SparkSession.builder \
        .appName("StreamlitSalesAnalysis") \
        .master("local[*]") \
        .config("spark.driver.extraJavaOptions", java_opts) \
        .getOrCreate()

st.set_page_config(page_title="Fintech Sales Dashboard", layout="wide")
st.title("📊 MANAV'S ONLINE SALES DASBOARD")

st.markdown("---")

# Sidebar for controls
st.sidebar.header("Analysis Settings")
data_path = "/home/ec2-user/pyspark_project/data/OnlineRetail.csv"

if st.sidebar.button('🚀 Run Spark Analysis'):
    with st.spinner('Spark is crunching the data...'):
        spark = get_spark()
        
        # Load and Clean
        df = spark.read.csv(data_path, header=True, inferSchema=True)
        df = df.filter(col("Quantity") > 0).withColumn("Revenue", col("Quantity") * col("UnitPrice"))
        
        # METRICS ROW
        total_rev = df.select(spark_sum("Revenue")).collect()[0][0]
        total_qty = df.select(spark_sum("Quantity")).collect()[0][0]
        
        col1, col2 = st.columns(2)
        col1.metric("Total Revenue", f"£{total_rev:,.2f}")
        col2.metric("Total Items Sold", f"{total_qty:,}")

        # GRAPH 1: Top Countries by Revenue
        st.subheader("🌍 Revenue by Country (Top 10)")
        country_df = df.groupBy("Country").agg(
            spark_round(spark_sum("Revenue"), 2).alias("Revenue")
        ).orderBy(col("Revenue").desc()).limit(10).toPandas()
        
        fig_rev = px.bar(country_df, x='Country', y='Revenue', color='Revenue', 
                         color_continuous_scale='Viridis', template="plotly_dark")
        st.plotly_chart(fig_rev, use_container_width=True)

        # GRAPH 2: Sales Volume vs Revenue (Scatter)
        st.subheader("📈 Quantity vs Revenue Correlation")
        scatter_df = df.groupBy("Country").agg(
            spark_sum("Quantity").alias("Total_Qty"),
            spark_sum("Revenue").alias("Total_Rev")
        ).toPandas()
        
        fig_scatter = px.scatter(scatter_df, x="Total_Qty", y="Total_Rev", text="Country", 
                                 size="Total_Rev", color="Country", template="plotly_dark")
        st.plotly_chart(fig_scatter, use_container_width=True)

        spark.stop()
else:
    st.info("Click 'Run Spark Analysis' in the sidebar to start the PySpark engine.")
