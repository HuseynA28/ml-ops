FROM centos:7

RUN yum -y update && yum clean all

RUN yum -y install openssh-server  python3 sudo

RUN adduser -m prod_user && \
    echo "Ankara06" | passwd prod_user --stdin && \
    usermod -aG wheel prod_user && \
    mkdir /home/prod_user/.ssh && \
    chown prod_user:prod_user -R  /home/prod_user/ && \
    chmod 700 /home/prod_user/.ssh

RUN     echo "%wheel         ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

RUN systemctl enable sshd.service

VOLUME [ "/sys/fs/cgroup" ]

ENTRYPOINT ["/usr/sbin/init"]