# Setup Instructions

## Conda Environment

A conda environment has been created for this project. Here's how to use it:

### Activate the conda environment

```bash
conda activate h5n1_bellevue
```

### Verify activation

You should see `(h5n1_bellevue)` at the beginning of your terminal prompt. You can also verify with:
```bash
which python  # Should point to conda environment
conda info --envs  # Shows active environment
```

### Install/Update dependencies

All dependencies are already installed via conda-forge. If you need to reinstall or add packages:

```bash
conda activate h5n1_bellevue
conda install -c conda-forge <package_name>
```

Or use pip for packages not available in conda:
```bash
pip install <package_name>
```

### Deactivate when done

```bash
conda deactivate
```

## Testing the Installation

Run the example script to verify everything works:

```bash
conda activate h5n1_bellevue
python src/example_risk_map.py
```

Or test the module directly:

```bash
conda activate h5n1_bellevue
python -c "from src.risk_map import RiskMap; print('✓ Module works!')"
```

## IDE Setup

If you're using VS Code or PyCharm:
- VS Code: Select the Python interpreter from the conda environment
  - Look for: `~/opt/anaconda3/envs/h5n1_bellevue/bin/python` (or similar)
- PyCharm: Configure the project interpreter to use the conda environment `h5n1_bellevue`

## Notes

- The conda environment is managed by conda (not in the project directory)
- Always activate the conda environment before running scripts
- Geospatial packages (geopandas, GDAL, etc.) are installed via conda-forge for better compatibility
- If you add new dependencies, you can update `requirements.txt` with: `pip freeze > requirements.txt` (for pip packages)

## Alternative: Using venv

If you prefer the standard Python `venv` instead of conda, you can use:
```bash
source venv/bin/activate  # Instead of conda activate
```

Both environments are set up and ready to use!

