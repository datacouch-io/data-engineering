# Start from the official Spark image
FROM apache/spark:3.5.6-scala2.12-java11-r-ubuntu

# Switch to root to install Python
USER root

# Install Python3 and pip, and clean up
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to non-root user (Spark uses UID 185)
USER 185

# Set working directory
WORKDIR /opt

# Copy Spark config
COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf

# Copy your custom scripts (assume they are executable)
COPY common.sh /common.sh
COPY spark-master /spark-master
COPY spark-worker /spark-worker

# Optional: Copy the PySpark script directly into image
COPY sample.py /opt/spark/sample.py

# Add Spark bin to PATH
ENV PATH="$PATH:/opt/spark/bin"

# Default command
CMD ["/bin/bash"]
