# Agentic Coding Scaffolding

A self-evolving scaffolding project for autonomous agentic coding loops powered by Kilo.

## Overview

This repository provides a foundation for agentic coding projects. It includes:

- A GitHub Actions workflow that runs a Kilo agent loop
- Project configuration for Kilo (AGENTS.md, kilo.json)
- Custom subagents and commands for scaffolding tasks
- A task handover protocol between agent sessions

## Architecture

```
.github/workflows/main.yml   # CI workflow: Kilo agent loop
.kilo/                       # Kilo project configuration
  agent/                     # Custom subagents
    scaffolder.md            # Scaffolder subagent definition
  command/                   # Custom commands
    handover.md              # Handover task command
    scaffold-project.md      # Scaffold-project command
  skill/                     # Custom skills
    scaffolding-helper.md    # Sample skill definition
  .gitignore                 # Ignore patterns for .kilo directory
.gitignore                   # Common ignore patterns
LICENSE                      # MIT License
.pre-commit-config.yaml      # Pre-commit hooks (ruff, mypy, tests, scaffold)
AGENTS.md                    # AI agent instructions
CHANGELOG.md                 # Changelog (Keep a Changelog format)
kilo.json                    # Kilo project configuration
Makefile                     # Common developer targets
pyproject.toml               # Python project configuration (pytest, ruff, mypy)
scaffold.sh                  # Project scaffolding script
tools/                       # Maintainer tools
  refresh_scaffold.py        # Refresh the file copies embedded in scaffold.sh
hello.py                     # Sample application entry point
abc_utils.py                 # Abstract base class utilities wrapping stdlib abc
ast_utils.py                 # Abstract syntax tree utilities wrapping stdlib ast
gzip_utils.py               # Gzip compression/decompression utilities wrapping stdlib gzip
pickle_utils.py              # Object serialization utilities wrapping stdlib pickle
calculator.py                # Simple calculator module with arithmetic operations
config_utils.py              # Configuration utilities for JSON file management
shapes.py                    # Geometry utilities for areas and perimeters
strings.py                   # String utilities for text operations
utils.py                     # General utility helper functions
stats.py                     # Statistical utility functions
math_utils.py               # Mathematical utility functions
mmap_utils.py               # Utilities wrapping the standard library mmap module
data_utils.py                # Data utility functions
dataclasses_utils.py         # Dataclass utilities (is_dataclass, asdict/astuple, fields, replace, make_dataclass)
datetime_utils.py           # Date and time utility functions
dbm_utils.py                 # Database utilities wrapping stdlib dbm (open/close, read/write/delete records, key listing)
template_utils.py           # String template rendering utilities (render_template, substitute, safe_substitute, render_from_dict, has_placeholders, extract_placeholders)
file_utils.py               # File and path utility functions
url_utils.py                # URL and web utility functions
uuid_utils.py               # UUID utility functions for generating and validating UUIDs
prompt_utils.py             # Prompt utility functions for working with text prompts
random_utils.py             # Random number generation and sampling utilities
re_utils.py                 # Regular expression utilities (compile, match, search, replace, split, escape)
tempfile_utils.py           # Temporary file and directory management utilities (mkstemp, mkdtemp, NamedTemporaryFile, TemporaryDirectory)
traceback_utils.py          # Traceback utilities
warnings_utils.py           # Warnings utilities
validation_utils.py         # Input validation utilities
crypto_utils.py             # Cryptographic utilities
list_utils.py              # Advanced list manipulation utilities
locale_utils.py           # Locale utility functions for working with locale identifiers and language tags
env_utils.py               # Environment variable handling utilities
logging_utils.py          # Logging configuration and helper utilities
cache_utils.py            # Caching utilities for memoizing function results
memoize_utils.py          # Memoization utilities (memoize decorator) with cache_clear
context_utils.py          # Context manager utilities for temporarily altering the runtime environment (working directory, environment variables, standard streams)
contextlib_utils.py        # Contextlib utility functions wrapping stdlib contextlib (suppress, nullcontext, closing, redirect_stdout/stderr, chdir, ExitStack)
itertools_utils.py         # Iteration helpers wrapping itertools (chain, flatten, chunk, product, combinations, permutations, etc.)
timing_utils.py           # Performance measurement helpers
timeit_utils.py           # Wrapper for stdlib timeit
async_utils.py            # Asynchronous utility functions
asyncio_utils.py     # Utilities wrapping the standard library asyncio module (run, create_task, gather, sleep, to_thread, wait_for)
bit_utils.py              # Bitwise utility functions for working with binary representations
call_once_utils.py        # Call-once execution utilities (call_once decorator)
concurrent_utils.py       # Concurrent execution utilities (ThreadPool, ProcessPool, asyncio)
concurrent_futures_utils.py # concurrent.futures wrappers with validation
priority_queue_utils.py   # Heap-based priority queue implementation
queue_utils.py            # FIFO queue helpers (enqueue, dequeue, peek, size, is_empty)
rate_limiter_utils.py     # Rate limiting utilities (token bucket algorithm)
retry_utils.py            # Retry utilities with exponential backoff and jitter
ring_buffer_utils.py     # Fixed-size circular (ring) buffer utilities
secrets_utils.py           # Cryptographically secure secrets and token utilities (token_bytes, token_hex, token_urlsafe, compare_digest, randbelow, randbits, choice)
selectors_utils.py           # Selectors utilities wrapping the standard library selectors module (create_default_selector, register, unregister, select, get_key, get_map, close_selector)
dict_utils.py            # Dictionary utilities (deep merge, flatten, unflatten, safe get, invert, filter)
json_utils.py            # JSON utility functions (read/write/parse/dump/validate)
collections_utils.py     # Collection utilities (chunk, flatten, frequency, merge_dicts, uniq, and more)
csv_utils.py             # CSV utility functions (read/write/append as dicts or lists)
set_utils.py             # Set operation utilities (subset, superset, intersection, union, difference, symmetric_difference, cartesian_product, power_set)
stat_utils.py        # Stat file type/mode utilities wrapping stdlib stat
statistics_utils.py        # Statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
string_utils.py            # Advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, indent_text, remove_extra_whitespace, title_case)
tree_utils.py              # Tree and nested structure utilities (get/set/delete nested, flatten/unflatten, map/filter)
type_utils.py              # Type introspection utilities (is_optional, is_union, is_generic, get_type_args, type_name, is_subclass_safe)
path_utils.py              # Path manipulation utilities (join, normalize, components, extensions)
color_utils.py             # Color manipulation utilities (hex/rgb/hsl, luminance, contrast, accessibility)
colorsys_utils.py          # Colorsys utilities wrapping the standard library colorsys module (RGB/HSL conversions, color math)
duration_utils.py          # Time duration utilities (parse, format, convert between units)
temp_utils.py              # Temporary file and directory management utilities
xml_utils.py               # XML parsing and generation utilities
seq_utils.py               # Sequence utilities (first, last, nth, head, tail, split_at, take_while, drop_while, interleave, adjacent_pairs, is_sorted)
number_utils.py            # Number utility functions (clamp, round_to, is_integer, format_number, percentage)
os_utils.py                # Operating system utilities (platform info, CPU count, disk usage, user info, executable lookup)
sort_utils.py              # Sorting utility functions (is_sorted, bubble_sort, merge_sort, nth_largest, top_n)
sys_utils.py               # Python runtime and system information utilities (version, argv, executable, recursion limit, stream encodings)
threading_utils.py         # Threading utilities wrapping the standard library threading module
networking_utils.py         # Networking utilities for TCP ports, hostname resolution, and local IP detection
graphlib_utils.py          # Graph and dependency resolution utilities (topological sort, cycle detection)
greeting_utils.py          # Greeting utilities (greet, format_names, random_greeting)
glob_utils.py              # Utilities for pathname pattern expansion wrapping the standard library glob module
keyword_utils.py            # Python keyword classification utilities wrapping the standard library keyword module
version_utils.py           # Version utility functions (parse, compare, normalize)
semver_utils.py            # Semantic versioning utilities
shutil_utils.py            # High-level file operations (copy, move, remove, archive, disk usage)
socketserver_utils.py           # Socketserver utilities wrapping the standard library socketserver module
sqlite3_utils.py           # SQLite database utilities wrapping stdlib sqlite3
ssl_utils.py              # SSL/TLS utilities wrapping stdlib ssl
pkgutil_utils.py          # Package and module discovery utilities wrapping stdlib pkgutil (iter_modules, walk_packages, get_data, read_text, resolve_name, iter_importers, extend_path, find_spec)
unicodedata_utils.py      # Unicode character database utilities wrapping stdlib unicodedata (unicodedata_lookup, unicodedata_name, unicodedata_normalize, unicodedata_category, unicodedata_bidirectional, unicodedata_combining, unicodedata_east_asian_width, unicodedata_mirrored, unicodedata_decimal, unicodedata_digit, unicodedata_numeric)
118:unittest_utils.py          # Utilities wrapping the standard library unittest module
tomllib_utils.py          # TOML parsing utilities wrapping stdlib tomllib (read_toml, load_toml_string, is_valid_toml)
token_utils.py            # Python token constant utilities wrapping stdlib token (is_eof, is_nonterminal, is_terminal, tok_name, exact_token_types, n_tokens, nt_offset)
sched_utils.py            # Scheduler utilities wrapping stdlib sched (scheduler, enter, enterabs, cancel, empty, run, queue)
quopri_utils.py           # Quoted-printable encoding and decoding utilities wrapping stdlib quopri (encode, decode, encode_file, decode_file, isqp)
numbers_utils.py          # Numeric abstract base class utilities wrapping stdlib numbers (Number, Complex, Real, Rational, Integral, is_number, is_integral)
netrc_utils.py            # Netrc utilities wrapping stdlib netrc (netrc, NetrcParseError)
getopt_utils.py           # Command line option parsing utilities wrapping stdlib getopt (getopt, gnu_getopt, GetoptError)
filecmp_utils.py          # File comparison utilities wrapping stdlib filecmp (cmp_files, cmp_directories, same_file)
errno_utils.py            # System error number utilities wrapping stdlib errno (errorcode, strerror, is_errno)
dis_utils.py              # Bytecode disassembly utilities wrapping stdlib dis (dis, disassemble, show_code, get_instructions, code_info, findlinestarts, findlabels)
contextvars_utils.py      # Context variable utilities wrapping stdlib contextvars (ContextVar, Token, Context, copy_context)
configparser_utils.py     # INI configuration file parsing utilities wrapping stdlib configparser (load_config, save_config, get_sections, get_options, read_files, write_config)
binascii_utils.py         # Binary-to-ASCII encoding and decoding utilities wrapping stdlib binascii (hexlify, unhexlify, b2a_base64, a2b_base64, b2a_uu, a2b_uu, b2a_qp, a2b_qp, crc32, adler32, crc_hqx)
shelve_utils.py           # Persistent key/value storage utilities wrapping stdlib shelve (open_shelf, close, sync, keys, get, set_value, delete, contains, is_shelf)
zlib_utils.py             # Zlib compression and checksum utilities wrapping stdlib zlib (zlib_compress, zlib_decompress, zlib_compressobj, zlib_decompressobj, zlib_crc32, zlib_adler32)
deprecation_utils.py      # Deprecation utilities (deprecated decorator) with optional version, replacement, and message
linecache_utils.py        # Line cache utilities (getline, getlines, updatecache, clearcache) wrapping stdlib linecache
plistlib_utils.py         # Property list utilities wrapping stdlib plistlib (plist_load, plist_loads, plist_dump, plist_dumps)
shlex_utils.py            # Simple lexical analysis utilities wrapping stdlib shlex (split, quote, join)
cmd_utils.py              # Command interpreter utilities wrapping stdlib cmd (identchars, prompt_default, main)
this_utils.py             # Zen of Python utilities wrapping stdlib this (zen_of_python, translation_table, cipher_index, this, print_zen)
tokenize_utils.py         # Source tokenization utilities wrapping stdlib tokenize (tokenize_source, tokenize_file, generate_tokens, untokenize, token_name, token_type, detect_encoding, significant_tokens)
socket_utils.py           # Low-level socket utilities wrapping stdlib socket (create_socket, connect_socket, send_all, receive_bytes, resolve_address, error_name)
sysconfig_utils.py        # Build configuration utilities wrapping stdlib sysconfig (get_config_vars, get_config_var, get_paths, get_path, get_platform, get_scheme_names)
mimetypes_utils.py        # MIME type detection utilities wrapping stdlib mimetypes (guess_type, guess_extension, guess_all_extensions, add_type, init_database)
code_utils.py             # Interactive console utilities wrapping stdlib code (interact, compile_command, console_class, interpreter_class)
codeop_utils.py           # Utilities for compiling possibly-incomplete Python source (wrapping stdlib codeop)
copyreg_utils.py          # Pickle support registration utilities wrapping stdlib copyreg (add_extension, remove_extension, clear_extension_cache, constructor, dispatch_table, pickle)
fileinput_utils.py        # File input iteration utilities wrapping stdlib fileinput (read_lines, count_lines, filenames)
fnmatch_utils.py          # Filename pattern matching utilities wrapping stdlib fnmatch (match, match_case, filter_names, translate)
getpass_utils.py          # Secure password input utilities wrapping stdlib getpass (getpass, getuser)
pathlib_utils.py          # Path manipulation utilities wrapping stdlib pathlib (ensure_dir, join, exists, is_file, is_dir, read_text, write_text, glob, rglob, suffix, stem, parent)
runpy_utils.py            # Python module execution utilities wrapping stdlib runpy (run_module, run_path)
tarfile_utils.py          # Tar archive utilities wrapping stdlib tarfile (tarfile_open, tarfile_add, tarfile_list, tarfile_extract, tarfile_extractall, tarfile_create)
types_utils.py            # Dynamic type creation utilities wrapping stdlib types (new_class, new_function, is_function, is_method, is_generator, is_coroutine, is_lambda, simple_namespace)
zoneinfo_utils.py         # IANA timezone utilities wrapping stdlib zoneinfo (zoneinfo_get, zoneinfo_available_timezones)
marshal_utils.py           # Object serialization utilities wrapping stdlib marshal
importlib_utils.py         # importlib utilities
atexit_utils.py            # atexit utilities for registering exit handlers
multiprocessing_utils.py   # multiprocessing utilities for pools, processes, locks, shared memory (dynamic import, reload, spec, metadata, resources)
zipfile_utils.py           # ZIP archive utilities wrapping stdlib zipfile (create_archive, list_names, extract_all, is_zipfile)
bz2_utils.py               # BZ2 compression utilities wrapping stdlib bz2 (bz2_compress, bz2_decompress, bz2_open, bz2_write, bz2_read)
lzma_utils.py              # LZMA compression utilities wrapping stdlib lzma (lzma_compress, lzma_decompress, lzma_open, lzma_write, lzma_read)
gc_utils.py                # GC utilities wrapping stdlib gc (enable, disable, isenabled, collect, get_count, get_stats, get_objects, get_referents, get_referrers, set_threshold, get_threshold, set_debug, get_debug)
gettext_utils.py           # Internationalization utilities wrapping stdlib gettext (gettext, dgettext, ngettext, dngettext, textdomain, bindtextdomain, install)
inspect_utils.py           # Callable and object introspection utilities (name, signature, parameters, source)
interval_utils.py          # Interval utilities (normalization, containment, overlap, intersection, union, merge)
textwrap_utils.py          # Text wrapping utilities (wrap_text, shorten_text, dedent_text, indent_text, fill_text)
prime_utils.py             # Prime number utilities (prime_factors, nth_prime, primes_up_to, next_prime, previous_prime)
decimal_utils.py           # Decimal arithmetic utilities (to_decimal, add, subtract, multiply, divide, power, quantize, compare, abs_value, negate, is_positive, is_negative, is_zero)
difflib_utils.py           # Difflib utility functions for sequence comparison and diffing
fractions_utils.py         # Fraction arithmetic utilities (to_fraction, add, subtract, multiply, divide, power, compare, abs_value, negate, is_positive, is_negative, is_zero, is_integer, numerator, denominator, to_float, from_float)
heapq_utils.py             # Heap queue utilities wrapping stdlib heapq (heapify, heappush, heappop, heapreplace, heappushpop, merge, nlargest, nsmallest)
markdown_utils.py          # Markdown utility functions (extract code blocks, strip formatting, count words, heading detection)
time_utils.py              # Time utility functions (now_epoch, now_iso, epoch_to_iso, iso_to_epoch)
timezone_utils.py          # Time zone utilities (IANA lookups, conversion, formatting, DST) wrapping stdlib zoneinfo
cli_utils.py               # Command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
hash_utils.py              # Hashing and checksum utilities (MD5, SHA1, SHA256, SHA512, CRC32, file hashing)
hmac_utils.py              # HMAC-based message authentication utilities (MD5, SHA1, SHA256, SHA512) with constant-time verification
hashlib_utils.py           # Hash utilities wrapping hashlib (MD5, SHA1, SHA256, SHA512, SHA3, BLAKE2)
platform_utils.py          # Platform utilities wrapping the standard library platform module
signal_utils.py            # Signal utilities wrapping the standard library signal module
http_utils.py              # HTTP status codes and response handling utilities
id_utils.py                # Identifier generation and validation utilities (generate_id, new_id, is_valid_id)
html_utils.py              # HTML escaping, unescaping, and tag-stripping utilities
bytes_utils.py             # Bytes and binary utilities (to_hex, from_hex, xor, chunk)
circuit_breaker_utils.py   # Circuit breaker resilience utilities (CircuitBreaker, CircuitOpenError) with thread-safe state transitions
array_utils.py             # Array utility functions wrapping the standard library array module
base64_utils.py            # Base64 and hexadecimal encoding/decoding utilities
bisect_utils.py            # Bisect utility functions for binary search on sorted sequences
trace_utils.py            # Execution tracing utilities wrapping stdlib trace (new_tracer, run_traced, run_script_traced, counted_lines, line_counts, called_functions, call_relationships, is_ignored_filename, merge_results, write_coverage_report, summarize_coverage, format_coverage_summary, clear_counts)
calendar_utils.py            # Calendar utilities for date and month calculations (is_leap_year, days_in_month, month_name, day_name, add_months)
cmath_utils.py               # Complex mathematics utilities wrapping the standard library cmath module
struct_utils.py            # Binary struct packing and unpacking utilities
pattern_utils.py           # Design pattern utilities (Singleton, Factory, Observer, Strategy)
pprint_utils.py            # Pretty-printing utilities wrapping stdlib pprint (pformat, pprint, isreadable, isrecursive, saferepr)
reprlib_utils.py           # Reprlib utilities wrapping stdlib reprlib (repr, get_ident, recursive_repr, Repr)
codecs_utils.py             # Codecs utilities wrapping stdlib codecs
traceback_utils.py         # Traceback utilities wrapping stdlib traceback (format_exception, format_exception_only, extract_stack, format_stack, format_exc)
tracemalloc_utils.py       # Tracemalloc memory tracing utilities wrapping stdlib tracemalloc (is_tracing, get_traced_memory, get_traceback_limit, start, stop, clear_traces)
tty_utils.py              # Terminal control utilities wrapping stdlib tty (cfmakeraw, cfmakecbreak, setraw, setcbreak)
doctest_utils.py           # Doctest utilities wrapping stdlib doctest (parse_doctests, find_doctests, run_string_examples, run_docstring_examples, run_module_examples, run_file_examples)
typing_utils.py            # Typing utilities wrapping stdlib typing (get_type_hints, get_origin, get_args, is_typeddict)
functools_utils.py         # Functional programming utilities (compose, pipe, curry, apply)
operator_utils.py          # Operator utilities (identity, negate, add, subtract, multiply, divide, power, modulo, clamp, between)
config_schema.py           # Typed configuration schema utilities (SchemaField, ConfigSchema, validators)
ctypes_utils.py            # Ctypes utility functions wrapping the standard library ctypes module
copy_utils.py              # Copy utilities (shallow/deep copy, dict copy, merge) wrapping stdlib copy module
exceptions_utils.py        # Custom exception classes and error handling utilities
email_utils.py             # Email utilities wrapping the standard library email.utils module
enum_utils.py              # Enum utilities for working with Python enum.Enum classes
io_utils.py                # Line-oriented and atomic input/output utilities
ini_utils.py                 # INI configuration file utilities (load, save, get, set, merge sections)
weakref_utils.py            # Weak reference utilities for managing weak references to objects
argparse_utils.py           # Argument parsing utilities
warnings_utils.py           # Utilities wrapping the standard library warnings module
compression_utils.py       # Compression and decompression utilities (gzip, bz2, zip, tar)
gzip_utils.py               # Gzip compression/decompression utilities wrapping stdlib gzip
ip_utils.py                # IP address validation and manipulation utilities
regex_utils.py             # Regular expression utilities (compile, match, search, replace, split, escape)
terminal_utils.py          # Terminal output utilities (ANSI color, progress bars, clear screen, prompts)
subprocess_utils.py         # Subprocess utilities (run_command, check_output, check_call)
tests/                     # Python unit tests
  test_abc_utils.py          # Tests for abc_utils.py
  test_ast_utils.py          # Tests for ast_utils.py
  test_async_utils.py         # Tests for async_utils.py
  test_asyncio_utils.py   # Tests for asyncio_utils.py
  test_array_utils.py        # Tests for array_utils.py
  test_base64_utils.py        # Tests for base64_utils.py
  test_binascii_utils.py      # Tests for binascii_utils.py
  test_bisect_utils.py       # Tests for bisect_utils.py
  test_trace_utils.py        # Tests for trace_utils.py
  test_bit_utils.py           # Tests for bit_utils.py
  test_bytes_utils.py         # Tests for bytes_utils.py
  test_circuit_breaker_utils.py   # Tests for circuit_breaker_utils.py
  test_cache_utils.py         # Tests for cache_utils.py
  test_memoize_utils.py      # Tests for memoize_utils.py
  test_calculator.py          # Tests for calculator.py
  test_calendar_utils.py      # Tests for calendar_utils.py
  test_cmath_utils.py        # Tests for cmath_utils.py
  test_cli_utils.py           # Tests for cli_utils.py
  test_color_utils.py         # Tests for color_utils.py
  test_colorsys_utils.py        # Tests for colorsys_utils.py
  test_collections_utils.py   # Tests for collections_utils.py
  test_compression_utils.py   # Tests for compression_utils.py
  test_config_schema.py       # Tests for config_schema.py
  test_config_utils.py        # Tests for config_utils.py
  test_configparser_utils.py  # Tests for configparser_utils.py
  test_ctypes_utils.py        # Tests for ctypes_utils.py
  test_concurrent_utils.py    # Tests for concurrent_utils.py
test_concurrent_futures_utils.py # Tests for concurrent_futures_utils.py
  test_context_utils.py       # Tests for context_utils.py
  test_crypto_utils.py        # Tests for crypto_utils.py
  test_csv_utils.py           # Tests for csv_utils.py
  test_data_utils.py          # Tests for data_utils.py
  test_dataclasses_utils.py      # Tests for dataclasses_utils.py
  test_datetime_utils.py      # Tests for datetime_utils.py
  test_dbm_utils.py        # Tests for dbm_utils.py
  test_decimal_utils.py       # Tests for decimal_utils.py
  test_dict_utils.py          # Tests for dict_utils.py
  test_duration_utils.py      # Tests for duration_utils.py
  test_env_utils.py           # Tests for env_utils.py
  test_exceptions_utils.py    # Tests for exceptions_utils.py
  test_file_utils.py          # Tests for file_utils.py
  test_fileinput_utils.py     # Tests for fileinput_utils.py
  test_fractions_utils.py     # Tests for fractions_utils.py
  test_fnmatch_utils.py       # Tests for fnmatch_utils.py
  test_functools_utils.py     # Tests for functools_utils.py
  test_glob_utils.py          # Tests for glob_utils.py
  test_graphlib_utils.py      # Tests for graphlib_utils.py
  test_greeting_utils.py      # Tests for greeting_utils.py
  test_hash_utils.py          # Tests for hash_utils.py
  test_hmac_utils.py          # Tests for hmac_utils.py
  test_hashlib_utils.py       # Tests for hashlib_utils.py
  test_heapq_utils.py         # Tests for heapq_utils.py
  test_keyword_utils.py       # Tests for keyword_utils.py
  test_linecache_utils.py     # Tests for linecache_utils.py
  test_hello.py               # Tests for hello.py
  test_html_utils.py          # Tests for html_utils.py
  test_http_utils.py          # Tests for http_utils.py
  test_id_utils.py            # Tests for id_utils.py
  test_ini_utils.py           # Tests for ini_utils.py
  test_io_utils.py            # Tests for io_utils.py
  test_ip_utils.py            # Tests for ip_utils.py
  test_itertools_utils.py     # Tests for itertools_utils.py
  test_json_utils.py          # Tests for json_utils.py
  test_list_utils.py          # Tests for list_utils.py
  test_locale_utils.py        # Tests for locale_utils.py
  test_logging_utils.py       # Tests for logging_utils.py
test_markdown_utils.py      # Tests for markdown_utils.py
   test_marshal_utils.py       # Tests for marshal_utils.py
   test_math_utils.py          # Tests for math_utils.py
  test_mmap_utils.py   # Tests for mmap_utils.py
  test_networking_utils.py    # Tests for networking_utils.py
  test_number_utils.py        # Tests for number_utils.py
  test_operator_utils.py      # Tests for operator_utils.py
  test_os_utils.py            # Tests for os_utils.py
test_path_utils.py          # Tests for path_utils.py
  test_pathlib_utils.py       # Tests for pathlib_utils.py
  test_pattern_utils.py       # Tests for pattern_utils.py
  test_pprint_utils.py        # Tests for pprint_utils.py
test_reprlib_utils.py       # Tests for reprlib_utils.py
test_traceback_utils.py     # Tests for traceback_utils.py
test_tracemalloc_utils.py   # Tests for tracemalloc_utils.py
test_tty_utils.py           # Tests for tty_utils.py
test_doctest_utils.py       # Tests for doctest_utils.py
test_typing_utils.py        # Tests for typing_utils.py
test_pickle_utils.py        # Tests for pickle_utils.py
  test_plistlib_utils.py      # Tests for plistlib_utils.py
  test_prime_utils.py         # Tests for prime_utils.py
  test_priority_queue_utils.py # Tests for priority_queue_utils.py
  test_prompt_utils.py        # Tests for prompt_utils.py
  test_queue_utils.py         # Tests for queue_utils.py
  test_random_utils.py        # Tests for random_utils.py
  test_re_utils.py            # Tests for re_utils.py
  test_tempfile_utils.py      # Tests for tempfile_utils.py
  test_traceback_utils.py     # Tests for traceback_utils.py
  test_warnings_utils.py      # Tests for warnings_utils.py
  test_rate_limiter_utils.py  # Tests for rate_limiter_utils.py
  test_regex_utils.py         # Tests for regex_utils.py
test_retry_utils.py         # Tests for retry_utils.py
test_ring_buffer_utils.py   # Tests for ring_buffer_utils.py
test_scaffold.py            # Tests for scaffold.sh
test_secrets_utils.py       # Tests for secrets_utils.py
   test_seq_utils.py           # Tests for seq_utils.py
   test_set_utils.py           # Tests for set_utils.py
   test_shapes.py              # Tests for shapes.py
   test_shelve_utils.py        # Tests for shelve_utils.py
   test_shutil_utils.py        # Tests for shutil_utils.py
   test_signal_utils.py        # Tests for signal_utils.py
   test_socketserver_utils.py     # Tests for socketserver_utils.py
test_sort_utils.py          # Tests for sort_utils.py
   test_sqlite3_utils.py       # Tests for sqlite3_utils.py
   test_ssl_utils.py           # Tests for ssl_utils.py
   test_pkgutil_utils.py       # Tests for pkgutil_utils.py
   test_stat_utils.py    # Tests for stat_utils.py
 test_statistics_utils.py    # Tests for statistics_utils.py
  test_stats.py               # Tests for stats.py
  test_string_utils.py        # Tests for string_utils.py
  test_strings.py             # Tests for strings.py
  test_struct_utils.py        # Tests for struct_utils.py
  test_subprocess_utils.py    # Tests for subprocess_utils.py
  test_sys_utils.py           # Tests for sys_utils.py
  test_tarfile_utils.py       # Tests for tarfile_utils.py
  test_threading_utils.py     # Tests for threading_utils.py
  test_template_utils.py      # Tests for template_utils.py
  test_terminal_utils.py      # Tests for terminal_utils.py
  test_temp_utils.py          # Tests for temp_utils.py
  test_textwrap_utils.py      # Tests for textwrap_utils.py
  test_time_utils.py          # Tests for time_utils.py
  test_timezone_utils.py      # Tests for timezone_utils.py
  test_timing_utils.py        # Tests for timing_utils.py
  test_timeit_utils.py        # Tests for timeit_utils.py
  test_tree_utils.py          # Tests for tree_utils.py
  test_type_utils.py          # Tests for type_utils.py
  test_url_utils.py           # Tests for url_utils.py
  test_utils.py               # Tests for utils.py
  test_uuid_utils.py          # Tests for uuid_utils.py
  test_validation_utils.py    # Tests for validation_utils.py
  test_version_utils.py       # Tests for version_utils.py
  test_semver_utils.py        # Tests for semver_utils.py
  test_interval_utils.py      # Tests for interval_utils.py
test_weakref_utils.py       # Tests for weakref_utils.py
   test_warnings_utils.py      # Tests for warnings_utils.py
   test_xml_utils.py           # Tests for xml_utils.py
   test_importlib_utils.py     # Tests for importlib_utils.py
test_atexit_utils.py        # Tests for atexit_utils.py
test_multiprocessing_utils.py # Tests for multiprocessing_utils.py
test_zipfile_utils.py       # Tests for zipfile_utils.py
   test_bz2_utils.py           # Tests for bz2_utils.py
test_lzma_utils.py          # Tests for lzma_utils.py
    test_gc_utils.py            # Tests for gc_utils.py
    test_zlib_utils.py          # Tests for zlib_utils.py
    test_argparse_utils.py      # Tests for argparse_utils.py
    test_call_once_utils.py     # Tests for call_once_utils.py
    test_codecs_utils.py        # Tests for codecs_utils.py
    test_contextlib_utils.py    # Tests for contextlib_utils.py
    test_contextvars_utils.py   # Tests for contextvars_utils.py
    test_copy_utils.py          # Tests for copy_utils.py
    test_deprecation_utils.py   # Tests for deprecation_utils.py
    test_difflib_utils.py       # Tests for difflib_utils.py
    test_dis_utils.py           # Tests for dis_utils.py
    test_email_utils.py         # Tests for email_utils.py
    test_enum_utils.py          # Tests for enum_utils.py
    test_errno_utils.py         # Tests for errno_utils.py
    test_filecmp_utils.py       # Tests for filecmp_utils.py
    test_getopt_utils.py        # Tests for getopt_utils.py
    test_gettext_utils.py       # Tests for gettext_utils.py
    test_gzip_utils.py          # Tests for gzip_utils.py
    test_inspect_utils.py       # Tests for inspect_utils.py
    test_netrc_utils.py         # Tests for netrc_utils.py
    test_numbers_utils.py       # Tests for numbers_utils.py
    test_platform_utils.py      # Tests for platform_utils.py
    test_quopri_utils.py        # Tests for quopri_utils.py
    test_sched_utils.py         # Tests for sched_utils.py
    test_selectors_utils.py     # Tests for selectors_utils.py
    test_shlex_utils.py         # Tests for shlex_utils.py
    test_token_utils.py         # Tests for token_utils.py
    test_tomllib_utils.py       # Tests for tomllib_utils.py
    test_unicodedata_utils.py   # Tests for unicodedata_utils.py
388:     test_unittest_utils.py       # Tests for unittest_utils.py
    test_cmd_utils.py           # Tests for cmd_utils.py
    test_this_utils.py          # Tests for this_utils.py
    test_tokenize_utils.py      # Tests for tokenize_utils.py
    test_socket_utils.py        # Tests for socket_utils.py
    test_sysconfig_utils.py     # Tests for sysconfig_utils.py
    test_mimetypes_utils.py     # Tests for mimetypes_utils.py
    test_code_utils.py          # Tests for code_utils.py
    test_codeop_utils.py        # Tests for codeop_utils.py
    test_copyreg_utils.py       # Tests for copyreg_utils.py
    test_getpass_utils.py       # Tests for getpass_utils.py
    test_runpy_utils.py         # Tests for runpy_utils.py
    test_types_utils.py         # Tests for types_utils.py
    test_zoneinfo_utils.py      # Tests for zoneinfo_utils.py
     ```

