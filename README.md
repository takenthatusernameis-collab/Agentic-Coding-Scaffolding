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
backoff_utils.py             # Backoff and retry delay utilities (constant, exponential)
hostname_utils.py            # Hostname validation and normalization utilities (is_valid_hostname, normalize_hostname, get_local_hostname, is_fully_qualified, split_hostname)
aifc_utils.py                # AIFF and AIFF-C format utilities wrapping stdlib aifc (open, is_available, aliases, re-exports Aifc_read, Aifc_write, Error) with input validation
ast_utils.py                 # Abstract syntax tree utilities wrapping stdlib ast
audioop_utils.py             # Audio utilities wrapping the standard library audioop module
gzip_utils.py               # Gzip compression/decompression utilities wrapping stdlib gzip
mailcap_utils.py            # Mailcap utilities wrapping stdlib mailcap
pickle_utils.py              # Object serialization utilities wrapping stdlib pickle
pickletools_utils.py         # Pickletools utilities wrapping stdlib pickletools
calculator.py                # Simple calculator module with arithmetic operations
config_utils.py              # Configuration utilities for JSON file management
shapes.py                    # Geometry utilities for areas and perimeters
strings.py                   # String utilities for text operations (reverse_string, reverse_words, is_palindrome, count_vowels, count_consonants, count_lowercase, count_uppercase, count_digits, count_letters, count_punctuation, truncate, levenshtein_distance, title_case, camel_to_snake, snake_to_camel, word_count, slugify, pad_left, pad_right, center, lstrip_chars, rstrip_chars, strip_chars, strip_non_ascii, truncate_bytes, is_alpha, is_alphanumeric, is_binary, is_ascii, is_digit, is_hex, is_integer, is_whitespace, is_space, is_printable, is_identifier, is_pangram, is_rotation, is_subsequence, is_title, is_upper, is_lower, swap_case, count_occurrences, first_n, last_n, take, drop, between, contains_any, contains_all, count_words, remove_punctuation, remove_digits, remove_blank_lines, chunk_string, initials, common_prefix, common_suffix, char_frequency, remove_whitespace, normalize_whitespace, starts_with, ends_with, removeprefix, removesuffix, partition, rpartition, split_lines, join_lines, replace_many, strip_html, and is_blank)
utils.py                     # General utility helper functions
stats.py                     # Statistical utility functions
math_utils.py               # Mathematical utility functions (factorial, fibonacci, gcd, lcm, is_prime, is_composite, clamp, is_even, combination, permutation)
mmap_utils.py               # Utilities wrapping the standard library mmap module
data_utils.py                # Data utility functions
dataclasses_utils.py         # Dataclass utilities (is_dataclass, asdict/astuple, fields, replace, make_dataclass)
datetime_utils.py           # Date and time utility functions
dbm_utils.py                 # Database utilities wrapping stdlib dbm (open/close, read/write/delete records, key listing)
template_utils.py           # String template rendering utilities (render_template, substitute, safe_substitute, render_from_dict, has_placeholders, extract_placeholders)
file_utils.py               # File and path utility functions
url_utils.py                # URL and web utility functions
urllib_utils.py             # URL parsing utilities wrapping stdlib urllib.parse
uuid_utils.py               # UUID utility functions for generating and validating UUIDs
prompt_utils.py             # Prompt utility functions for working with text prompts
random_utils.py             # Random number generation and sampling utilities
roman_utils.py              # Roman numeral conversion utilities (to_roman, from_roman, is_valid_roman)
re_utils.py                 # Regular expression utilities (compile, match, search, replace, split, escape)
rlcompleter_utils.py        # Interactive tab completion utilities wrapping stdlib rlcompleter (Completer, complete)
tempfile_utils.py           # Temporary file and directory management utilities (mkstemp, mkdtemp, NamedTemporaryFile, TemporaryDirectory)
traceback_utils.py          # Traceback utilities
warnings_utils.py           # Warnings utilities
validation_utils.py         # Input validation utilities
crypto_utils.py             # Cryptographic utilities
crypt_utils.py              # Password hashing utilities wrapping the standard library crypt module
telnetlib_utils.py           # Telnet client utilities wrapping the standard library telnetlib module
nntplib_utils.py             # NNTP client utilities wrapping the standard library nntplib module (NNTP, NNTP_SSL, create_nntp, create_nntp_ssl, GroupInfo, ArticleInfo) with input validation
sre_constants_utils.py      # Regex constants utilities wrapping the standard library sre_constants module
sre_parse_utils.py          # Regex parse utilities wrapping the standard library sre_parse module
spwd_utils.py               # Shadow password database utilities wrapping the standard library spwd module (getspnam, getspall, is_available) with input validation
sre_compile_utils.py        # Regular expression compile utilities wrapping the standard library sre_compile module (compile, isstring, compile_pattern, dis, is_available) with input validation
list_utils.py              # Advanced list manipulation utilities
locale_utils.py           # Locale utility functions for working with locale identifiers and language tags
env_utils.py               # Environment variable handling utilities
logging_utils.py          # Logging configuration and helper utilities
cache_utils.py            # Caching utilities for memoizing function results
memoize_utils.py          # Memoization utilities (memoize decorator) with cache_clear
maybe_utils.py             # Maybe/Option type utilities for functional programming patterns (Maybe, some, nothing, from_optional, map, flat_map, etc.)
either_utils.py            # Either/Result type utilities for functional programming patterns (Either, right, left, ok, err, from_optional, map, map_left, flat_map, and_then, filter, or_else, fold, swap, unwrap, unwrap_left, unwrap_or, unwrap_or_else, is_right, is_left, is_ok, is_err)
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
string_utils.py            # Advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, wrap_words, indent_text, remove_extra_whitespace, remove_blank_lines, truncate_words, title_case, dedent_text)
tree_utils.py              # Tree and nested structure utilities (get/set/delete nested, flatten/unflatten, map/filter)
type_utils.py              # Type introspection utilities (is_optional, is_union, is_generic, get_type_args, type_name, is_subclass_safe, is_literal, is_type_var, is_class_var, is_callable, is_tuple, is_list_type, is_dict_type, is_none_type, is_any, unwrap_optional, get_origin_name)
path_utils.py              # Path manipulation utilities (join, normalize, components, extensions)
color_utils.py             # Color manipulation utilities (hex/rgb/hsl, luminance, contrast, accessibility)
colorsys_utils.py          # Colorsys utilities wrapping the standard library colorsys module (RGB/HSL conversions, color math)
duration_utils.py          # Time duration utilities (parse, format, convert between units)
temp_utils.py              # Temporary file and directory management utilities
xml_utils.py               # XML parsing and generation utilities
seq_utils.py               # Sequence utilities (first, last, nth, head, tail, split_at, take_while, drop_while, flatten, interleave, adjacent_pairs, chunk, is_sorted)
number_utils.py            # Number utility functions (clamp, round_to, round_half_up, is_integer, format_number, percentage, lerp, map_range, remap, sign, is_even, is_odd, is_negative, is_positive, is_zero, is_non_negative, is_non_positive, is_between, is_close, in_range, is_finite, is_infinite, is_nan, safe_divide, is_perfect_cube, is_perfect_square, is_power_of_two, is_palindromic_number, gcd, lcm, ceil_div, is_divisible_by, is_multiple_of, divides, is_coprime, digit_sum, digit_count, digit_product, digital_root, is_triangular_number, is_perfect_number, is_automorphic_number, is_happy_number, is_armstrong_number, is_harshad_number, is_neon_number, is_strong_number, is_fibonacci_number, is_lucas_number, is_pronic_number, is_abundant_number, is_deficient_number, is_spy_number)
os_utils.py                # Operating system utilities (platform info, CPU count, disk usage, user info, executable lookup)
sort_utils.py              # Sorting utility functions (is_sorted, bubble_sort, merge_sort, nth_largest, top_n)
sys_utils.py               # Python runtime and system information utilities (version, argv, executable, recursion limit, stream encodings)
wave_utils.py              # Wave audio utilities wrapping stdlib wave (open_read, open_write, wave_info, read_frames, write_frames, create_writer)
sndhdr_utils.py            # Sound format detection utilities wrapping stdlib sndhdr (what, whathdr, tests, is_available) with input validation
uu_utils.py                # Uuencode utilities wrapping stdlib uu (uu_encode, uu_decode, encode_uu, decode_uu, parse_uu_header, is_uuencoded)
zipapp_utils.py            # Zipapp utilities wrapping stdlib zipapp (create_archive/create_zipapp, get_interpreter/get_zipapp_interpreter, is_zipapp_archive)
py_compile_utils.py        # Py_compile utilities wrapping stdlib py_compile (compile_file/py_compile_file, get_invalidation_mode, parse_invalidation_mode, is_pyc_file, main)
pyclbr_utils.py            # Pyclbr utilities wrapping stdlib pyclbr (read_module, read_module_ex, class_names, function_names, find_class, find_function, has_class, has_function, is_class, is_function)
pyexpat_utils.py           # XML parsing utilities wrapping stdlib pyexpat (ParserCreate, ExpatError, parse, parse_text, parse_file, error_string, version_info, is_available, ErrorPosition, CurrentPosition, set_base, get_base, set_param_entity_parsing, external_entity_parser, set_start_element_handler, set_end_element_handler, set_character_data_handler, set_processing_instruction_handler, attribute_mapping) with input validation
xdrlib_utils.py             # Xdrlib utilities wrapping stdlib xdrlib (pack_uint, unpack_uint, pack_int, unpack_int, pack_enum, unpack_enum, pack_bool, unpack_bool, pack_uhyper, unpack_uhyper, pack_hyper, unpack_hyper, pack_float, unpack_float, pack_double, unpack_double, pack_string, unpack_string, pack_bytes, unpack_bytes, pack_opaque, unpack_opaque, pack_fstring, unpack_fstring, pack_fopaque, unpack_fopaque, pack_array, unpack_array, pack_farray, unpack_farray, pack_list, unpack_list, pack_uint_array, unpack_uint_array)
compileall_utils.py         # Compileall utilities wrapping stdlib compileall (compile_file, compile_dir, compile_path, main, pyc_path)
modulefinder_utils.py        # Modulefinder utilities wrapping stdlib modulefinder (load_script, find_dependencies, find_modules, missing_modules, missing_importers, module_path, is_package, report)
optparse_utils.py          # Optparse utilities wrapping stdlib optparse (make_parser, add_option, add_flag, add_count_option, add_option_group, parse_args, get_option, has_option, remove_option, get_default_values, set_defaults, get_usage, format_usage, format_help, format_option_help, get_prog_name, dest_for, string_type, int_type, float_type, choice_type, values_to_dict)
smtplib_utils.py           # Smtplib utilities wrapping stdlib smtplib (quoteaddr, quote_string, quote_data, parse_address, address_only, format_address, getfqdn, parse_response, parse_ehlo_features, build_message, create_smtp, create_smtp_ssl, create_lmtp, send_message, send_text)
sunau_utils.py             # Sun AU format utilities wrapping stdlib sunau (open, open_au, open_read, open_write, open_sunau, read_sunau, write_sunau, Au_read, Au_write, Error, is_available) with input validation
threading_utils.py         # Threading utilities wrapping the standard library threading module
networking_utils.py         # Networking utilities for TCP ports, hostname resolution, and local IP detection
graphlib_utils.py          # Graph and dependency resolution utilities (topological sort, cycle detection)
greeting_utils.py          # Greeting utilities (format_greeting, format_names, format_farewell)
glob_utils.py              # Utilities for pathname pattern expansion wrapping the standard library glob module
keyword_utils.py            # Python keyword classification utilities wrapping the standard library keyword module
version_utils.py           # Version utility functions (parse, compare, normalize, sort_versions, bump_version, decrement_version, is_version_at_least, is_version_at_most, is_version_between, is_dev_version)
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
numbers_utils.py          # Numeric abstract base class utilities wrapping stdlib numbers (Number, Complex, Real, Rational, Integral, is_number, is_integral, is_perfect_number)
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
slugify_utils.py          # Slug utilities converting strings into URL-friendly slugs (slugify, is_slug)
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
opcode_utils.py          # Opcode utilities wrapping stdlib opcode (stack_effect, opmap/opname helpers)
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
interval_utils.py          # Interval utilities (normalization, containment, overlap, intersection, union, merge, length, midpoint, distance, subset, shift, symmetric_difference)
textwrap_utils.py          # Text wrapping utilities (wrap_text, shorten_text, dedent_text, indent_text, fill_text)
prime_utils.py             # Prime number utilities (is_prime, is_composite, prime_factors, nth_prime, primes_up_to, is_coprime, coprime, is_circular_prime, is_chen_prime, is_perfect_square, is_power_of_two, is_semiprime, is_squarefree, is_prime_power, is_emirp, is_twin_prime, is_palindromic_prime, is_mersenne_prime, is_sophie_germain_prime, is_safe_prime, sum_of_proper_divisors, is_perfect_number, is_abundant_number, is_deficient_number, is_cousin_prime, is_pythagorean_prime, is_sexy_prime, is_automorphic, is_truncatable_prime, is_wilson_prime, is_carmichael_number, is_korselt_number, is_giuga_number, radical, prime_count, prime_gap, primorial, total_prime_factors, distinct_prime_factors, largest_prime_factor)

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
case_utils.py             # Case conversion utilities (kebab, pascal, constant case) with input validation
trace_utils.py            # Execution tracing utilities wrapping stdlib trace (new_tracer, run_traced, run_script_traced, counted_lines, line_counts, called_functions, call_relationships, is_ignored_filename, merge_results, write_coverage_report, summarize_coverage, format_coverage_summary, clear_counts)
calendar_utils.py            # Calendar utilities for date and month calculations (is_leap_year, days_in_month, month_name, day_name, add_months)
chunk_utils.py               # IFF chunk utilities wrapping stdlib chunk (build_chunk, chunk_name, is_available, iter_chunks, open_chunk, peek_chunk, read_chunk, read_chunks, skip_chunk, write_chunk) with input validation
cgi_utils.py                 # CGI utilities wrapping the standard library cgi module (FieldStorage, MiniFieldStorage, escape, parse, parse_header, parse_multipart, parse_qs, parse_qsl, is_available) with input validation
cgitb_utils.py              # Cgitb utilities wrapping the standard library cgitb module (enable, disable, reset, lookup, scanvars, handler, text, html, small, strong, grey, pink, blue, is_available) with input validation
pipes_utils.py                # Pipeline utilities wrapping stdlib pipes (quote, quote_command, create_template, is_available, make_pipeline, step_kinds) with input validation
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
symtable_utils.py           # Symbol table utilities wrapping stdlib symtable (build_symbol_table, lookup_symbol_table, scope_type, scope_identifiers, child_scopes, iter_scopes, find_scope, describe_scope, symbol_info, symbol_flags, namespace_names, free_variables, global_names, local_names, parameter_names, imported_names, assigned_names, referenced_names, nonlocal_names)
profile_utils.py             # Profiling utilities wrapping stdlib profile (Profile, run, runctx, new_profiler, main)
pstats_utils.py              # Profiling statistics utilities wrapping stdlib pstats (Stats, SortKey, new_stats, load_stats, add_stats, print_stats, sort_stats, strip_dirs, reverse_order, dump_stats)
cprofile_utils.py            # Profiling utilities wrapping stdlib cProfile (Profile, new_profiler, run, runctx, runcall, profile_call, collect_stats, format_report, dump_stats, main)
select_utils.py              # I/O multiplexing utilities wrapping stdlib select (select, create_poller, poll_register, poll_poll, PIPE_BUF)
imaplib_utils.py             # IMAP4 client utilities wrapping stdlib imaplib (create_imap4, create_imap4_ssl, create_imap4_stream, parse_capabilities, has_capability, parse_flags, parse_fetch_flags, format_flags, parse_internaldate, format_internaldate, int_to_ap)
mailbox_utils.py             # Mailbox utilities wrapping stdlib mailbox (create_* factories)
unittest_utils.py            # Unittest utilities wrapping stdlib unittest (TestCase, TestSuite, TestLoader, TextTestRunner, make_suite, run_tests, main)
typing_utils.py            # Typing utilities wrapping stdlib typing (get_type_hints, get_origin, get_args, is_typeddict)
functools_utils.py         # Functional programming utilities (compose, pipe, curry, apply)
operator_utils.py          # Operator utilities (identity, negate, add, subtract, multiply, divide, power, modulo, clamp, between)
config_schema.py           # Typed configuration schema utilities (SchemaField, ConfigSchema, validators)
cooldown_utils.py          # Cooldown and throttling utilities for rate-limiting function calls
ctypes_utils.py            # Ctypes utility functions wrapping the standard library ctypes module
copy_utils.py              # Copy utilities (shallow/deep copy, dict copy, merge) wrapping stdlib copy module
exceptions_utils.py        # Custom exception classes and error handling utilities
email_utils.py             # Email utilities wrapping the standard library email.utils module
enum_utils.py              # Enum utilities wrapping the standard library enum module (Enum, IntEnum, StrEnum, Flag, IntFlag, auto, unique, member lookups, names/values, as_dict/as_list)
io_utils.py                # Line-oriented and atomic input/output utilities
ini_utils.py                 # INI configuration file utilities (load, save, get, set, merge sections)
weakref_utils.py            # Weak reference utilities for managing weak references to objects
argparse_utils.py           # Argument parsing utilities
warnings_utils.py           # Utilities wrapping the standard library warnings module
compression_utils.py       # Compression and decompression utilities (gzip, bz2, zip, tar)
gzip_utils.py               # Gzip compression/decompression utilities wrapping stdlib gzip
mailcap_utils.py            # Mailcap utilities wrapping stdlib mailcap
ip_utils.py                # IP address validation and manipulation utilities
regex_utils.py             # Regular expression utilities (compile, match, search, replace, split, escape)
terminal_utils.py          # Terminal output utilities (ANSI color, progress bars, clear screen, prompts)
subprocess_utils.py         # Subprocess utilities (run_command, check_output, check_call)
webbrowser_utils.py         # Web browser utilities wrapping stdlib webbrowser (open_url, open_new, open_new_tab, get_controller, register_browser, register_standard_browsers)
xmlrpc_utils.py             # XML-RPC utilities wrapping stdlib xmlrpc (dumps_value, loads_value, build_request, parse_method_call, parse_method_response, create_proxy, create_server)
syslog_utils.py             # System logging utilities wrapping stdlib syslog (open_log, log_message, close_log, set_log_mask, log_mask, log_upto, priority_name, facility_name)
faulthandler_utils.py        # Fault handler utilities wrapping stdlib faulthandler (enable, disable, is_enabled, dump_traceback, dump_traceback_later, cancel_dump_traceback_later, register, unregister)
resource_utils.py            # Resource usage utilities wrapping stdlib resource (get_rlimit, set_rlimit, prlimit, get_rusage, get_page_size, limit_names, limit_value, limit_name, usage_names, usage_as_dict, is_available)
pwd_utils.py                 # Password database utilities wrapping stdlib pwd (getpwuid, getpwnam, getpwall)
grp_utils.py                 # Group database utilities wrapping stdlib grp (getgrgid, getgrnam, getgrall)
termios_utils.py             # Terminal attribute utilities wrapping stdlib termios (get_attributes, set_attributes, make_raw, make_cbreak, get_window_size, set_window_size)
fcntl_utils.py               # File control utilities wrapping stdlib fcntl (flock, lockf, control, ioctl, duplicate_fd, file_lock)
pty_utils.py                 # Pseudo-terminal utilities wrapping stdlib pty (openpty, open_terminal, master_open, slave_open, fork, spawn, is_available)
stringprep_utils.py          # String preparation utilities wrapping stdlib stringprep (in_table, map_table, is_prohibited, is_allowed, map_text)
site_utils.py               # Site configuration utilities wrapping stdlib site (get_site_packages, get_user_base, get_user_site_packages, is_user_site_enabled)
tabnanny_utils.py            # Tabnanny utilities wrapping stdlib tabnanny (check, process_tokens, NannyNag)
encodings_utils.py           # Encoding name utilities wrapping stdlib encodings (normalize_encoding, is_known_encoding, is_alias, encoding_aliases, all_aliases, all_encodings)
zipimport_utils.py           # Zip archive import utilities wrapping stdlib zipimport (zip_importer, archive_names, get_source, get_code, get_filename, get_data, is_package, find_spec, invalidate_caches)
genericpath_utils.py         # Generic path utilities wrapping stdlib genericpath (exists, isfile, isdir, islink, commonprefix, getsize, getmtime, getatime, getctime, samefile)
posixpath_utils.py           # Posixpath utilities wrapping stdlib posixpath (abspath, basename, dirname, join, split, splitext, normpath, realpath, relpath, isabs, exists)
ntpath_utils.py              # Windows path utilities wrapping stdlib ntpath (splitdrive, splitroot, normcase, normpath, has_drive, is_unc_path, is_device_path, to_slashes)
nturl2path_utils.py         # URL to pathname conversions wrapping stdlib nturl2path (url2pathname, pathname2url)
curses_utils.py             # Terminal handling utilities wrapping stdlib curses (initscr, endwin, cbreak, echo, raw, colors)
bdb_utils.py                 # Debugger framework utilities wrapping stdlib bdb (create_bdb, set_breakpoint, clear_breakpoint, get_breakpoints, effective_breakpoint, checkfuncname)
pdb_utils.py                 # Interactive debugger utilities wrapping stdlib pdb (create_pdb, set_trace, post_mortem, pm, run, runeval, runctx, runcall)
ipaddress_utils.py           # IP address utilities wrapping stdlib ipaddress (ip_address, ip_network, ip_interface, is_valid_address, network_hosts, subnets, summarize_addresses)
pydoc_utils.py               # Documentation utilities wrapping stdlib pydoc (render_doc, doc, writedoc, writedocs, apropos, locate, resolve, safeimport, importfile, getdoc, synopsis, source_synopsis, describe, classify_class_attrs, classname, parentname, visiblename, isdata, ispackage, ispath, allmethods, splitdoc, stripid, replace, cram, plain, cli, help, getpager, browse) with input validation
pydoc_data_utils.py          # Documentation topic utilities wrapping stdlib pydoc_data (count_topics, get_topic, get_topic_names, get_topic_section, get_topic_sections, get_topic_title, get_topics, get_topics_subset, has_topic, search_topics, wrap_topic) with input validation
antigravity_utils.py         # Antigravity utilities wrapping the standard library antigravity module (geohash, fly, get_xkcd_url) with input validation
wsgiref_utils.py              # WSGI utilities wrapping the standard library wsgiref package (setup_testing_defaults, guess_scheme, application_uri, request_uri, shift_path_info, is_hop_by_hop, build_headers, header_values, encode_headers, file_wrapper, check_environ, environ_errors, validator, demo_app, make_server) with input validation
venv_utils.py                 # Virtual environment utilities wrapping the standard library venv package (create_environment, describe_environment, read_configuration, environment_paths, environment_python, activation_scripts, is_environment, find_environments, run_cli) with input validation
ensurepip_utils.py            # Bootstrap utilities wrapping the standard library ensurepip package (bootstrap, bundled_wheel, pip_version, is_pip_installed, run_cli, is_available) with input validation
readline_utils.py             # Command line editing utilities wrapping the standard library readline module (add_history, append_history_file, clear_history, get_history_item, remove_history_item, replace_history_item, history_items, search_history, make_completer, is_available) with input validation
builtins_utils.py             # Builtin utilities wrapping the standard library builtins module (absolute, all_true, any_true, ascii_str, binary_string, boolean, callable_object, character, divmod_pair, format_value, get_hash, hex_string, is_instance, is_subclass, iterator, length, maximum, minimum, octal_string, ordinal, power, representation, round_number, sorted_list, summation) with input validation
imghdr_utils.py               # Image format detection utilities wrapping the standard library imghdr module (detect, is_available, is_image, matching_formats, read_header, register_test, supported_formats, unregister_test, what) with input validation
posix_utils.py                # POSIX interface utilities wrapping the standard library posix module (open_fd, close_fd, read_fd, read_exactly, write_fd, write_all, create_pipe, file_info, create_directory, remove_path, scheduler_policy, describe_wait_status, is_available) with input validation
tests/                     # Python unit tests
  test_abc_utils.py          # Tests for abc_utils.py
  test_ast_utils.py          # Tests for ast_utils.py
  test_async_utils.py         # Tests for async_utils.py
  test_asyncio_utils.py   # Tests for asyncio_utils.py
  test_array_utils.py        # Tests for array_utils.py
  test_base64_utils.py        # Tests for base64_utils.py
  test_binascii_utils.py      # Tests for binascii_utils.py
  test_bisect_utils.py       # Tests for bisect_utils.py
  test_case_utils.py         # Tests for case_utils.py
  test_trace_utils.py        # Tests for trace_utils.py
  test_bit_utils.py           # Tests for bit_utils.py
  test_bytes_utils.py         # Tests for bytes_utils.py
  test_circuit_breaker_utils.py   # Tests for circuit_breaker_utils.py
  test_cache_utils.py         # Tests for cache_utils.py
  test_memoize_utils.py      # Tests for memoize_utils.py
  test_maybe_utils.py         # Tests for maybe_utils.py
  test_either_utils.py        # Tests for either_utils.py
  test_calculator.py          # Tests for calculator.py
  test_calendar_utils.py      # Tests for calendar_utils.py
  test_chunk_utils.py         # Tests for chunk_utils.py
  test_cgi_utils.py           # Tests for cgi_utils.py
  test_pipes_utils.py          # Tests for pipes_utils.py
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
ftplib_utils.py            # Ftplib utilities wrapping stdlib ftplib (FTP, FTP_TLS, create_ftp, create_ftp_tls, connect_ftp, parse257, parse150, parse227, parse229)
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
poplib_utils.py            # Poplib utilities wrapping stdlib poplib (POP3, POP3_SSL, create_pop3, create_pop3_ssl, connect_pop3)
asynchat_utils.py         # Asynchronous chat utilities wrapping stdlib asynchat (async_chat, find_prefix_at_end, simple_producer)
asyncore_utils.py         # Asynchronous socket services utilities wrapping stdlib asyncore (dispatcher, dispatcher_with_send, file_dispatcher, file_wrapper, loop, socket_map, read/write, close_all, poll variants, ExitNow, errorcode)
smtpd_utils.py            # SMTP server utilities wrapping stdlib smtpd (SMTPServer, DebuggingServer, PureProxy, SMTPChannel, create_smtp_server, create_debugging_server, create_pure_proxy, process_message)
  test_pattern_utils.py       # Tests for pattern_utils.py
  test_pprint_utils.py        # Tests for pprint_utils.py
