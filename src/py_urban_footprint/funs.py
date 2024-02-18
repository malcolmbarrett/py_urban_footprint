def gt_summarize_harvest(df): 
    """
    Summarizes the harvest data by FarmType in the given DataFrame.

    Parameters:
    df (polars.DataFrame): The input DataFrame containing the harvest data.

    Returns:
    great_tables.GT: The summarized harvest data in a great_tables.GT object.
    """
    import polars as pl
    from great_tables import GT
    harvest = (df
        .group_by("FarmType")
        .agg(pl.col("Harvested").mean())
        .sort("Harvested"))

    gt = (GT(harvest)
        .fmt_number(columns=["Harvested"])
        .cols_label(FarmType="Farm Type", Harvested="Harvested (kg)"))
    return gt
    
def gt_summarize_water_by_solar(farms):
    """
    Summarizes water usage by solar panels.

    Args:
        farms (polars.DataFrame): DataFrame containing farm data.

    Returns:
        great_tables.GT: A formatted table summarizing water usage by solar panels.
    """
    import polars as pl
    from great_tables import GT

    water_use_by_solar = farms.filter(pl.col("SolarPanels_bin") != "").group_by(pl.col("SolarPanels_bin")).agg(
        pl.col("WaterUse_GWP_2019").mean().alias("water_use"),
        pl.len().alias("n")
    ).sort("water_use")

    tbl = GT(water_use_by_solar).fmt_number("water_use").cols_label(
        SolarPanels_bin="Solar Panels",
        water_use="Water Use (L)",
        n="N"
    )

    return tbl


def plot_water_usage(farms):
    """
    Plots the water usage based on the size of production site and farm type.

    Args:
        farms (polars.DataFrame): DataFrame containing farm data.

    Returns:
        a seaborn plot
    """
    import seaborn as sns
    import polars as pl
    plot_data = (
        farms
            .filter(pl.col("SolarPanels_bin") != "")
            .with_columns(
                pl.col("SizeOfProductionSite").log(),
                pl.col("WaterUse_GWP_2019").log(),
            )
    )

    plot = sns.lmplot(
        data=plot_data,
        x="SizeOfProductionSite",
        y="WaterUse_GWP_2019",
        hue="FarmType",
        col="FarmType",
        palette="colorblind",
        legend="full"
    )

    return plot
