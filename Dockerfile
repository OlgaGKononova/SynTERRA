# Use an official Python runtime as a parent image
FROM python:3.8.9
# Set the working directory
WORKDIR /imasyndata

RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install libgl1-mesa-glx -y
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install gunicorn

# Copy the current directory contents into the container
COPY . /imasyndata
RUN pip3 install -r requirements.txt -e .

#CMD gunicorn app:server -b :8052 --error-logfile=errors.log