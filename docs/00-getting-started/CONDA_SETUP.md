# Conda Environment Setup Guide

**Project:** Customer Database System  
**Last Updated:** February 15, 2026  
**Environment Manager:** Conda (not venv)

---

## 🎯 Important: This Project Uses Conda

**⚠️ For AI Agents & Developers:** This project uses **Conda** for environment management, NOT Python venv.

- ✅ **Use:** `conda activate cds`
- ❌ **Don't use:** `python -m venv .venv` or `source .venv/bin/activate`

---

## 📦 What is Conda?

Conda is a powerful package and environment manager that:
- Manages Python versions and packages
- Handles non-Python dependencies (system libraries)
- Works across platforms (Windows, macOS, Linux)
- Provides better dependency resolution than pip

---

## 🚀 Quick Setup

### Method 1: Automatic Setup Script (Recommended)

```bash
cd /home/seanghortborn/projects/customer-database
./setup-conda.sh
```

This script will:
- Check if conda is installed
- Create the 'cds' environment if it doesn't exist
- Show you how to activate it
- (Optional) Explain direnv setup for auto-activation

### Method 2: Manual Setup

```bash
# If conda is already installed:
conda env create -f environment.yml
conda activate cds
```

---

## 🔄 Automatic Activation with direnv

For **automatic environment activation** when you `cd` into the project:

### 1. Install direnv

**Ubuntu/Debian:**
```bash
sudo apt install direnv
```

**macOS:**
```bash
brew install direnv
```

### 2. Add to Your Shell

**For Bash** (~/.bashrc):
```bash
eval "$(direnv hook bash)"
```

**For Zsh** (~/.zshrc):
```bash
eval "$(direnv hook zsh)"
```

Reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

### 3. Configure conda Support for direnv

Create `~/.config/direnv/direnvrc` with conda layout support:

```bash
mkdir -p ~/.config/direnv
cat > ~/.config/direnv/direnvrc << 'EOF'
# Conda layout for direnv
layout_conda() {
    local CONDA_DEFAULT_ENV="${1:-base}"
    local CONDA_HOME="${HOME}/anaconda3"  # or ~/miniconda3
    
    # Source conda initialization
    if [ -f "${CONDA_HOME}/etc/profile.d/conda.sh" ]; then
        source "${CONDA_HOME}/etc/profile.d/conda.sh"
    else
        echo "Error: Could not find conda at ${CONDA_HOME}"
        return 1
    fi
    
    # Activate the conda environment
    conda activate "$CONDA_DEFAULT_ENV"
    
    if [ $? -eq 0 ]; then
        export CONDA_DEFAULT_ENV="$CONDA_DEFAULT_ENV"
        export CONDA_PREFIX="$(conda info --base)/envs/$CONDA_DEFAULT_ENV"
        PATH_add "$CONDA_PREFIX/bin"
    fi
}
EOF
```

**Note:** Adjust `CONDA_HOME` if your conda installation is in a different location (e.g., `~/miniconda3`).

### 4. Allow direnv in This Project

```bash
cd /home/seanghortborn/projects/customer-database
direnv allow .
```

You should see: `direnv: loading ~/projects/customer-database/.envrc`

**That's it!** Now the conda environment will activate automatically whenever you enter this directory.

---

## 📋 Daily Usage

### With direnv (Automatic)
```bash
cd /home/seanghortborn/projects/customer-database
# Environment automatically activates! 🎉
```

### Without direnv (Manual)
```bash
cd /home/seanghortborn/projects/customer-database
conda activate cds
```

### Verify Active Environment
```bash
conda info --envs
# The active environment will have an asterisk (*) next to it
```

---

## 🔧 Environment Management

### View Environment Details
```bash
conda list                      # List all packages
conda env export > environment.yml   # Export current state
```

### Update Environment
```bash
# After changing environment.yml:
conda env update -f environment.yml --prune
```

### Add New Packages
```bash
conda activate cds
conda install package-name
# or
pip install package-name

# Then export:
conda env export > environment.yml
```

### Remove Environment (if needed)
```bash
conda deactivate
conda env remove -n cds
```

### Recreate Environment
```bash
conda env create -f environment.yml
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `environment.yml` | Conda environment specification |
| `.envrc` | direnv configuration for auto-activation |
| `setup-conda.sh` | Automated setup script |

---

## 🤖 For AI Agents

When working on this project:

1. **Always check for conda environment first:**
   ```bash
   conda env list | grep cds
   ```

2. **Activate before any Python operations:**
   ```bash
   conda activate cds
   ```

3. **Never suggest creating a venv:**
   - ❌ Don't: `python -m venv .venv`
   - ✅ Do: `conda activate cds`

4. **When adding dependencies:**
   - Prefer conda: `conda install package-name`
   - If not available in conda: `pip install package-name`
   - Always update: `conda env export > environment.yml`

5. **Include activation in scripts:**
   ```bash
   #!/bin/bash
   conda activate cds
   python script.py
   ```

---

## 👥 For New Team Members

### First-Time Setup

1. **Install Conda** (if not installed):
   - Download Miniconda: https://docs.conda.io/en/latest/miniconda.html
   - Or Anaconda: https://www.anaconda.com/download

2. **Clone the repository:**
   ```bash
   git clone https://github.com/SeanghortBorn/customer-database.git
   cd customer-database
   ```

3. **Run setup script:**
   ```bash
   ./setup-conda.sh
   ```

4. **Activate environment:**
   ```bash
   conda activate cds
   ```

5. **(Optional) Setup direnv for auto-activation** - Follow instructions in setup-conda.sh output

---

## ❓ FAQ

### Why Conda instead of venv?

- ✅ Conda manages Python versions (venv doesn't)
- ✅ Conda handles system dependencies
- ✅ Better for data science/ML projects
- ✅ Cross-platform compatibility
- ✅ Faster dependency resolution

### Can I still use pip?

Yes! While in the conda environment:
```bash
conda activate cds
pip install package-name
```

Just remember to export the environment afterward:
```bash
conda env export > environment.yml
```

### What if I don't have conda?

Install Miniconda (lightweight, recommended):
```bash
# Linux:
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Follow the prompts, then:
source ~/.bashrc
```

### How do I know if conda is activated?

Your terminal prompt will show `(cds)` at the beginning:
```
(cds) user@computer:~/projects/customer-database$
```

### direnv is not activating automatically?

Make sure you:
1. Installed direnv
2. Added the hook to your shell rc file
3. Reloaded your shell: `source ~/.bashrc`
4. Allowed this directory: `direnv allow .`

---

## 🔗 Related Documentation

- [Quick Start Guide](./QUICK_START.md) - Full setup with conda
- [Project Standards](../PROJECT_STANDARDS.md) - Organization guidelines
- [Action Plan](./ACTION_PLAN.md) - Week-by-week development guide

---

## 🆘 Troubleshooting

### "conda: command not found"

**Solution:** Conda is not installed or not in PATH
```bash
# Add to ~/.bashrc:
export PATH="$HOME/miniconda3/bin:$PATH"
source ~/.bashrc
```

### "Environment 'cds' does not exist"

**Solution:** Create it from environment.yml
```bash
conda env create -f environment.yml
```

### direnv says "blocked"

**Solution:** Allow the .envrc file
```bash
direnv allow .
```

### Packages not found in conda

**Solution:** Use pip for packages not in conda channels
```bash
conda activate cds
pip install package-name
conda env export > environment.yml
```

---

**Remember: Always activate the conda environment before working on this project!**

```bash
conda activate cds  # Your new best friend 🚀
```
