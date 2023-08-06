import os

SPLIT = '+'+'-'*77+'+'


class JLSysInfo:

    def __init__(self):
        pass

    def nvidia_smi(self):
        lines = [SPLIT, '|' + '显卡信息'.center(73,' ')+'|', SPLIT]
        smi = os.popen('nvidia-smi 2>&1').read().split('\n')
        if len(smi) == 2:
            smi[0] = f'|  {smi[0][:75].ljust(75)}|'
            smi[1] = SPLIT
        else:
            smi = [line for line in smi if line.strip()][1:]

        return lines + smi

    def free_h(self):
        lines = [SPLIT, '|' + '系统内存'.center(73,' ')+'|', SPLIT]
        for line in os.popen("free -h").read()[5:].replace('：   ','：').replace('available', 'available ').split('\n'):
            if line.strip():
                if len(line) > 76:
                    line = line[0:76]
                lines.append('| ' + line.ljust(73, ' ')+ '|')

        lines.append(SPLIT)
        return lines

    def show(self, smi=True, mem=True):
        if smi:
            for l in self.nvidia_smi():
                print(l)
        if mem:
            for l in self.free_h():
                print(l)


if __name__ == "__main__":
    sysinfo = JLSysInfo()
    sysinfo.show()

