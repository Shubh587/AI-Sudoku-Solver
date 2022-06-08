# Set base image (host OS)
FROM python:3.8

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /Sudoku_Solver

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install pip
#RUN apt-get install python3-pip

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .
COPY templates /Sudoku_Solver/templates
COPY static /Sudoku_Solver/static
COPY algorithm_revised.py .

# Specify the command to run on container start
CMD [ "python", "./app.py" ]