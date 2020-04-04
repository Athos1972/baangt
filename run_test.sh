echo "Running tests"
coverage run -m pytest
echo "Building coverage"
coverage html
echo "HTML Coverage: ${PWD}/htmlcov/index.html"