## How It Works

The CI workflow (`main.yml`) runs a loop of Kilo agent sessions. Each session receives the prompt:

> Execute the task assigned by the previous agent and prepare a task for the next agent!

After each session, the workflow:

1. Checks out the repository
2. Runs `kilo run` with the handover command
3. Commits any changes (excluding workflow files)
4. Pushes to the default branch

This creates a continuous, evolving codebase where each agent session builds on the previous one.

## Task Handover Protocol

Tasks for the next agent are posted on the Kilo shared board. Each session:

1. Reads the board for any assigned task
2. Executes the task
3. Posts a new task for the next session

## ABC Utilities Module

The project includes abstract base class utilities in `abc_utils.py` wrapping the standard library `abc` module: `ABC` and `ABCMeta` return the standard abstract base class and metaclass, `abstractmethod`, `abstractclassmethod`, `abstractstaticmethod`, and `abstractproperty` decorate methods and properties as abstract, `get_cache_token` returns the abstract methods cache token, and `update_abstractmethods` recomputes the abstract methods set on a class. The module is tested in `tests/test_abc_utils.py`.

## AST Utilities Module

The project includes abstract syntax tree utilities in `ast_utils.py` wrapping the standard library `ast` module: `parse` parses source code into a syntax tree with input validation, `unparse` converts a syntax tree back to source, `dump` returns a string representation of a node, `literal_eval` safely evaluates a literal expression, `get_docstring` extracts a docstring from a function node, `walk` iterates over all descendant nodes, `iter_fields` and `iter_child_nodes` iterate over fields and direct children, `find_all` returns all nodes matching a type, `fix_missing_locations` assigns line numbers to nodes, `increment_lineno` shifts line numbers, `copy_location` copies source location between nodes, and `node_to_string` unparses a node to a string. The module is tested in `tests/test_ast_utils.py`.

