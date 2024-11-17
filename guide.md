<!-- Initialization of the virtual env  -->
python -m venv venv
<!-- Activation of the virtual env -->
venv/Scripts/activate
<!-- Deactivation of the virtual env -->
venv/Scripts/deactivate
<!-- Updating of dependencies to the requirements file -->
pip freeze > requirements.txt
<!-- Installation of the dependencies -->
pip install -r requirements.txt 