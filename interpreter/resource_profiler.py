

"""
Resource Profiler

Implements resource profiling for Cogent interpreter: track and report resource usage (CPU, memory, time, etc.) for modules and processes.
"""

import time
import tracemalloc

class ParseProfileResult:
	def __init__(self, elapsed_sec, peak_mem_bytes):
		self.elapsed_sec = elapsed_sec
		self.peak_mem_bytes = peak_mem_bytes
	def __repr__(self):
		return f"ParseProfileResult(time={self.elapsed_sec:.6f}s, peak_mem={self.peak_mem_bytes/1024:.1f} KB)"

def profile_parse(parser, source_code):
	"""
	Profile the parsing of source_code using the given parser.
	Returns a ParseProfileResult with elapsed time and peak memory usage.
	"""
	tracemalloc.start()
	start = time.perf_counter()
	parser.parse_string(source_code)
	elapsed = time.perf_counter() - start
	_, peak = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	return ParseProfileResult(elapsed, peak)

# Example usage (for test or CLI):
# from interpreter.parser import CogentParser
# parser = CogentParser(grammar_path="grammar/cogent.ebnf")
# with open("examples/decking_analysis.cg") as f:
#     code = f.read()
# print(profile_parse(parser, code))

