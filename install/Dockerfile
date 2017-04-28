FROM ubuntu:16.04
RUN apt-get install python python-pip
RUN pip install python rake requests numpy beautifulsoup4 lxml Flask
RUN mkdir /root/.ssh/
ADD id_rsa /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
RUN git clone git@bitbucket.org:sindhuv/code_assist_python.git
WORKDIR "/code_assist_python/server"
EXPOSE 5000
CMD ["python", "app.py"]