test_reprlib_utils.py       # Tests for reprlib_utils.py
test_traceback_utils.py     # Tests for traceback_utils.py
test_tracemalloc_utils.py   # Tests for tracemalloc_utils.py
test_tty_utils.py           # Tests for tty_utils.py
test_doctest_utils.py       # Tests for doctest_utils.py
test_symtable_utils.py      # Tests for symtable_utils.py
test_profile_utils.py        # Tests for profile_utils.py
test_pstats_utils.py         # Tests for pstats_utils.py
test_cprofile_utils.py       # Tests for cprofile_utils.py
 test_select_utils.py         # Tests for select_utils.py
 test_imaplib_utils.py        # Tests for imaplib_utils.py
 test_mailbox_utils.py        # Tests for mailbox_utils.py

mailbox_utils.py             # Mailbox utilities wrapping stdlib mailbox (create_* factories)
 test_mailbox_utils.py        # Tests for mailbox_utils.py
test_unittest_utils.py       # Tests for unittest_utils.py
test_typing_utils.py        # Tests for typing_utils.py
test_pickle_utils.py        # Tests for pickle_utils.py
        test_pickletools_utils.py # Tests for pickletools_utils.py
  test_plistlib_utils.py      # Tests for plistlib_utils.py
  test_prime_utils.py         # Tests for prime_utils.py
  test_modulefinder_utils.py   # Tests for modulefinder_utils.py
  test_optparse_utils.py       # Tests for optparse_utils.py
  test_pyclbr_utils.py         # Tests for pyclbr_utils.py
  test_pyexpat_utils.py        # Tests for pyexpat_utils.py
  test_xdrlib_utils.py         # Tests for xdrlib_utils.py
  test_smtplib_utils.py        # Tests for smtplib_utils.py
  test_sunau_utils.py          # Tests for sunau_utils.py
  test_priority_queue_utils.py # Tests for priority_queue_utils.py
  test_prompt_utils.py        # Tests for prompt_utils.py
  test_queue_utils.py         # Tests for queue_utils.py
  test_random_utils.py        # Tests for random_utils.py
  test_roman_utils.py         # Tests for roman_utils.py
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
  test_urllib_utils.py        # Tests for urllib_utils.py
  test_utils.py               # Tests for utils.py
  test_uuid_utils.py          # Tests for uuid_utils.py
  test_validation_utils.py    # Tests for validation_utils.py
  test_version_utils.py       # Tests for version_utils.py
  test_semver_utils.py        # Tests for semver_utils.py
  test_interval_utils.py      # Tests for interval_utils.py
  test_venv_utils.py          # Tests for venv_utils.py
  test_audioop_utils.py       # Tests for audioop_utils.py
  test_ensurepip_utils.py     # Tests for ensurepip_utils.py
  test_readline_utils.py      # Tests for readline_utils.py
  test_builtins_utils.py      # Tests for builtins_utils.py
  test_imghdr_utils.py        # Tests for imghdr_utils.py
  test_posix_utils.py         # Tests for posix_utils.py
  test_telnetlib_utils.py     # Tests for telnetlib_utils.py
  test_sre_constants_utils.py # Tests for sre_constants_utils.py
  test_sre_parse_utils.py     # Tests for sre_parse_utils.py
  test_spwd_utils.py           # Tests for spwd_utils.py
 test_weakref_utils.py       # Tests for weakref_utils.py
    test_warnings_utils.py      # Tests for warnings_utils.py
    test_webbrowser_utils.py    # Tests for webbrowser_utils.py
    test_xml_utils.py           # Tests for xml_utils.py
    test_xmlrpc_utils.py        # Tests for xmlrpc_utils.py
    test_syslog_utils.py        # Tests for syslog_utils.py
    test_faulthandler_utils.py   # Tests for faulthandler_utils.py
    test_resource_utils.py       # Tests for resource_utils.py
    test_pwd_utils.py            # Tests for pwd_utils.py
    test_grp_utils.py            # Tests for grp_utils.py
    test_termios_utils.py        # Tests for termios_utils.py
    test_fcntl_utils.py          # Tests for fcntl_utils.py
    test_pty_utils.py            # Tests for pty_utils.py
    test_stringprep_utils.py     # Tests for stringprep_utils.py
    test_site_utils.py           # Tests for site_utils.py
    test_tabnanny_utils.py       # Tests for tabnanny_utils.py
    test_zipimport_utils.py      # Tests for zipimport_utils.py
    test_genericpath_utils.py    # Tests for genericpath_utils.py
    test_posixpath_utils.py      # Tests for posixpath_utils.py
    test_ntpath_utils.py         # Tests for ntpath_utils.py
    test_nturl2path_utils.py    # Tests for nturl2path_utils.py
    test_curses_utils.py        # Tests for curses_utils.py
    test_bdb_utils.py           # Tests for bdb_utils.py
    test_pdb_utils.py           # Tests for pdb_utils.py
    test_ipaddress_utils.py     # Tests for ipaddress_utils.py
    test_pydoc_utils.py          # Tests for pydoc_utils.py
    test_pydoc_data_utils.py     # Tests for pydoc_data_utils.py
    test_antigravity_utils.py    # Tests for antigravity_utils.py
    test_wsgiref_utils.py         # Tests for wsgiref_utils.py
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
 test_mailcap_utils.py       # Tests for mailcap_utils.py
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
    test_opcode_utils.py       # Tests for opcode_utils.py
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
The project includes backoff utilities in `backoff_utils.py`: `constant_backoff`, `exponential_backoff`, and `backoff_delay`. The module is tested in `tests/test_backoff_utils.py`.
The project includes hostname utilities in `hostname_utils.py`: `is_valid_hostname` validates an RFC 1123 hostname, `normalize_hostname` lowercases and strips a trailing dot, `get_local_hostname` returns the local machine hostname, `is_fully_qualified` reports whether a hostname is fully qualified, and `split_hostname` returns the DNS labels. All functions validate their inputs and raise ``TypeError`` or ``ValueError`` on invalid arguments. The module is tested in `tests/test_hostname_utils.py`.

