import matplotlib.pyplot as plt
from interpreter.parser import CogentParser
from interpreter.resource_profiler import profile_parse
import glob
import os

# Find all .cg files in examples/ or use a default
cg_files = glob.glob("examples/*.cg")
if not cg_files:
    cg_files = [None]

results = []
labels = []

for f in cg_files:
    if f:
        with open(f) as file:
            code = file.read()
        label = os.path.basename(f)
    else:
        code = '''module Example { goal: "Profile test" inputs: [x: Int] process: ["Step"] }'''
        label = "default"
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    res = profile_parse(parser, code)
    results.append(res)
    labels.append(label)

# Plot
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.bar(labels, [r.elapsed_sec for r in results], color='b', alpha=0.6, label='Time (s)')
ax2.plot(labels, [r.peak_mem_bytes/1024 for r in results], 'ro-', label='Peak Mem (KB)')

ax1.set_xlabel('File')
ax1.set_ylabel('Parse Time (s)', color='b')
ax2.set_ylabel('Peak Memory (KB)', color='r')
plt.title('Cogent Parser Performance')
fig.tight_layout()
plt.savefig('parse_profile.png')
plt.show()
