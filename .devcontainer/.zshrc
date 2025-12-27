# Enhanced Budget Pro Development Environment
export PS1="%F{cyan}[Budget Pro]%f %F{green}%~%f %# "

# Aliases
alias ll='ls -lah'
alias py='python'
alias pytest='python -m pytest'
alias analyze='python -m src.cli analyze'
alias batch='python -m src.cli batch'
alias web='python web_app.py'
alias ui='streamlit run ui_app.py'
alias test-integrations='python test_integrations.py'

# Quick commands
alias tests='pytest tests/ -v'
alias format='black src/ tests/'
alias lint='flake8 src/ tests/'
alias check='black --check src/ tests/ && flake8 src/ tests/'

# Project info
echo "Enhanced Budget Pro Dev Container"
echo "Python version: $(python --version)"
echo ""
echo "Quick commands:"
echo "  analyze --input <script> --out <dir>  - Analyze single script"
echo "  ui                                     - Launch Streamlit UI"
echo "  web                                    - Launch Flask web app"
echo "  tests                                  - Run test suite"
echo "  test-integrations                      - Test integrations"
echo ""