The project includes AIFF and AIFF-C format utilities in `aifc_utils.py` wrapping the standard library `aifc` module: `open` opens an AIFF file and returns an `Aifc_read` or `Aifc_write` object, `is_available` reports whether the interpreter ships the module, and aliases `open_aifc`, `read_aifc`, `write_aifc`, `open_read`, and `open_write` are provided. The classes `Aifc_read`, `Aifc_write`, and `Error` are re-exported. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The `aifc` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_aifc_utils.py`.

## OSS Audio Device Utilities Module

The project includes OSS audio device utilities in `ossaudiodev_utils.py` wrapping the standard library `ossaudiodev` module: `open` and `openmixer` are re-exported callables, `OSSAudioError` and `error` are re-exported, and `AFMT_S16_LE` and `SOUND_MIXER_PCM` are re-exported constants. The module is tested in `tests/test_ossaudiodev_utils.py`.

## AST Utilities Module

The project includes abstract syntax tree utilities in `ast_utils.py` wrapping the standard library `ast` module: `parse` parses source code into a syntax tree with input validation, `unparse` converts a syntax tree back to source, `dump` returns a string representation of a node, `literal_eval` safely evaluates a literal expression, `get_docstring` extracts a docstring from a function node, `walk` iterates over all descendant nodes, `iter_fields` and `iter_child_nodes` iterate over fields and direct children, `find_all` returns all nodes matching a type, `fix_missing_locations` assigns line numbers to nodes, `increment_lineno` shifts line numbers, `copy_location` copies source location between nodes, and `node_to_string` unparses a node to a string. The module is tested in `tests/test_ast_utils.py`.

## Pickle Utilities Module

The project includes object serialization utilities in `pickle_utils.py` wrapping the standard library `pickle` module: `dump` and `dumps` serialize objects to a binary file and bytes respectively, `load` and `loads` deserialize objects from a binary file and bytes, `pickler` and `unpickler` return streaming :class:`pickle.Pickler` and :class:`pickle.Unpickler` instances, `is_valid_protocol` reports whether a protocol number is supported, and `validate_protocol` normalizes a protocol argument (defaulting to the highest protocol) and raises `TypeError` for non-ints and `ValueError` for unsupported values. The module is tested in `tests/test_pickle_utils.py`.

## Pickletools Utilities Module

The project includes pickletools utilities in `pickletools_utils.py` wrapping the standard library `pickletools` module: `dis`, `genops`, `optimize`, `get_opcode_info`, `list_opcodes`, `is_opcode`, `get_pickle_size`, `decode_long`, `encode_long`. The module is tested in `tests/test_pickletools_utils.py`.

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

### Developer Commands

The `Makefile` bundles the common development tasks:

| Command | Description |
| --- | --- |
| `make test` | Run the Python test suite (pytest, with a unittest fallback) |
| `make lint` | Run the ruff code style checker |
| `make typecheck` | Run the mypy static type checker |
| `make run` | Run `hello.py` (`make run NAME=Alice` passes a name) |
| `make scaffold` | Scaffold a new project using `scaffold.sh` |
| `make refresh-scaffold` | Refresh the file copies embedded in `scaffold.sh` from the repository sources |
| `make pre-commit-install` | Install the pre-commit hooks into `.git/hooks` |
| `make pre-commit-run` | Run all pre-commit hooks against the tracked files |
| `make clean` | Remove the build artifacts |
| `make help` | Show all available targets |

## Calculator Module

The project includes a simple calculator module in `calculator.py` with functions for basic arithmetic operations: add, subtract, multiply, and divide. The module is tested in `tests/test_calculator.py`.

## Shapes Module

The project includes a geometry utilities module in `shapes.py` with functions for calculating the area and perimeter of circles, rectangles, triangles, and polygons. Circular sectors and arcs are supported via `sector_area` and `arc_length`, regular polygons via `regular_polygon_area` and `regular_polygon_perimeter`, and ellipses via `ellipse_area` and `ellipse_circumference`. `triangle_heron_area` computes area via Heron's formula, and `triangle_inradius` and `triangle_circumradius` return inradius and circumradius. 3D helpers include `sphere_surface_area`/`sphere_volume`, `cube_surface_area`/`cube_volume`, `cuboid_surface_area`/`cuboid_volume` (and `rectangular_prism_surface_area`/`rectangular_prism_volume` aliases), `cylinder_surface_area`/`cylinder_volume`, and `cone_surface_area`/`cone_volume`. Input validation enforces non-negative dimensions and the triangle inequality. The module is tested in `tests/test_shapes.py`.

## Strings Module

The project includes a string utilities module in `strings.py` with functions for common text operations: `reverse_string`, `reverse_words`, `is_palindrome`, `count_vowels`, `count_consonants`, `count_lowercase`, `count_uppercase`, `count_digits`, `count_letters`, `count_punctuation`, `truncate`, `levenshtein_distance`, `title_case`, `camel_to_snake`, `snake_to_camel`, `word_count`, `slugify`, `pad_left`, `pad_right`, `center`, `lstrip_chars`, `rstrip_chars`, `strip_chars`, `strip_non_ascii`, `truncate_bytes`, `is_alpha`, `is_alphanumeric`, `is_binary`, `is_ascii`, `is_digit`, `is_hex`, `is_integer`, `is_whitespace`, `is_space`, `is_printable`, `is_identifier`, `is_pangram`, `is_rotation`, `is_subsequence`, `is_title`, `is_upper`, `is_lower`, `swap_case`, `count_occurrences`, `first_n`, `last_n`, `take`, `drop`, `between`, `contains_any`, `contains_all`, `count_words`, `remove_punctuation`, `remove_digits`, `remove_blank_lines`, `chunk_string`, `initials`, `common_prefix`, `common_suffix`, `char_frequency`, `remove_whitespace`, `normalize_whitespace`, `starts_with`, `ends_with`, `removeprefix`, `removesuffix`, `partition`, `rpartition`, `split_lines`, `join_lines`, `replace_many`, `strip_html`, and `is_blank`. Added `chunk_string` for splitting strings into fixed-size chunks. The `is_palindrome` function is case-insensitive and ignores non-alphanumeric characters. The `take` helper is an alias for `first_n` and `drop` returns all but the first *n* characters, both validating that *n* is a non-negative integer. The module is tested in `tests/test_strings.py`.

## Statistics Module

The project includes a statistics utilities module in `stats.py` with functions for common statistical operations: `mean`, `median`, `median_low`, `median_high`, `median_grouped`, `mode`, `multimode`, `min_value`, `max_value`, `midrange`, `product`, `trimmed_mean`, `variance`, `pvariance`, `stddev`, `pstdev`, `skewness`, `kurtosis`, `mean_absolute_deviation`, `median_absolute_deviation`, `midhinge`, `quantile`, `covariance`, and `correlation`. The module supports both population and sample variance/stddev calculations. `median_grouped` estimates the median of grouped continuous data using the class interval approach. `covariance` computes the covariance between two paired lists (population or sample), and `correlation` returns the Pearson correlation coefficient ranging from -1 to 1. `trimmed_mean` discards a configurable number of values from each end of the sorted list before averaging, making it robust to outliers. `z_scores` returns the standardized z-scores of the values, measuring how many standard deviations each value is from the mean. `root_mean_square` returns the square root of the arithmetic mean of the squared values. `standard_error` returns the standard error of the mean, the sample standard deviation divided by the square root of the sample size (raising `ValueError` for lists with fewer than two elements). `range` returns the difference between the maximum and minimum values. `sum_values` returns the sum of all values, `sum_of_squares` the sum of the squared values, and `sum_of_cubes` the sum of the cubed values. `cumulative_sum` returns the running totals of the values, a list whose i-th element is the sum of the first i+1 elements (empty input yields an empty list). `coefficient_of_variation` returns the ratio of the standard deviation to the mean. `geometric_mean` and `harmonic_mean` compute the geometric and harmonic means respectively, both requiring strictly positive inputs. Input validation ensures appropriate errors for empty lists or invalid inputs. The module is tested in `tests/test_stats.py`.

The project includes a Roman numeral conversion utilities module in `roman_utils.py` with functions `to_roman`, `from_roman`, and `is_valid_roman` for converting between integers and Roman numerals in the range 1 to 3999. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_roman_utils.py`.

## License

MIT

## Math Utilities Module

The project includes a mathematical utilities module in `math_utils.py` with functions for common mathematical operations: `factorial`, `fibonacci`, `gcd`, `lcm`, `is_prime`, `is_composite`, `clamp`, and `is_even`. It also provides `combination` and `permutation` for combinatorial calculations. The module is tested in `tests/test_math_utils.py`.

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

## URL Parsing Utilities Module

The project includes URL parsing utilities in `urllib_utils.py` wrapping the standard library `urllib.parse` module: `parse_url` splits a URL into its scheme, netloc, path, parameters, query, and fragment, `build_url` and `urlunsplit` assemble a URL from its components, `urlsplit` splits a URL without separating the parameters, `join_url` resolves a relative reference against a base URL, `quote` and `quote_plus` percent-encode text, `unquote`, `unquote_plus`, and `unquote_to_bytes` decode percent-encoded text, `urlencode` encodes a mapping or a sequence of pairs into a query string, `parse_qs` and `parse_qsl` parse a query string, and `defrag` removes the fragment from a URL. Every helper validates its arguments before the standard library is reached. The module is tested in `tests/test_urllib_utils.py`.

## Configuration Utilities Module

The project includes a configuration utilities module in `config_utils.py` with functions for loading, saving, and manipulating configuration files: `load_config`, `save_config`, `get_config_value`, `set_config_value`, and `merge_configs`. The module currently supports JSON format and is tested in `tests/test_config_utils.py`.

## Random Utilities Module

The project includes a random utilities module in `random_utils.py` with functions for random number generation and sampling: `random_int`, `random_choice`, `random_sample`, `random_shuffle`, `weighted_choice`, `random_choices` (with replacement, alias `random_choice_with_replacement`), `random_uniform`, `random_gaussian`, `random_bool`, and `coin_flip`. Every function accepts an optional `seed` argument for reproducible results and validates its inputs. The module is tested in `tests/test_random_utils.py`.

## Validation Utilities Module

The project includes a validation utilities module in `validation_utils.py` with functions for common input validation: `is_email`, `is_numeric`, `is_integer`, `is_alphanumeric`, `is_boolean_string`, `is_none_or_empty`, `min_length`, `max_length`, `matches_regex`, and `is_valid_hostname`. The module is tested in `tests/test_validation_utils.py`.

## Cryptographic Utilities Module

The project includes a cryptographic utilities module in `crypto_utils.py` with functions for hashing and encoding: `hash_string`, `generate_token`, `base64_encode`, and `base64_decode`. The module is tested in `tests/test_crypto_utils.py`.

## List Utilities Module

The project includes an advanced list manipulation utilities module in `list_utils.py` with functions for common list operations: `partition`, `group_by`, `safe_get`, `find`, `drop`, `take`, `intersperse`, and `chunks`. Input validation ensures all functions raise `TypeError` when a non-list is passed. The module is tested in `tests/test_list_utils.py`.

## Locale Utilities Module

The project includes a locale utility functions module in `locale_utils.py` with helpers for working with locale identifiers and language tags: `normalize_locale` normalizes a locale string to `language_REGION` form, `language_code` extracts the language code, `region_code` extracts the region code, and `is_valid_locale` checks whether a string looks like a valid locale identifier. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_locale_utils.py`.

## Environment Utilities Module

The project includes an environment variable utilities module in `env_utils.py` with functions for reading, writing, and parsing environment variables: `get_env`, `get_env_required`, `get_env_int`, `get_env_float`, `get_env_bool`, `set_env`, `ensure_env`, `unset_env`, and `prefix_env`. Typed accessors parse values as `int`, `float`, and `bool`, with required-variable and default fallbacks. The module is tested in `tests/test_env_utils.py`.

## Logging Utilities Module

The project includes a logging utilities module in `logging_utils.py` with helpers for logging configuration and function-call tracing: `get_logger` returns a named logger (or the root logger), `configure_logging` configures the root logger with a consistent format, handlers, and level, and `log_calls` is a decorator factory that logs function entry and return values using `functools.wraps` to preserve metadata. The module is tested in `tests/test_logging_utils.py`.

## Cache Utilities Module

The project includes a caching utilities module in `cache_utils.py` with helpers for memoizing function results: `memoize` is a decorator factory that caches return values keyed by call arguments (with optional `maxsize` LRU eviction and `typed` argument distinction), `clear_cache` invalidates the cache of a memoized function, and `cache_info` returns a dictionary with `hits`, `misses`, `maxsize`, and `currsize` statistics. Decorated functions also expose `clear_cache` and `cache_info` attributes for direct introspection. The module is tested in `tests/test_cache_utils.py`.

## Memoization Utilities Module

The project includes a lightweight memoization utilities module in `memoize_utils.py` providing a single `memoize` decorator that caches a function's return values keyed by its positional and keyword arguments. Unlike `cache_utils.memoize`, this decorator takes the function directly (not as a factory) and exposes a `cache_clear` method on the wrapped callable to empty the cache. It validates that its argument is callable and raises `TypeError` otherwise. Maybe/Option type utilities are also provided in `maybe_utils.py` for functional programming patterns: `Maybe` represents an optional value with `some`, `nothing`, and `from_optional` constructors. It provides `is_some`, `is_nothing`, `unwrap`, `unwrap_or`, `unwrap_or_else`, `map`, `flat_map`, `and_then`, `filter`, `or_else`, `map_or`, and `map_or_else`. All operations are safe and return `Maybe` types for composable error handling. Either/Result type utilities are also provided in `either_utils.py` for functional programming patterns: `Either` represents one of two values with `right`, `left`, `ok`, `err`, and `from_optional` constructors. It provides `is_right`, `is_left`, `is_ok`, `is_err`, `unwrap`, `unwrap_left`, `unwrap_or`, `unwrap_or_else`, `map`, `map_left`, `flat_map`, `and_then`, `or_else`, `fold`, and `swap`. All operations are safe and return `Either` types for composable error handling. The modules are tested in `tests/test_memoize_utils.py`, `tests/test_maybe_utils.py`, and `tests/test_either_utils.py`.

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

The project includes a string utilities module in `string_utils.py` with advanced string manipulation functions: `slugify`, `camel_to_snake`, `snake_to_camel`, `is_isogram`, `pluralize`, `truncate`, `wrap_text`, `wrap_words`, `indent_text`, `remove_extra_whitespace`, `remove_blank_lines`, `truncate_words`, `title_case`, and `dedent_text`. `wrap_words` is a word-aware wrapper that greedily packs words into lines (optionally breaking long words), while `truncate_words` truncates to a maximum number of words. `is_isogram` checks whether a string contains no repeating letters. `dedent_text` is the inverse of `indent_text`: it removes the common leading whitespace from every line. Each function validates its inputs and raises `TypeError` for non-string arguments where appropriate. The module is tested in `tests/test_string_utils.py`.

## Type Utilities Module

The project includes a type introspection utilities module in `type_utils.py` with functions for inspecting Python type objects: `is_optional` detects `Optional[T]` / `Union[T, None]`, `is_union` detects any `Union` type, `is_generic` detects generic aliases like `List[int]`, `get_type_args` returns the type arguments of a generic, `type_name` produces a human-readable name for a type, `is_subclass_safe` checks subclass relationships without raising `TypeError`, `is_literal` detects `Literal[...]` type aliases, `is_type_var` detects `typing.TypeVar` instances, `is_class_var` detects `typing.ClassVar` aliases, `is_callable` detects `Callable` type aliases (bare and parameterized, e.g. `Callable[[int], str]`), `is_tuple` detects `Tuple` aliases, `is_list_type` detects `List` aliases, `is_dict_type` detects `Dict` aliases, `is_none_type` detects `NoneType`, `is_any` detects `typing.Any`, `unwrap_optional` returns the inner type of an `Optional[...]`, and `get_origin_name` returns the name of a generic type's origin. The module is tested in `tests/test_type_utils.py`.

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

## Cooldown Utilities Module

The project includes a cooldown and throttling utilities module in `cooldown_utils.py` for rate-limiting function calls. The `Cooldown` class enforces a minimum interval between calls to a callable: `ready()` reports whether a call is allowed right now, `remaining()` returns the seconds left before the next call is allowed, `call()` invokes the callable when the interval has elapsed and raises `TimeoutError` otherwise, and `__call__` wraps a callable so every invocation respects the cooldown. The `cooldown` decorator limits a function to one call per interval, and `is_available` reports that the module has no external dependencies. The class is thread-safe, so a single instance can be shared across threads. The module is tested in `tests/test_cooldown_utils.py`.

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

The project includes prompt utility functions in `prompt_utils.py` for working with text prompts: `truncate_prompt`, `format_prompt_template`, `clean_prompt`, `extract_keywords`, `extract_placeholders`, `has_placeholders`, `wrap_prompt`, `estimate_token_count`, `count_words`, `collapse_blank_lines`, `count_blank_lines`, `count_placeholders`, `count_sentences`, `truncate_words`, `truncate_lines`, `indent_lines`, `dedent_lines`, `remove_blank_lines`, `rstrip_lines`, `lstrip_lines`, `strip_lines`, `ensure_trailing_newline`, `normalize_line_endings`, `    first_line`, `last_line`, `count_lines`, `count_non_blank_lines`, `count_trailing_newlines`, `count_paragraphs`, `count_characters`, `count_non_whitespace_characters`, `count_whitespace_characters`, `count_digits`, `reverse_lines`, `strip_blank_lines`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_prompt_utils.py`.

