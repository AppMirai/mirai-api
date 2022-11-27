# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /code

# Set the working directory to /music_service
WORKDIR /code

# Copy the current directory contents into the container at /music_service
ADD . /code

# Install any needed packages specified in requirements.txt
RUN apt-get -y update
RUN apt-get -y install cmake
RUN apt-get -y install libopenblas-dev liblapack-dev
RUN apt-get -y install ffmpeg libsm6 libxext6 
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["makemigrations"]
CMD ["migrate"]
CMD ["runserver", "0.0.0.0:8000", "--noreload"]