## Pickle Utilities Module

The project includes object serialization utilities in `pickle_utils.py` wrapping the standard library `pickle` module: `dump` and `dumps` serialize objects to a binary file and bytes respectively, `load` and `loads` deserialize objects from a binary file and bytes, `pickler` and `unpickler` return streaming :class:`pickle.Pickler` and :class:`pickle.Unpickler` instances, `is_valid_protocol` reports whether a protocol number is supported, and `validate_protocol` normalizes a protocol argument (defaulting to the highest protocol) and raises `TypeError` for non-ints and `ValueError` for unsupported values. The module is tested in `tests/test_pickle_utils.py`.

## Calculator Module

Tasks for the next agent are posted on the Kilo shared board. Each session:

1. Reads the board for any assigned task
2. Executes the task
3. Posts a new task for the next session

## Getting Started

### For CI (Automated)

The workflow runs automatically on a schedule or via `workflow_dispatch`.

### For Local Development

Install the Kilo CLI and run:

```bash
kilo run --auto "Execute the task assigned by the previous agent and prepare a task for the next agent!"
```

## Calculator Module

The project includes a simple calculator module in `calculator.py` with functions for basic arithmetic operations: add, subtract, multiply, and divide. The module is tested in `tests/test_calculator.py`.

## Shapes Module

The project includes a geometry utilities module in `shapes.py` with functions for calculating the area and perimeter of circles, rectangles, and triangles. Input validation enforces non-negative dimensions and the triangle inequality. The module is tested in `tests/test_shapes.py`.

## Strings Module

The project includes a string utilities module in `strings.py` with functions for common text operations: `reverse_string`, `is_palindrome`, and `count_vowels`. The `is_palindrome` function is case-insensitive and ignores non-alphanumeric characters. The module is tested in `tests/test_strings.py`.

## Statistics Module

The project includes a statistics utilities module in `stats.py` with functions for common statistical operations: `mean`, `median`, `mode`, `variance`, and `stddev`. The module supports both population and sample variance/stddev calculations. Input validation ensures appropriate errors for empty lists or invalid inputs. The module is tested in `tests/test_stats.py`.

## License

MIT

## Math Utilities Module

The project includes a mathematical utilities module in `math_utils.py` with functions for common mathematical operations: `factorial`, `fibonacci`, `gcd`, `lcm`, `is_prime`, and `clamp`. The module is tested in `tests/test_math_utils.py`.

## Data Utilities Module

The project includes a data utilities module in `data_utils.py` with functions for data manipulation: `deep_copy`, `merge_dicts`, `pick`, `omit`, and `flatten_dict`. The module is tested in `tests/test_data_utils.py`.

## Dataclasses Utilities Module

The project includes dataclass utilities in `dataclasses_utils.py` wrapping the standard library `dataclasses` module: `is_dataclass` checks whether an object is a dataclass class or instance, `is_dataclass_instance` checks for dataclass instances specifically, `fields` returns a tuple of `Field` objects, `asdict` converts a dataclass instance to a dictionary, `astuple` converts to a tuple, `replace` returns a new instance with specified fields replaced, `make_dataclass` creates a new dataclass dynamically, `get_field_names` returns field names, `get_field_default` returns a field's default value, and `has_field` checks for a field's presence. The module also re-exports `field` and `MISSING` for convenience. The module is tested in `tests/test_dataclasses_utils.py`.

## Datetime Utilities Module

The project includes a date and time utilities module in `datetime_utils.py` with functions for date/time parsing, formatting, and arithmetic: `parse_datetime`, `format_datetime`, `days_between`, `is_leap_year`, `add_days`, and `get_weekday_name`. The module is tested in `tests/test_datetime_utils.py`.

## Database Utilities Module

The project includes database utilities in `dbm_utils.py` wrapping the standard library `dbm` module: `open_database` opens a database file, `close` and `sync_database` manage the connection, `write_record`/`read_record`/`delete_record`/`has_key`/`list_keys` manipulate byte keys and values, `which_database` detects the backend, `available_backends` lists usable backends, `is_valid_flag` validates open modes, and `dbm_error` exposes the dbm exception class. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_dbm_utils.py`.

## File Utilities Module

The project includes a file utilities module in `file_utils.py` with functions for file and path operations: `read_text`, `write_text`, `read_json`, `write_json`, `ensure_dir`, `list_files`, `copy_file`, and `delete_file`. The module is tested in `tests/test_file_utils.py`.

## File Input Utilities Module

The project includes file input utilities in `fileinput_utils.py` wrapping the standard library `fileinput` module: `read_lines` reads all lines from one or more text files, `count_lines` counts the total number of lines across files, and `filenames` collects the names of files as they are read (one per first line). All functions accept an optional iterable of file paths and validate their inputs. The module is tested in `tests/test_fileinput_utils.py`.

## URL Utilities Module

The project includes a URL and web utilities module in `url_utils.py` with functions for URL validation and manipulation: `is_valid_url`, `extract_domain`, `get_query_params`, `get_query_param`, `add_query_param`, `remove_query_param`, and `build_url`. The module is tested in `tests/test_url_utils.py`.

## Configuration Utilities Module

The project includes a configuration utilities module in `config_utils.py` with functions for loading, saving, and manipulating configuration files: `load_config`, `save_config`, `get_config_value`, `set_config_value`, and `merge_configs`. The module currently supports JSON format and is tested in `tests/test_config_utils.py`.

## Random Utilities Module

The project includes a random utilities module in `random_utils.py` with functions for random number generation and sampling: `random_int`, `random_choice`, `random_sample`, `random_shuffle`, `weighted_choice`, `random_uniform`, and `random_gaussian`. Every function accepts an optional `seed` argument for reproducible results and validates its inputs. The module is tested in `tests/test_random_utils.py`.

## Validation Utilities Module

The project includes a validation utilities module in `validation_utils.py` with functions for common input validation: `is_email`, `is_numeric`, `is_integer`, `is_alphanumeric`, `is_boolean_string`, `is_none_or_empty`, `min_length`, `max_length`, `matches_regex`, and `is_valid_hostname`. The module is tested in `tests/test_validation_utils.py`.

## Cryptographic Utilities Module

The project includes a cryptographic utilities module in `crypto_utils.py` with functions for hashing and encoding: `hash_string`, `generate_token`, `base64_encode`, and `base64_decode`. The module is tested in `tests/test_crypto_utils.py`.

## List Utilities Module

The project includes an advanced list manipulation utilities module in `list_utils.py` with functions for common list operations: `partition`, `group_by`, `safe_get`, `find`, `drop`, `take`, and `intersperse`. Input validation ensures all functions raise `TypeError` when a non-list is passed. The module is tested in `tests/test_list_utils.py`.

## Locale Utilities Module

The project includes a locale utility functions module in `locale_utils.py` with helpers for working with locale identifiers and language tags: `normalize_locale` normalizes a locale string to `language_REGION` form, `language_code` extracts the language code, `region_code` extracts the region code, and `is_valid_locale` checks whether a string looks like a valid locale identifier. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_locale_utils.py`.

## Environment Utilities Module

The project includes an environment variable utilities module in `env_utils.py` with functions for reading, writing, and parsing environment variables: `get_env`, `get_env_required`, `get_env_int`, `get_env_float`, `get_env_bool`, `set_env`, `ensure_env`, `unset_env`, and `prefix_env`. Typed accessors parse values as `int`, `float`, and `bool`, with required-variable and default fallbacks. The module is tested in `tests/test_env_utils.py`.

## Logging Utilities Module

The project includes a logging utilities module in `logging_utils.py` with helpers for logging configuration and function-call tracing: `get_logger` returns a named logger (or the root logger), `configure_logging` configures the root logger with a consistent format, handlers, and level, and `log_calls` is a decorator factory that logs function entry and return values using `functools.wraps` to preserve metadata. The module is tested in `tests/test_logging_utils.py`.

## Cache Utilities Module

The project includes a caching utilities module in `cache_utils.py` with helpers for memoizing function results: `memoize` is a decorator factory that caches return values keyed by call arguments (with optional `maxsize` LRU eviction and `typed` argument distinction), `clear_cache` invalidates the cache of a memoized function, and `cache_info` returns a dictionary with `hits`, `misses`, `maxsize`, and `currsize` statistics. Decorated functions also expose `clear_cache` and `cache_info` attributes for direct introspection. The module is tested in `tests/test_cache_utils.py`.

## Memoization Utilities Module

The project includes a lightweight memoization utilities module in `memoize_utils.py` providing a single `memoize` decorator that caches a function's return values keyed by its positional and keyword arguments. Unlike `cache_utils.memoize`, this decorator takes the function directly (not as a factory) and exposes a `cache_clear` method on the wrapped callable to empty the cache. It validates that its argument is callable and raises `TypeError` otherwise. The module is tested in `tests/test_memoize_utils.py`.

## Timing Utilities Module

The project includes a performance measurement utilities module in `timing_utils.py` with helpers for measuring and benchmarking code execution: `timer` is a context manager for timing code blocks, `elapsed_time` calculates elapsed time since a start time, and `benchmark` is a decorator that runs a function multiple times and reports average execution time. The module is tested in `tests/test_timing_utils.py`.

The project includes a `timeit_utils.py` module wrapping the standard library `timeit` with `timeit`, `repeat`, `default_timer`, and `Timer`. The module is tested in `tests/test_timeit_utils.py`.

## Concurrent Utilities Module

The project includes a concurrent execution utilities module in `concurrent_utils.py` with helpers for parallel and asynchronous processing: `ThreadPool` and `ProcessPool` context manager wrappers around the standard library executors, `gather` for running awaitables concurrently, `run_async` for running async coroutines from synchronous code, and `to_async` for converting synchronous functions to async. The module is tested in `tests/test_concurrent_utils.py`.

## Priority Queue Utilities Module

