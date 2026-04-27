import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Wine Quality EDA")


df = pd.read_csv("WineQT.csv")

#Color options
palette = st.sidebar.selectbox(
    "Renk Paleti Seç",
    ["viridis", "magma", "plasma", "inferno", "crest", "rocket", "mako"]
)

# Sidebar selection
st.sidebar.header("Görselleştirme Seçimi")
options = st.sidebar.multiselect(
    "Hangi grafikleri görmek istersin?",
    ["Density vs Alcohol",
     "Alcohol vs Density by Quality",
     "pH ve Fixed Acidity Boxplot",
     "Volatile Acidity Violin",
     "Residual Sugar vs Alcohol/Density",
     "Chlorides Histogram",
     "Chlorides vs Sulphates",
     "Total Acid by Quality",
     "Correlation Heatmap",
     "Quality Count Barplot",
     "KDE Plots for Each Column by Quality"
     ]
)


#  Graphics 1
if "Density vs Alcohol" in options:
    st.subheader("Density vs Alcohol")
    fig, ax = plt.subplots()
    ax.scatter(df["density"], df["alcohol"])
    ax.set_xlabel("Density")
    ax.set_ylabel("Alcohol")
    st.pyplot(fig)


#  Graphics 2
if "Alcohol vs Density by Quality" in options:
    st.subheader("Alcohol vs Density by Quality")
    fig, ax = plt.subplots()
    sns.scatterplot(x="density", y="alcohol", hue="quality", data=df, ax=ax,palette=palette)
    st.pyplot(fig)


#  Graphics 3
if "pH ve Fixed Acidity Boxplot" in options:
    st.subheader("pH ve Fixed Acidity Boxplot")
    fig, ax = plt.subplots(1,2, figsize=(12,5))
    sns.boxplot(x="quality", y="pH", data=df, ax=ax[0],palette=palette)
    sns.boxplot(x="quality", y="fixed acidity", data=df, ax=ax[1],palette=palette)
    st.pyplot(fig)


#  Graphics 4
if "Volatile Acidity Violin" in options:
    st.subheader("Volatile Acidity by Quality")
    fig, ax = plt.subplots()
    sns.violinplot(x="quality", y="volatile acidity", data=df, inner="stick", ax=ax,palette=palette)
    st.pyplot(fig)


#  Graphics 5
if "Residual Sugar vs Alcohol/Density" in options:
    df["alcohol_density_ratio"] = df['alcohol'] / df['density']
    st.subheader("Residual Sugar vs Alcohol/Density by Quality")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.scatterplot(
        x="residual sugar",
        y="alcohol_density_ratio",
        hue="quality",
        data=df,
        palette=palette,
        ax=ax
    )
    ax.set_xlabel("Residual Sugar")
    ax.set_ylabel("Alcohol/Density Ratio")
    ax.set_title("Residual Sugar vs Alcohol/Density by Quality")
    st.pyplot(fig)


#  Graphics 6
if "Chlorides Histogram" in options:
    st.subheader("Chlorides Histogram")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.histplot(df["chlorides"], kde=True, ax=ax,palette=palette)
    st.pyplot(fig)


#  Graphics 7
if "Chlorides vs Sulphates" in options:
    st.subheader("Chlorides vs Sulphates by Quality")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.scatterplot(x="chlorides", y="sulphates", hue="quality", data=df, ax=ax,palette=palette)
    ax.set_title("Chlorides vs Sulphates by Quality")
    st.pyplot(fig)


#  Graphics 8
if "Total Acid by Quality" in options:
    df['total_acid'] = df['fixed acidity'] + df['volatile acidity'] + df['citric acid']
    st.subheader("Total Acid by Quality")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.boxplot(x="quality", y="total_acid", data=df, ax=ax,palette=palette)
    ax.set_xlabel("Quality")
    ax.set_ylabel("Total Acid")
    ax.set_title("Total Acid by Quality")
    st.pyplot(fig)


#  Graphics 9
if "Correlation Heatmap" in options:
    st.subheader("Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(df.corr(), annot=True, ax=ax,cmap=palette)
    st.pyplot(fig)


# Graphics 10
if "Quality Count Barplot" in options:
    st.subheader("Quality Count")
    fig, ax = plt.subplots(figsize=(8,6))
    
    # renkleri belirle
    colors = sns.color_palette(palette, len(df["quality"].unique()))
    
    # Bar plot
    df["quality"].value_counts().sort_index().plot(kind="bar", ax=ax, color=colors)
    
    ax.set_xlabel("Quality")
    ax.set_ylabel("Count")
    st.pyplot(fig)



# Graphics 11
if "KDE Plots for Each Column by Quality" in options:
    st.subheader("KDE Plots for Each Column by Quality")

    columns = df.columns

    # 4x4 subplot
    fig, ax = plt.subplots(4, 4, figsize=(16, 15))
    ax = ax.flatten()

    # KDE plot loop
    for i, column in enumerate(columns):
        if pd.api.types.is_numeric_dtype(df[column]):
            sns.kdeplot(
                data=df,
                x=column,
                hue=df["quality"],
                ax=ax[i],
                palette=palette
            )
            ax[i].set_title(f"{column} Distribution")
            ax[i].set_xlabel(None)
        else:
            ax[i].axis("off")

    # Closing blank graphics
    for j in range(i + 1, len(ax)):
        ax[j].axis("off")

    plt.tight_layout()
    st.pyplot(fig)