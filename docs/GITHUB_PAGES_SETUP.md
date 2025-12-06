# Setting Up GitHub Pages for Interactive Risk Maps

This guide will help you host your interactive H5N1 risk maps on GitHub Pages so they can be accessed via a public URL.

## Quick Setup (5 minutes)

### Step 1: Enable GitHub Pages

1. Go to your GitHub repository on GitHub.com
2. Click **Settings** (top right)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select:
   - **Branch:** `main` (or `master`)
   - **Folder:** `/ (root)` or `/docs`
5. Click **Save**

### Step 2: Choose Your Approach

**Option A: Simple (Root Directory)** ⭐ Recommended
- Put `nyc_risk_map.html` in the root directory
- Access at: `https://yourusername.github.io/repo-name/nyc_risk_map.html`

**Option B: Docs Folder**
- Put files in `docs/` folder
- Access at: `https://yourusername.github.io/repo-name/docs/nyc_risk_map.html`

**Option C: Dedicated Pages Branch**
- Create a `gh-pages` branch
- Put files there
- More complex but cleaner

---

## Recommended: Create an Index Page

Create a nice landing page that links to your maps:

### Create `index.html` in root or `docs/`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>H5N1 Risk Mapping - Bellevue Hospital</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .map-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .map-card h2 {
            color: #27ae60;
            margin-top: 0;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 10px;
            transition: background-color 0.3s;
        }
        .btn:hover {
            background-color: #2980b9;
        }
        .info {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>H5N1 Risk Mapping Dashboard</h1>
    <p><strong>Bellevue Hospital - Critical Care Unit</strong></p>
    
    <div class="info">
        <h3>About This Project</h3>
        <p>Interactive risk maps for H5N1 (Avian Influenza) outbreaks in NYC by zip code. 
        Risk scores combine population density, poultry susceptibility, water proximity, 
        healthcare capacity, and socioeconomic vulnerability.</p>
    </div>

    <div class="map-card">
        <h2>📊 Complete H5N1 Risk Map</h2>
        <p>Interactive map showing composite risk scores for all NYC zip codes. 
        Click on any zip code to see detailed risk information.</p>
        <a href="data/processed/nyc_risk_map.html" class="btn">View Interactive Map</a>
    </div>

    <div class="map-card">
        <h2>🐔 Poultry Susceptibility Map</h2>
        <p>Visualization of poultry susceptibility index from USGS data across NYC zip codes.</p>
        <a href="data/processed/poultry_susceptibility_map.html" class="btn">View Poultry Map</a>
    </div>

    <div class="map-card">
        <h2>📄 Documentation</h2>
        <ul>
            <li><a href="docs/RISK_METHODOLOGY.md">Risk Methodology</a></li>
            <li><a href="docs/RISK_FACTORS_EXPLAINED.md">Risk Factors Explained</a></li>
            <li><a href="docs/RISK_MAPPING_RESULTS.md">Mapping Results</a></li>
        </ul>
    </div>

    <div class="info">
        <h3>📝 Note</h3>
        <p>Maps require internet connection to load external libraries (Leaflet, etc.). 
        All geographic data is embedded in the HTML files.</p>
    </div>

    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d;">
        <p>Generated: 2025 | Bellevue Hospital H5N1 Risk Mapping Project</p>
    </footer>
</body>
</html>
```

---

## Step-by-Step Instructions

### 1. Create Index Page

I'll create an `index.html` file for you that links to your maps.

### 2. Update File Paths

If you put the index in the root, make sure the links point to:
- `data/processed/nyc_risk_map.html`
- `data/processed/poultry_susceptibility_map.html`

### 3. Commit and Push

```bash
git add index.html
git commit -m "Add GitHub Pages index page"
git push
```

### 4. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Select branch: `main`
3. Select folder: `/ (root)` or `/docs`
4. Click Save

### 5. Access Your Site

After a few minutes, your site will be available at:
```
https://yourusername.github.io/repo-name/
```

---

## File Structure Options

### Option A: Root Directory (Simplest)
```
repo/
├── index.html          ← Landing page
├── data/
│   └── processed/
│       ├── nyc_risk_map.html
│       └── poultry_susceptibility_map.html
└── docs/
    └── (documentation)
```

**GitHub Pages Source:** `/ (root)`

### Option B: Docs Folder
```
repo/
├── docs/
│   ├── index.html     ← Landing page
│   ├── nyc_risk_map.html
│   └── (other docs)
└── data/
    └── processed/
        └── (maps)
```

**GitHub Pages Source:** `/docs`

---

## Troubleshooting

### Maps don't load
- Check that file paths are correct (relative to index.html)
- Make sure HTML files are committed to the repository
- Check browser console for errors (F12)

### 404 errors
- Wait a few minutes after enabling Pages (takes time to deploy)
- Check that the branch and folder settings are correct
- Verify file names match exactly (case-sensitive)

### Large files
- GitHub Pages has a 1 GB repository limit
- Your HTML files (6-9 MB) are fine
- If you hit limits, consider using GitHub LFS

---

## Custom Domain (Optional)

If you have a custom domain:
1. Add a `CNAME` file with your domain name
2. Update DNS settings
3. GitHub will handle the rest

---

## Updating Maps

When you regenerate maps:
1. Update the HTML files
2. Commit and push
3. GitHub Pages will automatically update (may take a few minutes)

---

## Security Note

GitHub Pages sites are **public** by default. If your repository is private, you can still use GitHub Pages, but consider:
- Making the repository public, OR
- Using GitHub's private Pages feature (if available for your plan)

