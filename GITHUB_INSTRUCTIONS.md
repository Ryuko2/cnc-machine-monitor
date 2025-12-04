# 🚀 GitHub Setup Instructions

This guide walks you through publishing your CNC Machine Monitor to GitHub.

## 📋 Before You Start

Make sure you have:
- [x] A GitHub account ([create one here](https://github.com/join))
- [x] Git installed on your computer
- [x] All project files downloaded to a folder

---

## 🎯 Quick Setup (5 Steps)

### Step 1: Prepare Your Project

**Windows:**
```cmd
cd path\to\cnc-machine-monitor
setup-git.bat
```

**Mac/Linux:**
```bash
cd path/to/cnc-machine-monitor
chmod +x setup-git.sh
./setup-git.sh
```

This script will:
- Initialize Git repository
- Add all files
- Create initial commit

### Step 2: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Fill in the details:
   ```
   Repository name: cnc-machine-monitor
   Description: 🏭 Real-time CNC machine monitoring dashboard
   Visibility: Public (or Private if you prefer)
   ```
3. **Important**: Do NOT check any boxes (README, .gitignore, license)
4. Click "Create repository"

### Step 3: Connect Local to GitHub

Copy the commands from the GitHub page that start with:
```bash
git remote add origin https://github.com/YOUR-USERNAME/cnc-machine-monitor.git
git branch -M main
git push -u origin main
```

**Or use this (replace YOUR-USERNAME):**
```bash
git remote add origin https://github.com/YOUR-USERNAME/cnc-machine-monitor.git
git push -u origin main
```

### Step 4: Configure Repository

1. **Add Topics** (Settings → About → Topics):
   - cnc
   - manufacturing  
   - iot
   - monitoring
   - fastapi
   - websocket
   - python
   - dashboard
   - real-time
   - industrial

2. **Update Description**:
   > 🏭 Real-time CNC machine monitoring dashboard with WebSocket support, historical data logging, and mobile-responsive interface

3. **Add Website** (if deployed):
   - Add your deployment URL

### Step 5: Update README

Edit `README.md` and replace:
- `yourusername` → Your actual GitHub username
- Update contact information
- Add any custom details about your setup

---

## 📝 Manual Setup (Alternative)

If the scripts don't work, follow these steps:

### Initialize Git
```bash
cd cnc-machine-monitor
git init
git branch -M main
```

### Add Files
```bash
git add .
```

### Create Commit
```bash
git commit -m "Initial commit: CNC Machine Monitor v1.0.0"
```

### Push to GitHub
```bash
git remote add origin https://github.com/YOUR-USERNAME/cnc-machine-monitor.git
git push -u origin main
```

---

## 🎨 Making Your Repository Look Professional

### 1. Add a Social Preview Image

1. Take a screenshot of your dashboard (1280x640px recommended)
2. Go to: Settings → Options → Social preview
3. Upload your image

### 2. Create a Great README

Your README should include:
- ✅ Project description
- ✅ Features list
- ✅ Screenshots/GIF demo
- ✅ Installation instructions
- ✅ Usage examples
- ✅ Contributing guidelines
- ✅ License information

(Already included in your README.md!)

### 3. Add Badges

Add these to the top of README.md:
```markdown
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
```

### 4. Enable GitHub Features

- **Issues**: For bug reports and feature requests
- **Discussions**: For community questions
- **Wiki**: For extended documentation
- **Projects**: For roadmap tracking

---

## 📦 What's Included

Your repository contains:

```
cnc-machine-monitor/
├── .github/                    # GitHub configuration
│   ├── workflows/             # CI/CD actions
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── backend/                    # Python backend
│   ├── api.py                 # FastAPI server
│   └── haas_machine.py        # Machine simulation
├── frontend/                   # Web interface
│   └── index.html             # Dashboard
├── .gitignore                 # Git ignore rules
├── API_DOCUMENTATION.md       # API reference
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guide
├── DEPLOYMENT.md              # Deployment guide
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── INSTALLATION.md            # Installation guide
├── LICENSE                    # MIT License
├── QUICKSTART.md              # Quick start guide
├── README.md                  # Main documentation
├── requirements.txt           # Python dependencies
├── setup-git.sh               # Git setup (Unix)
├── setup-git.bat              # Git setup (Windows)
├── start.sh                   # Start script (Unix)
└── start.bat                  # Start script (Windows)
```

---

## 🔄 Keeping Your Repository Updated

### Making Changes

```bash
# Make your changes to files
git add .
git commit -m "Description of changes"
git push
```

### Creating Releases

1. Go to: Releases → Draft a new release
2. Create tag: v1.0.0
3. Release title: "CNC Monitor v1.0.0"
4. Describe changes
5. Publish release

### Version Numbering

Follow Semantic Versioning:
- **Major** (1.0.0): Breaking changes
- **Minor** (1.1.0): New features, backwards compatible
- **Patch** (1.0.1): Bug fixes

---

## 👥 Collaboration Features

### Branch Protection

Protect your main branch:
1. Settings → Branches → Add rule
2. Branch pattern: `main`
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
4. Save changes

### Pull Request Workflow

Contributors can:
1. Fork your repository
2. Create feature branch
3. Make changes
4. Submit pull request
5. You review and merge

### Issues and Labels

Create labels for:
- `bug` - Something isn't working
- `enhancement` - New feature request
- `documentation` - Documentation improvements
- `help wanted` - Extra attention needed
- `good first issue` - Good for newcomers

---

## 🌟 Promote Your Project

### 1. Write a Blog Post
Share your project story on:
- Dev.to
- Medium
- Your personal blog

### 2. Share on Social Media
- Twitter/X with #CNC #IoT #Manufacturing
- LinkedIn with manufacturing groups
- Reddit (r/CNC, r/programming)

### 3. Product Hunt
Launch on Product Hunt for visibility

### 4. List on Awesome Lists
Add to relevant awesome lists:
- Awesome Python
- Awesome FastAPI
- Awesome IoT

---

## ❓ Troubleshooting

### "Permission denied (publickey)"
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR-USERNAME/cnc-machine-monitor.git
```

### "Repository not found"
- Check URL is correct
- Ensure you're logged in to GitHub
- Verify repository was created

### "Updates were rejected"
```bash
# Pull latest changes first
git pull origin main --rebase
git push
```

### Large Files Error
If you have large files:
```bash
# Remove from git
git rm --cached large_file.db
# Add to .gitignore
echo "*.db" >> .gitignore
git commit -m "Remove database files"
```

---

## 📚 Next Steps

After publishing:

1. ✅ Add a screenshot to README
2. ✅ Create first release (v1.0.0)
3. ✅ Set up GitHub Actions (already included)
4. ✅ Enable GitHub Pages for docs (optional)
5. ✅ Share with the community
6. ✅ Start accepting contributions

---

## 🆘 Need Help?

- 📖 [GitHub Documentation](https://docs.github.com)
- 💬 [GitHub Community](https://github.community)
- 📧 [Contact GitHub Support](https://support.github.com)

---

## 🎉 Congratulations!

Your CNC Machine Monitor is now on GitHub and ready to share with the world!

Remember to:
- Keep your code clean
- Write meaningful commit messages
- Respond to issues and PRs
- Keep documentation updated
- Have fun and build something awesome!

---

**Made with ❤️ for the manufacturing community**
