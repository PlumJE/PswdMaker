# Use the official Buildozer base image
FROM kivy/buildozer:latest

# Set the working directory inside the container
WORKDIR /home/user/app

# Copy the project files into the container
COPY . /home/user/app

# Run Buildozer directly when the container starts
ENTRYPOINT ["buildozer"]
CMD ["-v", "android", "debug"]
