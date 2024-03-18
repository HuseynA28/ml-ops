FROM centos:7

RUN yum -y update && yum clean all

RUN yum -y install openssh-server  python3 sudo

RUN adduser -m test_user && \
    echo "Ankara06" | passwd test_user --stdin && \
    usermod -aG wheel test_user && \
    mkdir /home/test_user/.ssh && \
    chown test_user:test_user -R  /home/test_user/ && \
    chmod 700 /home/test_user/.ssh

RUN     echo "%wheel         ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

RUN systemctl enable sshd.service

VOLUME [ "/sys/fs/cgroup" ]

ENTRYPOINT ["/usr/sbin/init"]