## Regex Utilities Module

The project includes regular expression utilities in `regex_utils.py` for safe regex compilation, matching, extraction, and manipulation: `compile_pattern`, `is_valid_pattern`, `match_pattern`, `search_pattern`, `find_all`, `replace_pattern`, `split_pattern`, `escape_pattern`, `extract_groups`, and `named_groups`. The module is tested in `tests/test_regex_utils.py`.


## Regular Expression Utilities Module (re_utils)

The project includes regular expression utilities in `re_utils.py` wrapping the standard library `re` module: `find_all` returns all non-overlapping matches as strings, `find_matches` returns `re.Match` objects, `search` and `match` find patterns, `full_match` requires the entire string to match, `split` splits by pattern, `sub` and `subn` substitute matches with strings or callables, `compile_regex` compiles a regex pattern with optional flags, and `escape` escapes special characters. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_re_utils.py`.

## Rlcompleter Utilities Module

The project includes interactive tab completion utilities in `rlcompleter_utils.py` wrapping the standard library `rlcompleter` module: `Completer` wraps the standard library completer with input validation, and `complete` returns the *state*-th completion for *text* in a namespace. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_rlcompleter_utils.py`.

## Tree Utilities Module

The project includes tree and nested structure utilities in `tree_utils.py` for getting, setting, deleting, flattening, unflattening, mapping, and filtering nested structures: `get_nested`, `set_nested`, `delete_nested`, `flatten_tree`, `unflatten_tree`, `map_tree`, and `filter_tree`. The module is tested in `tests/test_tree_utils.py`.

## UUID Utilities Module

The project includes UUID utility functions in `uuid_utils.py` for generating and validating UUIDs: `generate_uuid`, `generate_uuid4`, `generate_uuid1`, `is_valid_uuid`, and `parse_uuid`. The module is tested in `tests/test_uuid_utils.py`.

## Utils Module

The project includes general utility helper functions in `utils.py`: `flatten`, `chunk`, `unique`, `is_empty`, `remove_none`, `last`, `first`, and `second`. The module is tested in `tests/test_utils.py`.

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

## HTML Parser Utilities Module

The project includes HTML parser utilities in `html_parser_utils.py` wrapping the standard library `html.parser` module: `HTMLParser` is re-exported for custom parsing, `strip_tags` removes all HTML tags leaving only text content, and `parse_html` creates and feeds a parser with optional custom handlers for start/end tags, data, comments, entities, declarations, and processing instructions. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_html_parser_utils.py`.


## HTML Entities Utilities Module

The project includes HTML entities utilities in `html_entities_utils.py` wrapping the standard library `html.entities` module: `name2codepoint`, `codepoint2name`, `entitydefs`, and `html5` are re-exported, with helpers `name_to_codepoint`/`get_entity_by_name` to look up entity names, `codepoint_to_name` to look up names from codepoints, and `decode_entity`/`unescape_entity` to decode named entities to characters. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_html_entities_utils.py`.


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

## Case Conversion Utilities Module

The project includes case conversion utilities in `case_utils.py`: `kebab_case` converts text to kebab-case, `pascal_case` converts text to PascalCase, `constant_case` converts text to CONSTANT_CASE, `snake_case` converts text to snake_case, `camel_case` converts text to camelCase, `screaming_snake_case` is an alias for `constant_case`, `spinal_case` is an alias for `kebab_case`, `train_case` is an alias for `pascal_case`, `dot_case` converts text to dot.case, `slash_case` converts text to slash/case, `title_case` converts text to Title Case, and `sentence_case` converts text to sentence case. Words are split on whitespace, separators, and case transitions such as camelCase and PascalCase boundaries. All functions validate their inputs and raise `TypeError` for non-string arguments. The module is tested in `tests/test_case_utils.py`.

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

The project includes sequence utilities in `seq_utils.py` for common sequence operations: `first`, `last`, and `nth` retrieve elements by position (returning `None` when absent or out of range); `head` and `tail` return leading or trailing elements; `split_at` divides a sequence at an index; `take_while` and `drop_while` consume elements based on a predicate; `interleave` round-robins elements from multiple sequences; `adjacent_pairs` forms consecutive pairs; `flatten` removes one level of nesting; `chunk` splits a sequence into fixed-size chunks; and `is_sorted` checks ascending or descending order with an optional key. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_seq_utils.py`.

## Number Utilities Module

The project includes number utility functions in `number_utils.py` for common numeric operations: `clamp` restricts a value to a closed interval, `round_to` rounds a value to a given number of decimal places (banker's rounding), `round_half_up` rounds a value to a given number of decimal places rounding halves away from zero, `is_integer` tests whether a value is integral, `format_number` formats a number with thousands separators and fixed decimals, `percentage` returns a part as a percentage of a total formatted as a string, `lerp` linearly interpolates between two values, `sign` returns the sign of a number, and `is_even`, `is_odd`, `is_negative`, `is_positive`, `is_zero`, `is_non_negative`, `is_non_positive`, `is_between`, `is_close`, `is_finite`, `is_infinite`, and `is_nan` test integer-valued, parity, sign, range, and special floating-point properties; `digit_sum` returns the sum of the decimal digits of an integer; `digit_count` returns the number of decimal digits of an integer; `is_perfect_number` tests whether a positive integer is a perfect number (equal to the sum of its proper divisors); `is_perfect_cube` tests whether a positive integer is a perfect cube; `is_perfect_square` tests whether a non-negative integer is a perfect square; `is_power_of_two` tests whether a positive integer is a power of two; `is_palindromic_number` tests whether an integer is palindromic in base 10; `digital_root` returns the recursive digital root of an integer; `is_triangular_number` tests whether an integer is a triangular number; `is_automorphic_number` tests whether a non-negative integer is automorphic (its square ends with the decimal representation of the number itself, e.g. 5, 6, 25, 76, 376, 625); `is_happy_number` tests whether an integer is a happy number (repeatedly summing the squares of its decimal digits eventually reaches 1); `is_armstrong_number` tests whether an integer is an Armstrong (narcissistic) number; `is_harshad_number` tests whether a positive integer is a Harshad (Niven) number (divisible by the sum of its decimal digits); `is_neon_number` tests whether a non-negative integer is a neon number (the sum of the digits of its square equals the number itself, e.g. 0, 1, 9); `is_strong_number` tests whether a positive integer is a strong number (the sum of the factorials of its decimal digits equals the number itself, e.g. 1, 2, 145, 40585); `is_fibonacci_number` tests whether a non-negative integer is a Fibonacci number (using the closed-form identity that 5n²+4 or 5n²-4 is a perfect square); `is_lucas_number` tests whether an integer is a Lucas number (the sequence defined by L(0)=2, L(1)=1, L(n)=L(n-1)+L(n-2), e.g. 2, 1, 3, 4, 7, 11, 18, 29); `is_pronic_number` tests whether a non-negative integer is a pronic number (a product of two consecutive integers, n*(n+1), e.g. 0, 2, 6, 12, 20); `is_abundant_number` tests whether a positive integer is an abundant number (the sum of its proper divisors exceeds the number itself, e.g. 12, 18, 20); `is_deficient_number` tests whether a positive integer is a deficient number (the sum of its proper divisors is less than the number itself, e.g. 1, 2, 4, 8); `gcd` returns the greatest common divisor of two integers; `lcm` returns the least common multiple of two integers; `ceil_div` returns the ceiling of the division of two integers; `is_divisible_by` and `is_multiple_of` test divisibility; `divides` is an alias for `is_divisible_by`; `is_coprime` reports whether two integers share no common positive factor other than 1; `safe_divide` divides two numbers, returning 0.0 when the denominator is zero; `map_range` and `remap` map a value from one range to another. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_number_utils.py`.

## Operating System Utilities Module

The project includes operating system utilities in `os_utils.py` for inspecting the platform and environment: `get_platform_info` returns system/release/version/machine/processor/Python details, `get_cpu_count` reports the available CPU count, `get_disk_usage` reports total/used/free/percent disk usage, `get_user_home` and `get_username` return the current user's home and login name, `find_executable` locates an executable on ``PATH``, `expand_path` expands ``~`` and environment variables to an absolute path, and `is_executable` checks whether a path exists and is executable. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_os_utils.py`.

## Sorting Utilities Module

The project includes sorting utility functions in `sort_utils.py` for sorting and ordering operations: `is_sorted` checks whether a sequence is sorted, `bubble_sort` and `merge_sort` return new sorted lists, `nth_largest` returns the n-th largest element (1-based), and `top_n` returns the top n items sorted by key. All functions accept an optional `key` and `reverse` argument. The module is tested in `tests/test_sort_utils.py`.

## Graph and Dependency Resolution Utilities Module

The project includes graph and dependency resolution utilities in `graphlib_utils.py` for topological sorting and cycle detection of directed graphs using the standard library `graphlib` module: `topological_sort` returns nodes in dependency order, `has_cycle` detects cycles, `dependency_order` orders items by their dependencies, and `is_valid_ordering` validates a candidate ordering. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_graphlib_utils.py`.

## Version Utilities Module

The project includes version utility functions in `version_utils.py` for parsing, comparing, normalizing, sorting, and bumping dotted version strings: `parse_version` parses a dotted version string into a tuple of integers, `compare_versions` compares two version strings returning -1/0/1, `is_valid_version` returns `True` if a value is a non-empty dotted string of digit components, `get_major_version`/`get_minor_version`/`get_patch_version` extract individual components (returning 0 if missing), `normalize_version` pads or truncates a version to a fixed component count, `sort_versions` sorts a list of version strings in ascending order, `max_version`/`min_version` return the greatest/least version from a list, `bump_major`/`bump_minor`/`bump_patch` increment a specific component (resetting lower-significance components to zero), and `bump_version` dispatches to one of those three based on a `part` argument (`"major"`, `"minor"`, or `"patch"`, defaulting to `"patch"`), and `decrement_major`/`decrement_minor`/`decrement_patch` decrement a specific component (resetting lower-significance components to zero and raising `ValueError` when the component is already 0), and `decrement_version` dispatches to one of those three based on a `part` argument (`"major"`, `"minor"`, or `"patch"`, defaulting to `"patch"`), `is_prerelease`/`get_prerelease` detect and extract prerelease suffixes (separated by `-`), `get_build_metadata` extracts build metadata (separated by `+`), and `strip_prerelease`/`strip_build_metadata`/`strip_metadata` remove suffixes, `is_stable` returns `True` when the major version component is at least 1, and `is_initial_release` returns `True` when the major version component is 0, and `is_compatible` returns `True` when two versions share the same major version component, and `is_version_at_least`/`is_version_at_most`/`is_version_between` report whether a version satisfies lower/upper/bounded comparisons (with aliases `at_least`/`at_most`/`between`/`is_between`), and `is_dev_version` returns `True` when the prerelease tag starts with `dev` (case-insensitive). All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_version_utils.py`.

## Text Wrapping Utilities Module

The project includes text wrapping utility functions in `textwrap_utils.py` for wrapping, shortening, dedenting, indenting, and filling text using the standard library `textwrap` module: `wrap_text`, `shorten_text`, `dedent_text`, `indent_text`, and `fill_text`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_textwrap_utils.py`.

## Prime Number Utilities Module

The project includes prime number utilities in `prime_utils.py` for prime-related operations: `is_prime` checks whether an integer is prime, `is_composite` returns `True` if an integer is composite (a positive integer with more than two divisors; 0, 1, negatives, and primes are not composite), `prime_factors` returns the prime factors of an integer, `nth_prime` returns the nth prime (1-indexed), `primes_up_to` returns all primes up to a limit, `is_coprime` checks whether two integers are coprime (alias `coprime`), `is_circular_prime` tests whether a prime remains prime under every cyclic rotation of its decimal digits, `is_chen_prime` tests whether a prime is a Chen prime (a prime *p* such that *p + 2 is either prime or semiprime), `next_prime` returns the smallest prime greater than or equal to a lower bound, `prev_prime` returns the largest prime less than or equal to an upper bound, `is_perfect_square` tests whether a non-negative integer is a perfect square, `is_power_of_two` tests whether a positive integer is a power of two (1, 2, 4, ...), `is_semiprime` tests whether an integer is a semiprime (product of exactly two prime factors counting multiplicity), `is_squarefree` tests whether an integer is squarefree, `is_prime_power` tests whether a number is a prime power, `is_emirp` tests whether a prime is an emirp, `is_twin_prime` tests whether a prime is a twin prime, `is_palindromic_prime` tests whether a prime is palindromic in base 10, `is_mersenne_prime` tests whether a number is a Mersenne prime, `is_sophie_germain_prime` tests whether a prime is a Sophie Germain prime, `is_safe_prime` tests whether a prime is a safe prime, `sum_of_proper_divisors` returns the sum of proper divisors, `aliquot_sum` is an alias, `is_perfect_number`, `is_abundant_number`, and `is_deficient_number` classify numbers by their abundance, `is_cousin_prime` tests whether a prime differs by 4 from another prime, `is_sexy_prime` tests whether a prime differs by 6 from another prime, `radical` returns the product of the distinct prime factors of an integer (rad(n)), `prime_count` returns the number of primes less than or equal to a limit (the prime counting function π(*n*), returning 0 for any input below 2), `primorial` returns the product of all primes less than or equal to *n* (*n#*), `total_prime_factors` returns the total number of prime factors with multiplicity (Ω(n)), `distinct_prime_factors` returns the number of distinct prime factors (ω(n)), and `largest_prime_factor` returns the largest prime factor of an integer, `is_automorphic` tests whether a non-negative integer is automorphic (its square ends with the decimal representation of the number itself, e.g. 5, 6, 25, 76, 376, 625), `is_truncatable_prime` tests whether a prime remains prime when digits are removed one at a time from either the left or the right (a two-sided truncatable prime, e.g. 3797), `is_pythagorean_prime` tests whether a prime is a Pythagorean prime (a prime of the form 4k + 1), `is_wilson_prime` tests whether a prime *p* satisfies the Wilson congruence modulo *p*² ((p - 1)! ≡ -1 (mod p**2)); the only known Wilson primes are 5, 13, and 563, `is_carmichael_number` tests whether a composite squarefree integer with at least three prime factors satisfies Korselt's criterion (a Fermat pseudoprime to every base coprime to *n*; the smallest is 561), `is_korselt_number` tests whether a composite squarefree integer *n* satisfies Korselt's criterion (for every prime factor *p* of *n*, *p - 1* divides *n - 1*), and `is_giuga_number` tests whether a composite squarefree integer *n* is a Giuga number (for every prime factor *p* of *n*, *p* divides *n // p - 1*; the smallest is 30). All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_prime_utils.py`.


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