The project includes a priority queue utilities module in `priority_queue_utils.py` with a heap-based `PriorityQueue` implementation and helper functions. The queue uses a min-heap with an incrementing counter to preserve insertion order for equal priorities. It provides `push`, `pop`, `peek`, `is_empty`, `size`, `clear`, and convenience functions like `create_priority_queue` and `merge_queues`. The module is tested in `tests/test_priority_queue_utils.py`.

## Queue Utilities Module

The project includes a queue utilities module in `queue_utils.py` providing a simple FIFO `Queue` class backed by `collections.deque` along with module-level helper functions. The `Queue` class supports `enqueue`, `dequeue`, `peek`, `is_empty`, `size`, `clear`, `to_list`, and `from_list`, with `IndexError` raised on dequeue or peek from an empty queue. Module-level functions `create`, `enqueue`, `dequeue`, `peek`, `is_empty`, and `size` provide functional-style wrappers. The module is tested in `tests/test_queue_utils.py`.

## Rate Limiter Utilities Module

The project includes a rate limiting utilities module in `rate_limiter_utils.py` implementing the token bucket algorithm. It provides a `RateLimiter` class, a `token_bucket` context manager, and a `rate_limit` decorator for limiting function call frequency. The module is tested in `tests/test_rate_limiter_utils.py`.

## Retry Utilities Module

The project includes a retry utilities module in `retry_utils.py` with decorators for retrying operations with backoff: `retry` for simple retries with fixed delay and backoff, `retry_with_backoff` for exponential backoff with optional jitter, and `retry_count` which returns the result along with the number of retries performed. The module is tested in `tests/test_retry_utils.py`.

## Dictionary Utilities Module

The project includes a dictionary utilities module in `dict_utils.py` with functions for deep merging, flattening/unflattening nested dictionaries, safe nested gets, dictionary inversion, and predicate-based filtering. The module is tested in `tests/test_dict_utils.py`.

## JSON Utilities Module

The project includes a JSON utilities module in `json_utils.py` with functions for reading, writing, parsing, serializing, validating, and pretty-printing JSON data. The module is tested in `tests/test_json_utils.py`.

## CSV Utilities Module

The project includes a CSV utilities module in `csv_utils.py` with functions for reading and writing CSV files as dictionaries or lists, and appending rows. The module is tested in `tests/test_csv_utils.py`.

## Set Utilities Module

The project includes a set operation utilities module in `set_utils.py` with functions for common set-theoretic and combinatorial operations: `is_subset`, `is_superset`, `intersection`, `union`, `difference`, `symmetric_difference`, `cartesian_product`, and `power_set`. The module is tested in `tests/test_set_utils.py`.

## Stat Utilities Module

The project includes a stat utilities module in `stat_utils.py` with functions for inspecting file types and permission modes using the standard library `stat` and `os.stat`: `file_mode`, `file_type`, `is_directory`, `is_regular_file`, `is_symlink`, `is_socket`, `is_fifo`, `is_device`, `filemode`, and `stat_info`. All functions validate their inputs by delegating to `os.stat`, which raises `TypeError` for invalid paths and `OSError` for missing files. The module is tested in `tests/test_stat_utils.py`.

## Statistical Utilities Module

The project includes a statistical utilities module in `statistics_utils.py` with functions for data analysis beyond `stats.py`: `harmonic_mean`, `geometric_mean`, `median_even`, `percentile`, `covariance`, `correlation`, `z_score`, and `normalize`. The module is tested in `tests/test_statistics_utils.py`.

## String Utilities Module

The project includes a string utilities module in `string_utils.py` with advanced string manipulation functions: `slugify`, `camel_to_snake`, `snake_to_camel`, `pluralize`, `truncate`, `wrap_text`, `indent_text`, `remove_extra_whitespace`, and `title_case`. Each function validates its inputs and raises `TypeError` for non-string arguments. The module is tested in `tests/test_string_utils.py`.

## Type Utilities Module

The project includes a type introspection utilities module in `type_utils.py` with functions for inspecting Python type objects: `is_optional` detects `Optional[T]` / `Union[T, None]`, `is_union` detects any `Union` type, `is_generic` detects generic aliases like `List[int]`, `get_type_args` returns the type arguments of a generic, `type_name` produces a human-readable name for a type, and `is_subclass_safe` checks subclass relationships without raising `TypeError`. The module is tested in `tests/test_type_utils.py`.

## Path Utilities Module

The project includes a path manipulation utilities module in `path_utils.py` with functions for joining, normalizing, splitting, and inspecting filesystem paths: `join_path`, `normalize_path`, `get_absolute_path`, `get_relative_path`, `get_parent_dir`, `get_file_name`, `get_file_stem`, `get_file_extension`, `change_extension`, `is_absolute`, `get_path_components`, `get_common_path`, and `ensure_extension`. The module is tested in `tests/test_path_utils.py`.

## Pathlib Utilities Module

The project includes path manipulation utilities in `pathlib_utils.py` wrapping the standard library `pathlib` module: `ensure_dir` creates a directory (and parents) if missing and returns it, `join` joins path parts into a `Path`, `exists`, `is_file`, and `is_dir` test filesystem entries, `read_text` and `write_text` read/write text files (creating parent directories as needed), `glob` and `rglob` return sorted `Path` lists matching a pattern, and `suffix`, `stem`, and `parent` expose common `Path` attributes. The module is tested in `tests/test_pathlib_utils.py`.

## Color Utilities Module

