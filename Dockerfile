# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /Sudoku_Solver

# Get packages for requirements.txt
RUN apk add --no-cache --update \
    python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev \
    libpq postgresql-dev 

RUN pip install --upgrade cython

RUN pip install --upgrade pip

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .
COPY templates /Sudoku_Solver/templates
COPY static /Sudoku_Solver/static
COPY algorithm_revised.py .

# Specify the command to run on container start
CMD [ "python", "./app.py" ]