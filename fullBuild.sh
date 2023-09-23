#!/bin/bash
cd catBlog
make
# cd ../evilBlog
# make
# cd ../trustedIntermediary
# make
# cd ..
exec /usr/sbin/sshd -D