The project includes a color manipulation utilities module in `color_utils.py` with functions for converting between color representations (hexadecimal, RGB, HSL), computing WCAG 2.1 relative luminance and contrast ratios, checking accessibility, and adjusting/blending colors: `validate_hex`, `hex_to_rgb`, `rgb_to_hex`, `rgb_to_hsl`, `hsl_to_rgb`, `get_luminance`, `get_contrast_ratio`, `is_accessible`, `adjust_brightness`, and `blend_colors`. Colors are accepted as either a hex string (``#RRGGBB``) or an RGB tuple. The module is tested in `tests/test_color_utils.py`.

## Colorsys Utilities Module

The project includes colorsys utilities in `colorsys_utils.py` wrapping the standard library `colorsys` module: `rgb_to_hls` converts RGB to HLS, `hls_to_rgb` converts HLS to RGB, `rgb_to_hsv` converts RGB to HSV, `hsv_to_rgb` converts HSV to RGB, `rgb_to_yiq` converts RGB to YIQ, and `yiq_to_rgb` converts YIQ to RGB. The module is tested in `tests/test_colorsys_utils.py`.

## Design Pattern Utilities Module

The project includes a design pattern utilities module in `pattern_utils.py` with reusable implementations of common object-oriented design patterns: `Singleton` (a thread-safe metaclass and `SingletonBase` base class that restrict a class to a single instance), `Factory` (a registry-based factory that creates objects by name), `Observer`/`Observable` (a publish-subscribe mechanism for change notifications), and `Strategy`/`StrategyContext` (plug-and-play algorithm selection). The module is tested in `tests/test_pattern_utils.py`.

## Pretty-Printing Utilities Module

The project includes pretty-printing utilities in `pprint_utils.py` wrapping the standard library `pprint` module: `pformat` returns a formatted string representation of an object, `pprint` prints a formatted representation to a stream, `isreadable` reports whether an object's representation is readable by `eval`, `isrecursive` reports whether an object contains a recursive reference, and `saferepr` returns a safe string representation that truncates recursive structures. All functions forward their keyword arguments to the standard library. The module is tested in `tests/test_pprint_utils.py`.

## Reprlib Utilities Module

The project includes reprlib utilities in `reprlib_utils.py` wrapping the standard library `reprlib` module: `repr` returns a string representation that truncates long objects, `get_ident` returns the identifier used to track recursive objects, `Repr` is a configurable subclass of `reprlib.Repr` with validated constructor arguments, `aRepr` is the default instance, and `recursive_repr` is a decorator that guards against infinite recursion. The module is tested in `tests/test_reprlib_utils.py`.

## Codecs Utilities Module

The project includes codecs utilities in `codecs_utils.py` wrapping the standard library `codecs` module: `encode` and `decode` encode/decode objects, `lookup` looks up a codec by name, `getencoder`/`getdecoder` return encoder/decoder functions, `getincrementalencoder`/`getincrementaldecoder` return incremental encoders/decoders, `getreader`/`getwriter` return stream readers/writers, `open` opens a file with a given encoding, and `register`/`register_error`/`lookup_error` manage codec registration and error handlers. The module is tested in `tests/test_codecs_utils.py`.

## Bz2 Utilities Module

The project includes BZ2 compression utilities in `bz2_utils.py` wrapping the standard library `bz2` module: `bz2_compress` compresses bytes, `bz2_decompress` decompresses bz2-compressed bytes, `bz2_open` opens a bz2 file with optional compression level, `bz2_write` writes bytes to a bz2 file, and `bz2_read` reads and decompresses a bz2 file. The module is tested in `tests/test_bz2_utils.py`.

## Gzip Utilities Module

The project includes gzip compression/decompression utilities in `gzip_utils.py` wrapping the standard library `gzip` module: `gzip_compress` compresses bytes with optional compression level, `gzip_decompress` decompresses gzip-compressed bytes, `gzip_open` opens a gzip file, `gzip_write` writes bytes to a gzip file, and `gzip_read` reads and decompresses a gzip file. The module is tested in `tests/test_gzip_utils.py`.

## Configuration File Parsing Utilities Module

The project includes configuration file parsing utilities in `configparser_utils.py` wrapping the standard library `configparser` module: `load_config` reads an INI-style file into a dictionary of sections (excluding the DEFAULT section), `save_config` writes a configuration dictionary to an INI file, `get_sections` and `get_options` list the sections and options of a parser, `read_files` reads and parses multiple files, and `write_config` serializes a parser to a file. The module re-exports `ConfigParser`, `RawConfigParser`, `BasicInterpolation`, `ExtendedInterpolation`, `DEFAULTSECT`, and the common `configparser` exceptions. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_configparser_utils.py`.

## Configuration Schema Module

The project includes a configuration schema module in `config_schema.py` with declarative, typed configuration schemas. `SchemaField` describes a single typed field (`str`, `int`, `float`, `bool`) with optional defaults, required flags, and validators, and `ConfigSchema` composes fields to validate, coerce, and normalize configuration dictionaries. Built-in validators include `int_validator`, `float_validator`, `str_validator`, `bool_validator`, `email_validator`, `hostname_validator`, `url_validator`, `range_validator`, `choices_validator`, and `regex_validator`. The module is tested in `tests/test_config_schema.py`.

Completed task: Added a new `config_schema.py` module with typed configuration schema utilities (`SchemaField`, `ConfigSchema`, validators such as `range_validator`, `choices_validator`, `email_validator`) and its tests. Synchronized the scaffold template: added `config_schema.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions. Verified all tests pass, ruff and mypy are clean.

## Ctypes Utilities Module

The project includes a ctypes utilities module in `ctypes_utils.py` wrapping the standard library `ctypes` module. It re-exports the fundamental C-compatible data types (`c_int`, `c_char_p`, `c_void_p`, `c_size_t`, `c_double`, and more), the composite types (`Structure`, `Union`, `POINTER`, `Array`), the factory (`CFUNCTYPE`), and helper functions (`sizeof`, `alignment`, `addressof`, `pointer`, `byref`, `cast`, `memmove`, `memset`, `string_at`, `create_string_buffer`, `create_unicode_buffer`, `get_errno`, `set_errno`, `get_last_error`, `set_last_error`, `find_library`). The module is tested in `tests/test_ctypes_utils.py`.

## Exception Utilities Module

The project includes custom exception types and utilities in `exceptions_utils.py`: custom exceptions (`ValidationError`, `ConfigurationError`, `NotFoundError`, `PermissionError_`, `TimeoutError_`) with support for error details and field metadata; helper functions `catch_and_wrap()` to catch and wrap exceptions while preserving the cause, `get_error_details()` to extract exception type/message/traceback as a dict, and `is_instance_of_any()` to test for membership in an exception tuple. The module is tested in `tests/test_exceptions_utils.py`.

## Email Utilities Module

The project includes email utilities in `email_utils.py` wrapping the standard library `email.utils` module: `email_formatdate` returns an RFC 2822 formatted date string, `email_parsedate` parses an RFC 2822 date string into a time tuple, `email_parsedate_to_datetime` parses into a datetime, `email_mktime_tz` converts a time tuple to a UTC timestamp, `email_parseaddr` and `email_formataddr` parse and format address headers, `email_getaddresses` parses multiple address values, `email_make_msgid` generates a Message-ID, `email_quote` and `email_unquote` quote and unquote header strings, and `email_format_datetime` formats a datetime as an RFC 2822 date string. The module is tested in `tests/test_email_utils.py`.

## Enum Utilities Module

The project includes enum utilities in `enum_utils.py` for working with Python `enum.Enum` classes: `enum_to_dict` converts an enum class to a name-to-value dictionary, `get_enum_member` looks up a member by name or value, `is_enum_member` checks whether a value matches a member, `list_enum_members` returns all members in declaration order, `enum_value_from_name` returns a member's value by name, and `enum_name_from_value` returns a member's name by value. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_enum_utils.py`.

## IO Utilities Module

The project includes line-oriented and atomic input/output utilities in `io_utils.py`: `read_lines` and `write_lines` for line-based file IO, `append_text` to append to files, `atomic_write_text` to write content atomically via a temp file and `os.replace`, `stream_copy` to copy file contents in chunks, `count_lines` to count lines, and `iter_lines` to stream lines without loading the file into memory. The module is tested in `tests/test_io_utils.py`.

## Terminal Utilities Module

The project includes terminal output utilities in `terminal_utils.py` for formatting terminal output with ANSI escape sequences: `supports_color` detects color support, `colorize` and `print_colored` render text in ANSI colors (black, red, green, yellow, blue, magenta, cyan, white) with optional bold, `clear_screen` clears the terminal, `get_terminal_size` returns the `(columns, lines)`, `ProgressBar` renders a terminal progress bar (usable as a context manager), `progress_bar` wraps an iterable with a progress bar, and `prompt` reads user input with an optional default. Color output is automatically disabled when the stream is not a TTY or the `NO_COLOR` environment variable is set. The module is tested in `tests/test_terminal_utils.py`.

## Async Utilities Module

The project includes asynchronous utility functions in `async_utils.py` for running blocking code in threads, gathering coroutines with timeouts, sleeping asynchronously, and retrying async operations: `run_in_thread`, `gather_with_timeout`, `async_sleep`, and `retry_async`. The module is tested in `tests/test_async_utils.py`.

## Bit Utilities Module

The project includes bitwise utility functions in `bit_utils.py` for working with binary representations of non-negative integers: `count_set_bits` counts the number of 1 bits, `is_power_of_two` tests whether a value is a power of two, `next_power_of_two` and `prev_power_of_two` find the nearest power of two, `reverse_bits` reverses bits within a width, `rotate_left` and `rotate_right` rotate bits, `get_bit`, `set_bit`, `clear_bit`, and `toggle_bit` read or modify individual bits, and `is_even`/`is_odd` test parity. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_bit_utils.py`.

## Collections Utilities Module

The project includes collection utilities in `collections_utils.py` for working with iterables and data structures: `chunk`, `flatten`, `deep_flatten`, `windowed`, `uniq`, `uniq_by`, `frequency`, `most_common`, `least_common`, `merge_dicts`, `to_deque`, `pluck`, `compact`, and `partition_by`. The module is tested in `tests/test_collections_utils.py`.

## Compression Utilities Module

The project includes compression and decompression utilities in `compression_utils.py` supporting gzip, bz2, zip, and tar formats for bytes/strings and archive operations. The module is tested in `tests/test_compression_utils.py`.

## Functools Utilities Module

The project includes functional programming utilities in `functools_utils.py` for composing, piping, and currying functions: `compose`, `pipe`, `curry`, and `apply`. The module is tested in `tests/test_functools_utils.py`.

## IP Utilities Module

The project includes IP address validation and manipulation utilities in `ip_utils.py` for IPv4/IPv6 validation, version detection, conversion between strings and integers, and property checks: `is_valid_ip`, `is_valid_ipv4`, `is_valid_ipv6`, `get_ip_version`, `ip_to_int`, and `int_to_ip`. The module is tested in `tests/test_ip_utils.py`.

## Prompt Utilities Module

The project includes prompt utility functions in `prompt_utils.py` for working with text prompts: `truncate_prompt`, `format_prompt_template`, `clean_prompt`, `extract_keywords`, `wrap_prompt`, and `estimate_token_count`. The module is tested in `tests/test_prompt_utils.py`.

## Regex Utilities Module

The project includes regular expression utilities in `regex_utils.py` for safe regex compilation, matching, extraction, and manipulation: `compile_pattern`, `is_valid_pattern`, `match_pattern`, `search_pattern`, `find_all`, `replace_pattern`, `split_pattern`, `escape_pattern`, `extract_groups`, and `named_groups`. The module is tested in `tests/test_regex_utils.py`.


## Regular Expression Utilities Module (re_utils)

The project includes regular expression utilities in `re_utils.py` wrapping the standard library `re` module: `find_all` returns all non-overlapping matches as strings, `find_matches` returns `re.Match` objects, `search` and `match` find patterns, `full_match` requires the entire string to match, `split` splits by pattern, `sub` and `subn` substitute matches with strings or callables, `compile_regex` compiles a regex pattern with optional flags, and `escape` escapes special characters. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_re_utils.py`.

## Tree Utilities Module

The project includes tree and nested structure utilities in `tree_utils.py` for getting, setting, deleting, flattening, unflattening, mapping, and filtering nested structures: `get_nested`, `set_nested`, `delete_nested`, `flatten_tree`, `unflatten_tree`, `map_tree`, and `filter_tree`. The module is tested in `tests/test_tree_utils.py`.

## UUID Utilities Module

The project includes UUID utility functions in `uuid_utils.py` for generating and validating UUIDs: `generate_uuid`, `generate_uuid4`, `generate_uuid1`, `is_valid_uuid`, and `parse_uuid`. The module is tested in `tests/test_uuid_utils.py`.

## Utils Module

The project includes general utility helper functions in `utils.py`: `flatten`, `chunk`, `unique`, and `is_empty`. The module is tested in `tests/test_utils.py`.

## CLI Utilities Module

The project includes command-line interface utilities in `cli_utils.py` for building simple CLI applications: `create_parser` builds an :mod:`argparse` parser with standard ``--verbose`` and ``--version`` options, `parse_arguments` parses command-line arguments, and `main_wrapper` wraps a main function to return consistent process exit codes (``0`` on success, ``1`` on error, ``130`` on keyboard interrupt). The module is tested in `tests/test_cli_utils.py`.

## Hashing and Checksum Utilities Module

The project includes hashing and checksum utilities in `hash_utils.py` for computing cryptographic hashes and checksums: `md5`, `sha1`, `sha256`, `sha512`, `crc32`, and `hash_file`. Both string and bytes inputs are supported, and `hash_file` supports multiple algorithms. The module is tested in `tests/test_hash_utils.py`.

## HMAC Utilities Module

The project includes HMAC-based message authentication utilities in `hmac_utils.py` for computing HMAC signatures (MD5, SHA1, SHA256, SHA512) with constant-time signature verification: `hmac_md5`, `hmac_sha1`, `hmac_sha256`, `hmac_sha512`, `hmac_new`, `sign`, `verify`, and `compare_digest`. The module is tested in `tests/test_hmac_utils.py`.


## Hashlib Utilities Module

The project includes hash utilities in `hashlib_utils.py` wrapping the standard library `hashlib` module: `md5_hash`, `sha1_hash`, `sha256_hash`, `sha512_hash`, `sha3_256_hash`, `sha3_512_hash`, `blake2b_hash`, and `blake2s_hash` compute digests of bytes-like input, and `file_hash` computes the digest of file contents using a specified algorithm with chunked reading. All functions validate inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_hashlib_utils.py`.

## Platform Utilities Module

The project includes platform utilities in `platform_utils.py` wrapping the standard library `platform` module: functions to query system information (`get_system`, `get_release`, `get_version`, `get_machine`, `get_processor`, `get_node`, `get_uname`), Python implementation details (`get_python_implementation`, `get_python_version`, `get_python_version_tuple`, `get_python_build`, `get_python_compiler`, `get_python_revision`), and platform identification (`get_platform`, `platform_info`). Input validation is performed where applicable with `TypeError` or `ValueError` raised for invalid arguments. The module is tested in `tests/test_platform_utils.py`.

## Signal Utilities Module

The project includes signal utilities in `signal_utils.py` wrapping the standard library `signal` module: `is_valid_signal` checks whether a number is a valid signal, `get_signal_name` returns the name of a signal, and `signal_names` lists all available signal names. Handlers can be inspected with `get_handler`, set with `set_handler`, registered with `register_handler`, and reset to default with `unregister_handler`. Convenience helpers `register_int_handler` and `register_term_handler` register handlers for `SIGINT` and `SIGTERM` respectively, while `interrupt_handler` and `suspend_handler` provide common handler implementations. `alarm` schedules a `SIGALRM`, `pause` waits for the next signal, and `signal_info` returns a summary dictionary. All functions validate inputs and raise `TypeError` or `ValueError` for invalid arguments. The module is tested in `tests/test_signal_utils.py`.

## INI Configuration Utilities Module

The project includes an INI configuration utilities module in `ini_utils.py` for working with INI-style configuration files: `load_config`, `save_config`, `get_config_value`, `set_config_value`, `merge_configs`, `list_sections`, `has_section`, and `get_section`. Section-based access uses dot notation (``section.key``), keys preserve their case, and parent directories are created automatically on save. The module is tested in `tests/test_ini_utils.py`.

## Filename Pattern Matching Utilities Module

The project includes filename pattern matching utilities in `fnmatch_utils.py` wrapping the standard library `fnmatch` module: `match` tests whether a filename matches a shell-style pattern (case-normalized on the operating system), `match_case` is a case-sensitive variant, `filter_names` returns the subset of names matching a pattern, and `translate` converts a shell-style pattern to a regular expression. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_fnmatch_utils.py`.

## HTML Utilities Module

The project includes HTML utility functions in `html_utils.py` for escaping, unescaping, and sanitizing HTML content: `escape_html` escapes special characters (`&`, `<`, `>`, `"`, `'`) for safe insertion into HTML documents, `unescape_html` decodes named and numeric HTML entities back to their original characters, `strip_tags` removes all HTML tags leaving only text content, and `escape_attribute` escapes values for safe use inside HTML attributes. All functions validate their inputs and raise `TypeError` for non-string arguments. The module is tested in `tests/test_html_utils.py`.

## Bytes Utilities Module

The project includes bytes and binary utilities in `bytes_utils.py` for working with raw bytes: `to_hex` returns the hexadecimal representation of bytes, `from_hex` decodes a hex string back into bytes, `xor` XORs data with a repeating key, and `chunk` splits bytes into fixed-size chunks. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_bytes_utils.py`.

## Itertools Utilities Module

The project includes iteration helpers in `itertools_utils.py` wrapping the standard library `itertools` module with input validation: `chain_iterables`, `flatten_once`, `take_while_pred`, `chunk_iterable`, `product_of`, `combinations_of`, and more. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_itertools_utils.py`.

## Base64 Utilities Module

The project includes Base64 and hexadecimal encoding/decoding utilities in `base64_utils.py`: `base64_encode` and `base64_decode` for standard and URL-safe Base64, `base64_encode_bytes` and `base64_decode_bytes` for raw bytes, `hex_encode` and `hex_decode` for hexadecimal, and `is_valid_base64` / `is_valid_hex` for validation. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_base64_utils.py`.

## Binary-to-ASCII Encoding Utilities Module

The project includes binary-to-ASCII encoding and decoding utilities in `binascii_utils.py` wrapping the standard library `binascii` module: `hexlify` and `unhexlify` convert between binary data and hexadecimal strings, `b2a_base64` and `a2b_base64` encode/decode Base64, `b2a_uu` and `a2b_uu` encode/decode UUencoding, `b2a_qp` and `a2b_qp` encode/decode quoted-printable, `crc32` computes a CRC32 checksum, `adler32` computes an Adler32 checksum, and `crc_hqx` computes a CRC-HQX checksum with an optional initial value. All functions accept str or bytes and raise `TypeError` for unsupported types. The module is tested in `tests/test_binascii_utils.py`.

## Bisect Utilities Module

The project includes bisect utility functions in `bisect_utils.py` for binary search on sorted sequences, wrapping the standard library `bisect` module: `bisect_left` and `bisect_right` return the insertion point to the left or right of existing entries, `insort_left` and `insort_right` insert elements while maintaining sort order, and `find_leftmost` / `find_rightmost` return the index of the first or last occurrence of a value (or `None` when absent). All functions accept an optional `lo`/`hi` range and validate their inputs. The module is tested in `tests/test_bisect_utils.py`.

## Binary Struct Utilities Module

The project includes binary struct packing and unpacking utilities in `struct_utils.py` wrapping the standard library `struct` module: `pack` and `unpack` convert between values and bytes, `pack_into` and `unpack_from` read/write at a buffer offset, `calcsize` reports the byte size of a format string, and `is_valid_format` validates a format string. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid input. The module is tested in `tests/test_struct_utils.py`.

## HTTP Status Codes and Response Handling Module

The project includes HTTP utility functions in `http_utils.py` for working with HTTP status codes and response handling: `STATUS_CODES` is a mapping of standard HTTP status codes to their reason phrases, `status_code_category` returns the leading digit (1-5) of a status code, `status_message` returns the standard reason phrase or `None` for unknown codes, and the `is_informational`, `is_success`, `is_redirection`, `is_client_error`, `is_server_error`, and `is_error` predicates classify a status code into its response category. The module is tested in `tests/test_http_utils.py`.

## Time Duration Utilities Module

The project includes time duration utilities in `duration_utils.py` for parsing, formatting, and converting time durations: `parse_duration` parses human-readable duration strings (e.g. `"1h30m"`, `"90s"`, `"2.5 days"`) into total seconds, `format_duration` renders seconds as a compact human-readable string, `seconds_to_hms` and `hms_to_seconds` convert between seconds and `(hours, minutes, seconds)`, `to_seconds` combines time components into seconds, `duration_between` computes the `timedelta` between two datetimes, and `add_duration` adds a parsed duration to a datetime. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_duration_utils.py`.

## Temporary File and Directory Utilities Module

The project includes temporary file and directory utilities in `temp_utils.py` for creating, writing, reading, and cleaning up temporary filesystem resources: `create_temp_file` and `create_temp_dir` create named temp files/directories, `temp_file` and `temp_dir` are context managers that remove resources on exit, `write_temp_file` and `read_temp_file` read/write temp file contents, `cleanup_temp_path` removes a temp file or directory, `is_temp_path` checks whether a path lives under the system temp directory, and `temp_path_exists` reports whether a path exists. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_temp_utils.py`.


## Temporary Files Utilities Module (tempfile_utils)

The project includes temporary file and directory utilities in `tempfile_utils.py` wrapping the standard library `tempfile` module: `get_tempdir` and `gettempprefix` return temp directory and prefix, `mkstemp` and `mkdtemp` create temporary files and directories, `NamedTemporaryFile`, `SpooledTemporaryFile`, and `TemporaryDirectory` provide context managers/file objects for temporary resources. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_tempfile_utils.py`.

## XML Parsing and Generation Utilities Module

The project includes XML parsing and generation utilities in `xml_utils.py` for parsing XML documents and strings, building XML elements, converting between elements and dictionaries, querying with XPath, and serializing elements back to strings using the standard library `xml.etree.ElementTree` module: `parse_xml`, `parse_xml_string`, `build_xml`, `add_child`, `set_attribute`, `get_attribute`, `element_to_dict`, `dict_to_element`, `find_elements`, `find_element`, `get_element_text`, `set_element_text`, `xml_to_string`, and `validate_well_formed`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_xml_utils.py`.

## Sequence Utilities Module

The project includes sequence utilities in `seq_utils.py` for common sequence operations: `first`, `last`, and `nth` retrieve elements by position (returning `None` when absent or out of range); `head` and `tail` return leading or trailing elements; `split_at` divides a sequence at an index; `take_while` and `drop_while` consume elements based on a predicate; `interleave` round-robins elements from multiple sequences; `adjacent_pairs` forms consecutive pairs; and `is_sorted` checks ascending or descending order with an optional key. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_seq_utils.py`.

## Number Utilities Module

The project includes number utility functions in `number_utils.py` for common numeric operations: `clamp` restricts a value to a closed interval, `round_to` rounds a value to a given number of decimal places, `is_integer` tests whether a value is integral, `format_number` formats a number with thousands separators and fixed decimals, and `percentage` returns a part as a percentage of a total formatted as a string. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_number_utils.py`.

## Operating System Utilities Module

The project includes operating system utilities in `os_utils.py` for inspecting the platform and environment: `get_platform_info` returns system/release/version/machine/processor/Python details, `get_cpu_count` reports the available CPU count, `get_disk_usage` reports total/used/free/percent disk usage, `get_user_home` and `get_username` return the current user's home and login name, `find_executable` locates an executable on ``PATH``, `expand_path` expands ``~`` and environment variables to an absolute path, and `is_executable` checks whether a path exists and is executable. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_os_utils.py`.

## Sorting Utilities Module

The project includes sorting utility functions in `sort_utils.py` for sorting and ordering operations: `is_sorted` checks whether a sequence is sorted, `bubble_sort` and `merge_sort` return new sorted lists, `nth_largest` returns the n-th largest element (1-based), and `top_n` returns the top n items sorted by key. All functions accept an optional `key` and `reverse` argument. The module is tested in `tests/test_sort_utils.py`.

## Graph and Dependency Resolution Utilities Module

The project includes graph and dependency resolution utilities in `graphlib_utils.py` for topological sorting and cycle detection of directed graphs using the standard library `graphlib` module: `topological_sort` returns nodes in dependency order, `has_cycle` detects cycles, `dependency_order` orders items by their dependencies, and `is_valid_ordering` validates a candidate ordering. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_graphlib_utils.py`.

## Version Utilities Module

The project includes version utility functions in `version_utils.py` for parsing, comparing, and normalizing dotted version strings: `parse_version` parses a dotted version string into a tuple of integers, `compare_versions` compares two version strings returning -1/0/1, `is_greater` returns whether one version is greater than another, and `normalize_version` pads or truncates a version to a fixed component count. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_version_utils.py`.

## Text Wrapping Utilities Module

The project includes text wrapping utility functions in `textwrap_utils.py` for wrapping, shortening, dedenting, indenting, and filling text using the standard library `textwrap` module: `wrap_text`, `shorten_text`, `dedent_text`, `indent_text`, and `fill_text`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_textwrap_utils.py`.

## Prime Number Utilities Module

The project includes prime number utilities in `prime_utils.py` for prime-related operations: `prime_factors` returns the prime factors of an integer, `nth_prime` returns the nth prime (1-indexed), `primes_up_to` returns all primes up to a limit, `next_prime` finds the next prime after a given number, and `previous_prime` finds the previous prime before a given number. The module builds on `math_utils.is_prime` and validates its inputs. The module is tested in `tests/test_prime_utils.py`.

## Decimal Utilities Module

The project includes decimal arithmetic utilities in `decimal_utils.py` for precise decimal number operations using the standard library `decimal` module: `to_decimal`, `add`, `subtract`, `multiply`, `divide`, `power`, `quantize`, `compare`, `abs_value`, `negate`, `is_positive`, `is_negative`, and `is_zero`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_decimal_utils.py`.


## Difflib Utilities Module

The project includes difflib utility functions in `difflib_utils.py` for sequence comparison and diffing using the standard library `difflib` module: `get_close_matches` finds close matches for a word, `ratio` returns the similarity ratio between two strings, `unified_diff` and `context_diff` produce unified/context diffs between sequences of lines, and `ndiff` produces a human-readable delta. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_difflib_utils.py`.


## Heap Queue Utilities Module

The project includes heap queue utilities in `heapq_utils.py` wrapping the standard library `heapq` module: `heapify`, `heappush`, `heappop`, `heapreplace`, `heappushpop`, `merge`, `nlargest`, and `nsmallest`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_heapq_utils.py`.

## Operator Utilities Module

The project includes operator utilities in `operator_utils.py` for common functional operations: `identity`, `negate`, arithmetic operators `add`, `subtract`, `multiply`, `divide`, `power`, and `modulo`, plus `clamp` to bound a value to a range and `between` to test membership in an interval (inclusive by default). All functions are generic over their arguments. The module is tested in `tests/test_operator_utils.py`.

## System Utilities Module

The project includes Python runtime and system information utilities in `sys_utils.py` for inspecting the interpreter and runtime environment: `get_python_version` returns the version as a dictionary, `get_python_version_string` returns the full version string, `get_executable` returns the interpreter path, `get_argv` returns command-line arguments, `get_platform` returns the platform identifier, `get_path` returns the module search path, `get_recursion_limit`/`set_recursion_limit` read and set the recursion limit, `get_stdout_encoding`/`get_stderr_encoding`/`get_stdin_encoding` report stream encodings, `is_interactive` detects interactive sessions, `get_frame_info` inspects a stack frame, and `get_refcount` returns an object's reference count. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_sys_utils.py`.

## Context Utilities Module

The project includes context manager utilities in `context_utils.py` for temporarily altering the runtime environment and restoring it on exit: `chdir` changes the current working directory, `temp_environ` updates environment variables (optionally clearing the rest), `redirect_stdout` and `redirect_stderr` redirect the standard streams, and `suppress` swallows listed exceptions. All context managers restore the previous state even when an exception is raised within the context. The module is tested in `tests/test_context_utils.py`.

## Networking Utilities Module

The project includes networking utilities in `networking_utils.py` for TCP port and host operations: `is_valid_port` validates port numbers (1-65535), `is_port_open` checks whether a TCP port is reachable on a host, `find_free_port` returns an unused local TCP port, `resolve_hostname` resolves a hostname to its IPv4 address, `get_local_ip` returns the local machine's IPv4 address, and `tcp_ping` measures TCP connection latency. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_networking_utils.py`.

## Markdown Utilities Module

The project includes Markdown utility functions in `markdown_utils.py` for working with Markdown text: `extract_code_blocks` extracts fenced code blocks (``` ... ```), `strip_markdown` removes common Markdown formatting while keeping readable text, `count_words` counts whitespace-delimited words, `is_heading` detects Markdown headings, and `heading_level` returns the heading level (1-6) or 0 if not a heading. All functions validate their inputs and raise `TypeError` for non-string arguments. The module is tested in `tests/test_markdown_utils.py`.

## Time Utilities Module

The project includes time utility functions in `time_utils.py` for working with timestamps and durations: `now_epoch` returns the current Unix timestamp in seconds, `now_iso` returns the current UTC time as an ISO 8601 string, `epoch_to_iso` converts a Unix timestamp to an ISO 8601 UTC string, and `iso_to_epoch` parses an ISO 8601 string into a Unix timestamp (returning `None` for invalid input). The module is tested in `tests/test_time_utils.py`.

## Timezone Utilities Module

The project includes time zone utilities in `timezone_utils.py` for working with IANA time zones using the standard library `zoneinfo` module: `get_timezone` looks up a `ZoneInfo` by name, `is_valid_timezone` validates an identifier, `get_utc_now` returns the current UTC time, `get_local_timezone` returns the system local zone, `convert_datetime` converts datetimes between zones, `format_datetime` renders a datetime for a zone, `utc_offset` reports the UTC offset, `is_dst` reports daylight saving time status, and `get_common_timezones` / `get_all_timezones` list zone identifiers. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_timezone_utils.py`.

## Template Utilities Module

The project includes string template utilities in `template_utils.py` for rendering and substituting variables in template strings: `render_template` renders a template using `str.format()` style placeholders, `substitute` renders a template using `string.Template` style placeholders, `safe_substitute` renders a template without raising on missing placeholders, `render_from_dict` renders a template from a mapping of variables, `has_placeholders` checks whether a template contains any placeholders, and `extract_placeholders` returns the placeholder names found in a template. The module supports both `str.format()` style and `string.Template` style placeholders and is tested in `tests/test_template_utils.py`.

## Fractions Utilities Module

The project includes fraction arithmetic utilities in `fractions_utils.py` for exact rational number operations using the standard library `fractions` module: `to_fraction`, `add`, `subtract`, `multiply`, `divide`, `power`, `compare`, `abs_value`, `negate`, `is_positive`, `is_negative`, `is_zero`, `is_integer`, `numerator`, `denominator`, `to_float`, and `from_float`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_fractions_utils.py`.

## Identifier Utilities Module

The project includes identifier generation and validation utilities in `id_utils.py` for creating short, URL-safe random identifiers: `generate_id` returns a random alphanumeric string of a given length, `new_id` returns a default 8-character identifier, and `is_valid_id` checks whether a string is a valid identifier of a given length. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_id_utils.py`.

## Inspect Utilities Module

The project includes callable and object introspection utilities in `inspect_utils.py` for working with Python callables using the standard library `inspect` module: `get_callable_name` returns the name of a callable or the class name of a callable instance, `is_callable` tests whether an object can be called, `is_async_callable` detects coroutine functions, `get_signature` returns an `inspect.Signature`, `get_parameter_names` and `get_parameter_kinds` describe a callable's parameters, `count_parameters` returns the parameter count, `has_parameter` checks for a named parameter, `bind_arguments` binds positional and keyword arguments with defaults applied, `is_builtin` detects built-in functions, and `get_source_file`/`get_source_lines` locate a callable's source. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_inspect_utils.py`.

## Call Once Utilities Module

The project includes call-once execution utilities in `call_once_utils.py` for ensuring a function runs only a single time: `call_once` decorates a function so its first invocation is cached and all subsequent calls return the cached result without re-invoking the wrapped function. Execution is thread-safe and the returned wrapper exposes a `reset` method to clear the cached state. The module is tested in `tests/test_call_once_utils.py`.

## Circuit Breaker Utilities Module

The project includes circuit breaker utilities in `circuit_breaker_utils.py` implementing the circuit breaker resilience pattern: `CircuitBreaker` wraps an operation and short-circuits calls once a configurable failure threshold is reached, cycling through `CLOSED`, `OPEN`, and `HALF_OPEN` states with thread-safe transitions.     `CircuitBreaker.call` executes a callable through the breaker, `can_execute` reports whether a call would be allowed, and `reset` returns the circuit to the closed state. A `CircuitOpenError` is raised when the circuit rejects a call. The module is tested in `tests/test_circuit_breaker_utils.py`.

## Deprecation Utilities Module

The project includes deprecation utilities in `deprecation_utils.py` for marking APIs as deprecated: `deprecated` decorates a callable so every invocation emits a `DeprecationWarning` describing the deprecation. An optional `version` records when the deprecation was introduced, an optional `replacement` names the suggested alternative, and an optional `message` overrides the default warning text. The wrapped callable forwards all arguments and return values and preserves its metadata via `functools.wraps`. The module is tested in `tests/test_deprecation_utils.py`.

## Ring Buffer Utilities Module

The project includes fixed-size circular (ring) buffer utilities in `ring_buffer_utils.py`: `RingBuffer` is a bounded buffer that overwrites the oldest element when full, with `append`, `get`, `peek`, `pop`, `clear`, `to_list`, `from_list`, plus `capacity`, `is_full`, and `is_empty` properties. Module-level helpers `create`, `append`, `get`, `pop`, `peek`, `is_empty`, `is_full`, `size`, `clear`, and `to_list` are also provided. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_ring_buffer_utils.py`.

## Copy Utilities Module

The project includes copy utilities in `copy_utils.py` for duplicating Python objects and mappings using the standard library `copy` module: `shallow_copy` returns a shallow copy, `deep_copy` returns a deep copy, `copy_dict` and `deep_copy_dict` return shallow and deep copies of a dictionary, `merge_copy` merges multiple dictionaries into a new one without mutating the inputs, and `is_same_object` performs an identity check. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_copy_utils.py`.

## Warnings Utilities Module

The project includes argument parsing utilities in `argparse_utils.py` wrapping the standard library `argparse` module: `make_parser` creates an `ArgumentParser` with common defaults, `add_flag` adds a boolean store_true flag, `add_option` adds a single-value option, `add_positional` adds a positional argument, `add_subparsers` adds subcommands support, `parse_args` parses arguments, `int_positive` validates positive integers, and `float_range` creates a float range validator. The module is tested in `tests/test_argparse_utils.py`.

The project includes warnings utilities in `warnings_utils.py` wrapping the standard library `warnings` module: `warn` emits a warning message with an optional category and stacklevel, `simplefilter` sets the global warning filter action, `catch_warnings` is a context manager that captures warnings emitted within its scope, `filterwarnings` adds a warning filter entry, and `resetwarnings` clears all warning filters. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_warnings_utils.py`.

## Threading Utilities Module

The project includes threading utilities in `threading_utils.py` wrapping the standard library `threading` module: `create_lock` and `create_rlock` return new lock and reentrant lock objects, `create_semaphore` and `create_bounded_semaphore` return semaphores with a validated initial counter, `create_event` returns an event, `create_condition` returns a condition variable, `create_timer` and `create_thread` build configured timer and thread objects, `current_thread` returns the caller's thread, `active_count` reports the number of alive threads, `enumerate_threads` lists alive threads, and `synchronized` is a decorator that serializes calls using a lock. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_threading_utils.py`.

## Selectors Utilities Module

The project includes selectors utilities in `selectors_utils.py` wrapping the standard library `selectors` module for I/O multiplexing: `create_default_selector` returns a platform-default selector, `register` and `unregister` monitor or stop monitoring file objects for read/write events, `select` waits until registered file objects are ready, `get_key` and `get_map` inspect registrations, and `close_selector` releases resources. Event masks `EVENT_READ` and `EVENT_WRITE` are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` for invalid arguments. The module is tested in `tests/test_selectors_utils.py`.

## Socketserver Utilities Module

The project includes socketserver utilities in `socketserver_utils.py` wrapping the standard library `socketserver` module for building TCP/UDP servers: `create_tcp_server` and `create_udp_server` create validated server instances, `handle_one_request` processes a single request, `serve_forever` blocks serving requests, `shutdown_server` and `close_server` stop and release a server, and `get_server_address` / `is_serving` inspect bound address and serving state. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_socketserver_utils.py`.

## Glob Utilities Module

The project includes glob utilities in `glob_utils.py` for pathname pattern expansion wrapping the standard library `glob` module: `glob_pattern` returns a list of paths matching a pattern, `iglob` returns an iterator over matching paths, `escape` escapes special characters in a pathname so it can be matched literally, and `has_magic` reports whether a pathname contains glob special characters. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_glob_utils.py`.

## Keyword Utilities Module

The project includes keyword classification utilities in `keyword_utils.py` wrapping the standard library `keyword` module: `is_keyword` reports whether a word is a Python keyword, `is_soft_keyword` reports whether a word is a Python soft keyword (such as `match` and `_`), `kwlist` returns a copy of the list of keywords, `softkwlist` returns a copy of the list of soft keywords, and `main` runs the keyword module's interactive entry point. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_keyword_utils.py`.

## Shlex Utilities Module

The project includes simple lexical analysis utilities in `shlex_utils.py` wrapping the standard library `shlex` module: `split` splits a shell-like string into a list of tokens, `quote` returns a shell-escaped version of a string, and `join` joins a sequence of tokens back into a single shell-escaped string. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_shlex_utils.py`.

## Contextlib Utilities Module

The project includes contextlib utility functions in `contextlib_utils.py` for wrapping the standard library `contextlib` module: `suppress` returns a context manager that silences listed exceptions, `nullcontext` returns a context manager that yields a given value, `closing` ensures an object's `close()` method is called on exit, `redirect_stdout` and `redirect_stderr` temporarily redirect the standard streams, `chdir` temporarily changes the current working directory, and `ExitStack` is a re-export of the standard library exit stack. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_contextlib_utils.py`.

## Typing Utilities Module

The project includes typing utilities in `typing_utils.py` wrapping the standard library `typing` module: `get_type_hints` returns the type hints of a callable or object, `get_origin` returns the unsubscripted generic type, `get_args` returns the type arguments, and `is_typeddict` reports whether a type is a `TypedDict`. The module also re-exports `overload`, `Final`, `Literal`, and `ClassVar` for convenience. All functions forward their keyword arguments to the standard library. The module is tested in `tests/test_typing_utils.py`.

## Traceback Utilities Module

The project includes traceback utilities in `traceback_utils.py` wrapping the standard library `traceback` module: `format_exception` formats an exception as a list of strings, `format_exception_only` formats the exception portion, `extract_stack` returns the current stack as `FrameSummary` objects, `format_stack` renders the current stack trace, and `format_exc` returns the active exception as a string. All functions forward to the standard library. The module is tested in `tests/test_traceback_utils.py`.

## Tracemalloc Utilities Module

The project includes tracemalloc memory tracing utilities in `tracemalloc_utils.py` wrapping the standard library `tracemalloc` module: `is_tracing` reports whether tracing is active, `get_traced_memory` returns current and peak traced memory, `get_traceback_limit` returns the traceback limit, `start` begins tracing allocations, `stop` ends tracing, and `clear_traces` discards recorded traces. The module is tested in `tests/test_tracemalloc_utils.py`.

## Doctest Utilities Module

The project includes doctest utilities in `doctest_utils.py` wrapping the standard library `doctest` module: `parse_doctests` parses the `>>>` examples of a text into doctest objects, `find_doctests` discovers the examples of a module, class, or function, `run_string_examples` runs the examples of a text, `run_docstring_examples` runs the examples of the docstring of an object, `run_module_examples` runs every example of a module, `run_file_examples` runs the examples of a text file, `summarize_results` renders a one line summary of a run, and `format_failure` describes a failed example. The module also re-exports `DocTestSuite`, `DocTestRunner`, and `OutputChecker`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_doctest_utils.py`.

## TTY Utilities Module

The project includes terminal control utilities in `tty_utils.py` wrapping the standard library `tty` module: `cfmakeraw` and `cfmakecbreak` change the terminal mode of a file descriptor to raw or cbreak mode, `setraw` and `setcbreak` set the terminal of a file descriptor to raw or cbreak mode with an optional `when` flag, and the module is tested in `tests/test_tty_utils.py`.

## SQLite Utilities Module

The project includes SQLite database utilities in `sqlite3_utils.py` wrapping the standard library `sqlite3` module: `connect` opens a connection (defaulting to an in-memory database), `execute` and `executemany` run SQL statements with optional parameters, `fetch_all`, `fetch_one`, and `fetch_many` return query results, `create_table` creates a table if it does not exist, `insert_row` inserts a row and returns its id, `query` returns rows as dictionaries keyed by column name, and `table_exists` checks whether a table exists. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_sqlite3_utils.py`.

## Plistlib Utilities Module

The project includes plistlib utility functions in `plistlib_utils.py` wrapping the standard library `plistlib` module: `plist_load` loads a plist from a binary file object, `plist_loads` loads a plist from bytes, `plist_dump` writes an object as a plist to a binary file object, and `plist_dumps` serializes an object to plist bytes. The module is tested in `tests/test_plistlib_utils.py`.

## Tarfile Utilities Module

The project includes tarfile utility functions in `tarfile_utils.py` wrapping the standard library `tarfile` module: `tarfile_open` opens a tar archive, `tarfile_add` adds a file to a (possibly new) tar archive with an optional arcname, `tarfile_list` lists member names in a tar archive, `tarfile_extract` extracts a single member, `tarfile_extractall` extracts all members, and `tarfile_create` creates a new tar archive containing a list of files with optional arcnames. The module is tested in `tests/test_tarfile_utils.py`.

## Unicode Data Utilities Module

The project includes Unicode data utilities in `unicodedata_utils.py` wrapping the standard library `unicodedata` module: `unicodedata_lookup` looks up a character by name, `unicodedata_name` returns the name of a character, `unicodedata_normalize` returns the normal form of a Unicode string, `unicodedata_category` returns the general category, `unicodedata_bidirectional` returns the bidirectional class, `unicodedata_combining` returns the combining class, `unicodedata_east_asian_width` returns the east asian width, `unicodedata_mirrored` returns whether a character is mirrored, and `unicodedata_decimal`, `unicodedata_digit`, and `unicodedata_numeric` return the numeric value of a character. The module is tested in `tests/test_unicodedata_utils.py`.

## ZIP Utilities Module

The project includes ZIP archive utilities in `zipfile_utils.py` wrapping the standard library `zipfile` module: `create_archive` creates a ZIP archive at a path containing a list of files, `list_names` returns the member names in an archive, `extract_all` extracts all members of an archive into a destination directory, and `is_zipfile` reports whether a path points to a valid ZIP archive. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_zipfile_utils.py`.

## Gettext Utilities Module

The project includes internationalization utilities in `gettext_utils.py` wrapping the standard library `gettext` module: `gettext` translates a message in the current domain, `dgettext` translates a message in a named domain, `ngettext` and `dngettext` select singular or plural translations based on a count, `textdomain` sets or gets the current message domain, `bindtextdomain` binds a domain to a locale directory, and `install` installs the translation function into Python's builtins namespace. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_gettext_utils.py`.

## SSL Utilities Module

The project includes SSL/TLS utilities in `ssl_utils.py` wrapping the standard library `ssl` module: `create_default_context` and `create_context` create SSL contexts with protocol validation, `match_hostname` verifies a certificate against a hostname (with fallback for Python 3.12+ where `ssl.match_hostname` is removed), `get_server_certificate` and `get_server_certificate_tuple` retrieve DER-encoded certificates from a connected socket, `cert_time_to_seconds` converts ASN.1 GENERALIZEDTIME strings to epoch seconds, `verify_cert_chain` validates a certificate chain, `get_default_verify_paths` returns the system's default CA paths, `is_tls_version_supported` checks TLS version support, `get_cert_subject`, `get_cert_issuer`, and `get_cert_san` extract certificate fields, and `cert_is_valid_at_time` checks whether a certificate is valid at a given time. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_ssl_utils.py`.

## Pkgutil Utilities Module

The project includes package and module discovery utilities in `pkgutil_utils.py` wrapping the standard library `pkgutil` module: `iter_modules` lists the modules found in a search path, `walk_packages` recursively lists modules and sub-packages, `get_data` reads a data file shipped inside a package as bytes, `read_text` reads and decodes such a data file, `resolve_name` resolves a dotted name to the module or attribute it refers to, `iter_importers` returns the meta path finders consulted for a module, `extend_path` extends a package path with namespace package directories, and `find_spec` returns the import spec for a module. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_pkgutil_utils.py`.

## Contextvars Utilities Module

The project includes context variable utilities in `contextvars_utils.py` wrapping the standard library `contextvars` module: the module re-exports `ContextVar`, `Token`, and `Context`, and `copy_context` returns a copy of the current context. The module is tested in `tests/test_contextvars_utils.py`.

## Dis Utilities Module

The project includes bytecode disassembly utilities in `dis_utils.py` wrapping the standard library `dis` module: the module re-exports `dis`, `disassemble`, `show_code`, `get_instructions`, `code_info`, `distb`, `disco`, and `Bytecode`, and adds `findlinestarts` and `findlabels`, which resolve line starts and jump targets across Python versions. The module is tested in `tests/test_dis_utils.py`.

## Errno Utilities Module

The project includes system error number utilities in `errno_utils.py` wrapping the standard library `errno` module: `errorcode` returns the symbolic name of an error code, `strerror` returns the human readable message for an error code, and `is_errno` reports whether a symbolic name matches a given error code. The module is tested in `tests/test_errno_utils.py`.

## Filecmp Utilities Module

The project includes file comparison utilities in `filecmp_utils.py` wrapping the standard library `filecmp` module: `cmp_files` compares two files, `cmp_directories` compares two directories and returns a `dircmp` result, and `same_file` reports whether two paths refer to the same file. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_filecmp_utils.py`.

## Getopt Utilities Module

The project includes command line option parsing utilities in `getopt_utils.py` wrapping the standard library `getopt` module: `getopt` parses short and long options using the traditional syntax, `gnu_getopt` parses them using the GNU permutation syntax, and `GetoptError` is re-exported for error handling. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_getopt_utils.py`.

## Netrc Utilities Module

The project includes netrc utilities in `netrc_utils.py` wrapping the standard library `netrc` module: the module re-exports the `netrc` parser and the `NetrcParseError` exception for handling malformed netrc files. The module is tested in `tests/test_netrc_utils.py`.

## Numbers Utilities Module

The project includes numeric abstract base class utilities in `numbers_utils.py` wrapping the standard library `numbers` module: the module re-exports `Number`, `Complex`, `Real`, `Rational`, and `Integral`, and adds `is_number` and `is_integral` predicates. The module is tested in `tests/test_numbers_utils.py`.

## Quopri Utilities Module

The project includes quoted-printable utilities in `quopri_utils.py` wrapping the standard library `quopri` module: `encode` and `decode` convert quoted-printable data to and from bytes, `encode_file` and `decode_file` convert files in place, and `isqp` reports whether a string contains quoted-printable data. The module is tested in `tests/test_quopri_utils.py`.

## Sched Utilities Module

The project includes scheduler utilities in `sched_utils.py` wrapping the standard library `sched` module: `scheduler` creates a scheduler instance, `enter` and `enterabs` schedule delayed and absolute events, `cancel` removes a scheduled event, `empty` reports whether the queue is empty, `run` executes the pending events, and `queue` returns the pending events. The module is tested in `tests/test_sched_utils.py`.

## Shelve Utilities Module

The project includes persistent key/value storage utilities in `shelve_utils.py` wrapping the standard library `shelve` module: `open_shelf` opens a shelf backed by a database file, `close` closes it, `sync` writes back pending changes when writeback caching is enabled, `keys` lists the stored keys, `get` reads a value with a default fallback, `set_value` stores a value, `delete` removes a key, and `is_shelf` reports whether an object is a shelf. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_shelve_utils.py`.

## Zlib Utilities Module

The project includes zlib compression and checksum utilities in `zlib_utils.py` wrapping the standard library `zlib` module: `zlib_compress` compresses bytes at a given compression level, `zlib_decompress` reverses it, `zlib_compressobj` and `zlib_decompressobj` create streaming compression and decompression objects, and `zlib_crc32` and `zlib_adler32` compute CRC-32 and Adler-32 checksums. The module is tested in `tests/test_zlib_utils.py`.

## Token Utilities Module

The project includes Python token constant utilities in `token_utils.py` wrapping the standard library `token` module: `is_eof`, `is_nonterminal`, and `is_terminal` classify a token type, `tok_name` returns the token name mapping, `exact_token_types` returns the exact token type mapping, `n_tokens` returns the number of token types, and `nt_offset` returns the non-terminal offset. The module is tested in `tests/test_token_utils.py`.

## Tomllib Utilities Module

The project includes TOML parsing utilities in `tomllib_utils.py` wrapping the standard library `tomllib` module: `read_toml` parses a TOML file, `load_toml_string` parses a TOML document from a string, and `is_valid_toml` reports whether a string is valid TOML. The module is tested in `tests/test_tomllib_utils.py`.

## Command Interpreter Utilities Module

The project includes command interpreter utilities in `cmd_utils.py` wrapping the standard library `cmd` module: `identchars` returns the characters allowed in command names, `prompt_default` returns the default prompt string, and `main` exposes the module's `main` entry point when it is available. The `Cmd` class is a thin subclass of `cmd.Cmd`. The module is tested in `tests/test_cmd_utils.py`.

## Zen of Python Utilities Module

The project includes Zen of Python utilities in `this_utils.py` wrapping the standard library `this` module: `zen_of_python` returns the Zen of Python as a single string, `translation_table` returns the ROT13 translation table used to encode the Zen, `cipher_index` returns the cipher key index, `this` returns the module's `this` callable when it is available (or `None`), and `print_zen` prints the Zen of Python to standard output. The module is tested in `tests/test_this_utils.py`.

## Source Tokenization Utilities Module

The project includes source tokenization utilities in `tokenize_utils.py` wrapping the standard library `tokenize` module: `tokenize_source` tokenizes in-memory source text, `tokenize_file` tokenizes a file using its declared encoding, `generate_tokens` yields tokens from a `readline` callable, `untokenize` rebuilds source text from a token stream, `token_name` returns the name registered for a token type, `token_type` returns the numeric type registered for a token name, `detect_encoding` detects the source encoding of a byte stream, `significant_tokens` drops comments and blank lines, and the `is_comment`, `is_string`, `is_number`, `is_name` and `is_keyword` predicates classify individual tokens. The module is tested in `tests/test_tokenize_utils.py`.

## Socket Utilities Module

The project includes low-level socket utilities in `socket_utils.py` wrapping the standard library `socket` module: `create_socket` creates a socket for a given address family and socket type, `create_tcp_socket` and `create_udp_socket` create stream and datagram sockets, `socket_address` validates a `(host, port)` pair, `resolve_address` resolves a host and port into candidate addresses, `connect_socket` and `create_connection` establish client connections, `bind_socket`, `listen_socket` and `accept_connection` set up servers, `send_all`, `send_to`, `receive_bytes` and `receive_from` move data over sockets, `set_timeout`, `get_timeout`, `set_nonblocking`, `set_reuse_address` and `set_keepalive` configure socket options, `shutdown_socket` and `close_socket` release sockets, `get_socket_name` and `get_peer_name` inspect bound and peer addresses, `socket_family_name` and `socket_type_name` translate numeric constants into readable names, `error_name` maps operating system error codes to their symbolic names, `get_hostname` returns the local hostname, `has_ipv6` reports IPv6 support, and `is_ipv6_address` checks IPv6 address strings. The module is tested in `tests/test_socket_utils.py`.

## Build Configuration Utilities Module

The project includes build configuration utilities in `sysconfig_utils.py` wrapping the standard library `sysconfig` module: `get_config_vars` returns the configuration variables of the running interpreter, `get_config_var` returns the value of a single configuration variable, `has_config_var` reports whether a configuration variable is defined, `list_config_var_names` returns the sorted names of the known configuration variables, `get_paths` returns the installation paths of a scheme, `get_path` returns a single installation path, `get_platform` returns the platform string of the interpreter, `get_python_version` returns the version as `major.minor`, `get_default_scheme` returns the default installation scheme, `get_preferred_scheme` resolves the preferred scheme of an installation type, `get_scheme_names` returns the known installation schemes, `is_python_build` reports whether the interpreter was built from source, `get_config_h_filename` returns the path of `pyconfig.h`, and `get_makefile_filename` returns the path of the interpreter `Makefile`. The module is tested in `tests/test_sysconfig_utils.py`.

## MIME Type Utilities Module

The project includes MIME type utilities in `mimetypes_utils.py` wrapping the standard library `mimetypes` module: `guess_type` guesses the MIME type and content encoding of a file name or URL, `guess_extension` guesses the extension of a MIME type, `guess_all_extensions` returns every extension registered for a MIME type, `type_for_extension` returns the MIME type of an extension, `add_type` registers a custom extension for a MIME type, `init_database` initializes the MIME type database and reads extra `mime.types` files, `normalize_extension` lower cases an extension and adds the leading dot, `is_valid_mime_type` reports whether a value is a well formed `type/subtype` pair, `mime_category` returns the top level type of a MIME type, and `is_text_mime_type` reports whether a MIME type describes textual content. The module is tested in `tests/test_mimetypes_utils.py`.

## Interactive Console Utilities Module

The project includes interactive console utilities in `code_utils.py` wrapping the standard library `code` module: `interact` runs an interactive console session, `compile_command` compiles a single console command and returns `None` while the input is incomplete, `console_class` returns the `InteractiveConsole` class, and `interpreter_class` returns the `InteractiveInterpreter` class. The module is tested in `tests/test_code_utils.py`.

## Codeop Utilities Module

The project includes codeop utilities in `codeop_utils.py` wrapping the standard library `codeop` module: `compile_command` compiles a possibly-incomplete source string and returns a code object when the source is complete, or `None` when it is incomplete; `Compile` is the re-exported `codeop.Compile` compiler; and `CommandCompiler` is the re-exported `codeop.CommandCompiler` class. The module is tested in `tests/test_codeop_utils.py`.

## Copyreg Utilities Module

The project includes pickle support registration utilities in `copyreg_utils.py` wrapping the standard library `copyreg` module: `add_extension` and `remove_extension` register and unregister pickling extensions for a type, `clear_extension_cache` clears the extension cache, `constructor` registers a reduction function for a type, `dispatch_table` returns the global dispatch table, and `pickle` registers a reduction function for a type. The module is tested in `tests/test_copyreg_utils.py`.

## Getpass Utilities Module

The project includes secure password input utilities in `getpass_utils.py` wrapping the standard library `getpass` module: `getpass` prompts for a password without echoing it back to the terminal, and `getuser` returns the name of the user running the process. The module is tested in `tests/test_getpass_utils.py`.

## Runpy Utilities Module

The project includes Python module execution utilities in `runpy_utils.py` wrapping the standard library `runpy` module: `run_module` executes a module and returns its globals, and `run_path` executes a Python file and returns its globals. The module is tested in `tests/test_runpy_utils.py`.

## Types Utilities Module

The project includes dynamic type utilities in `types_utils.py` wrapping the standard library `types` module: `new_class` and `new_function` create classes and functions at runtime, `is_function`, `is_method`, `is_generator`, `is_coroutine`, and `is_lambda` report the runtime type of an object, and `simple_namespace` creates a `SimpleNamespace`. The module is tested in `tests/test_types_utils.py`.

## Zoneinfo Utilities Module

The project includes IANA timezone utilities in `zoneinfo_utils.py` wrapping the standard library `zoneinfo` module: `zoneinfo_get` returns a `ZoneInfo` for an IANA key and `zoneinfo_available_timezones` returns the set of available keys. The module is tested in `tests/test_zoneinfo_utils.py`.

## Array Utilities Module

The project includes array utilities in `array_utils.py` wrapping the standard library `array` module: `array_create` and `array_fromlist` build typed arrays, `array_tolist` converts an array to a list, `array_append`, `array_extend`, and `array_insert` add elements, `array_pop` and `array_remove` delete elements, `array_reverse` reverses an array in place, `array_buffer_info` reports the buffer layout, `array_byteswap` swaps the byte order of every item, and `array_count` and `array_index` search for a value. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_array_utils.py`.

## Atexit Utilities Module

The project includes exit handler utilities in `atexit_utils.py` wrapping the standard library `atexit` module: `register` and `add` schedule a function to run at interpreter exit, `unregister` and `remove` cancel a scheduled function, `clear` drops every registered handler, `get_registered` lists the registered handlers, and `run_exit_handlers` runs them immediately. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_atexit_utils.py`.

## Calendar Utilities Module

The project includes calendar utilities in `calendar_utils.py` wrapping the standard library `calendar` module: `is_leap_year` reports whether a year is a leap year, `days_in_month` returns the number of days in a month, `first_day_of_month` returns the weekday a month starts on, `month_name` and `day_name` return localized names, `month_calendar` renders a month grid, `weekdays_in_month` and `weekend_days_in_month` collect the matching dates, `is_weekend` reports whether a date falls on a weekend, and `add_months` shifts a date by a number of months. The module is tested in `tests/test_calendar_utils.py`.

## Complex Mathematics Utilities Module

The project includes complex mathematics utilities in `cmath_utils.py` wrapping the standard library `cmath` module: `phase`, `polar`, and `rect` convert between rectangular and polar forms, `exp`, `log`, `log10`, and `sqrt` provide the elementary functions, `sin`, `cos`, `tan`, `asin`, `acos`, and `atan` provide the trigonometric functions, `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, and `atanh` provide the hyperbolic functions, and `isfinite`, `isinf`, `isnan`, and `isclose` inspect complex values. The module is tested in `tests/test_cmath_utils.py`.

## Concurrent Futures Utilities Module

The project includes `concurrent.futures` utilities in `concurrent_futures_utils.py` wrapping the standard library `concurrent.futures` module: `ThreadPoolExecutor` and `ProcessPoolExecutor` are re-exported, `Future` and `as_completed` support result collection, `wait` waits on a set of futures with the `FIRST_COMPLETED` and `FIRST_EXCEPTION` policies, `thread_pool_executor` and `process_pool_executor` build validated executors, `submit` schedules a callable, `as_completed_iter` yields futures as they finish, and `wait_futures` waits for a group of futures. The module is tested in `tests/test_concurrent_futures_utils.py`.

## Garbage Collector Utilities Module

The project includes garbage collector utilities in `gc_utils.py` wrapping the standard library `gc` module: `enable` and `disable` toggle automatic collection, `isenabled` reports the current state, `collect` runs a collection pass, `get_count` reports the collection counters, `get_objects` lists tracked objects, `get_referents` and `get_referrers` inspect object relationships, `get_stats` reports per-generation statistics, `set_debug` and `get_debug` control the debug flags, and `set_threshold` and `get_threshold` manage the collection thresholds. The module is tested in `tests/test_gc_utils.py`.

## Greeting Utilities Module

The project includes greeting utilities in `greeting_utils.py`: `format_greeting` renders a greeting for a person and `format_names` renders a greeting for a list of people. The module is tested in `tests/test_greeting_utils.py`.

## Importlib Utilities Module

The project includes import utilities in `importlib_utils.py` wrapping the standard library `importlib` module: `import_module` and `reload_module` load and reload modules, `find_spec` and `get_spec` return import specifications, `get_module_name_from_path` derives a module name from a file path, `is_module_available` reports whether a module can be imported, `get_source_file` and `get_loader` describe a module's origin, `get_distribution` and `get_distribution_version` read installed package metadata, `get_entry_points` lists entry points, `read_text` and `read_binary` read package resources, `is_resource` reports resource availability, `path` returns a package's search path, and `get_attr_from_module` and `call_func_from_module` reach into imported modules. The module is tested in `tests/test_importlib_utils.py`.

## Interval Utilities Module

The project includes interval utilities in `interval_utils.py`: `normalize_interval` orders the bounds of an interval, `is_valid_interval` reports whether the bounds are ordered, `interval_contains` tests for containment, `interval_overlaps` tests for overlap, `interval_intersection` and `interval_union` combine two intervals, `merge_intervals` collapses overlapping intervals, and `interval_length` measures the span. The module is tested in `tests/test_interval_utils.py`.

## Line Cache Utilities Module

The project includes line cache utilities in `linecache_utils.py` wrapping the standard library `linecache` module: `getline` and `getlines` read cached source lines, `checkcache` reports whether a file has stale cached data, `updatecache` refreshes the cache for a file, `lazycache` loads a file's lines on demand, and `clearcache` empties the cache. The module is tested in `tests/test_linecache_utils.py`.

## LZMA Utilities Module

The project includes LZMA compression utilities in `lzma_utils.py` wrapping the standard library `lzma` module: `lzma_compress` compresses bytes, `lzma_decompress` reverses it, `lzma_open` opens a compressed file, and `lzma_write` and `lzma_read` stream data through an archive. The module is tested in `tests/test_lzma_utils.py`.

## Marshal Utilities Module

The project includes object serialization utilities in `marshal_utils.py` wrapping the standard library `marshal` module: `dumps` and `loads` serialize and deserialize objects to and from bytes, `dump` and `load` write and read serialized objects to a file, and `get_version` reports the supported marshal version. The module is tested in `tests/test_marshal_utils.py`.

## Multiprocessing Utilities Module

The project includes multiprocessing utilities in `multiprocessing_utils.py` wrapping the standard library `multiprocessing` module: `get_context` selects a start method, `cpu_count` reports the available CPUs, `active_children` and `current_process` report process state, `freeze_support` enables frozen executables, `create_pool`, `pool_map`, and `pool_starmap` run work in a pool, `create_queue` and `create_simple_queue` build queues, `create_lock`, `create_rlock`, `create_semaphore`, `create_event`, and `create_condition` build synchronization primitives, `create_value` and `create_array` build shared memory, `create_process` and `run_in_process` start a child process, and `is_forking`, `is_spawn`, and `is_forkserver` report the active start method. The module is tested in `tests/test_multiprocessing_utils.py`.

## Secrets Utilities Module

The project includes cryptographically secure secret utilities in `secrets_utils.py` wrapping the standard library `secrets` module: `token_bytes`, `token_hex`, and `token_urlsafe` generate random tokens, `compare_digest` compares two secrets in constant time, `randbelow` and `randbits` generate random numbers, and `choice` picks a random element from a sequence. All functions validate their inputs and raise `ValueError` on invalid arguments. The module is tested in `tests/test_secrets_utils.py`.

## Semantic Versioning Utilities Module

The project includes semantic versioning utilities in `semver_utils.py`: the `SemanticVersion` class parses and compares version strings, `parse_semver` parses a semantic version, `compare_semver` compares two versions, `bump_major`, `bump_minor`, and `bump_patch` increment a version component, and `is_valid_semver` reports whether a string is a valid semantic version. The module is tested in `tests/test_semver_utils.py`.

## Shutil Utilities Module

The project includes high-level file operation utilities in `shutil_utils.py` wrapping the standard library `shutil` module: `copy_file` and `copy_tree` copy files and directories, `move` moves a path, `remove_tree` deletes a directory tree, `disk_usage` reports disk usage for a path, `make_archive` and `unpack_archive` build and expand archives, and `which` locates an executable on `PATH`. The module is tested in `tests/test_shutil_utils.py`.

## Subprocess Utilities Module

The project includes subprocess utilities in `subprocess_utils.py` wrapping the standard library `subprocess` module: `run_command` runs a command and captures its output, `check_output` runs a command and returns its standard output, and `check_call` runs a command and raises on a non-zero exit status. The module is tested in `tests/test_subprocess_utils.py`.

## Weak Reference Utilities Module

The project includes weak reference utilities in `weakref_utils.py` wrapping the standard library `weakref` module: `WeakRef` and `WeakMethod` are re-exported, `create_weakref` creates a weak reference to an object, `create_proxy` creates a transparent proxy, `get_object` resolves a reference to its target, `is_alive` reports whether the target still exists, and `create_finalizer` registers a callback for when the target is collected. The module is tested in `tests/test_weakref_utils.py`.

## Unittest Utilities Module

The project includes utilities wrapping the standard library `unittest` module in `unittest_utils.py`: `TestCase`, `TestSuite`, `TestLoader`, `TextTestRunner` are re-exported, along with `make_suite`, `run_tests`, `main`, and `defaultTestLoader`. The module is tested in `tests/test_unittest_utils.py`.

## Timeit Utilities Module

The project includes timeit utilities in `timeit_utils.py` wrapping the standard library `timeit` module: `timeit`, `repeat`, `default_timer`, and `Timer`. The module is tested in `tests/test_timeit_utils.py`.

## Mmap Utilities Module

The project includes utilities wrapping the standard library `mmap` module in `mmap_utils.py`: `create_anonymous`, `create_file_mmap`, `access_read`, `access_write`, `access_copy`, `pagesize`, `allocation_granularity`, `constants`, `is_mmap`, `write_bytes`, `read_bytes`, `find_bytes`, and `close_mmap`. The module is tested in `tests/test_mmap_utils.py`.

## Asyncio Utilities Module

The project includes utilities wrapping the standard library `asyncio` module in `asyncio_utils.py`: `run`, `create_task`, `gather`, `sleep`, `to_thread`, `wait_for`, `current_task`, `all_tasks`, `iscoroutinefunction`, `iscoroutine`, `get_event_loop`, and `get_running_loop`, along with re-exports of `Event`, `Lock`, `Queue`, and `Semaphore`. The module is tested in `tests/test_asyncio_utils.py`.

## Trace Utilities Module

The project includes execution tracing utilities in `trace_utils.py` wrapping the standard library `trace` module: `new_tracer` creates a tracer that counts the executed lines, `run_traced` runs a callable under a tracer and returns its result together with the coverage results, `run_script_traced` runs a Python script under a tracer and returns its exit code, `counted_lines` maps every recorded line to the number of times it was executed, `line_counts` groups those counts by file, `called_functions` lists the functions that were called, `call_relationships` lists the recorded calling relationships, `is_ignored_filename` reports whether a file is left out of the coverage report, `merge_results` merges the counts of two runs, `write_coverage_report` writes the coverage report, `summarize_coverage` returns a per file coverage summary, `format_coverage_summary` renders that summary as a table, and `clear_counts` discards the counts recorded by a tracer. The module also re-exports `Trace`, `CoverageResults`, and `PRAGMA_NOCOVER`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_trace_utils.py`.
profile_utils.py
tests/test_profile_utils.py
`profile_utils.py`


## Profile Utilities Module

The project includes profiling utilities in `profile_utils.py` wrapping the standard library `profile` module: `run` profiles a single statement, `runctx` profiles a statement in given namespaces, `new_profiler` creates a new profiler instance, `Profile` is the profiler class, and `main` runs the profile module's command-line entry point. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_profile_utils.py`.


## Pstats Utilities Module

The project includes profiling statistics utilities in `pstats_utils.py` wrapping the standard library `pstats` module: `new_stats` creates `Stats` objects from profile files, `load_stats` loads statistics, `add_stats` merges statistics, `print_stats` prints reports, `sort_stats` sorts results, `strip_dirs` removes path prefixes, `reverse_order` reverses sort order, and `dump_stats` saves statistics to files. `Stats` and `SortKey` are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_pstats_utils.py`.
