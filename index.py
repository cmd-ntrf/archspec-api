from archspec.cpu.detect import compatible_microarchitectures
from flask import Flask, request

app = Flask(__name__)

@app.route('/<arch>', methods=['GET', 'POST'])
def host(arch):
    """Detects the host micro-architecture and returns it"""
    error = None
    if request.method == 'GET':
        return 'curl -X POST -H "Content-Type: text/plain" --data "$(cat /proc/cpuinfo)" https://archspec-api.vercel.app/$(uname -m)'
    if request.method == 'POST':
        info = {}
        lines = request.data.decode('utf-8').split('\n')
        for line in lines:
            key, separator, value = line.partition(":")
            if separator != ":" and info:
                break
            info[key.strip()] = value.strip()
        #import pdb; pdb.set_trace()
        candidates = compatible_microarchitectures(info, arch)
        target = sorted(
           candidates, key=lambda t: (len(t.ancestors), len(t.features)), reverse=True
        )[0]
        return str(target)

