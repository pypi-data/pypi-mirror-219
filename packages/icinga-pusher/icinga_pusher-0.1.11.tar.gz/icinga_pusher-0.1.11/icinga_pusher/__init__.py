import os
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

ICINGA_DRY_RUN = "ICINGA_DRY_RUN"

requests.packages.urllib3.disable_warnings()


class IcingaService(object):

    def __init__(self, icinga, mon_host, service):
        self.icinga = icinga
        self.mon_host = mon_host
        self.service = service

    def push_state(self, exit_status: int, plugin_output: str, performance_data: Optional[list] = None):

        if ICINGA_DRY_RUN in os.environ:
            logger.debug("Env ICINGA_DRY_RUN is set. Not pushing Icinga state")
            return

        if type(exit_status) != int:
            raise TypeError(f"exit_status must be an int ({exit_status=})")

        headers = {
            "Accept": "application/json",
        }

        data = {
            "exit_status": exit_status,
            "filter": f'host.name=="{self.mon_host}" && service.name=="{self.service}"',
            "type": "Service",
            "plugin_output": plugin_output,
        }

        if performance_data:
            if type(performance_data) != list:
                raise TypeError(f"performance_data must be an int ({performance_data=})")
            data.update({"performance_data": performance_data})

        # https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#process-check-result
        try:
            resp = requests.post(f"{self.icinga.hostname}:5665/v1/actions/process-check-result",
                                 json=data,
                                 headers=headers,
                                 verify=self.icinga.ssl_verify,
                                 auth=(self.icinga.username, self.icinga.password))
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Could not set Icinga status of service {self.service}. {e}")
            if isinstance(e, requests.exceptions.HTTPError):
                logger.error(f"Response: {e.response.text}")
        else:
            logger.info(f"Sucessfully set Icinga status for service {self.service}")


class Icinga(object):
    CHECK_OK = 0
    CHECK_WARNING = 1
    CHECK_CRITICAL = 2
    CHECK_UNKNOWN = 3

    def __init__(self, hostname: str, username: str, password: str, ssl_verify: bool = True) -> IcingaService:
        self.username = username
        self.password = password
        if not hostname.startswith("https://"):
            raise ValueError(f"Hostname must start with https {hostname=}")
        self.hostname = hostname
        self.ssl_verify = ssl_verify

    def service(self, hostname, service):
        return IcingaService(self, hostname, service)


if __name__ == '__main__':
    i = Icinga("https://icinga.example.com", "api-user", "api-password")
    service = i.service("monitored_host", "service-name")
    service.push_state(Icinga.CHECK_OK, "plugin_output - this check worked fine", ["performance_data=200", "c=d"])
    service.push_state(Icinga.CHECK_CRITICAL, "plugin_output - this check failed")
