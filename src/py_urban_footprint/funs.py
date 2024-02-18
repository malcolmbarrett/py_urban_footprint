

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