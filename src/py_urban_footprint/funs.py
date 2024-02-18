

def gt_summarize_harvest(df): 
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