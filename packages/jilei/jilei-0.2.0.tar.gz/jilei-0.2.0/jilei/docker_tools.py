import docker


client = docker.from_env()


class JLDocker():
    def __init__(self, env_file=None):
        if not env_file:
            self.client = docker.from_env()

    def _fit_in_line(self, line, length):
        diff = length - len(line)
        if diff < 0:
            return line[:length]
        else:
            return line + " "*diff

    def list(self, all=True):

        def _command(cmd, entrypoints):
            cmd = cmd if cmd else []
            entrypoints = entrypoints if entrypoints else []
            return " ".join(cmd + entrypoints)

        def _ports(ports):
            line = ""
            for k,v in ports.items():
                if not v:
                    line = line + ", " + k
                else:
                    line = line + ", " + v[0]['HostIp']+":" + v[0]['HostPort'] + "->" + k
            return line[2:]

        #for c in self.client.containers.list(all=all):
        #    print(c.attrs['NetworkSettings']['Networks'])

        NetworkName = 'bridge'
        return [[
                c.name,
                c.image.tags[0],
                c.status,
                _command(c.attrs['Config']['Cmd'], c.attrs['Config']['Entrypoint']),
                _ports(c.ports),
                c.attrs['NetworkSettings']['Networks'][NetworkName]['IPAddress']

            ]
            for c in self.client.containers.list(all=all)
        ]

    def ps(self, all=True):
        containers = self.list(all=all)
        space = lambda n : " "*n
        SPLIT = 7

        line = "-"*160
        header = "|  " + "name" + space(16-4-2) \
                +"|  " + "image" + space(16-5-2) \
                +"|  " + "ip address" + space(16-10-2) \
                +"|  " + "status" + space(10-6-2) \
                +"|  " + "command" + space(42-7-2) \
                +"|  " + "ports" + space(60-5-2-SPLIT) \
                +"|"

        print(line)
        print(header)
        print(line)
        for c in containers:
            name = "  " + self._fit_in_line(c[0], 12) + "  "
            image = "  " + self._fit_in_line(c[1], 12) + "  "
            ip = "  " + self._fit_in_line(c[5], 12) + "  "
            status = "  " + self._fit_in_line(c[2], 6) + "  "
            status = "\033[1;32m{}\033[0m".format(status) if "runnin" in status else status
            cmd = "  " + self._fit_in_line(c[3], 38) + "  "
            ports = "  " + self._fit_in_line(c[4], 50) + " "
            print(f"|{name}|{image}|{ip}|{status}|{cmd}|{ports}|")

        print(line)


if __name__ == "__main__":
    dock = JLDocker()
    dock.ps()
