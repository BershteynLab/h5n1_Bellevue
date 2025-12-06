#!/usr/bin/env python3
"""
Prepare risk map files for sharing.
Creates a shareable package with instructions.
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_shareable_package():
    """Create a zip file with the map and instructions."""
    
    # File paths
    map_file = 'data/processed/nyc_risk_map.html'
    static_map = 'data/processed/nyc_risk_map.png'
    output_dir = 'share'
    zip_name = f'h5n1_risk_map_{datetime.now().strftime("%Y%m%d")}.zip'
    
    # Check if map exists
    if not os.path.exists(map_file):
        print(f"ERROR: Map file not found: {map_file}")
        print("Please run: python src/example_risk_map_real_data.py")
        return
    
    # Create share directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy files
    print("Preparing files for sharing...")
    shutil.copy2(map_file, os.path.join(output_dir, 'nyc_risk_map.html'))
    print(f"  ✓ Copied interactive map")
    
    if os.path.exists(static_map):
        shutil.copy2(static_map, os.path.join(output_dir, 'nyc_risk_map.png'))
        print(f"  ✓ Copied static map")
    
    # Create README
    readme_content = """H5N1 Risk Map - Interactive Visualization
==========================================

INSTRUCTIONS FOR VIEWING:
-------------------------
1. Extract this zip file to any location on your computer
2. Open 'nyc_risk_map.html' in any web browser:
   - Double-click the file, OR
   - Right-click → Open With → Choose your browser
3. Make sure you have an internet connection (required for map libraries)
4. The interactive map will load automatically

INTERACTIVE FEATURES:
---------------------
- Click on any zip code to see detailed risk information
- Zoom in/out using mouse wheel or controls
- Pan by clicking and dragging
- Color coding shows risk levels:
  * Green/Yellow: Low to Medium risk
  * Orange: High risk
  * Red: Very High risk

REQUIREMENTS:
-------------
- Any modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for loading map libraries)
- No additional software needed

TROUBLESHOOTING:
-----------------
- If the map doesn't load:
  * Try a different web browser
  * Make sure you have internet connection
  * Check that pop-ups aren't blocked
  * Try refreshing the page (F5)

- If you see a blank page:
  * Wait a few seconds for libraries to load
  * Check browser console for errors (F12 → Console)
  * Try opening in a different browser

FILE INFORMATION:
------------------
- Interactive Map: nyc_risk_map.html (6.7 MB)
- Static Map: nyc_risk_map.png (if included)
- All geographic data is embedded in the HTML file
- No additional data files needed

CONTACT:
--------
For questions about the risk map or methodology, please refer to:
- docs/RISK_METHODOLOGY.md - Methodology documentation
- docs/RISK_FACTORS_EXPLAINED.md - Detailed factor explanations

Generated: {date}
""".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with open(os.path.join(output_dir, 'README.txt'), 'w') as f:
        f.write(readme_content)
    print(f"  ✓ Created README.txt")
    
    # Create zip file
    print(f"\nCreating zip file: {zip_name}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            zipf.write(file_path, file)
            print(f"  ✓ Added {file}")
    
    zip_size = os.path.getsize(zip_name) / (1024 * 1024)  # MB
    print(f"\n✓ Shareable package created: {zip_name}")
    print(f"  Size: {zip_size:.2f} MB")
    print(f"\nYou can now:")
    print(f"  1. Email this file (if under 25 MB)")
    print(f"  2. Upload to file sharing service (Dropbox, Google Drive, etc.)")
    print(f"  3. Share via USB drive or network")
    
    # Cleanup
    print(f"\nCleaning up temporary files...")
    shutil.rmtree(output_dir)
    print(f"✓ Done!")

if __name__ == '__main__':
    print("=" * 60)
    print("Preparing H5N1 Risk Map for Sharing")
    print("=" * 60)
    print()
    create_shareable_package()

