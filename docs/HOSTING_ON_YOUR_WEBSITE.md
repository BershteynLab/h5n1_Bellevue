# Hosting Maps on Your Own Website

Since your GitHub repository is private, you can't use free GitHub Pages. But the good news is: **the HTML files are completely self-contained** and will work on any web server!

## ✅ What You Need

**Just the HTML file!** That's it.

The HTML files (`nyc_risk_map.html` and `poultry_susceptibility_map.html`) are **self-contained**:
- ✅ All geographic data is embedded in the HTML
- ✅ All zip code boundaries are embedded
- ✅ All risk scores are embedded
- ✅ Only external dependencies are CDN libraries (Leaflet, jQuery, etc.) loaded from the internet

## 📤 How to Host

### Option 1: Upload Just the HTML File (Simplest) ⭐

1. **Upload the HTML file** to your web server:
   ```
   nyc_risk_map.html → your-website.com/maps/nyc_risk_map.html
   ```

2. **That's it!** The map will work immediately.

3. **Access it at:**
   ```
   https://your-website.com/maps/nyc_risk_map.html
   ```

**No other files needed!** The HTML file is completely standalone.

---

### Option 2: Create a Landing Page

If you want a nice landing page (like the `index.html` I created), you can:

1. **Upload both files:**
   - `index.html` (landing page)
   - `nyc_risk_map.html` (the map)

2. **Update the link in `index.html`** to point to where you put the map:
   ```html
   <!-- Change this line in index.html -->
   <a href="nyc_risk_map.html" class="btn">View Interactive Map</a>
   <!-- Or use full path: -->
   <a href="/maps/nyc_risk_map.html" class="btn">View Interactive Map</a>
   ```

---

## 🔍 What the HTML Files Need

The HTML files only need:
- ✅ **Internet connection** (to load external libraries from CDNs):
  - Leaflet (map library)
  - jQuery
  - Bootstrap
  - Font Awesome

These are loaded from public CDNs (jsdelivr, cdnjs, etc.), so as long as your website visitors have internet, it will work.

---

## 📁 File Structure Options

### Minimal (Just the Map)
```
your-website.com/
└── maps/
    └── nyc_risk_map.html  ← Just this file!
```

### With Landing Page
```
your-website.com/
├── index.html              ← Landing page (optional)
└── maps/
    ├── nyc_risk_map.html
    └── poultry_susceptibility_map.html
```

### With Documentation (If You Want)
```
your-website.com/
├── index.html
├── maps/
│   ├── nyc_risk_map.html
│   └── poultry_susceptibility_map.html
└── docs/
    ├── RISK_METHODOLOGY.md
    └── (other docs)
```

**Note:** Markdown files won't render as HTML on a regular web server - you'd need to convert them or use a static site generator.

---

## 🚀 Upload Instructions

### Via FTP/SFTP:
1. Connect to your web server
2. Navigate to your public HTML directory (usually `public_html/`, `www/`, or `html/`)
3. Upload `nyc_risk_map.html`
4. Done!

### Via cPanel/Web Interface:
1. Log into your hosting control panel
2. Use File Manager
3. Navigate to public directory
4. Upload the HTML file
5. Done!

### Via Command Line (SSH):
```bash
# Copy file to server
scp data/processed/nyc_risk_map.html user@your-server.com:/var/www/html/maps/

# Or if you have SSH access
ssh user@your-server.com
cd /var/www/html/maps/
# Then upload via your preferred method
```

---

## ✅ Testing

After uploading:

1. **Visit the URL** in your browser:
   ```
   https://your-website.com/maps/nyc_risk_map.html
   ```

2. **Check that:**
   - Map loads (may take a few seconds for libraries to load)
   - You can zoom and pan
   - Clicking zip codes shows popups
   - Colors display correctly

3. **If it doesn't work:**
   - Check browser console (F12 → Console) for errors
   - Verify file permissions (should be readable: `chmod 644`)
   - Check that your web server serves `.html` files correctly

---

## 🔒 Security Considerations

Since the HTML files contain all data embedded:
- ✅ No database needed
- ✅ No server-side processing needed
- ✅ Works on any static web hosting
- ⚠️ All data is visible in the HTML source (if that's a concern)

If you need to keep data private, you'd need to:
- Use server-side authentication
- Or host on a password-protected area
- Or use a different approach

---

## 📊 File Sizes

- `nyc_risk_map.html`: **6.7 MB** (all data embedded)
- `poultry_susceptibility_map.html`: **9.5 MB** (all data embedded)

These are fine for web hosting - most servers allow files up to 100+ MB.

---

## 💡 Pro Tips

1. **Compression:** Enable gzip compression on your server to reduce load times
2. **CDN:** Consider using a CDN for faster library loading
3. **Caching:** Set appropriate cache headers for the HTML file
4. **HTTPS:** Use HTTPS for security (most modern sites do this automatically)

---

## 🆘 Troubleshooting

### Map doesn't load
- Check browser console for errors
- Verify internet connection (needed for CDN libraries)
- Check file permissions on server

### Blank map
- Wait a few seconds (libraries need to load)
- Check browser console for JavaScript errors
- Try a different browser

### 404 error
- Verify the file path is correct
- Check file permissions
- Make sure the file is in the public directory

---

## Summary

**Bottom line:** Just upload the HTML file(s) to your web server. No other files needed. The maps are completely self-contained and will work on any web server that can serve HTML files.