The project includes numeric abstract base class utilities in `numbers_utils.py` wrapping the standard library `numbers` module: the module re-exports `Number`, `Complex`, `Real`, `Rational`, and `Integral`, and adds `is_number`, `is_integral`, and `is_perfect_number` predicates. The module is tested in `tests/test_numbers_utils.py`.

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

## Mailcap Utilities Module

The project includes mailcap utilities in `mailcap_utils.py` wrapping the standard library `mailcap` module: `getcaps`, `list_mailcap_files`, `read_mailcap_file`, `parse_line`, `parse_field`, `find_match`, `lookup`, `subst`, and `find_param`. The module is tested in `tests/test_mailcap_utils.py`.

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

## Maybe Utilities Module

The project includes Maybe/Option type utilities in `maybe_utils.py` for functional programming patterns: `Maybe` represents an optional value with `some`, `nothing`, and `from_optional` constructors. It provides `is_some`, `is_nothing`, `unwrap`, `unwrap_or`, `unwrap_or_else`, `map`, `flat_map`, `and_then`, `filter`, `or_else`, and `map_or`. All operations are safe and return `Maybe` types for composable error handling. Either/Result type utilities are also provided in `either_utils.py` for functional programming patterns: `Either` represents one of two values with `right`, `left`, `ok`, `err`, and `from_optional` constructors. It provides `is_right`, `is_left`, `is_ok`, `is_err`, `unwrap`, `unwrap_left`, `unwrap_or`, `unwrap_or_else`, `map`, `map_left`, `flat_map`, `and_then`, `filter`, `or_else`, `fold`, and `swap`. All operations are safe and return `Either` types for composable error handling. The modules are tested in `tests/test_maybe_utils.py` and `tests/test_either_utils.py`.

## Zoneinfo Utilities Module

The project includes IANA timezone utilities in `zoneinfo_utils.py` wrapping the standard library `zoneinfo` module: `zoneinfo_get` returns a `ZoneInfo` for an IANA key and `zoneinfo_available_timezones` returns the set of available keys. The module is tested in `tests/test_zoneinfo_utils.py`.

The project includes opcode utilities in `opcode_utils.py` wrapping the standard library `opcode` module, exposing helpers for stack effects and opcode classification. The module is tested in `tests/test_opcode_utils.py`.

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

The project includes greeting utilities in `greeting_utils.py`: `format_greeting` renders a greeting for a person, `format_names` renders a greeting for a list of people, and `format_farewell` renders a farewell for a person. The module is tested in `tests/test_greeting_utils.py`.

## Importlib Utilities Module

The project includes import utilities in `importlib_utils.py` wrapping the standard library `importlib` module: `import_module` and `reload_module` load and reload modules, `find_spec` and `get_spec` return import specifications, `get_module_name_from_path` derives a module name from a file path, `is_module_available` reports whether a module can be imported, `get_source_file` and `get_loader` describe a module's origin, `get_distribution` and `get_distribution_version` read installed package metadata, `get_entry_points` lists entry points, `read_text` and `read_binary` read package resources, `is_resource` reports resource availability, `path` returns a package's search path, and `get_attr_from_module` and `call_func_from_module` reach into imported modules. The module is tested in `tests/test_importlib_utils.py`.

## Interval Utilities Module

The project includes interval utilities in `interval_utils.py`: `normalize_interval` orders the bounds of an interval, `is_valid_interval` reports whether the bounds are ordered, `interval_contains` tests for containment, `interval_overlaps` tests for overlap, `interval_intersection` and `interval_union` combine two intervals, `merge_intervals` collapses overlapping intervals, `interval_length` measures the span, `interval_midpoint` returns the center of an interval, `interval_distance` reports the gap between two intervals, `interval_is_subset` tests whether one interval lies within another, `interval_shift` translates an interval by a constant, and `interval_symmetric_difference` returns the portions of two intervals that are not shared. The module is tested in `tests/test_interval_utils.py`.

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


## Select Utilities Module

The project includes I/O multiplexing utilities in `select_utils.py` wrapping the standard library `select` module: `select` waits for file descriptors to become readable, writable, or exceptional with input validation, `create_poller` builds a `select.poll` object, `poll_register` registers a file descriptor with an event mask, and `poll_poll` polls for pending events. `PIPE_BUF` is re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_select_utils.py`.


## Symtable Utilities Module

The project includes symbol table utilities in `symtable_utils.py` wrapping the standard library `symtable` module: `build_symbol_table` builds the symbol table of a block of source code, `lookup_symbol_table` analyses the source file of an importable module, `scope_type` reports whether a scope is a module, function, class, annotation, or comprehension, `scope_identifiers` lists the names bound in a scope, `child_scopes` and `iter_scopes` walk the nested scope tree, `find_scope` locates a nested scope by name, `describe_scope` summarizes a scope, `symbol_info` and `symbol_flags` describe how a symbol is used, `namespace_names` lists the names bound in the namespace a symbol introduces, and `free_variables`, `global_names`, `local_names`, `parameter_names`, `imported_names`, `assigned_names`, `referenced_names`, and `nonlocal_names` collect the names of a scope by usage. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_symtable_utils.py`.

## Hello Module

The project includes a sample application entry point in `hello.py`: `main` prints a greeting for the given name and defaults to `"World"`, and running the module directly greets the name given on the command line. The module is tested in `tests/test_hello.py`.


## Imaplib Utilities Module
## Mailbox Utilities Module

The project includes mailbox utilities in `mailbox_utils.py` wrapping the standard library `mailbox` module: factory helpers for mbox/Maildir/MH/MMDF/Babyl mailboxes and message objects, plus exception type checks. The module is tested in `tests/test_mailbox_utils.py`.


The project includes IMAP4 client utilities in `imaplib_utils.py` wrapping the standard library `imaplib` module: `create_imap4` builds an `IMAP4` client, `create_imap4_ssl` builds an `IMAP4_SSL` client, `create_imap4_stream` builds an `IMAP4_stream` client for a local command, `parse_capabilities` reads the capability names a server advertises, `has_capability` reports whether a capability is advertised, `parse_flags` reads the flags of a `FLAGS` response, `parse_fetch_flags` extracts the flags from a `FETCH` response, `format_flags` renders flags in the wire format, `parse_internaldate` reads an `INTERNALDATE` value, `format_internaldate` renders a timestamp as an `INTERNALDATE` value, and `int_to_ap` converts an integer into its `A`-`P` digit representation. `IMAP4`, `IMAP4_SSL`, `IMAP4_stream`, `IMAP4Error`, `IMAP4AbortError`, `IMAP4ReadOnlyError`, `CRLF`, `IMAP4_PORT`, and `IMAP4_SSL_PORT` are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_imaplib_utils.py`.


## Wave Utilities Module

The project includes wave audio utilities in `wave_utils.py` wrapping the standard library `wave` module: `open_read` and `open_write` open WAV files for reading and writing, `wave_info` returns the audio parameters as a dictionary, `read_frames` and `write_frames` transfer raw frame data, `create_writer` builds a configured :class:`wave.Wave_write`, and `get_params`/`set_params` plus the per-field setters inspect and adjust channel count, sample width, frame rate, frame count, and compression type. `Error`, `WAVE_FORMAT_PCM`, and `WAVE_FORMAT_EXTENSIBLE` are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_wave_utils.py`.


## Uuencode Utilities Module

The project includes uuencode utilities in `uu_utils.py` wrapping the standard library `uu` module: `uu_encode` writes the uuencoded form of a payload to a file, `uu_decode` decodes a uuencoded file back into bytes, `encode_uu` and `decode_uu` do the same entirely in memory, `parse_uu_header` reads the `begin <mode> <name>` header, and `is_uuencoded` reports whether a payload carries such a header. `DEFAULT_FILE_MODE` is the permission mask recorded in the header when the caller does not pick one. Unlike the standard library decoder, the helpers never derive an output filename from the header, so nothing is written to the working directory unless an explicit destination is given. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The standard library `uu` module was removed in Python 3.13, so the helpers raise `RuntimeError` when the interpreter no longer ships it. The module is tested in `tests/test_uu_utils.py`.

The project includes zipapp utilities in `zipapp_utils.py` wrapping the standard library `zipapp` module: `create_archive` / `create_zipapp` create a Python executable archive from source directories or archives, optionally with a custom interpreter and main module; `get_interpreter` / `get_zipapp_interpreter` extract the shebang interpreter from an archive; `is_zipapp_archive` detects whether a file is a zipapp archive. The module re-exports `zipapp.ZipAppError` as `ZipAppError`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments where appropriate. The module is tested in `tests/test_zipapp_utils.py`.

