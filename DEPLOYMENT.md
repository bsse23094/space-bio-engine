# Deployment Guide

## Frontend Deployment (GitHub Pages)

### Quick Deployment

1. **Build the production bundle:**
```bash
cd Frontend
npm run deploy
```

2. **Deploy to GitHub Pages:**
```bash
# Install gh-pages if not already installed
npm install -g angular-cli-ghpages

# Deploy
npx angular-cli-ghpages --dir=dist/frontend/browser --no-silent
```

3. **Enable GitHub Pages in Repository Settings:**
   - Go to repository Settings > Pages
   - Source: Deploy from `gh-pages` branch
   - Save

4. **Access your site:**
   - URL: `https://bsse23094.github.io/space-bio-engine`

### Manual Deployment

If you prefer manual deployment:

```bash
# Build
cd Frontend
npm run deploy

# The output will be in dist/frontend/browser
# Push this to gh-pages branch manually
```

## Backend Deployment (Render.com)

### Step-by-Step Guide

1. **Create account on [Render.com](https://render.com)** (Free tier available)

2. **Connect your GitHub repository**

3. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your `space-bio-engine` repository
   - Configure:

```yaml
Name: space-bio-backend
Environment: Python 3
Root Directory: Backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

4. **Environment Variables:**
   - Add if needed (Render auto-assigns PORT)

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes for first deploy)

6. **Get your backend URL:**
   - Example: `https://space-bio-backend.onrender.com`

7. **Update Frontend API URL:**
   
Edit `Frontend/src/environments/environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  apiBase: 'https://space-bio-backend.onrender.com/api/v1'
};
```

8. **Rebuild and redeploy frontend:**
```bash
cd Frontend
npm run deploy
npx angular-cli-ghpages --dir=dist/frontend/browser
```

### Alternative: Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy from Backend directory
cd Backend
railway init
railway up

# Get deployment URL
railway open
```

## CORS Configuration

Ensure backend allows your frontend domain:

**File: `Backend/app/main.py`**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bsse23094.github.io",  # Production
        "http://localhost:4200",         # Development
        "http://localhost:8000"          # Local backend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Verify Deployment

### Frontend
- Visit: `https://bsse23094.github.io/space-bio-engine`
- Check browser console for errors
- Test navigation between pages

### Backend
- Visit: `https://your-backend.onrender.com/docs`
- Check API documentation loads
- Test an endpoint (e.g., `/health` or `/api/v1/articles`)

### Integration
- Open frontend
- Try searching for articles
- Check dashboard loads statistics
- Verify charts render correctly

## Troubleshooting

### Frontend Issues

**404 on page refresh:**
- Ensure `base-href` is set correctly
- GitHub Pages needs a 404.html that redirects to index.html

**API calls failing:**
- Check CORS configuration in backend
- Verify API URL in `environment.prod.ts`
- Check browser console for CORS errors

### Backend Issues

**Free tier sleep:**
- Render.com free tier sleeps after 15 mins of inactivity
- First request after sleep takes 30-60 seconds

**Build failures:**
- Check Python version (3.13 required)
- Verify requirements.txt has all dependencies
- Check Render logs for specific errors

**Memory issues:**
- Free tier has 512MB RAM limit
- Optimize data loading if needed
- Consider caching strategies

## Continuous Deployment

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: |
          cd Frontend
          npm ci
          
      - name: Build
        run: |
          cd Frontend
          npm run deploy
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./Frontend/dist/frontend/browser
```

This will automatically deploy your frontend whenever you push to main branch.

## Cost Estimate

- **GitHub Pages**: Free (public repositories)
- **Render.com Free Tier**: 
  - 750 hours/month
  - Sleeps after 15 mins inactivity
  - 512 MB RAM
  - Good for demo/development

- **Railway.app Free Tier**:
  - $5 credit/month
  - No sleep
  - 512 MB RAM
  - Better for active development

Both are sufficient for demo purposes!
