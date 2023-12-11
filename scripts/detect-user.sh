#! /bin/sh

set -e

PWD_UID=$(stat . -c "%u")
if command -v useradd > /dev/null; then
    USERADD="useradd -d ${HOME}"
    GROUPADD="groupadd"
else
    USERADD="adduser -D -H -h ${HOME}"
    GROUPADD="addgroup"
fi

if [ -S /var/run/docker.sock ]; then
    DOCKER_GID=$(stat /var/run/docker.sock -c "%g")
    if getent group ${DOCKER_GID} > /dev/null ; then
        USERADD="${USERADD} -G $(stat /var/run/docker.sock -c "%G")"
    else
        ${GROUPADD} -g ${DOCKER_GID} docker
        USERADD="${USERADD} -G docker"
    fi;
fi

if [ "$(id -u)" -ne "${PWD_UID}" ] ; then
  getent passwd ${PWD_UID} || ${USERADD} -u ${PWD_UID} enix
  PWD_UNAME=$(stat . -c "%U")
  if command -v sudo > /dev/null; then
    sudo -HEu ${PWD_UNAME} "$@"
  else
    exec su ${PWD_UNAME} "$@"
  fi;
else
  "$@"
fi