The project includes py_compile utilities in `py_compile_utils.py` wrapping the standard library `py_compile` module: `compile_file` / `py_compile_file` byte-compile one Python source file to bytecode and return the resulting ``.pyc`` path, with optional explicit target name, display name, raise-on-error flag, optimization level, and invalidation mode; `parse_invalidation_mode` and `get_invalidation_mode` resolve a ``PycInvalidationMode`` from a string, enum, or ``None`` (falling back to the interpreter's default); `is_pyc_file` reports whether a path looks like a compiled bytecode file; and `main` runs the ``py_compile`` command-line interface. The module re-exports ``py_compile.PyCompileError`` as `PyCompileError` and ``py_compile.PycInvalidationMode`` as `PycInvalidationMode`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_py_compile_utils.py`.


## Compileall Utilities Module

The project includes compileall utilities in `compileall_utils.py` wrapping the standard library `compileall` module: `compile_file` byte-compiles a single Python source file and reports whether the compilation succeeded; `compile_dir` byte-compiles every source file below a directory, with an optional recursion limit, a worker count, a skip pattern, and the legacy bytecode layout; `compile_path` byte-compiles the modules found on ``sys.path``; `main` runs the ``compileall`` command-line interface and returns its exit code, restoring ``sys.argv`` afterwards; and `pyc_path` reports the PEP 3147 cache location the compiler would use for a source file without creating it. The invalidation mode accepts either a ``PycInvalidationMode`` member or its name, with dashes or underscores. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_compileall_utils.py`.


## Modulefinder Utilities Module

The project includes dependency analysis utilities in `modulefinder_utils.py` wrapping the standard library `modulefinder` module: `load_script` analyses a script statically and returns the module finder that holds the result; `find_dependencies` returns the sorted names of every module the script imports; `find_modules` maps every dependency to the file it was found in; `missing_modules` returns the imports that could not be resolved; `missing_importers` names the modules that import those unresolved names; `module_path` returns the file a single dependency was found in; `is_package` reports whether a dependency is a package; and `report` returns the textual dependency report instead of printing it. The analysis is purely static: the script is never imported and never executed. `Module` and `ModuleFinder` are re-exported from the standard library. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_modulefinder_utils.py`.


## Optparse Utilities Module

The project includes command-line option parsing utilities in `optparse_utils.py` wrapping the standard library `optparse` module: `make_parser` creates an `OptionParser` with validated metadata; `add_option` adds an option to a parser or to an option group; `add_flag` adds a boolean flag; `add_count_option` adds an option that counts its occurrences; and `add_option_group` creates an option group. `parse_args` parses a command line and returns the parsed values together with the remaining arguments, and it can either keep the standard library behaviour of printing a usage message and terminating the interpreter or raise `OptionParseError` instead. `get_option`, `has_option`, and `remove_option` query and change the registered options; `get_default_values` and `set_defaults` work with the default values; `get_usage`, `format_usage`, `format_help`, `format_option_help`, and `get_prog_name` render the help text; `dest_for` returns the destination attribute the standard library derives from an option string; `string_type`, `int_type`, `float_type`, and `choice_type` are value converters; and `values_to_dict` turns the parsed values into a plain dictionary. `Option`, `OptionParser`, `OptionGroup`, `OptionContainer`, `Values`, `OptionError`, `OptionValueError`, `OptionConflictError`, `BadOptionError`, `SUPPRESS_HELP`, and `SUPPRESS_USAGE` are re-exported from the standard library. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_optparse_utils.py`.


## Pyclbr Utilities Module

The project includes class and function browser utilities in `pyclbr_utils.py` wrapping the standard library `pyclbr` module: `read_module` returns the classes defined in a module, `read_module_ex` returns both its classes and its top-level functions, and `class_names`, `function_names`, `find_class`, `find_function`, `has_class`, `has_function`, `is_class`, and `is_function` query the result. The analysis is purely static: the source is read but never imported or executed, so the module is safe to inspect from a test suite. `Class` and `Function` are re-exported from the standard library. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_pyclbr_utils.py`.


## Pyexpat Utilities Module

The project includes XML parsing utilities in `pyexpat_utils.py` wrapping the standard library `pyexpat` module: `ParserCreate` creates a parser, `parse_text` and `parse_file` parse a document from text or a file, `error_string` describes an error code, `version_info` reports the expat library version, and `is_available` reports whether the interpreter ships the module. The parser reports the position of an error through `error_position` and its current position through `current_position`, both returned as named tuples. The helpers `set_base`, `get_base`, `set_param_entity_parsing`, and `external_entity_parser` configure the parser, while `set_start_element_handler`, `set_end_element_handler`, `set_character_data_handler`, and `set_processing_instruction_handler` set the event handlers. The `attribute_mapping` helper normalizes element attributes into a plain dictionary. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_pyexpat_utils.py`.


## Xdrlib Utilities Module

The project includes XDR (eXternal Data Representation) utilities in `xdrlib_utils.py` wrapping the standard library `xdrlib` module: `pack_uint` and `unpack_uint` encode and decode 32-bit unsigned integers; `pack_int` and `unpack_int` do the same for signed integers; `pack_enum` and `unpack_enum` encode enumeration values; `pack_bool` and `unpack_bool` encode booleans; `pack_uhyper`, `unpack_uhyper`, `pack_hyper`, and `unpack_hyper` handle 64-bit integers; `pack_float`, `unpack_float`, `pack_double`, and `unpack_double` handle floating point numbers; `pack_string`, `unpack_string`, `pack_bytes`, `unpack_bytes`, `pack_opaque`, and `unpack_opaque` handle length-prefixed data; `pack_fstring`, `unpack_fstring`, `pack_fopaque`, and `unpack_fopaque` handle fixed length data; `pack_array`, `unpack_array`, `pack_farray`, and `unpack_farray` handle arrays; `pack_list` and `unpack_list` handle terminated lists; and `pack_uint_array` and `unpack_uint_array` are pre-wired helpers for arrays of unsigned integers. `Packer`, `Unpacker`, `Error`, and `ConversionError` are re-exported from the standard library. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments, and a truncated payload raises `ValueError` instead of `EOFError`. The encoding is pure computation, so the module never opens a network connection or spawns a process. The standard library `xdrlib` module was removed in Python 3.13, so the helpers raise `RuntimeError` when the interpreter no longer ships it. The module is tested in `tests/test_xdrlib_utils.py`.


## Smtplib Utilities Module

The project includes SMTP client utilities in `smtplib_utils.py` wrapping the standard library `smtplib` module: `quoteaddr` quotes an address the way a server expects it; `quote_string` quotes a string so that it can be used inside a header; `quote_data` quotes a message body so that it cannot end the message early; `parse_address` splits an address into its display name and its address; `address_only` returns an address without its display name; `format_address` formats a display name and an address as a single header value; `getfqdn` returns the fully qualified domain name of a host; `parse_response` parses a raw server reply into its code and its message; and `parse_ehlo_features` parses the service extensions a server announced in its EHLO reply. `build_message` assembles a complete `email.message.EmailMessage` from plain values and guesses the media type of an attachment from its file name. `create_smtp`, `create_smtp_ssl`, and `create_lmtp` build the standard library clients, and `send_message` and `send_text` send a message with a client the caller already owns. `SMTP`, `SMTP_SSL`, `LMTP`, and the standard library error classes are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module never opens a connection on its own, so the caller stays in control of when a connection is attempted and the test suite stays hermetic. The module is tested in `tests/test_smtplib_utils.py`.


tests/test_ftplib_utils.py - Tests for ftplib_utils module

## Ftplib Utilities Module

The project includes FTP utilities in `ftplib_utils.py` wrapping the standard library `ftplib` module: `FTP` and `FTP_TLS` classes, `error_reply`, `error_temp`, `error_perm`, `error_proto`, `all_errors`, `FTP_PORT`, `MAXLINE`, plus validated helpers `create_ftp`, `create_ftp_tls`, `connect_ftp`, `parse257`, `parse150`, `parse227`, `parse229`.


tests/test_poplib_utils.py - Tests for poplib_utils module
tests/test_asynchat_utils.py - Tests for asynchat_utils module
tests/test_asyncore_utils.py - Tests for asyncore_utils module
tests/test_smtpd_utils.py - Tests for smtpd_utils module

## Poplib Utilities Module

The project includes POP3 utilities in `poplib_utils.py` wrapping the standard library `poplib` module: `POP3`, `POP3_SSL`, `error_proto`, `POP3_PORT`, `POP3_SSL_PORT`, plus validated helpers `create_pop3`, `create_pop3_ssl`, `connect_pop3`.


tests/test_webbrowser_utils.py - Tests for webbrowser_utils module

## Webbrowser Utilities Module

The project includes web browser utilities in `webbrowser_utils.py` wrapping the standard library `webbrowser` module: `open_url` displays a URL with the default browser, `open_new` opens a URL in a new browser window, `open_new_tab` opens a URL in a new browser tab, `get_controller` returns the controller of a registered browser, `register_browser` registers a browser controller class under a name, and `register_standard_browsers` registers the browsers the standard library can discover on the system. `Error` is re-exported from the standard library. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments, so a caller never reaches the browser with a malformed request. The module is tested in `tests/test_webbrowser_utils.py`.


tests/test_xmlrpc_utils.py - Tests for xmlrpc_utils module

## Xmlrpc Utilities Module

The project includes XML-RPC utilities in `xmlrpc_utils.py` wrapping the standard library `xmlrpc` package: `dumps_value` encodes arguments into a request or response document, `loads_value` decodes a document into its arguments and method name, `build_request` builds a method call document, `parse_method_call` parses a method call, `parse_method_response` parses a method response and raises `Fault` for a fault, `marshal_params` and `unmarshal_params` encode and decode a bare `<params>` document, `create_marshaller` and `create_transport` build the standard library encoding and transport objects, `create_proxy` builds a lazy client proxy, `create_dispatcher` builds a dispatcher that maps remote calls onto local callables, `register_function`, `register_instance`, `register_introspection_functions` and `register_multicall_functions` populate a dispatcher, `resolve_dotted_attribute` and `list_public_methods` inspect the objects a dispatcher exposes, and `create_server` and `create_multi_path_server` build the standard library servers. `Fault`, `ProtocolError`, `ResponseError`, `Binary`, `DateTime`, `Marshaller`, `Unmarshaller`, `Transport`, `ServerProxy`, `MultiCall`, `SimpleXMLRPCServer`, `MultiPathXMLRPCServer`, `SimpleXMLRPCDispatcher`, and the standard library request handlers are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The encoding helpers are pure computation and the connection helpers only build objects, so the module never opens a connection on its own. The module is tested in `tests/test_xmlrpc_utils.py`.


tests/test_syslog_utils.py - Tests for syslog_utils module

## Syslog Utilities Module

The project includes system logging utilities in `syslog_utils.py` wrapping the standard library `syslog` module: `open_log` opens the system logger for the program, `log_message` sends a message with a given severity, `close_log` closes the log again, `set_log_mask` restricts the severities that are recorded and returns the previous mask, `log_mask` computes the mask of a single severity, `log_upto` computes the mask of every severity up to and including a given one, `priority_name` and `facility_name` turn the numeric severities and facilities into names, `priority_names`, `facility_names` and `option_names` return the known constants, and `is_available` reports whether the interpreter ships the standard library module. The severity constants (`LOG_EMERG`, `LOG_ALERT`, `LOG_CRIT`, `LOG_ERR`, `LOG_WARNING`, `LOG_NOTICE`, `LOG_INFO`, `LOG_DEBUG`), the facility constants (`LOG_KERN` up to `LOG_LOCAL7`) and the option flags (`LOG_PID`, `LOG_CONS`, `LOG_ODELAY`, `LOG_NDELAY`, `LOG_NOWAIT`, `LOG_PERROR`) are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The `syslog` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers that talk to the system logger raise a `RuntimeError` elsewhere. The module is tested in `tests/test_syslog_utils.py`.


tests/test_faulthandler_utils.py - Tests for faulthandler_utils module

## Faulthandler Utilities Module

The project includes fault handler utilities in `faulthandler_utils.py` wrapping the standard library `faulthandler` module: `enable` enables the fault handler with optional file and thread dumping, `disable` disables it, `is_enabled` reports whether it is enabled, `dump_traceback` dumps the current tracebacks of all threads to a file, `dump_traceback_later` schedules a traceback dump after a timeout with optional repetition or exit, `cancel_dump_traceback_later` cancels the scheduled dump, `register` registers a signal handler for dumping tracebacks, `unregister` unregisters a signal handler, and `is_available` reports whether the interpreter ships the standard library module. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The file argument accepts the standard error stream, a file descriptor, or a writable file object, and the import degrades gracefully so that the helpers raise a `RuntimeError` when the interpreter does not ship the `faulthandler` module. The module is tested in `tests/test_faulthandler_utils.py`.


tests/test_resource_utils.py - Tests for resource_utils module

## Resource Utilities Module

The project includes resource usage utilities in `resource_utils.py` wrapping the standard library `resource` module: `get_rlimit` reads the soft and the hard limit of a resource for the running process, `set_rlimit` sets the limits of a resource for the running process, `prlimit` reads or sets the limits of another process, `get_rusage` reports the resource usage of a process, `get_page_size` returns the size of a memory page, `limit_names` returns the limit constants of the host platform, `limit_value` and `limit_name` translate a limit between its name and its value, `usage_names` returns the usage constants, `usage_as_dict` turns a usage record into a dictionary, and `is_available` reports whether the interpreter ships the standard library module. The limits are returned in a `Limit` named tuple with a `soft` and a `hard` field, the usage is returned in a `Usage` named tuple with the same fields on every platform, and every limit can be addressed by its name such as `"RLIMIT_NOFILE"`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The `resource` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers that talk to the operating system raise a `RuntimeError` elsewhere, and `prlimit` is only available on Linux. The module is tested in `tests/test_resource_utils.py`.

## Password Database Utilities Module

The project includes password database utilities in `pwd_utils.py` wrapping the standard library `pwd` module: `getpwuid` looks up a user by numeric identifier, `getpwnam` looks up a user by name, `getpwall` returns every entry in the password database, and `is_available` reports whether the interpreter ships the standard library module. Records are returned as `Passwd` named tuples with the fields `name`, `passwd`, `uid`, `gid`, `gecos`, `dir`, and `shell`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments, while lookups for missing entries raise `KeyError`. The `pwd` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise a `RuntimeError` elsewhere. The module is tested in `tests/test_pwd_utils.py`.

## Group Database Utilities Module

The project includes group database utilities in `grp_utils.py` wrapping the standard library `grp` module: `getgrgid` looks up a group by numeric identifier, `getgrnam` looks up a group by name, `getgrall` returns every entry in the group database, and `is_available` reports whether the interpreter ships the standard library module. Records are returned as `Group` named tuples with the fields `name`, `passwd`, `gid`, and `mem`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments, while lookups for missing entries raise `KeyError`. The `grp` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise a `RuntimeError` elsewhere. The module is tested in `tests/test_grp_utils.py`.

## Termios Utilities Module

The project includes terminal attribute utilities in `termios_utils.py` wrapping the standard library `termios` module: `get_attributes` reads the attributes of a terminal, `set_attributes` writes them back, `make_raw` builds a raw configuration, `make_cbreak` builds a cbreak configuration, `set_read_timeout` and `set_blocking` configure how a read waits for data, `get_window_size` and `set_window_size` read and write the size of the window, `drain` waits until the output was transmitted, `flush` discards the data the terminal has not processed yet, `pause_output` and `resume_output` suspend and resume the output, `send_break` sends a break, `control_character_names` returns the names of the control characters, `baud_rates` returns the standard baud rates, and `is_available` reports whether the interpreter ships the standard library module. The attributes are returned in an `Attributes` named tuple with the fields `iflag`, `oflag`, `cflag`, `lflag`, `ispeed`, `ospeed`, and `cc`, and the size of the window is returned in a `WindowSize` named tuple with the fields `rows`, `columns`, `x_pixels`, and `y_pixels`. The control character slots (`VINTR`, `VQUIT`, `VERASE`, `VKILL`, `VEOF`, `VTIME`, `VMIN`, and the rest) and the moments and queues of the standard library (`TCSANOW`, `TCSADRAIN`, `TCSAFLUSH`, `TCIFLUSH`, and `TCOFLUSH`) are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The `termios` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise a `RuntimeError` elsewhere. The module is tested in `tests/test_termios_utils.py`.

## File Control Utilities Module

The project includes file control utilities in `fcntl_utils.py` wrapping the standard library `fcntl` module: `flock` places an advisory lock on a file, `unlock` releases it, `lockf` places an advisory lock on a region of a file, `control` performs the other control operations on a file descriptor, `ioctl` performs a device specific control operation, `get_descriptor_flags` and `set_descriptor_flags` read and write the flags of a file descriptor, `is_cloexec` reports whether a file descriptor is closed when the process executes a new program, `get_file_status_flags` and `set_file_status_flags` read and write the status flags of an open file, `duplicate_fd` copies a file descriptor, `file_lock` locks a file for the duration of a block of code, `lock_kind` and `lock_modes` translate the name of a lock mode into its operation, and `is_available` reports whether the interpreter ships the standard library module. The lock operations (`LOCK_SH`, `LOCK_EX`, `LOCK_NB`, and `LOCK_UN`), the record lock commands (`F_LOCK`, `F_TLOCK`, and `F_ULOCK`), and the control constants (`F_GETFD`, `F_SETFD`, `F_GETFL`, `F_SETFL`, `F_DUPFD`, `F_DUPFD_CLOEXEC`, and `FD_CLOEXEC`) are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The `fcntl` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise a `RuntimeError` elsewhere. The module is tested in `tests/test_fcntl_utils.py`.

## Pseudo-terminal Utilities Module

The project includes pseudo-terminal utilities in `pty_utils.py` wrapping the standard library `pty` module: `openpty` opens a new pseudo-terminal pair and returns `(master_fd, slave_fd)`, `open_terminal` opens the same pair under a name that spells out its purpose, `master_open` opens a pseudo-terminal and returns `(name, fd)`, `slave_open` opens the slave end of a pseudo-terminal by name, `fork` forks a process and connects the child's controlling terminal to a new pseudo-terminal, and `spawn` runs a program with a pseudo-terminal as its controlling terminal and waits for it. The result of `fork` is a `ForkResult` named tuple with the fields `pid` and `master_fd`, and the constants `STDIN_FILENO`, `STDOUT_FILENO`, `STDERR_FILENO`, and `CHILD` are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The `pty` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise a `RuntimeError` elsewhere. The standard library deprecated `master_open` and `slave_open` in Python 3.12, so the wrapper never calls them and works on every supported interpreter. The module is tested in `tests/test_pty_utils.py`.

## String Preparation Utilities Module

The project includes string preparation utilities in `stringprep_utils.py` wrapping the standard library `stringprep` module: `table_names` returns the names of the set tables of RFC 3454, `map_table_names` returns the names of the mapping tables, `in_table` reports whether a character belongs to a set table, `map_table` maps a character with a mapping table, `is_unassigned` reports whether a character is an unassigned code point, `is_mapped_to_nothing` reports whether a character is commonly mapped to nothing, `is_prohibited` reports whether a character belongs to the prohibited output, `is_allowed` reports whether a character may be stored in a prepared string, `is_bidi_allowed` reports whether a character may appear in a bidirectional name, `map_text` performs the mapping step of RFC 3454 on a whole string, `find_problems` reports the characters that prevent a string from being stored, and `is_preparable` reports whether a string may be prepared. The tables are also exposed as the read-only mappings `TABLES` and `MAP_TABLES`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is pure computation, so it works on every platform and never touches the file system, the network, or a process. The module is tested in `tests/test_stringprep_utils.py`.

## Site Utilities Module

The project includes site configuration utilities in `site_utils.py` wrapping the standard library `site` module: `get_site_packages` returns the global site-packages directories the interpreter looks for packages in, `get_site_prefixes` returns the installation prefixes those directories are looked up in, `get_user_base` returns the base directory a user installs packages below, and `get_user_site_packages` returns the site-packages directory of the user. The helpers `get_enable_user_site`, `is_user_site_enabled`, and `check_enable_user_site` report the setting of the user site directory, the last one with the tri-state of the standard library, which disables the directory for security reasons when the process runs with a different effective user. The helper `make_path` joins path segments and reports them in the absolute and normalized form the standard library stores the paths of the search path in. The helpers `remove_duplicate_paths`, `add_site_dir`, `add_site_packages`, and `add_user_site_packages` change the search path of the process the way the standard library changes it, and `add_site_dir` also processes the `.pth` files of the directory it adds. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is pure computation apart from the helpers that read the search path of the process, so it works on every platform. The tests of the project replace the search path of the process with a copy, so the suite never changes the search path of the interpreter that runs it. The module is tested in `tests/test_site_utils.py`.

## Tabnanny Utilities Module

The project includes tabnanny utilities in `tabnanny_utils.py` wrapping the standard library `tabnanny` module: `check` scans a file or a directory for ambiguous indentation and raises :class:`NannyNag` when it finds a mix of tabs and spaces, and `process_tokens` processes a stream of tokens and raises :class:`NannyNag` on ambiguous indentation. :class:`NannyNag` is re-exported from the standard library and carries the offending line number, message, and source line. All functions validate their inputs and raise :class:`TypeError` on invalid arguments. The module is pure computation, so it works on every platform and never touches the file system, the network, or a process. The module is tested in `tests/test_tabnanny_utils.py`.

## Encodings Utilities Module

The project includes encoding name utilities in `encodings_utils.py` wrapping the standard library `encodings` module: `normalize_encoding` returns the canonical form of an encoding name, `is_known_encoding` reports whether a name is a known alias or canonical name, `is_alias` reports whether a name is an alias, `encoding_aliases` lists the aliases of an encoding, `all_aliases` exposes the read-only alias mapping, and `all_encodings` lists every canonical encoding name. The alias mapping is exposed as the read-only mapping `ALIASES`. All functions validate their inputs and raise :class:`TypeError` on invalid arguments. The module is pure computation, so it works on every platform and never touches the file system, the network, or a process. The module is tested in `tests/test_encodings_utils.py`.

## Zipimport Utilities Module

The project includes Zip archive import utilities in `zipimport_utils.py` wrapping the standard library `zipimport` module: `zip_importer` returns an importer for a Zip archive, `archive_names` lists the members of an archive, `get_source` returns the source code of a module inside an archive, `get_code` returns the code object of that module, `get_filename` returns the path the module would be loaded from, `get_data` returns the bytes of a member of the archive, `is_package` reports whether a module is a package, `find_spec` returns the import specification of a module, and `invalidate_caches` drops the cached directory information of the archives. :class:`ZipImportError` is re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The module only reads the archive the caller points it at, so it never touches the network or a process. The module is tested in `tests/test_zipimport_utils.py`.

## IP Address Utilities Module

The project includes generic path utilities in `genericpath_utils.py` wrapping the standard library `genericpath` module: `exists` tests whether a path exists, `isfile` tests whether a path is a regular file, `isdir` tests whether a path is a directory, `islink` tests whether a path is a symbolic link, `getsize` returns the size of a file, `getmtime` returns the last modification time, `getatime` returns the last access time, `getctime` returns the metadata change time, `commonprefix` returns the longest common leading component, `samefile` tests whether two paths reference the same file, `sameopenfile` tests whether two open files reference the same file, `samestat` tests whether two stat buffers reference the same file. The constant `ALLOW_MISSING` is re-exported. All functions validate their inputs and raise :class:`TypeError` on invalid arguments. The module is pure computation, so it works on every platform and never touches the file system in special ways beyond standard operations. The module is tested in `tests/test_genericpath_utils.py`.

## Posixpath Utilities Module

The project includes posixpath utilities in `posixpath_utils.py` wrapping the standard library `posixpath` module: `abspath`, `basename`, `commonpath`, `commonprefix`, `dirname`, `exists`, `expanduser`, `expandvars`, `getatime`, `getctime`, `getmtime`, `getsize`, `isabs`, `isdir`, `isfile`, `isjunction`, `islink`, `ismount`, `join`, `lexists`, `normcase`, `normpath`, `realpath`, `relpath`, `samefile`, `sameopenfile`, `samestat`, `split`, `splitdrive`, `splitext`, `splitroot`. The wrapper adds the helper `is_rooted`, which reports whether a path starts at the root of the file system. The constants `ALLOW_MISSING`, `sep`, `altsep`, `curdir`, `pardir`, `extsep`, `pathsep`, `defpath`, `devnull`, and `supports_unicode_filenames` are re-exported. All functions validate their inputs and raise :class:`TypeError` on invalid arguments. The module is tested in `tests/test_posixpath_utils.py`.

## Ntpath Utilities Module

The project includes Windows path utilities in `ntpath_utils.py` wrapping the standard library `ntpath` module: `abspath`, `basename`, `commonpath`, `commonprefix`, `dirname`, `exists`, `expanduser`, `expandvars`, `getatime`, `getctime`, `getmtime`, `getsize`, `isabs`, `isdevdrive`, `isdir`, `isfile`, `isjunction`, `islink`, `ismount`, `join`, `lexists`, `normcase`, `normpath`, `realpath`, `relpath`, `samefile`, `sameopenfile`, `samestat`, `split`, `splitdrive`, `splitroot`, `splitext`. The wrapper adds the helpers the standard library leaves to the caller: `has_drive` reports whether a path carries a drive specification, `is_unc_path` reports whether a path names a share of a network, `is_device_path` reports whether a path names a device, and `to_slashes` and `to_backslashes` convert the separators of a path. The constants `ALLOW_MISSING`, `sep`, `altsep`, `curdir`, `pardir`, `extsep`, `pathsep`, `defpath`, `devnull`, and `supports_unicode_filenames` are re-exported. All functions validate their inputs and raise :class:`TypeError` on invalid arguments. The module is written in pure Python, so it works on every platform and a caller can work with Windows paths on a machine that runs a different operating system. The module is tested in `tests/test_ntpath_utils.py`.

## Nturl2path Utilities Module

The project includes URL-to-pathname conversion utilities in `nturl2path_utils.py` wrapping the standard library `nturl2path` module: `url2pathname` converts a file URL to a pathname, and `pathname2url` converts a pathname to a file URL. Both functions validate their inputs and raise :class:`TypeError` on invalid arguments. The module is pure computation, so it works on every platform and never touches the file system or the network. The module is tested in `tests/test_nturl2path_utils.py`.

## Curses Utilities Module

The project includes terminal handling utilities in `curses_utils.py` wrapping the standard library `curses` module: `initscr` initializes the standard screen, `endwin` restores the terminal, `isendwin` reports whether the terminal was restored, `cbreak` and `nocbreak` switch cbreak mode, `echo` and `noecho` switch echoing, `raw` and `noraw` switch raw mode, `nl` and `nonl` switch newline translation, `qiflush` and `noqiflush` switch queue flushing on interrupt, `intrflush` configures interrupt flushing, `meta` switches the meta key, `halfdelay` sets a half-delay read, `curs_set` sets the cursor visibility, `getsyx` and `setsyx` read and set the virtual cursor, `start_color` initializes color support, `has_colors` and `can_change_color` report color capabilities, `init_pair` and `init_color` define colors and pairs, `color_content` and `pair_content` report colors, `color_pair` returns the attribute of a pair, `pair_number` returns the pair of an attribute, `use_default_colors` assigns the default colors, `baudrate` returns the baud rate, `beep` and `flash` signal the user, `delay_output` and `napms` delay output, `flushinp` discards pending input, `ungetch` and `unget_wch` push characters back onto the input queue, `newwin` creates a window, `doupdate` updates the physical screen, `erasechar` and `killchar` return the control characters, `keyname` names a key, `longname` and `termname` name the terminal, `termattrs` reports the supported attributes, `has_ic` and `has_il` report insert/delete capabilities, `has_key` reports whether a key is recognized, `filter` restricts the terminal to the current line, `typeahead` sets the typeahead descriptor, `mouseinterval` and `mousemask` configure mouse reporting, `resize_term` and `resizeterm` resize the screen, `is_term_resized` reports a resize, `update_lines_cols` updates the size, `setupterm` reads terminal capabilities, `putp` writes a string, and `use_env` selects the source of the terminal size. The constants `OK`, `ERR`, the `A_*` video attributes, the `COLOR_*` colors, the `KEY_*` special keys, and the `window` class are re-exported. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The :mod:`curses` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_curses_utils.py`.

The project includes IP address utilities in `ipaddress_utils.py` wrapping the standard library `ipaddress` module: `ip_address` returns the address object of a text, an integer, or a packed byte string, `ip_network` returns the network object of a network, `ip_interface` returns the interface object of an address that carries a prefix length, `is_valid_address` reports whether a value names a valid address, `is_valid_network` reports whether a value names a valid network, `is_valid_interface` reports whether a value names a valid interface, `address_version` returns the version of an address, `to_packed` returns the packed bytes of an address, `from_packed` returns the address that a packed byte string holds, `network_hosts` returns the usable hosts of a network, `subnets` splits a network into its subnets, `summarize_addresses` returns the smallest set of networks that still covers a list of networks, `network_overlaps` reports whether two networks overlap, `address_within` reports whether an address lies inside a network, `common_prefix_length` returns the length of the common prefix of a list of addresses, `next_address` returns the address that follows an address, `previous_address` returns the address that precedes an address, and `sort_addresses` returns the addresses of a list in ascending order. The classes `IPv4Address`, `IPv6Address`, `IPv4Network`, `IPv6Network`, `IPv4Interface`, and `IPv6Interface` are re-exported from the standard library, and so are the errors `AddressValueError` and `NetmaskValueError`. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The module is pure computation, so it works on every platform and never touches the file system, the network, or a process. The module is tested in `tests/test_ipaddress_utils.py`.

The project includes documentation utilities in `pydoc_utils.py` wrapping the standard library `pydoc` module: `render_doc`, `doc`, `writedoc`, `writedocs`, `apropos`, `locate`, `resolve`, `safeimport`, `importfile`, `getdoc`, `synopsis`, `source_synopsis`, `describe`, `classify_class_attrs`, `classname`, `parentname`, `visiblename`, `isdata`, `ispackage`, `ispath`, `allmethods`, `splitdoc`, `stripid`, `replace`, `cram`, `plain`, `cli`, `help`, `getpager`, `plainpager`, and `browse` render, resolve, page, and browse documentation, `format_exception_only` formats exceptions, and the classes `Doc`, `HTMLDoc`, `HTMLRepr`, `Helper`, `ModuleScanner`, `Repr`, `TextDoc`, and `TextRepr` together with the error `ErrorDuringImport` are re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The module is pure computation, so it works on every platform and never touches the network. The module is tested in `tests/test_pydoc_utils.py`.

## Bdb Utilities Module

The project includes debugger framework utilities in `bdb_utils.py` wrapping the standard library `bdb` module: `create_bdb` creates a debugger of the framework, `set_breakpoint` sets a breakpoint in a file, `clear_breakpoint` removes a single breakpoint, `clear_breakpoints` removes every breakpoint of a file, and `clear_all_breakpoints` empties the registry of the process. The helpers `get_breakpoints`, `get_breakpoint`, and `get_file_breakpoints` report the registered breakpoints, `enable_breakpoint` and `disable_breakpoint` change the state of a breakpoint, `is_breakpoint_enabled` reports it, and `breakpoint_hits` counts the hits of a breakpoint. The helper `canonical_filename` returns the absolute name of a file, the way the standard library stores it, `effective_breakpoint` reports the breakpoint that is effective for a line of code, and `checkfuncname` reports whether a breakpoint matches the line a frame runs. The classes `Bdb` and `Breakpoint` together with the error `BdbQuit` are re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The module is pure computation, so it works on every platform and never starts a debugger of its own. The module is tested in `tests/test_bdb_utils.py`.

## Pdb Utilities Module

The project includes interactive debugger utilities in `pdb_utils.py` wrapping the standard library `pdb` module: `create_pdb` creates an interactive debugger, `set_trace` enters the debugger at the frame of the caller, `post_mortem` enters the debugger with the frame of a traceback, and `pm` enters it with the traceback of the last exception. The helpers `run`, `runeval`, `runctx`, and `runcall` run a statement, an expression, a statement in given namespaces, and a function under the control of the debugger. The class `Pdb` together with the error `Restart` is re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` on invalid arguments. Every helper opens the prompt of the debugger on the standard input of the process, so a program that calls one of them has to answer the prompt; the tests of the project patch the standard library instead, so the suite never waits for a prompt. The module is tested in `tests/test_pdb_utils.py`.

## Wsgiref Utilities Module

The project includes WSGI utilities in `wsgiref_utils.py` wrapping the standard library `wsgiref` package: `setup_testing_defaults` fills the environment of a request with the defaults the standard library uses for tests, `guess_scheme` reports the scheme of a request, `application_uri` returns the base URI of the application, `request_uri` returns the full URI of a request, and `shift_path_info` moves the first segment of the path of a request to the name of the script. The helpers `is_hop_by_hop` reports whether a header belongs to a single connection, `build_headers` builds the collection of the headers of a response, `header_values` returns every value of a header, `encode_headers` returns the headers in the form that is sent over the wire, and `file_wrapper` reads a stream in blocks. The helpers `check_environ` checks the environment of a request against the specification, `environ_errors` collects the problems of an environment in a list, `validator` returns the middleware that checks an application against the specification, `demo_app` runs the demonstration application of the standard library, and `make_server` creates a server that serves an application. The classes `Headers`, `FileWrapper`, `WSGIServer`, and `WSGIRequestHandler` together with the warning `WSGIWarning` are re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The module never opens a connection: the helpers of the environment of a request work on a dictionary, the helpers of the headers of a response work on a list, and the tests patch the standard library when they check that a server is created, so the suite never binds a socket. The module is tested in `tests/test_wsgiref_utils.py`.

## Pydoc Data Utilities Module

The project includes documentation topic utilities in `pydoc_data_utils.py` wrapping the standard library `pydoc_data` package: `get_topics` returns a copy of the topics of the Python Language Reference, `get_topics_subset` returns the topics of the given names, `get_topic` returns the text of a single topic, `get_topic_names` returns the names of the topics, `count_topics` returns the number of the topics, and `has_topic` reports whether a topic exists. The helper `get_topic_title` returns the title of a topic, `get_topic_sections` returns the headings of the sections of a topic, and `get_topic_section` returns the text of a single section. The helper `search_topics` returns the topics that hold a text, and `wrap_topic` returns the text of a topic, wrapped for a terminal. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The module is pure computation, so it works on every platform and never touches the network, the file system, or a process. The module is tested in `tests/test_pydoc_data_utils.py`.

## Antigravity Utilities Module

The project includes antigravity utilities in `antigravity_utils.py` wrapping the standard library `antigravity` module: `geohash` returns the geohash of a coordinate with the Munroe algorithm of https://xkcd.com/426/, `fly` opens the XKCD comic about Python in a browser, and `get_xkcd_url` returns the address of the comic. The constant `XKCD_URL` holds the address of the comic as well. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The standard library module opens a browser when it is imported, so the wrapper re-implements the algorithm of the standard library with :mod:`hashlib` instead of importing it, and a browser is only started by `fly`. The module is tested in `tests/test_antigravity_utils.py`.

## Cprofile Utilities Module

The project includes profiling utilities in `cprofile_utils.py` wrapping the standard library `cProfile` module: `new_profiler` creates a profiler, `run` profiles a single statement, `runctx` profiles a statement in given namespaces, `runcall` profiles a single call and returns its result, and `profile_call` returns the result of a profiled call together with its statistics. The helper `collect_stats` returns the statistics a profiler collected, `format_report` returns the report of a profiling run as text, `dump_stats` writes the statistics of a profiling run to a file, and `main` runs the command-line interface of the standard library. The class `Profile` is re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds three conveniences to the standard library: the report of a profiling run is returned as text instead of being printed to the standard output, a profiled call returns its statistics together with its result, and a timer that does not return the integer number of ticks the profiler needs is rejected with a clear message instead of failing inside the profiler. The module is tested in `tests/test_cprofile_utils.py`.

## Venv Utilities Module

The project includes virtual environment utilities in `venv_utils.py` wrapping the standard library `venv` package: `create_environment` creates a virtual environment and returns a description of it, `describe_environment` describes an environment that already exists, `read_configuration` returns the settings of the configuration file of an environment as a mapping, `is_environment` reports whether a directory holds an environment, `environment_paths` returns the directories of an environment the way the standard library computes them, `environment_python` returns the interpreter of an environment, `activation_scripts` returns the scripts that activate an environment, `find_environments` returns the environments of a directory tree, and `run_cli` runs the command-line interface of the standard library and returns its exit code. The class `EnvBuilder` is re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds three conveniences to the standard library: the creation of an environment returns a description of the result instead of nothing, the directories of an environment are computed without creating it, and the environments of a directory tree are found. The helpers that create an environment write to the directory they are given and nothing else, and the helpers that only read an environment never write to it, so the tests of the project create every environment in a temporary directory of their own and the suite never installs a package and never reaches the network. The module is tested in `tests/test_venv_utils.py`.
## Audio Utilities Module

The project includes audio utilities in `audioop_utils.py` wrapping the standard library `audioop` module (`frame_count`, `convert_sample_width`, `convert_to_u_law`, `convert_from_u_law`, `convert_to_a_law`, `convert_from_a_law`, `shift_bias`, `add_fragments`, `scale`, `average`, `average_peak_to_peak`, `root_mean_square`, `peak_value`, `peak_range`, `peak_to_peak`, `count_zero_crossings`, `find_scale_factor`, `mix_to_mono`, `duplicate_to_stereo`, `swap_byte_order`, `reverse_samples`, `sample_at`, `resample`, `encode_adpcm`, `decode_adpcm`, `describe_fragment`) with typed signatures, docstrings, `__all__`, and input validation, plus unit tests in `tests/test_audioop_utils.py`. The class `Resampler` keeps the state of the resampling, the helper `is_available` reports whether the interpreter still ships the module, and the module degrades gracefully on Python 3.13 where `audioop` was removed, raising `RuntimeError` pointing at `audioop-lts`. The wrapper validates arguments, rejects empty fragments in measurements, supports negative sample indices, and provides `describe_fragment` returning measurements together.

## Ensurepip Utilities Module

The project includes bootstrap utilities in `ensurepip_utils.py` wrapping the standard library `ensurepip` package: `bootstrap` installs the `pip` the interpreter carries and returns a `BootstrapResult` record of the installation, `pip_version` reports the version of the bundled `pip` as text, `bundled_wheel` returns the path of the wheel the interpreter carries, `is_pip_installed` reports whether the running interpreter can import `pip` without importing it, `run_cli` runs the command-line interface of the standard library and returns its exit code, and `is_available` reports whether the interpreter ships the package. The record of an installation holds its `pip_version`, `root`, `upgrade`, `user`, `altinstall`, `default_pip`, and `verbosity`. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds four conveniences to the standard library: the installation returns a record instead of nothing, the wheel the interpreter carries is located, the presence of `pip` is reported without importing it, and the command-line interface returns its exit code instead of terminating the interpreter. The installation uses the wheel the interpreter was built with, so it never reaches the network, and the tests of the project patch the standard library instead, so the suite installs no package. The module is tested in `tests/test_ensurepip_utils.py`.

## Readline Utilities Module

The project includes command line editing utilities in `readline_utils.py` wrapping the standard library `readline` module: `add_history` adds a line to the history, `clear_history` removes every entry, `get_history_item` reads the entry at a position, `remove_history_item` removes the entry at a position and returns it, `replace_history_item` replaces the entry at a position and returns the entry it replaced, `history_items` returns every entry of the history as a list, and `search_history` returns the entries that start with a prefix. The helpers that touch a file always name the file they touch: `read_history_file` loads a history file, `write_history_file` writes the history to a file, `append_history_file` appends the last entries of the history to a file, and `read_init_file` executes an init file, while `default_history_file` reports the history file the standard library uses by default. The helpers of the editor are `parse_and_bind`, `set_history_length`, `get_history_length`, `get_current_history_length`, `set_completer`, `get_completer`, `set_completer_delims`, `get_completer_delims`, `set_startup_hook`, `set_pre_input_hook`, `set_completion_display_matches_hook`, `get_completion_type`, `get_begidx`, `get_endidx`, `get_line_buffer`, `insert_text`, `redisplay`, and `set_auto_history`. The helper `make_completer` returns a completer for a fixed list of words, and `is_available` reports whether the interpreter ships the module. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds four conveniences to the standard library: the history is returned as a list, the positions of the history are numbered the same way everywhere, the helpers that touch a file always name the file they touch, and a completer for a list of words is offered. The standard library reads an entry by its one-based position but removes and replaces it by its zero-based position, so the wrapper numbers every position the same way, with the one-based number. The `readline` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The helpers that touch a file only touch the file they are given, so the tests of the project create every file in a temporary directory of their own and the suite never reads the history file of the user. The module is tested in `tests/test_readline_utils.py`.

The project includes builtin utilities in `builtins_utils.py` wrapping the standard library `builtins` module: `absolute`, `all_true`, `any_true`, `ascii_str`, `binary_string`, `boolean`, `callable_object`, `character`, `divmod_pair`, `format_value`, `get_hash`, `hex_string`, `is_instance`, `is_subclass`, `iterator`, `length`, `maximum`, `minimum`, `octal_string`, `ordinal`, `power`, `representation`, `round_number`, `sorted_list`, `summation` are provided with validation. The module is tested in `tests/test_builtins_utils.py`.

## Imghdr Utilities Module

The project includes image format detection utilities in `imghdr_utils.py` wrapping the standard library `imghdr` module: `what` returns the format of an image that is given as a path or as a binary stream, `detect` returns the format of a header that is already in memory, `matching_formats` returns every format a header matches instead of only the first one, `is_image` reports whether a file holds an image, `read_header` reads the header of a file and restores the position of a stream, `supported_formats` lists the formats the interpreter recognizes, `register_test` registers a detection function, `unregister_test` removes one again, and `is_available` reports whether the interpreter ships the module. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds four conveniences to the standard library: a header can be inspected without a file, every matching format can be listed, the formats the interpreter knows can be listed, and a detection function can be registered and removed again. The standard library recognizes the format `jpeg`, `png`, `gif`, `tiff`, `rgb`, `pbm`, `pgm`, `ppm`, `rast`, `xbm`, `bmp`, `webp`, and `exr`. The `imghdr` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The wrapper only reads the file it is given and never writes to the filesystem, so the tests of the project create every file in a temporary directory of their own. The module is tested in `tests/test_imghdr_utils.py`.

## Posix Utilities Module

The project includes POSIX interface utilities in `posix_utils.py` wrapping the standard library `posix` module: `open_fd` opens a path and returns the descriptor of the open file, `close_fd` closes a descriptor, `read_fd` reads up to a number of bytes, `read_exactly` reads until the requested number of bytes arrived, `write_fd` writes bytes, `write_all` writes until every byte left, `seek_fd` moves the position of a descriptor, `read_at` and `write_at` read and write at an offset without moving the position, `duplicate_fd` and `duplicate_fd_to` copy a descriptor, `create_pipe` creates a pipe, `is_terminal` reports whether a descriptor is a terminal, `is_blocking` and `set_blocking` report and change the blocking mode, `is_inheritable` and `set_inheritable` report and change the inheritable flag, `sync_fd` and `sync_data` write a file to the storage device, `truncate_fd` sets the length of a file, and `terminal_size` reports the size of a terminal. The filesystem is reported by `file_info`, which returns the metadata of a file as one `FileInfo` record, by `file_mode` and `file_size`, by `device_number` and `make_device`, which translate between a device number and its major and minor number, and by `path_accessible`, `is_readable`, `is_writable`, and `is_executable`. The filesystem is changed by `create_directory`, which creates the missing parents of a directory, by `remove_directory`, `delete_file`, and `remove_path`, which removes a path whatever it is, by `rename_path`, `create_hard_link`, `create_symbolic_link`, and `read_symbolic_link`, by `change_owner` and `change_mode`, and by `set_umask`, which reports the mask it replaced. The extended attributes of a file are read and written by `read_xattr`, `write_xattr`, `list_xattrs`, and `remove_xattr`. The scheduling of a process is reported by `scheduler_policy`, `scheduler_policy_name`, `scheduler_priorities`, `scheduler_parameters`, `affinity_mask`, and `yield_cpu`, and the wait status of a process is turned into an exit code by `exit_code_of` and into a readable sentence by `describe_wait_status`. The system itself is reported by `uname`, `cpu_count`, `load_average`, `process_times`, `system_limit`, `system_limits`, `system_configuration`, `login_name`, `terminal_device`, and `error_message`. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds seven conveniences to the standard library: a descriptor is read until the requested number of bytes arrived and written until every byte left, a directory is created together with its parents, a path is removed whatever it is, the metadata of a file is returned as one record, the scheduling policy is reported by name, a wait status is turned into a readable sentence, and the limits of the system are reported by name. The `posix` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The wrapper never forks a process and never touches a path it was not given, so the tests of the project create every file in a temporary directory of their own. The module is tested in `tests/test_posix_utils.py`.

## Chunk Utilities Module

The project includes IFF chunk utilities in `chunk_utils.py` wrapping the standard library `chunk` module: `open_chunk` opens the next chunk of a binary stream and returns the `Chunk` object of the standard library, `read_chunk` returns the next chunk of a file or a byte stream as one `ChunkRecord`, `peek_chunk` returns the next chunk without consuming it, `iter_chunks` returns an iterator over the chunks of a file, `read_chunks` returns every chunk of a file as a list, `skip_chunk` passes over the payload of the next chunk, `chunk_name` decodes the identifier of a chunk as text, `build_chunk` returns the bytes of a chunk, `write_chunk` writes a chunk to a file or a binary stream, and `is_available` reports whether the interpreter ships the module. A `ChunkRecord` carries the identifier of a chunk, the size its header declares, and its payload, and the identifier is decoded as text by the `text_name` property. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds four conveniences to the standard library: a chunk is returned as one record that carries its identifier, its size, and its payload, the next chunk can be inspected without consuming it, the identifier of a chunk is decoded as text, and a chunk can be written again, which the standard library cannot do at all. The `chunk` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully: the helpers that read a chunk raise :class:`RuntimeError` when the module is missing, while the helpers that only encode a chunk keep working. The wrapper only touches the files and the streams it is given, so the tests of the project create every file in a temporary directory of their own. The module is tested in `tests/test_chunk_utils.py`.

## Pipes Utilities Module

The project includes pipeline utilities in `pipes_utils.py` wrapping the standard library `pipes` module: `quote` and `quote_command` return a shell-quoted string, `create_template` returns a fresh pipeline template, `is_available` reports whether the interpreter ships the module, `make_pipeline` runs a template as a pipeline, and `step_kinds` lists the valid kinds of pipeline steps. The template class `Template` is re-exported. The constants `SOURCE`, `SINK`, `FILEIN_FILEOUT`, `FILEIN_STDOUT`, `STDIN_FILEOUT`, and `STDIN_STDOUT` are re-exported from the standard library, so they can be handed to the template of the standard library as the kind of a step. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The `pipes` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_pipes_utils.py`.

## Crypt Utilities Module

The project includes password hashing utilities in `crypt_utils.py` wrapping the standard library `crypt` module: `crypt` hashes a password with a salt, `mksalt` creates a salt for a method, `hash_password` hashes a password with a salt of its own, `verify` reports whether a password matches a stored hash, `identify_method` reports the method a hash was created with, `is_hash` reports whether a value looks like a hash, `methods` lists the methods the interpreter supports, and `is_available` reports whether the interpreter ships the module. The constants `METHOD_BLOWFISH`, `METHOD_CRYPT`, `METHOD_MD5`, `METHOD_SHA256`, and `METHOD_SHA512` are re-exported. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds four conveniences to the standard library: a password is compared with a hash in constant time, the method of a hash is identified without the password, the salt is created together with the hash that uses it, and the supported methods can be listed. The `crypt` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers that hash a password raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_crypt_utils.py`.

## Telnet Utilities Module

The project includes telnet client utilities in `telnetlib_utils.py` wrapping the standard library `telnetlib` module: `create_telnet` creates a client, `connect_telnet` creates a client and opens the connection, `read_until` and `read_until_text` read the data of a connection up to a marker, `read_all` reads the data until the peer closes the connection, `read_some` reads at least one byte, `read_eager` and `read_very_eager` read without waiting for more than one round trip, `read_lazy` and `read_very_lazy` read without waiting at all, `read_sb_data` reads the data of a subnegotiation, `write` writes bytes and reports the number of bytes that reached the peer, `send_line` writes a line and ends it, `expect` and `expect_text` read until one of a list of patterns matched, `close` closes the connection, `escape_iac` doubles every byte that introduces a command, `strip_iac` removes the commands of the protocol from a payload, `command_name` and `option_name` report the name of a command or an option, and `is_available` reports whether the interpreter ships the module. The client class `Telnet` is re-exported, and the constants `IAC`, `DONT`, `DO`, `WONT`, `WILL`, `SE`, `NOP`, `DM`, `BRK`, `IP`, `AO`, `AYT`, `EC`, `EL`, `GA`, `SB`, and `theNULL` are re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds six conveniences to the standard library: the data of a connection can be read as text, a line can be sent in one call, the number of bytes that reached the peer is reported, the telnet commands can be removed from a payload or escaped in one, and the name of a command or an option can be looked up. The `telnetlib` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers that need it raise :class:`RuntimeError` when the module is missing, while the helpers that only work on the protocol itself keep working. The tests of the project talk to a server of the loopback interface of their own, so the suite never reaches the network. The module is tested in `tests/test_telnetlib_utils.py`.

## Sre Constants Utilities Module

The project includes regular expression constants utilities in `sre_constants_utils.py` wrapping the standard library `sre_constants` module: `get_opcodes` returns the opcodes if available, `opcodenames` returns a mapping of opcode numbers to names, `lookup_opcode` resolves an opcode number to its name, `op_code` resolves an opcode name to its number, `assert_valid_flags` validates regex flags, `get_all` returns all public constants, `error_codes` returns error codes if available, and `is_available` reports whether the interpreter ships the module. Common constants such as `LITERAL`, `BRANCH`, `ANY`, `MAXCODE`, and the `SRE_FLAG_*` flags are re-exported when available. The exception class `error` is re-exported. All functions validate their inputs and raise :class:`TypeError` on invalid arguments. The module degrades gracefully and helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_sre_constants_utils.py`.

## Sre Parse Utilities Module

The project includes regular expression parse utilities in `sre_parse_utils.py` wrapping the standard library `sre_parse` module: `parse_pattern` parses a regular expression pattern into a `SubPattern` tree, `parse_template` parses a replacement template, `pattern_width` reports the minimum and maximum width of a pattern, `pattern_dump` returns the text dump of a parsed tree, and `is_available` reports whether the interpreter ships the module. The classes `SubPattern` and `State` together with the exception `error` are re-exported, and common constants such as `LITERAL`, `BRANCH`, `CHARSET`, `GROUPREF`, `SUBPATTERN`, and the `SRE_FLAG_*` flags are re-exported when available. All functions validate their inputs and raise :class:`TypeError` on invalid arguments. The module degrades gracefully and helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_sre_parse_utils.py`.


## Spwd Utilities Module

The project includes shadow password database utilities in `spwd_utils.py` wrapping the standard library `spwd` module: `getspnam` looks up a user's shadow entry, `getspall` returns all shadow entries, and `is_available` reports whether the interpreter ships the module. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The `spwd` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_spwd_utils.py`.
## Cgi Utilities Module

The project includes CGI utilities in `cgi_utils.py` wrapping the standard library `cgi` module: `FieldStorage` and `MiniFieldStorage` parse form data, `parse_header` parses MIME headers, `parse` parses a query string or form data, `parse_qs` and `parse_qsl` parse query strings, `parse_multipart` parses multipart form data, `escape` replaces special HTML characters, and `is_available` reports whether the interpreter ships the module. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The wrapper adds validation and conveniences while degrading gracefully when the module is missing. The `cgi` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_cgi_utils.py`.

`cgi.parse_qs` and `cgi.parse_qsl` were only added to the standard library in Python 3.13, so on the interpreters that still ship the `cgi` module the wrapper falls back to the equivalent functions of `urllib.parse`, which share the signature, and the helpers keep working on every interpreter.

## Cgitb Utilities Module

The project includes cgitb utilities in `cgitb_utils.py` wrapping the standard library `cgitb` module: `enable` enables the traceback handler, `disable` disables it, `reset` resets the state, `lookup` looks up an object, `scanvars` scans variables for a frame, `handler` handles an exception, `text` formats a traceback as text, `html` formats a traceback as HTML, `small` formats a small report, `strong` formats a strong report, `grey` formats a grey report, `pink` formats a pink report, `blue` formats a blue report, `reset` resets formatting, `enable` enables the handler, and `is_available` reports whether the interpreter ships the module. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The `cgitb` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_cgitb_utils.py`.

## Nntplib Utilities Module

The project includes NNTP utilities in `nntplib_utils.py` wrapping the standard library `nntplib` module: `NNTP` and `NNTP_SSL` provide NNTP client connections, `create_nntp` and `create_nntp_ssl` create connections with input validation, `GroupInfo` and `ArticleInfo` are re-exported records, and the constants and errors are re-exported from the standard library. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The `nntplib` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_nntplib_utils.py`.

## Sndhdr Utilities Module

The project includes sound header detection utilities in `sndhdr_utils.py` wrapping the standard library `sndhdr` module: `what` returns the format of a sound file, `whathdr` returns the format and parameters, `tests` lists the test functions, `is_available` reports whether the interpreter ships the module. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The `sndhdr` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_sndhdr_utils.py`.

## Sun AU Utilities Module

The project includes Sun AU format utilities in `sunau_utils.py` wrapping the standard library `sunau` module: `open` opens a Sun AU file and returns an `Au_read` or `Au_write` object, `open_au` is an alias for `open`, `open_read` opens a file for reading, and `open_write` opens a file for writing. The convenience aliases `open_sunau`, `read_sunau`, and `write_sunau` are also provided. The classes `Au_read` and `Au_write` together with the error `Error` are re-exported from the standard library, and `is_available` reports whether the interpreter ships the module. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The `sunau` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_sunau_utils.py`.

## Sre Compile Utilities Module

The project includes sre_compile utilities in `sre_compile_utils.py` wrapping the standard library `sre_compile` module: `compile` compiles a pattern, `isstring` checks if an object is a string, `compile_pattern` compiles a regex pattern, `dis` disassembles a pattern, and `is_available` reports whether the interpreter ships the module. All functions validate their inputs and raise :class:`TypeError` or :class:`ValueError` on invalid arguments. The `sre_compile` module is an internal implementation detail, so the import degrades gracefully and the helpers raise :class:`RuntimeError` when the module is missing. The module is tested in `tests/test_sre_compile_utils.py`.

Deprecated-module wrappers: `cgitb_utils.py`, `nntplib_utils.py`, `sndhdr_utils.py`, `sre_compile_utils.py`, `sre_parse_utils.py`.

## Slugify Utilities Module

The project includes slug utilities in `slugify_utils.py`: `slugify` and `is_slug`. The module is tested in `tests/test_slugify_utils.py`.

## Type Check Utilities Module

The project includes type checking utilities in `type_check_utils.py`: `is_str`, `is_int`, `is_float`, `is_bool`, `is_list`, `is_dict`, `is_tuple`, `is_set`, `is_frozenset`, `is_none`, `is_bytes`, `is_numeric`, `is_iterable`, `is_callable`, `is_protocol`, `is_module`, `is_namedtuple`, `is_typeddict`, `is_awaitable`, `is_type_var`, `ensure_type`, `coerce_to_str`, `coerce_to_int`, `coerce_to_float`, and `coerce_to_bool`. The module is tested in `tests/test_type_check_utils.py`.
