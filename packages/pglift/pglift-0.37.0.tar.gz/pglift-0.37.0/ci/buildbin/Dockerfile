FROM rockylinux:8
RUN dnf install -y cargo rust make autoconf git libpq python39-pip \
    && dnf clean all \
    && rm -rf /var/cache/yum

RUN pip3 install tox
RUN useradd --uid 5432 --create-home runner
USER runner
WORKDIR /home/runner
