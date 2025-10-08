# GitHub Setup Guide

## Steps to Connect Your Project to GitHub

### 1. Create a New Repository on GitHub

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `instruction-detection-tabnet` (or your preferred name)
   - **Description**: "Instruction detection system using TabNet deep learning architecture"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### 2. Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands in your terminal:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/instruction-detection-tabnet.git

# Verify the remote was added
git remote -v

# Push your code to GitHub
git branch -M main
git push -u origin main
```

### 3. Alternative: Using SSH (Recommended for frequent pushes)

If you have SSH keys set up:

```bash
git remote add origin git@github.com:YOUR_USERNAME/instruction-detection-tabnet.git
git branch -M main
git push -u origin main
```

### 4. Set Up SSH Keys (If Not Already Done)

If you don't have SSH keys configured:

```bash
# Generate a new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start the ssh-agent
eval "$(ssh-agent -s)"

# Add your SSH key to the ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copy the SSH key to clipboard (Windows)
clip < ~/.ssh/id_ed25519.pub

# Or display it to copy manually
cat ~/.ssh/id_ed25519.pub
```

Then:
1. Go to GitHub → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your key and save

### 5. Future Updates

After the initial setup, to push changes:

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push
```

### 6. Useful Git Commands

```bash
# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull

# View differences
git diff

# Undo changes (before commit)
git checkout -- filename

# View remote repositories
git remote -v
```

## Current Repository Status

✅ Git repository initialized
✅ Initial commit created
✅ All project files added

**Next step**: Create the GitHub repository and run the connection commands above!

## Project Structure on GitHub

Your repository will include:
- Source code (`src/`)
- Dataset (`data/raw/`)
- Trained model (`models/`)
- Documentation (`README.md`)
- Configuration files
- Jupyter notebooks
- Streamlit web app

## Recommended .gitignore Additions

The `.gitignore` file is already configured to exclude:
- Python cache files
- Virtual environment
- IDE settings
- Temporary files
- Log files

If you want to exclude the trained model from GitHub (to save space), uncomment this line in `.gitignore`:
```
# models/*.zip
```

## Collaboration Tips

If working with others:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/instruction-detection-tabnet.git
   cd instruction-detection-tabnet
   ```

2. **Set up environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Train the model**:
   ```bash
   python src/train.py
   ```

## GitHub Repository Settings Recommendations

After pushing to GitHub:

1. **Add Topics**: Add relevant tags like `tabnet`, `deep-learning`, `nlp`, `instruction-detection`, `pytorch`
2. **Enable Issues**: For bug tracking and feature requests
3. **Add Description**: Brief description of the project
4. **Add Website**: Link to deployed Streamlit app (if hosted)
5. **Create Releases**: Tag versions when you reach milestones

## License

Consider adding a license file. Common choices:
- MIT License (permissive)
- Apache 2.0 (permissive with patent grant)
- GPL-3.0 (copyleft)

You can add a license through GitHub's interface when creating the repository or later through Settings.
