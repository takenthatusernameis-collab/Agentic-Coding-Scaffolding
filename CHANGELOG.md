## Unreleased

- Add `imghdr_utils.py` wrapping the standard library `imghdr` module (`what`, `detect`, `matching_formats`, `is_image`, `read_header`, `supported_formats`, `register_test`, `unregister_test`, `is_available`) with typed signatures, docstrings, `__all__`, and input validation, plus unit tests in `tests/test_imghdr_utils.py`.
- Synchronized `imghdr_utils.py` and `tests/test_imghdr_utils.py` across `scaffold.sh` header comment and heredocs, the embedded `pyproject.toml`, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py` assertions, and this CHANGELOG.
- Repaired the `imghdr_utils` handover that the previous session left behind: the module was a stub without the validation, the docstrings, and the typed signatures the other wrappers carry, it imported the standard library module at the top level so it failed to import on Python 3.13, and it was missing from every surface but `pyproject.toml`.
- The wrapper adds the conveniences the standard library leaves to the caller: a header can be inspected without a file, every matching format can be listed instead of only the first one, the formats the interpreter knows can be listed, and a detection function can be registered and removed again.
- The `imghdr` module was deprecated in Python 3.11 and removed in Python 3.13 as part of :pep:`594`, so the import degrades gracefully and the helpers raise a `RuntimeError` that names the missing module.
- The test suite is hermetic: every file is created in a temporary directory the test owns, the standard library is patched for the degradation tests, and the suite never writes outside its own temporary directories.

- Add `pyexpat_utils.py` wrapping the standard library `pyexpat` module (`ParserCreate`, `ExpatError`, `parse`, `parse_text`, `parse_file`, `error_string`, `version_info`, `is_available`, `ErrorPosition`, `CurrentPosition`, `set_base`, `get_base`, `set_param_entity_parsing`, `external_entity_parser`, `set_start_element_handler`, `set_end_element_handler`, `set_character_data_handler`, `set_processing_instruction_handler`, `attribute_mapping`) with input validation, plus unit tests in `tests/test_pyexpat_utils.py`.
- Synchronized `pyexpat_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- The wrapper adds the conveniences the standard library leaves to the caller: a document is parsed from text or from a file behind one helper that names the file it reads, the attributes of an element are returned as a mapping, and the parser reports the position of an error as one record instead of three calls.

- Add `readline_utils.py` wrapping the standard library `readline` module (`add_history`, `append_history_file`, `clear_history`, `default_history_file`, `get_history_item`, `history_items`, `make_completer`, `read_history_file`, `remove_history_item`, `replace_history_item`, `search_history`, `write_history_file`, `is_available`) with input validation, plus unit tests in `tests/test_readline_utils.py`.
- Synchronized `readline_utils.py`, `builtins_utils.py`, `tests/test_readline_utils.py`, and `tests/test_builtins_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- The history is returned as a list, the positions of the history are numbered the same way everywhere, the helpers that touch a file always name the file they touch, and a completer for a list of words is offered.
- The standard library reads an entry of the history by its one-based position but removes and replaces it by its zero-based position, so the wrapper numbers every position the same way, with the one-based number.
- The `readline` module only exists on Unix-like platforms, so the import degrades gracefully and the helpers raise `RuntimeError` when the module is missing.

- Add `audioop_utils.py` wrapping the standard library `audioop` module with input validation, the `Resampler` class, graceful degradation on Python 3.13 where `audioop` was removed, and conveniences like `describe_fragment`, `sample_at`, and precise measurements; plus unit tests in `tests/test_audioop_utils.py`.
- Synchronized `audioop_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Repaired the `audioop_utils` handover that the previous session left behind: six tests failed because they contradicted the standard library, the generator neither listed the module in its header comment nor registered it in the embedded `pyproject.toml`, and the copies of the module and of its test that the generator embeds were stale.
- The peak to peak value of a fragment is the distance between two turning points of its waveform, so the wrapper documents the measurement the way the standard library computes it, and the tests compare with the standard library.
- `find_scale_factor` rejects a fragment that does not hold a whole number of sixteen bit samples with a `ValueError` instead of letting the standard library fail.
- The README section of `audioop_utils.py` lists the helpers of the wrapper instead of the names of the standard library.
- Add `ensurepip_utils.py` wrapping the standard library `ensurepip` package (`bootstrap`, `bundled_wheel`, `pip_version`, `is_pip_installed`, `run_cli`, `is_available`) with input validation and the record `BootstrapResult`, plus unit tests in `tests/test_ensurepip_utils.py`.
- Synchronized `ensurepip_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- The installation of the bundled `pip` returns a record of what was installed, the wheel the interpreter carries is located, the presence of `pip` is reported without importing it, and the command line interface of the standard library returns its exit code instead of terminating the interpreter.
- Add `venv_utils.py` wrapping the standard library `venv` package (`create_environment`, `describe_environment`, `read_configuration`, `environment_paths`, `environment_python`, `activation_scripts`, `is_environment`, `find_environments`, `run_cli`) with input validation and the re-exported class `EnvBuilder`, plus unit tests in `tests/test_venv_utils.py`.
- Synchronized `venv_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Return a description of a virtual environment when it is created, compute the directories of an environment without creating it, find the environments of a directory tree, and return the exit code of the command-line interface of the standard library.
- Add `cprofile_utils.py` wrapping the standard library `cProfile` module (`new_profiler`, `run`, `runctx`, `runcall`, `profile_call`, `collect_stats`, `format_report`, `dump_stats`, `main`) with input validation and the re-exported class `Profile`, plus unit tests in `tests/test_cprofile_utils.py`.
- Synchronized `cprofile_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Return the report of a profiling run as text instead of printing it to the standard output, let a profiled call return its statistics together with its result, and reject a timer that does not return the integer number of ticks the profiler needs with a clear message instead of a failure inside the profiler.
- Add `urllib_utils.py` wrapping the standard library `urllib.parse` module (`parse_url`, `build_url`, `urlsplit`, `urlunsplit`, `join_url`, `quote`, `quote_plus`, `unquote`, `unquote_plus`, `unquote_to_bytes`, `urlencode`, `parse_qs`, `parse_qsl`, `defrag`) with input validation, plus unit tests in `tests/test_urllib_utils.py`.
- Synchronized `urllib_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.

- Add `antigravity_utils.py` wrapping the standard library `antigravity` module (`geohash`, `fly`, `get_xkcd_url`) with input validation, plus unit tests in `tests/test_antigravity_utils.py`.
- Synchronized `antigravity_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.

- Add `pydoc_data_utils.py` wrapping the standard library `pydoc_data` package (`count_topics`, `get_topic`, `get_topic_names`, `get_topic_section`, `get_topic_sections`, `get_topic_title`, `get_topics`, `get_topics_subset`, `has_topic`, `search_topics`, `wrap_topic`) with input validation, plus unit tests in `tests/test_pydoc_data_utils.py`.
- Add `wsgiref_utils.py` wrapping the standard library `wsgiref` package (`setup_testing_defaults`, `guess_scheme`, `application_uri`, `request_uri`, `shift_path_info`, `is_hop_by_hop`, `build_headers`, `header_values`, `encode_headers`, `file_wrapper`, `check_environ`, `environ_errors`, `validator`, `demo_app`, `make_server`) with input validation, and the re-exported classes `Headers`, `FileWrapper`, `WSGIServer`, and `WSGIRequestHandler` together with the warning `WSGIWarning`, plus unit tests in `tests/test_wsgiref_utils.py`.
- Synchronized `wsgiref_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `site_utils.py` wrapping the standard library `site` module (`get_site_packages`, `get_site_prefixes`, `get_user_base`, `get_user_site_packages`, `get_enable_user_site`, `is_user_site_enabled`, `check_enable_user_site`, `make_path`, `remove_duplicate_paths`, `add_site_dir`, `add_site_packages`, `add_user_site_packages`) with input validation, plus unit tests in `tests/test_site_utils.py`.
- Synchronized `site_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `bdb_utils.py` wrapping the standard library `bdb` module (`create_bdb`, `set_breakpoint`, `clear_breakpoint`, `clear_breakpoints`, `clear_all_breakpoints`, `get_breakpoints`, `get_breakpoint`, `get_file_breakpoints`, `enable_breakpoint`, `disable_breakpoint`, `is_breakpoint_enabled`, `breakpoint_hits`, `canonical_filename`, `effective_breakpoint`, `checkfuncname`) with input validation and the re-exported classes `Bdb` and `Breakpoint` together with the error `BdbQuit`, plus unit tests in `tests/test_bdb_utils.py`.
- Add `pdb_utils.py` wrapping the standard library `pdb` module (`create_pdb`, `set_trace`, `post_mortem`, `pm`, `run`, `runeval`, `runctx`, `runcall`) with input validation and the re-exported class `Pdb` together with the error `Restart`, plus unit tests in `tests/test_pdb_utils.py`.
- Synchronized `bdb_utils.py` and `pdb_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `ntpath_utils.py` wrapping the standard library `ntpath` module (abspath, basename, commonpath, commonprefix, dirname, exists, expanduser, expandvars, isabs, isdevdrive, isjunction, join, normcase, normpath, realpath, relpath, split, splitdrive, splitroot, splitext) with input validation, the re-exported constants, and the helpers `has_drive`, `is_unc_path`, `is_device_path`, `to_slashes`, and `to_backslashes`, plus unit tests in `tests/test_ntpath_utils.py`.
- Add `nturl2path_utils.py` wrapping the standard library `nturl2path` module (url2pathname, pathname2url) with input validation where applicable and unit tests in `tests/test_nturl2path_utils.py`.
- Add `curses_utils.py` wrapping the standard library `curses` module (initscr, endwin, isendwin, savetty, resetty, def_prog_mode, def_shell_mode, reset_prog_mode, reset_shell_mode, resetterm, setterm, cbreak, nocbreak, echo, noecho, raw, noraw, nl, nonl, qiflush, noqiflush, norqflush, intrflush, meta, halfdelay, curs_set, getsyx, setsyx, start_color, has_colors, can_change_color, init_pair, init_color, color_content, pair_content, color_pair, pair_number, use_default_colors, baudrate, beep, flash, delay_output, flushinp, napms, ungetch, unget_wch, newwin, doupdate, erasechar, killchar, keyname, longname, termname, termattrs, has_ic, has_il, has_key, filter, typeahead, mouseinterval, mousemask, resize_term, resizeterm, is_term_resized, update_lines_cols, setupterm, putp, use_env) with input validation, the re-exported constants and the `window` class, graceful degradation when the module is missing, plus unit tests in `tests/test_curses_utils.py`.
- Synchronized `nturl2path_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Synchronized `ntpath_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Repaired the end of `scaffold.sh`, which lost the summary of the generated project and the post-scaffold smoke test, so a scaffolded project no longer reported its files and the `--no-test` flag had no effect.
- Added the table of the developer commands to the README, so the generated project documents the targets of its `Makefile`.
- Extended `tools/refresh_scaffold.py` so that it also refreshes the documents that are embedded as templates (`README.md`, `AGENTS.md`, and `CHANGELOG.md`), with the name of the project replaced by the placeholder the generator substitutes.
- Repaired `posixpath_utils.py` and `genericpath_utils.py`, which failed the lint and the type check of the repository: the imports of the constants were placed between the definitions of the module, several lines were longer than the limit of the linter, and the calls into the standard library returned an untyped value.
- Add `posixpath_utils.py` wrapping the standard library `posixpath` module with POSIX path operations, plus unit tests in `tests/test_posixpath_utils.py`.

- Add `genericpath_utils.py` wrapping the standard library `genericpath` module (exists, isfile, isdir, islink, getsize, getmtime, getatime, getctime, commonprefix, samefile, sameopenfile, samestat, ALLOW_MISSING) with input validation and re-exports, plus unit tests in `tests/test_genericpath_utils.py`.
- Add `ipaddress_utils.py` wrapping the standard library `ipaddress` module (ip_address, ip_network, ip_interface, is_valid_address, is_valid_network, is_valid_interface, address_version, to_packed, from_packed, network_hosts, subnets, summarize_addresses, network_overlaps, address_within, common_prefix_length, next_address, previous_address, sort_addresses) with input validation and the re-exported address classes and errors, plus unit tests in `tests/test_ipaddress_utils.py`.
- Synchronized `genericpath_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Synchronized `ipaddress_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `pydoc_utils.py` wrapping the standard library `pydoc` module (`render_doc`, `doc`, `writedoc`, `writedocs`, `apropos`, `locate`, `resolve`, `safeimport`, `importfile`, `getdoc`, `synopsis`, `source_synopsis`, `describe`, `classify_class_attrs`, `classname`, `parentname`, `visiblename`, `isdata`, `ispackage`, `ispath`, `allmethods`, `splitdoc`, `stripid`, `replace`, `cram`, `plain`, `cli`, `help`, `getpager`, `plainpager`, `browse`) with input validation, and the re-exported classes `Doc`, `HTMLDoc`, `HTMLRepr`, `Helper`, `ModuleScanner`, `Repr`, `TextDoc`, and `TextRepr` together with the error `ErrorDuringImport`, plus unit tests in `tests/test_pydoc_utils.py`.
- Synchronized `pydoc_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Extend `tools/refresh_scaffold.py` so that it also creates the heredoc of a wrapper module that the generator does not embed yet, so a new module no longer has to be added to `scaffold.sh` by hand.
- Add `zipimport_utils.py` wrapping the standard library `zipimport` module (zip_importer, archive_names, get_source, get_code, get_filename, get_data, is_package, find_spec, invalidate_caches) with input validation and the re-exported `ZipImportError`, plus unit tests in `tests/test_zipimport_utils.py`.
- Synchronized `zipimport_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `encodings_utils.py` wrapping the standard library `encodings` module (normalize_encoding, is_known_encoding, is_alias, encoding_aliases, all_aliases, all_encodings) with input validation and the read-only `ALIASES` mapping, plus unit tests in `tests/test_encodings_utils.py`.
- Synchronized `encodings_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `tabnanny_utils.py` wrapping the standard library `tabnanny` module (check, process_tokens, NannyNag) with input validation, plus unit tests in `tests/test_tabnanny_utils.py`.
- Synchronized `tabnanny_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `stringprep_utils.py` wrapping the standard library `stringprep` module (table_names, map_table_names, in_table, map_table, is_unassigned, is_mapped_to_nothing, is_prohibited, is_allowed, is_bidi_allowed, map_text, find_problems, is_preparable) with input validation and read-only table mappings, plus unit tests in `tests/test_stringprep_utils.py`.
- Synchronized `stringprep_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `fcntl_utils.py` wrapping the standard library `fcntl` module (flock, lockf, control, ioctl, duplicate_fd, file_lock, unlock, get_descriptor_flags, set_descriptor_flags, get_file_status_flags, set_file_status_flags, is_cloexec, lock_kind, lock_modes, is_available) with input validation, plus unit tests in `tests/test_fcntl_utils.py`.
- Add `pty_utils.py` wrapping the standard library `pty` module (openpty, open_terminal, master_open, slave_open, fork, spawn, is_available) with input validation, a `ForkResult` named tuple, and re-exported constants, plus unit tests in `tests/test_pty_utils.py`.
- Synchronized `fcntl_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Synchronized `pty_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Repaired `pty_utils.py`, which called the `pty.master_open` and `pty.slave_open` functions that the standard library deprecated in Python 3.12, and which returned the result of `fork` as a plain tuple; the wrapper now opens the pseudo-terminal with `os.openpty` and returns a `ForkResult` named tuple.
- Completed the `pty_utils.py` synchronization, which left the architecture tree of the README and of the README template embedded in `scaffold.sh` without the new module.
- Add `termios_utils.py` wrapping the standard library `termios` module (get_attributes, set_attributes, make_raw, make_cbreak, set_read_timeout, set_blocking, get_window_size, set_window_size, drain, flush, pause_output, resume_output, send_break, control_character_names, baud_rates, is_available) with input validation, plus unit tests in `tests/test_termios_utils.py`.
- Synchronized `termios_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Repaired the README template embedded in `scaffold.sh`, which did not document the `pwd_utils`, `grp_utils`, `opcode_utils`, `pickletools_utils`, and `zipapp_utils` modules or their tests.
- Repaired the changelog template embedded in `scaffold.sh`, which did not mention the `dbm_utils`, `tracemalloc_utils`, and `tty_utils` modules or the tests of the `asyncio_utils`, `dbm_utils`, `mmap_utils`, `tracemalloc_utils`, and `tty_utils` modules.
- Strengthened `tests/test_scaffold_sync.py` with checks that the README and the changelog templates embedded in `scaffold.sh` document every module and every test the scaffold generates, so a generated project never ships a module it does not describe.
- Add `resource_utils.py` wrapping the standard library `resource` module (get_rlimit, set_rlimit, prlimit, get_rusage, get_page_size, limit_names, limit_value, limit_name, usage_names, usage_as_dict, is_available) with input validation, plus unit tests in `tests/test_resource_utils.py`.
- Add `pwd_utils.py` wrapping the standard library `pwd` module (getpwuid, getpwnam, getpwall) with input validation, plus unit tests in `tests/test_pwd_utils.py`.
- Add `grp_utils.py` wrapping the standard library `grp` module (getgrgid, getgrnam, getgrall) with input validation, plus unit tests in `tests/test_grp_utils.py`.
- Synchronized `pwd_utils.py` and `grp_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `syslog_utils.py` wrapping the standard library `syslog` module (open_log, log_message, close_log, set_log_mask, log_mask, log_upto, priority_name, priority_names, facility_name, facility_names, option_names, is_available) with input validation, plus unit tests in `tests/test_syslog_utils.py`.
- Synchronized `syslog_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `faulthandler_utils.py` wrapping the standard library `faulthandler` module (enable, disable, is_enabled, dump_traceback, dump_traceback_later, cancel_dump_traceback_later, register, unregister, is_available) with input validation, plus unit tests in `tests/test_faulthandler_utils.py`.
- Synchronized `faulthandler_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Strengthened `tests/test_scaffold_sync.py` with a check that the `pyproject.toml` template embedded in `scaffold.sh` registers every module the scaffold generates, so a generated project never ships a module it does not declare.
- Add `webbrowser_utils.py` wrapping the standard library `webbrowser` module (open_url, open_new, open_new_tab, get_controller, register_browser, register_standard_browsers, Error) with input validation, plus unit tests in `tests/test_webbrowser_utils.py`.
- Synchronized `webbrowser_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `xmlrpc_utils.py` wrapping the standard library `xmlrpc` package (dumps_value, loads_value, build_request, parse_method_call, parse_method_response, marshal_params, unmarshal_params, create_marshaller, create_transport, create_proxy, create_dispatcher, register_function, register_instance, register_introspection_functions, register_multicall_functions, resolve_dotted_attribute, list_public_methods, create_server, create_multi_path_server) with input validation, plus unit tests in `tests/test_xmlrpc_utils.py`.
- Synchronized `xmlrpc_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Repaired the misplaced `ftplib_utils.py` and `poplib_utils.py` entries, which had been written above the `## Unreleased` heading of this changelog.
- Add `ftplib_utils.py` wrapping the standard library `ftplib` module (FTP, FTP_TLS, error classes, FTP_PORT, MAXLINE, create_ftp, create_ftp_tls, connect_ftp, parse257, parse150, parse227, parse229) with input validation, plus unit tests in `tests/test_ftplib_utils.py`.
- Add `poplib_utils.py` wrapping the standard library `poplib` module (POP3, POP3_SSL, error_proto, POP3_PORT, POP3_SSL_PORT, create_pop3, create_pop3_ssl, connect_pop3) with input validation, plus unit tests in `tests/test_poplib_utils.py`.

- Add `smtplib_utils.py` wrapping the standard library `smtplib` module (quoteaddr, quote_string, quote_data, parse_address, address_only, format_address, getfqdn, parse_response, parse_ehlo_features, build_message, create_smtp, create_smtp_ssl, create_lmtp, send_message, send_text) with input validation, plus unit tests in `tests/test_smtplib_utils.py`.
- Synchronized `smtplib_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `xdrlib_utils.py` wrapping the standard library `xdrlib` module (pack_uint, unpack_uint, pack_int, unpack_int, pack_enum, unpack_enum, pack_bool, unpack_bool, pack_uhyper, unpack_uhyper, pack_hyper, unpack_hyper, pack_float, unpack_float, pack_double, unpack_double, pack_string, unpack_string, pack_bytes, unpack_bytes, pack_opaque, unpack_opaque, pack_fstring, unpack_fstring, pack_fopaque, unpack_fopaque, pack_array, unpack_array, pack_farray, unpack_farray, pack_list, unpack_list, pack_uint_array, unpack_uint_array) with input validation, plus unit tests in `tests/test_xdrlib_utils.py`.
- Synchronized `xdrlib_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Repaired the missing `tests/test_pyclbr_utils.py` entry in the README template embedded in `scaffold.sh`, so a scaffolded project documents the test of every module it ships.
- Completed the `pyclbr_utils.py` handover: the module and its test existed and were registered in `pyproject.toml`, but `scaffold.sh` never embedded either of them, so `tests/test_scaffold_sync.py` failed and a scaffolded project was missing the module entirely. Both heredocs are now part of the generator.
- Repaired the pre-existing `mypy` failure in `pyclbr_utils.py` (the `read_module_ex` return annotation claimed `Dict[str, Class | Function]`, but the standard library also returns a `__path__` entry whose value is a list of strings) and the pre-existing `ruff` failure (the now-unused `Union` import).
- Verified that a scaffolded project is still a faithful copy: the generated tree ships `pyclbr_utils.py` and `tests/test_pyclbr_utils.py`, and its 3307 tests, ruff, and mypy all pass.
- Add `pyclbr_utils.py` wrapping the standard library `pyclbr` module (`read_module`, `read_module_ex`, `class_names`, `function_names`, `find_class`, `find_function`, `has_class`, `has_function`, `is_class`, `is_function`) with input validation, plus unit tests in `tests/test_pyclbr_utils.py`.
- Synchronized `pyclbr_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `optparse_utils.py` wrapping the standard library `optparse` module (`make_parser`, `add_option`, `add_flag`, `add_count_option`, `add_option_group`, `parse_args`, `get_option`, `has_option`, `remove_option`, `get_default_values`, `set_defaults`, `get_usage`, `format_usage`, `format_help`, `format_option_help`, `get_prog_name`, `dest_for`, `string_type`, `int_type`, `float_type`, `choice_type`, `values_to_dict`) with input validation, plus unit tests in `tests/test_optparse_utils.py`.
- Synchronized `optparse_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `modulefinder_utils.py` wrapping the standard library `modulefinder` module (`load_script`, `find_dependencies`, `find_modules`, `missing_modules`, `missing_importers`, `module_path`, `is_package`, `report`) with input validation, plus unit tests in `tests/test_modulefinder_utils.py`.
- Synchronized `modulefinder_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Repaired the broken `pickletools_utils.py` handover: the wrapper passed an `output` keyword and an unknown `compact` flag to `pickletools.dis`, returned the raw `OpcodeInfo` object (a plain class since Python 3.12, so the documented tuple contract was broken), and encoded integers as a pickle stream that `decode_long` could not read. The module now follows the standard library API, `get_opcode_info` returns a tuple of the documented opcode fields, and `encode_long` produces a payload the running interpreter decodes again.
- Add `compileall_utils.py` wrapping the standard library `compileall` module (`compile_file`, `compile_dir`, `compile_path`, `main`, `pyc_path`) with input validation, plus unit tests in `tests/test_compileall_utils.py`.
- Synchronized `compileall_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Repaired the interrupted `py_compile_utils.py` handover: the previous session registered the module in `pyproject.toml` and documented it in the README, the command documentation, and the changelog, but never embedded `py_compile_utils.py` and `tests/test_py_compile_utils.py` in `scaffold.sh`, so `tests/test_scaffold_sync.py` failed and a scaffolded project was missing the module. Both heredocs are now part of the generator.
- Rewrote `compileall_utils.py` and `tests/test_compileall_utils.py` to match the conventions of the other wrappers: typed signatures, docstrings, `__all__`, and input validation. The `compileall.main` entry point reads `sys.argv` itself, so the wrapper installs the arguments temporarily and restores `sys.argv` afterwards; the tests narrow `sys.path` so the suite never byte-compiles the interpreter's own import path.
- Add `py_compile_utils.py` wrapping the standard library `py_compile` module (`compile_file`/`py_compile_file`, `get_invalidation_mode`, `parse_invalidation_mode`, `is_pyc_file`, `main`) with `PyCompileError` and `PycInvalidationMode` re-exports, plus unit tests in `tests/test_py_compile_utils.py`.
- Synchronized `py_compile_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Add `uu_utils.py` wrapping the standard library `uu` module (`uu_encode`, `uu_decode`, `encode_uu`, `decode_uu`, `parse_uu_header`, `is_uuencoded`) with input validation, plus unit tests in `tests/test_uu_utils.py`.
- Synchronized `uu_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Add `zipapp_utils.py` wrapping the standard library `zipapp` module (`create_archive`/`create_zipapp`, `get_interpreter`/`get_zipapp_interpreter`, `is_zipapp_archive`) with `ZipAppError` re-export, plus unit tests in `tests/test_zipapp_utils.py`.
- Synchronized `zipapp_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.
- Stopped the test suite from writing into the repository root: `tests/test_wave_utils.py` passed the literal path `"path"` to `wave_utils.create_writer`, which created a file named `path` in the current working directory. The test now uses a temporary directory, and `wave_utils.create_writer` closes the writer when a parameter setter fails instead of leaking the handle.
- Repaired the pre-existing `mypy` failures in `mailcap_utils.py`, `mailbox_utils.py`, and `wave_utils.py` and the pre-existing `ruff` failures in `mailbox_utils.py`, `tests/test_mailcap_utils.py`, and `tests/test_wave_utils.py`; `make lint` and `make typecheck` are green again.
- Add `wave_utils.py` wrapping the standard library `wave` module (`open_read`, `open_write`, `wave_info`, `read_frames`, `write_frames`, `create_writer`, `get_params`, `set_params`, and per-field parameter setters) with input validation, plus unit tests in `tests/test_wave_utils.py`.
- Add `mailbox_utils.py` wrapping the standard library `mailbox` module (factory helpers for mbox/Maildir/MH/MMDF/Babyl, message factories, and exception type checks) with unit tests in `tests/test_mailbox_utils.py`.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [Unreleased]

- Moved the scaffold summary and smoke test to the end of `scaffold.sh`: both used to run in the middle of the generator, so the "Created files" listing missed every module written after that point and the smoke test only discovered the tests written up to that point. The smoke test now also runs after the project name has been substituted into the templated documents.
- Removed the stray `raises.` file (about 1.1 MB) that a shell redirection accident had committed to the repository root.
- Added `mailbox_utils.py` wrapping the standard library `mailbox` module (`create_mbox`, `create_maildir`, `create_mh`, `create_babyl`, `create_mmdf`, `open_mailbox`, `add_message`, `get_message`, `remove_message`, `iter_messages`, `iter_message_keys`, `list_message_keys`, `lock_mailbox`, `unlock_mailbox`) with input validation, plus `tests/test_mailbox_utils.py`.
- Added `mailcap_utils.py` wrapping the standard library `mailcap` module with mailcap helpers, plus `tests/test_mailcap_utils.py`.
- Registered `asyncio_utils`, `imaplib_utils`, `mailbox_utils`, `mmap_utils`, `profile_utils`, `pstats_utils`, `timeit_utils`, and `unittest_utils` in the `pyproject.toml` template embedded in `scaffold.sh`, so a generated project declares every module it ships.
- Added `imaplib_utils.py` to the generated project — IMAP4 client utilities wrapping the standard library `imaplib` module (`create_imap4`, `create_imap4_ssl`, `create_imap4_stream`, `parse_capabilities`, `has_capability`, `parse_flags`, `parse_fetch_flags`, `format_flags`, `parse_internaldate`, `format_internaldate`, `int_to_ap`) with input validation, plus `tests/test_imaplib_utils.py`.
- Synchronized `imaplib_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Closed the embedded `README.md` template gap: the README written into a scaffolded project now documents every wrapper module it ships. The architecture tree lists every module and every test file, and each module has its own documentation section — 190 module sections, up from 44. The repository `README.md` gained the missing tree entries for `profile_utils.py`, `pstats_utils.py`, `select_utils.py`, and `unittest_utils.py`, plus a `Hello Module` section.
- Fixed the project name placeholder in generated projects: `scaffold.sh` now substitutes the project name into `README.md`, `AGENTS.md`, and `CHANGELOG.md` after writing them, so a scaffolded project no longer ships documents that contain the literal placeholder. `tests/test_scaffold.py` guards the substitution.
- Fixed the pre-existing `mypy` errors that broke `make typecheck`: the implicit `Optional` annotations in `traceback_utils.py`, `tempfile_utils.py`, and `warnings_utils.py`, the `profile.main` entry that the type stubs do not declare, and the narrow `pstats.Stats` constructor signature. `make typecheck` now passes for the whole project.
- Added `symtable_utils.py` to the generated project — symbol table utilities wrapping the standard library `symtable` module (`build_symbol_table`, `lookup_symbol_table`, `scope_type`, `scope_identifiers`, `child_scopes`, `iter_scopes`, `find_scope`, `describe_scope`, `symbol_info`, `symbol_flags`, `namespace_names`, `free_variables`, `global_names`, `local_names`, `parameter_names`, `imported_names`, `assigned_names`, `referenced_names`, `nonlocal_names`) with input validation, plus `tests/test_symtable_utils.py`.
- Synchronized `symtable_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `pstats_utils.py` to the generated project — profiling statistics utilities wrapping the standard library `pstats` module (`Stats`, `SortKey`, `new_stats`, `load_stats`, `add_stats`, `print_stats`, `sort_stats`, `strip_dirs`, `reverse_order`, `dump_stats`) with input validation, plus `tests/test_pstats_utils.py`.
- Synchronized `pstats_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `select_utils.py` to the generated project — I/O multiplexing utilities wrapping the standard library `select` module (`select`, `create_poller`, `poll_register`, `poll_poll`, `PIPE_BUF`) with input validation, plus `tests/test_select_utils.py`.
- Synchronized `select_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.


- Added `trace_utils.py` to the generated project — execution tracing utilities wrapping the standard library `trace` module (`new_tracer`, `run_traced`, `run_script_traced`, `counted_lines`, `line_counts`, `called_functions`, `call_relationships`, `is_ignored_filename`, `merge_results`, `write_coverage_report`, `summarize_coverage`, `format_coverage_summary`, `clear_counts`) with input validation, plus `tests/test_trace_utils.py`.
- Synchronized `trace_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `profile_utils.py` to the generated project — profiling utilities wrapping the standard library `profile` module (`Profile`, `run`, `runctx`, `new_profiler`) with input validation, plus `tests/test_profile_utils.py`.
- Synchronized `profile_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Replaced the placeholder `trace_utils.py` that earlier sessions left behind — it re-exported only `Trace` and `CoverageResults`, had no test file, and was not generated by `scaffold.sh` — with a complete wrapper of the standard library `trace` module and a test suite of 65 tests.
- Removed the broken template leftovers in `.kilo/command/scaffold-project.md` (`-  — trace utility functions wrapping the standard library trace module (, )` and `-  — unit tests for`), whose module name and function list had been expanded away.
- Added `doctest_utils.py` to the generated project — doctest utilities wrapping the standard library `doctest` module (`parse_doctests`, `find_doctests`, `run_string_examples`, `run_docstring_examples`, `run_module_examples`, `run_file_examples`, `summarize_results`, `format_failure`) with input validation, plus `tests/test_doctest_utils.py`.
- Synchronized `doctest_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Restored the byte-identical embedded copies of `timeit_utils.py`, `tests/test_mmap_utils.py`, `tests/test_tty_utils.py`, and `tests/test_unittest_utils.py` in `scaffold.sh`: they had drifted from the repository sources, so scaffolded projects shipped outdated modules and failed the synchronization guard.
- Added `tools/refresh_scaffold.py`, a maintainer tool that rewrites the file copies embedded in `scaffold.sh` from the repository sources and reports stale copies with `--check`, plus `tests/test_refresh_scaffold.py` and a `make refresh-scaffold` target.
- Made `.kilo/command/scaffold-project.md` an exact copy of its embedded counterpart in `scaffold.sh`; the embedded copy had drifted and listed some modules twice.
- `scaffold.sh` now copies itself into every project it generates, so a scaffolded project ships a working generator again: its `make scaffold` target, its `scaffold.sh` pre-commit hook, and its documented ability to scaffold further projects all work instead of referring to a missing file.
- Marked `scaffold.sh` executable in the repository; `make scaffold` and the `scaffold.sh` pre-commit hook failed with a permission error because the file was not executable.

- Added `mimetypes_utils.py` to the generated project — MIME type detection utilities wrapping the standard library `mimetypes` module (`guess_type, guess_extension, guess_all_extensions, type_for_extension, add_type, init_database, normalize_extension, is_valid_mime_type, mime_category, is_text_mime_type`) with input validation, plus `tests/test_mimetypes_utils.py`.
- Synchronized `mimetypes_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `sysconfig_utils.py` to the generated project — build configuration utilities wrapping the standard library `sysconfig` module (`get_config_vars`, `get_config_var`, `has_config_var`, `list_config_var_names`, `get_paths`, `get_path`, `get_platform`, `get_python_version`, `get_default_scheme`, `get_preferred_scheme`, `get_scheme_names`, `is_python_build`, `get_config_h_filename`, `get_makefile_filename`) with input validation, plus `tests/test_sysconfig_utils.py`.
- Synchronized `sysconfig_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `socket_utils.py` to the generated project — low-level socket utilities wrapping the standard library `socket` module (`create_socket, create_tcp_socket, create_udp_socket, socket_address, resolve_address, connect_socket, create_connection, bind_socket, listen_socket, accept_connection, send_all, send_to, receive_bytes, receive_from, set_timeout, get_timeout, set_nonblocking, set_reuse_address, set_keepalive, shutdown_socket, close_socket, get_socket_name, get_peer_name, socket_family_name, socket_type_name, error_name, get_hostname, has_ipv6, is_ipv6_address`) with input validation, plus `tests/test_socket_utils.py`.
- Synchronized `socket_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `cmd_utils.py` to the generated project — command interpreter utilities wrapping the standard library `cmd` module (`identchars`, `prompt_default`, `main`) with input validation, plus `tests/test_cmd_utils.py`.
- Synchronized `cmd_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `this_utils.py` to the generated project — Zen of Python utilities wrapping the standard library `this` module (`zen_of_python`, `translation_table`, `cipher_index`, `this`, `print_zen`) with input validation, plus `tests/test_this_utils.py`.
- Synchronized `this_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `tokenize_utils.py` to the generated project — source tokenization utilities wrapping the standard library `tokenize` module (`tokenize_source, tokenize_file, generate_tokens, untokenize, token_name, token_type, detect_encoding, significant_tokens, is_comment, is_string, is_number, is_name, is_keyword`) with input validation, plus `tests/test_tokenize_utils.py`.
- Synchronized `tokenize_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `dbm_utils.py` to the generated project — database utilities wrapping the standard library `dbm` module (`open_database`, `close`, `which_database`, `available_backends`, `read_record`, `write_record`, `delete_record`, `has_key`, `list_keys`, `sync_database`, `is_valid_flag`, `dbm_error`) with input validation, plus `tests/test_dbm_utils.py`.
- Synchronized `dbm_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Restored the missing `tests/test_this_utils.py` entry in the generated project's README test tree, which earlier sessions left out of the embedded README template.
- Added `code_utils.py` to the generated project — interactive console utilities wrapping the standard library `code` module (`interact`, `compile_command`, `console_class`, `interpreter_class`) with input validation, plus `tests/test_code_utils.py`.
- Synchronized `code_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `codeop_utils.py` to the generated project — utilities for compiling possibly-incomplete Python source wrapping the standard library `codeop` module (`compile_command`, `Compile`, `CommandCompiler`) with input validation, plus `tests/test_codeop_utils.py`.
- Synchronized `codeop_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `copyreg_utils.py` to the generated project — pickle support registration utilities wrapping the standard library `copyreg` module (`add_extension`, `remove_extension`, `clear_extension_cache`, `constructor`, `dispatch_table`, `pickle`) with input validation, plus `tests/test_copyreg_utils.py`.
- Synchronized `copyreg_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `fileinput_utils.py` to the generated project — file input iteration utilities wrapping the standard library `fileinput` module (`read_lines`, `count_lines`, `filenames`) with input validation, plus `tests/test_fileinput_utils.py`.
- Synchronized `fileinput_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `fnmatch_utils.py` to the generated project — filename pattern matching utilities wrapping the standard library `fnmatch` module (`match`, `match_case`, `filter_names`, `translate`) with input validation, plus `tests/test_fnmatch_utils.py`.
- Synchronized `fnmatch_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `getpass_utils.py` to the generated project — secure password input utilities wrapping the standard library `getpass` module (`getpass`, `getuser`) with input validation, plus `tests/test_getpass_utils.py`.
- Synchronized `getpass_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `id_utils.py` to the generated project — identifier generation and validation utilities (`generate_id`, `new_id`, `is_valid_id`) with input validation, plus `tests/test_id_utils.py`.
- Synchronized `id_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `memoize_utils.py` to the generated project — memoization utilities (`memoize` decorator) that cache function return values keyed by call arguments with a `cache_clear` method, plus `tests/test_memoize_utils.py`.
- Synchronized `memoize_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `pathlib_utils.py` to the generated project — path manipulation utilities wrapping the standard library `pathlib` module (`ensure_dir`, `join`, `exists`, `is_file`, `is_dir`, `read_text`, `write_text`, `glob`, `rglob`, `suffix`, `stem`, `parent`) with input validation, plus `tests/test_pathlib_utils.py`.
- Synchronized `pathlib_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `runpy_utils.py` to the generated project — Python module execution utilities wrapping the standard library `runpy` module (`run_module`, `run_path`) with input validation, plus `tests/test_runpy_utils.py`.
- Synchronized `runpy_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `secrets_utils.py` to the generated project — cryptographically secure secrets and token utilities wrapping the standard library `secrets` module (`token_bytes`, `token_hex`, `token_urlsafe`, `compare_digest`, `randbelow`, `randbits`, `choice`) with input validation, plus `tests/test_secrets_utils.py`.
- Synchronized `secrets_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Synchronized `ssl_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `tarfile_utils.py` to the generated project — tar archive utilities wrapping the standard library `tarfile` module (`tarfile_open`, `tarfile_add`, `tarfile_list`, `tarfile_extract`, `tarfile_extractall`, `tarfile_create`) with input validation, plus `tests/test_tarfile_utils.py`.
- Synchronized `tarfile_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `types_utils.py` to the generated project — dynamic type creation utilities wrapping the standard library `types` module (`new_class`, `new_function`, `is_function`, `is_method`, `is_generator`, `is_coroutine`, `is_lambda`, `simple_namespace`) with input validation, plus `tests/test_types_utils.py`.
- Synchronized `types_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `zoneinfo_utils.py` to the generated project — IANA timezone utilities wrapping the standard library `zoneinfo` module (`zoneinfo_get`, `zoneinfo_available_timezones`) with input validation, plus `tests/test_zoneinfo_utils.py`.
- Added `opcode_utils.py` to the generated project — opcode utilities wrapping the standard library `opcode` module (stack effect computation and opcode classification helpers), plus `tests/test_opcode_utils.py`.
- Synchronized `zoneinfo_utils.py` and `opcode_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `rlcompleter_utils.py` to the generated project — interactive tab completion utilities wrapping the standard library `rlcompleter` module (`Completer`, `complete`) with input validation, plus `tests/test_rlcompleter_utils.py`.
- Synchronized `rlcompleter_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `tracemalloc_utils.py` to the generated project — tracemalloc memory tracing utilities wrapping the standard library `tracemalloc` module (`is_tracing`, `get_traced_memory`, `get_traceback_limit`, `start`, `stop`, `clear_traces`), plus `tests/test_tracemalloc_utils.py`.
- Synchronized `tracemalloc_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Refreshed every module and test copy embedded in `scaffold.sh` so the generator emits the current repository sources byte for byte; 73 modules and 71 tests had drifted to older revisions, which made scaffolded projects fail 9 of their own tests and fail ruff and mypy.
- Added the missing `tests/test_importlib_utils.py` generator heredoc: the module was generated but its test file was not, so scaffolded projects shipped an untested module.
- Quoted the `dataclasses_utils.py` and `tests/test_dataclasses_utils.py` generator heredocs so their docstring backticks are no longer subject to shell command substitution.
- Completed the documentation surface for every wrapper module: added the 18 missing README module sections, the 31 missing README tree entries, the 5 missing `.kilo/command/scaffold-project.md` module entries, and the missing CHANGELOG entries.
- Completed the `scaffold.sh` header comment inventory: every wrapper module and its test now has a header entry, and the six duplicate entries left by earlier sessions were removed.

- Fixed the scaffold pipeline drift: 15 wrapper modules (`cmd_utils.py`, `code_utils.py`, `copyreg_utils.py`, `fileinput_utils.py`, `fnmatch_utils.py`, `getpass_utils.py`, `id_utils.py`, `memoize_utils.py`, `pathlib_utils.py`, `runpy_utils.py`, `secrets_utils.py`, `ssl_utils.py`, `tarfile_utils.py`, `types_utils.py`, and `zoneinfo_utils.py`) existed in the repository but were never added to `scaffold.sh`, so scaffolded projects were missing them entirely. Each module and its test now have generator heredocs, header comment entries, embedded `pyproject.toml` `py_modules` entries, embedded README tree and module sections, embedded CHANGELOG entries, README tree and module sections, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and `CHANGELOG.md` entries.
- Added `tests/test_scaffold_sync.py`, a synchronization guard that fails when a wrapper module is missing from `pyproject.toml`, `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, `CHANGELOG.md`, or `tests/test_scaffold.py`, or when an embedded copy differs from the repository file.

- Added `gc_utils.py` — GC utilities wrapping the standard library `gc` module (`enable`, `disable`, `isenabled`, `collect`, `get_count`, `get_stats`, `get_objects`, `get_referents`, `get_referrers`, `set_threshold`, `get_threshold`, `set_debug`, `get_debug`), plus `tests/test_gc_utils.py`.
- Added `greeting_utils.py` — Greeting utilities (`greet`, `format_names`, `random_greeting`) for formatted greeting strings, plus `tests/test_greeting_utils.py`.
- Added `tests/test_markdown_utils.py` — unit tests for `markdown_utils.py`.
- Added `tests/test_multiprocessing_utils.py` — unit tests for `multiprocessing_utils.py`.
- Added `tests/test_shutil_utils.py` — unit tests for `shutil_utils.py`.
- Added `atexit_utils.py` — exit handler utilities wrapping the standard library `atexit` module (`register`, `unregister`, `run_exitfuncs`, `_clear`, `_run_exitfuncs`) with input validation, plus `tests/test_atexit_utils.py`.
- Added `lzma_utils.py` — LZMA compression utilities wrapping the standard library `lzma` module (`lzma_compress`, `lzma_decompress`, `lzma_open`, `lzma_write`, `lzma_read`) with input validation, plus `tests/test_lzma_utils.py`.
- Added `tests/test_codecs_utils.py` — unit tests for `codecs_utils.py`.

- Added `shelve_utils.py` — persistent key/value storage utilities wrapping the standard library `shelve` module (`open_shelf`, `close`, `sync`, `keys`, `get`, `set_value`, `delete`, `contains`, `is_shelf`) with input validation, plus `tests/test_shelve_utils.py`.
- Synchronized `shelve_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `zlib_utils.py` — zlib compression and checksum utilities wrapping the standard library `zlib` module (`zlib_compress`, `zlib_decompress`, `zlib_compressobj`, `zlib_decompressobj`, `zlib_crc32`, `zlib_adler32`) with input validation, plus `tests/test_zlib_utils.py`.
- Synchronized `zlib_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `pkgutil_utils.py` — package and module discovery utilities wrapping the standard library `pkgutil` module (`iter_modules`, `walk_packages`, `get_data`, `read_text`, `resolve_name`, `iter_importers`, `extend_path`, `find_spec`) with input validation, plus `tests/test_pkgutil_utils.py`.
- Synchronized `pkgutil_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Fixed malformed heredocs in `scaffold.sh` that swallowed the `linecache_utils.py`, `platform_utils.py`, `semver_utils.py`, `shutil_utils.py`, `hashlib_utils.py`, `time_utils.py`, and `template_utils.py` sections into neighbouring generated files; the scaffold smoke test now completes successfully.
- Resynced the embedded `gettext_utils.py`, `heapq_utils.py`, `inspect_utils.py`, `threading_utils.py`, and `traceback_utils.py` modules (and their tests) in `scaffold.sh` with the current repository versions so the scaffolded project test suite passes.
- Registered the existing `multiprocessing_utils.py`, `numbers_utils.py`, and `sched_utils.py` modules in `pyproject.toml` `py_modules`.
- Added `TestScaffoldHeredocs` to `tests/test_scaffold.py`, guarding against unbalanced or nested heredocs in `scaffold.sh` and against generated Python files that are written empty.

- Registered the existing `unicodedata_utils.py` module and `tests/test_unicodedata_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `unicodedata_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `tomllib_utils.py` module and `tests/test_tomllib_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `tomllib_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `token_utils.py` module and `tests/test_token_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `token_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `sched_utils.py` module and `tests/test_sched_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `sched_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `quopri_utils.py` module and `tests/test_quopri_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `quopri_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `numbers_utils.py` module and `tests/test_numbers_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `numbers_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `netrc_utils.py` module and `tests/test_netrc_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `netrc_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `getopt_utils.py` module and `tests/test_getopt_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `getopt_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `filecmp_utils.py` module and `tests/test_filecmp_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `filecmp_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `errno_utils.py` module and `tests/test_errno_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `errno_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `dis_utils.py` module and `tests/test_dis_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `dis_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `contextvars_utils.py` module and `tests/test_contextvars_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `contextvars_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `configparser_utils.py` module and `tests/test_configparser_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `configparser_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Registered the existing `binascii_utils.py` module and `tests/test_binascii_utils.py` with the project: added them to `pyproject.toml` `py_modules`, `scaffold.sh` (header comment, embedded pyproject, module and test heredocs, embedded README and CHANGELOG), the README tree and module section, `.kilo/command/scaffold-project.md`, and the `tests/test_scaffold.py` assertions.
- Synchronized `binascii_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `ssl_utils.py` to the generated project — SSL/TLS utilities wrapping the standard library `ssl` module (`create_default_context`, `create_context`, `match_hostname`, `get_server_certificate`, `get_server_certificate_tuple`, `cert_time_to_seconds`, `verify_cert_chain`, `get_default_verify_paths`, `is_tls_version_supported`, `get_cert_subject`, `get_cert_issuer`, `get_cert_san`, `cert_is_valid_at_time`) with input validation, plus `tests/test_ssl_utils.py`.
- Synchronized `ssl_utils.py` across `pyproject.toml` `py_modules`, README tree and module section, and this CHANGELOG Unreleased entry.

- Added `ctypes_utils.py` — ctypes utility functions wrapping the standard library `ctypes` module (re-exports fundamental C types, `Structure`, `Union`, `POINTER`, `Array`, `CFUNCTYPE`, and helpers `sizeof`, `alignment`, `addressof`, `pointer`, `byref`, `cast`, `memmove`, `memset`, `string_at`, `create_string_buffer`, `create_unicode_buffer`, `get_errno`, `set_errno`, `get_last_error`, `set_last_error`, `find_library`), plus `tests/test_ctypes_utils.py`.
- Synchronized `ctypes_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, and this CHANGELOG Unreleased entry.

- Added `gettext_utils.py` — internationalization utilities wrapping the standard library `gettext` module (`gettext`, `dgettext`, `ngettext`, `dngettext`, `textdomain`, `bindtextdomain`, `install`) with input validation, plus `tests/test_gettext_utils.py`.
- Synchronized `gettext_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `signal_utils.py` — signal utilities wrapping the standard library `signal` module (`alarm`, `pause`, `register_handler`, `register_int_handler`, `register_term_handler`, `set_handler`, `get_handler`, `get_signal_name`, `is_valid_signal`, `signal_names`, `interrupt_handler`, `suspend_handler`, `unregister_handler`, `signal_info`) with input validation, plus `tests/test_signal_utils.py`.
- Synchronized `signal_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `zipfile_utils.py` — ZIP archive utilities wrapping the standard library `zipfile` module (`create_archive`, `list_names`, `extract_all`, `is_zipfile`) with input validation, plus `tests/test_zipfile_utils.py`.
- Synchronized `zipfile_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `bz2_utils.py` — BZ2 compression utilities wrapping the standard library `bz2` module (`bz2_compress`, `bz2_decompress`, `bz2_open`, `bz2_write`, `bz2_read`), plus `tests/test_bz2_utils.py`.
- Synchronized `bz2_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `marshal_utils.py` — object serialization utilities wrapping the standard library `marshal` module (`dumps`, `loads`, `dump`, `load`, `get_version`) with input validation, plus `tests/test_marshal_utils.py`.
- Synchronized `marshal_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `sqlite3_utils.py` — SQLite database utilities (`connect`, `execute`, `executemany`, `fetch_all`, `fetch_one`, `fetch_many`, `create_table`, `insert_row`, `query`, `table_exists`) wrapping the standard library `sqlite3` module, plus `tests/test_sqlite3_utils.py`.
- Synchronized `sqlite3_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `pickle_utils.py` — object serialization utilities wrapping the standard library `pickle` module (`dump`, `dumps`, `load`, `loads`, `pickler`, `unpickler`, `is_valid_protocol`, `validate_protocol`) with input validation, plus `tests/test_pickle_utils.py`.
- Synchronized `pickle_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `stat_utils.py` — stat file type/mode utilities (`file_mode`, `file_type`, `is_directory`, `is_regular_file`, `is_symlink`, `is_socket`, `is_fifo`, `is_device`, `filemode`, `stat_info`) wrapping the standard library `stat` and `os.stat` modules, plus `tests/test_stat_utils.py`.
- Synchronized `stat_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Removed a duplicate `copy_utils` entry from `pyproject.toml` `py_modules` (it was listed twice, once near `config_schema` and once near `colorsys_utils`); the module itself, its tests, and all scaffold/doc entries were already present and correct.

- Added `abc_utils.py` — abstract base class utilities wrapping the standard library `abc` module (`ABC`, `ABCMeta`, `abstractmethod`, `abstractclassmethod`, `abstractstaticmethod`, `abstractproperty`, `get_cache_token`, `update_abstractmethods`), plus `tests/test_abc_utils.py`.

- Added `ast_utils.py` — abstract syntax tree utilities wrapping the standard library `ast` module (`parse`, `unparse`, `dump`, `literal_eval`, `get_docstring`, `walk`, `iter_fields`, `iter_child_nodes`, `find_all`, `fix_missing_locations`, `increment_lineno`, `copy_location`, `node_to_string`), plus `tests/test_ast_utils.py`.

- Synchronized `abc_utils.py` and `ast_utils.py` across `pyproject.toml` `py_modules`, README tree and module sections, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` header comment and heredocs for the modules and their tests, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Synchronized `codecs_utils.py` across the README by adding the missing `## Codecs Utilities Module` section; the module, tests, `pyproject.toml` `py_modules`, `.kilo/command/scaffold-project.md`, and `tests/test_scaffold.py` assertions were already present.

- Synchronized `reprlib_utils.py` across the README by adding the missing `## Reprlib Utilities Module` section; the module, tests, `pyproject.toml` `py_modules`, `scaffold.sh`, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and CHANGELOG entries were already present.

- Added `traceback_utils.py` — traceback utilities wrapping the standard library `traceback` module (`format_exception`, `format_exception_only`, `extract_stack`, `format_stack`, `format_exc`), plus `tests/test_traceback_utils.py`.
- Synchronized `traceback_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `typing_utils.py` — typing utilities wrapping the standard library `typing` module (`get_type_hints`, `get_origin`, `get_args`, `is_typeddict`) with re-exports of `overload`, `Final`, `Literal`, and `ClassVar`, plus `tests/test_typing_utils.py`.
- Synchronized `typing_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `pprint_utils.py` — pretty-printing utilities wrapping the standard library `pprint` module (`pformat`, `pprint`, `isreadable`, `isrecursive`, `saferepr`) with input validation, plus `tests/test_pprint_utils.py`.
- Synchronized `pprint_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `colorsys_utils.py` — colorsys utilities wrapping the standard library `colorsys` module (`rgb_to_hls`, `hls_to_rgb`, `rgb_to_hsv`, `hsv_to_rgb`, `rgb_to_yiq`, `yiq_to_rgb`) with input validation, plus `tests/test_colorsys_utils.py`.
- Synchronized `colorsys_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, and this CHANGELOG Unreleased entry.

- Added `dataclasses_utils.py` — dataclass utilities wrapping the standard library `dataclasses` module (`is_dataclass`, `is_dataclass_instance`, `fields`, `asdict`, `astuple`, `replace`, `make_dataclass`, `get_field_names`, `get_field_default`, `has_field`) with input validation, plus `tests/test_dataclasses_utils.py`.
- Synchronized `dataclasses_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, and this CHANGELOG Unreleased entry.

- Added `linecache_utils.py` — line cache utilities wrapping the standard library `linecache` module (`getline`, `getlines`, `updatecache`, `clearcache`) with input validation, plus `tests/test_linecache_utils.py`.
- Synchronized `linecache_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `contextlib_utils.py` — contextlib utility functions wrapping the standard library `contextlib` module (`suppress`, `nullcontext`, `closing`, `redirect_stdout`, `redirect_stderr`, `chdir`, `ExitStack`) with input validation, plus `tests/test_contextlib_utils.py`.
- Synchronized `contextlib_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `keyword_utils.py` — Python keyword classification utilities wrapping the standard library `keyword` module (`is_keyword`, `is_soft_keyword`, `kwlist`, `softkwlist`, `main`) with input validation, plus `tests/test_keyword_utils.py`.
- Synchronized `keyword_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `shlex_utils.py` — simple lexical analysis utilities wrapping the standard library `shlex` module (`split`, `quote`, `join`) with input validation, plus `tests/test_shlex_utils.py`.
- Synchronized `shlex_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `glob_utils.py` — utilities for pathname pattern expansion wrapping the standard library `glob` module (`glob_pattern`, `iglob`, `escape`, `has_magic`) with input validation, plus `tests/test_glob_utils.py`.
- Synchronized `glob_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `email_utils.py` — email utilities wrapping the standard library `email.utils` module (`email_formatdate`, `email_parsedate`, `email_parsedate_to_datetime`, `email_mktime_tz`, `email_parseaddr`, `email_formataddr`, `email_getaddresses`, `email_make_msgid`, `email_quote`, `email_unquote`, `email_format_datetime`) with input validation, plus `tests/test_email_utils.py`.
- Synchronized `email_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `socketserver_utils.py` — Socketserver utilities wrapping the standard library `socketserver` module for building TCP/UDP servers (`create_tcp_server`, `create_udp_server`, `handle_one_request`, `serve_forever`, `shutdown_server`, `close_server`, `get_server_address`, `is_serving`) with input validation, plus `tests/test_socketserver_utils.py`.
- Synchronized `socketserver_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `threading_utils.py` — threading utilities wrapping the standard library `threading` module (`create_lock`, `create_rlock`, `create_semaphore`, `create_bounded_semaphore`, `create_event`, `create_condition`, `create_timer`, `create_thread`, `current_thread`, `active_count`, `enumerate_threads`, `synchronized`) with input validation, plus `tests/test_threading_utils.py`.
- Synchronized `threading_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `cmath_utils.py` — complex mathematics utilities wrapping the standard library `cmath` module (`phase`, `polar`, `rect`, `exp`, `log`, `log10`, `sqrt`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh`, `isfinite`, `isinf`, `isnan`, `isclose`) with input validation, plus `tests/test_cmath_utils.py`.
- Synchronized `cmath_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `difflib_utils.py` — difflib utility functions for sequence comparison and diffing (`get_close_matches`, `ratio`, `unified_diff`, `context_diff`, `ndiff`) wrapping the standard library `difflib` module, plus `tests/test_difflib_utils.py`.
- Synchronized `difflib_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `bisect_utils.py` — bisect utility functions for binary search on sorted sequences (`bisect_left`, `bisect_right`, `insort_left`, `insort_right`, `find_leftmost`, `find_rightmost`) wrapping the standard library `bisect` module, plus `tests/test_bisect_utils.py`.
- Synchronized `bisect_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `warnings_utils.py` — utilities wrapping the standard library `warnings` module (`warn`, `simplefilter`, `catch_warnings`, `filterwarnings`, `resetwarnings`) with input validation, plus `tests/test_warnings_utils.py`.
- Synchronized `warnings_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `argparse_utils.py` — argument parsing utilities (`make_parser`, `add_flag`, `add_option`, `add_positional`, `add_subparsers`, `parse_args`, `int_positive`, `float_range`) wrapping the standard library `argparse` module, plus `tests/test_argparse_utils.py`.
- Synchronized `argparse_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `selectors_utils.py` — selectors utilities wrapping the standard library `selectors` module (`create_default_selector`, `register`, `unregister`, `select`, `get_key`, `get_map`, `close_selector`, `EVENT_READ`, `EVENT_WRITE`) for I/O multiplexing with input validation, plus `tests/test_selectors_utils.py`.
- Synchronized `selectors_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `hmac_utils.py` — HMAC-based message authentication utilities (`hmac_md5`, `hmac_sha1`, `hmac_sha256`, `hmac_sha512`, `hmac_new`, `sign`, `verify`, `compare_digest`) wrapping the standard library `hmac` and `hashlib` modules with constant-time verification, plus `tests/test_hmac_utils.py`.
- Synchronized `hmac_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Synchronized `copy_utils.py` across the `scaffold.sh` heredoc for `.kilo/command/scaffold-project.md` so the scaffolded project documentation lists the module and its tests; previously the doc entry was missing, causing `tests/test_scaffold.py::test_scaffold_project_doc_lists_all_modules` to fail.

- Added `copy_utils.py` — copy utilities (`shallow_copy`, `deep_copy`, `copy_dict`, `deep_copy_dict`, `merge_copy`, `is_same_object`) wrapping the standard library `copy` module with input validation, plus `tests/test_copy_utils.py`.
- Synchronized `copy_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `timezone_utils.py` — time zone utilities using the standard library `zoneinfo` module (`get_timezone`, `is_valid_timezone`, `get_utc_now`, `get_local_timezone`, `convert_datetime`, `format_datetime`, `utc_offset`, `is_dst`, `get_common_timezones`, `get_all_timezones`) with input validation, plus `tests/test_timezone_utils.py`.
- Synchronized `timezone_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `ring_buffer_utils.py` — fixed-size circular (ring) buffer utilities (`RingBuffer`, `create`, `append`, `get`, `peek`, `pop`, `clear`, `to_list`, `from_list`, plus `capacity`, `is_full`, `is_empty`) with input validation, plus `tests/test_ring_buffer_utils.py`.
- Synchronized `ring_buffer_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions.

- Added `deprecation_utils.py` — deprecation utilities (`deprecated` decorator) that emit a `DeprecationWarning` on each invocation of a deprecated callable, with optional `version`, `replacement`, and custom `message` fields, plus `tests/test_deprecation_utils.py`.
- Synchronized `deprecation_utils.py` across `pyproject.toml` `py_modules` and README module section.

- Added `circuit_breaker_utils.py` — circuit breaker resilience utilities (`CircuitBreaker`, `CircuitOpenError`) implementing the circuit breaker pattern with thread-safe `CLOSED`/`OPEN`/`HALF_OPEN` state transitions, failure threshold, recovery timeout, and expected-exception filtering, plus `tests/test_circuit_breaker_utils.py`.
- Synchronized `circuit_breaker_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `call_once_utils.py` — call-once execution utilities (`call_once` decorator) ensuring a wrapped function runs only a single time, with thread-safe caching and a `reset` method, plus `tests/test_call_once_utils.py`.
- Synchronized `call_once_utils.py` across `scaffold.sh` header comment, `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `enum_utils.py` — enum utilities for working with Python `enum.Enum` classes (`enum_to_dict`, `get_enum_member`, `is_enum_member`, `list_enum_members`, `enum_value_from_name`, `enum_name_from_value`) with input validation.
- `tests/test_enum_utils.py` — unit tests for `enum_utils.py`
- Added `enum_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions.

- Added `inspect_utils.py` — callable and object introspection utilities (`get_callable_name`, `is_callable`, `is_async_callable`, `get_signature`, `get_parameter_names`, `get_parameter_kinds`, `count_parameters`, `has_parameter`, `bind_arguments`, `is_builtin`, `get_source_file`, `get_source_lines`) using the standard library `inspect` module with input validation.
- `tests/test_inspect_utils.py` — unit tests for `inspect_utils.py`

- Added `id_utils.py` to the generated project — identifier generation and validation utilities (`generate_id`, `new_id`, `is_valid_id`) for short URL-safe random identifiers with input validation.
- `tests/test_id_utils.py` — unit tests for `id_utils.py`

- Added `interval_utils.py` — interval utilities (`normalize_interval`, `is_valid_interval`, `interval_contains`, `interval_overlaps`, `interval_intersection`, `interval_union`, `merge_intervals`, `interval_length`) for closed numeric intervals with input validation.
- `tests/test_interval_utils.py` — unit tests for `interval_utils.py`
- Added `interval_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and test tree, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- Synchronized the `scaffold.sh` README tree with the repository `README.md` project structure tree: the scaffold template was missing 23 modules (`template_utils.py`, `uuid_utils.py`, `prompt_utils.py`, `itertools_utils.py`, `color_utils.py`, `number_utils.py`, `os_utils.py`, `sort_utils.py`, `prime_utils.py`, `decimal_utils.py`, `fractions_utils.py`, `heapq_utils.py`, `markdown_utils.py`, `bytes_utils.py`, `functools_utils.py`, `operator_utils.py`, `exceptions_utils.py`, `io_utils.py`, `ini_utils.py`, `weakref_utils.py`, `compression_utils.py`, `ip_utils.py`, `regex_utils.py`, `subprocess_utils.py`) and 26 test files (`test_async_utils.py`, `test_base64_utils.py`, `test_bytes_utils.py`, `test_calendar_utils.py`, `test_cli_utils.py`, `test_context_utils.py`, `test_decimal_utils.py`, `test_duration_utils.py`, `test_fractions_utils.py`, `test_hash_utils.py`, `test_html_utils.py`, `test_ini_utils.py`, `test_itertools_utils.py`, `test_networking_utils.py`, `test_number_utils.py`, `test_operator_utils.py`, `test_os_utils.py`, `test_prompt_utils.py`, `test_seq_utils.py`, `test_sort_utils.py`, `test_subprocess_utils.py`, `test_sys_utils.py`, `test_temp_utils.py`, `test_template_utils.py`, `test_terminal_utils.py`, `test_uuid_utils.py`, `test_weakref_utils.py`, `test_xml_utils.py`) from the repo tree, and had a stray `tests/test_calendar_utils.py` entry outside the `tests/` sub-section. Replaced both the module and tests sections of the scaffold template tree with the canonical alphabetized repo tree so scaffolded projects inherit a complete, consistent structure.

- Registered `locale_utils` across the full scaffold pipeline: the module existed as a source file with passing tests and was listed in `pyproject.toml` `py_modules`, but was missing from `scaffold.sh` (header comment, `py_modules` list, README tree, module/test sections, and CHANGELOG entries), `README.md` (tree, test tree, module description section), `.kilo/command/scaffold-project.md` (modules and tests lists), and `tests/test_scaffold.py` (required files, module lists, and functional smoke test). Added the `locale_utils.py` and `tests/test_locale_utils.py` heredoc blocks to `scaffold.sh`, the `test_locale_utils_functions_work` smoke test, and synchronized all documentation so scaffolded projects now include the locale utilities module.

- Added the missing `tests/test_compression_utils.py` and `tests/test_ip_utils.py` heredoc blocks to `scaffold.sh`: both modules existed as source files with passing tests and were registered in `pyproject.toml` `py_modules`, but the test heredocs were absent, so `--no-test` scaffolded projects were missing them. Verified the scaffold smoke test now generates both test files.

- Rebuilt the `scaffold.sh` header comment from the canonical README tree: removed 23 duplicate module/test entries and added the 6 missing modules (`itertools_utils`, `compression_utils`, `ip_utils`, `prompt_utils`, `uuid_utils`, `template_utils`) plus their test entries so the header lists every module exactly once in tree order.

- Removed a corrupted artifact left by a previous session: a phantom directory named `<` containing a bogus `</rfl:parameter>home/.../tests/test_copy_utils.py` file (a tool-call path leaked into file content). The `copy_utils.py` module does not exist in this repository; the artifact was untracked and is now deleted. Cleared the stale `.ruff_cache` so `make lint` reports against the real tree.

- Fixed a leaked line-number token (`113:`) in the `README.md` project structure tree that appeared as a prefix on the `compression_utils.py` entry.

- Added the missing `tests/test_subprocess_utils.py`, `tests/test_hash_utils.py`, `tests/test_weakref_utils.py`, `tests/test_fractions_utils.py`, and `tests/test_stats.py` entries to the Unreleased CHANGELOG section so the generated changelog lists every test file (the modules themselves were already documented, but their test entries were absent).

- Fixed `scaffold.sh` so it actually generates `functools_utils.py`, `itertools_utils.py`, and `regex_utils.py` (and their tests) in scaffolded projects: the modules were registered in `pyproject.toml` `py_modules` and listed in the scaffold header comment but had no heredoc blocks, so scaffolded projects were missing them. Added the 6 missing heredoc blocks and verified the scaffold smoke test generates all modules with passing tests, ruff, and mypy.

- Registered `template_utils` in `pyproject.toml` `py_modules`, where it was missing and causing an inconsistency with `scaffold.sh`, the README tree, and the CHANGELOG.

- `template_utils.py` — string template rendering utilities (`render_template`, `substitute`, `safe_substitute`, `render_from_dict`, `has_placeholders`, `extract_placeholders`) supporting `str.format()` and `string.Template` styles with placeholder extraction
- `tests/test_template_utils.py` — unit tests for `template_utils.py`

### Added
- `pickletools_utils.py` — stdlib `pickletools` wrapper module with tests
- `tests/test_pickletools_utils.py` — unit tests for `pickletools_utils.py`

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `time_utils.py` — time utility functions for working with timestamps and durations (`now_epoch`, `now_iso`, `epoch_to_iso`, `iso_to_epoch`)
- `timeit_utils.py` — wrapper for stdlib timeit (timeit, repeat, default_timer, Timer)
- `asyncio_utils.py` — utilities wrapping the standard library asyncio module (run, create_task, gather, sleep, to_thread, wait_for)
- `tests/test_asyncio_utils.py` — unit tests for `asyncio_utils.py`
- `tests/test_time_utils.py` — unit tests for `time_utils.py`
- Added `time_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions
- Added `asyncio_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `decimal_utils.py` — decimal arithmetic utilities (`to_decimal`, `add`, `subtract`, `multiply`, `divide`, `power`, `quantize`, `compare`, `abs_value`, `negate`, `is_positive`, `is_negative`, `is_zero`) using the standard library `decimal` module with input validation
- `tests/test_decimal_utils.py` — unit tests for `decimal_utils.py`
- Added `decimal_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `heapq_utils.py` — heap queue utilities wrapping the standard library `heapq` module (`heapify`, `heappush`, `heappop`, `heapreplace`, `heappushpop`, `merge`, `nlargest`, `nsmallest`) with input validation
- `tests/test_heapq_utils.py` — unit tests for `heapq_utils.py`
- Added `heapq_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `calendar_utils.py` — calendar utilities (`is_leap_year`, `days_in_month`, `first_day_of_month`, `month_name`, `day_name`, `month_calendar`, `weekdays_in_month`, `weekend_days_in_month`, `is_weekend`, `add_months`) for date and month calculations using stdlib `calendar` with input validation
- `tests/test_calendar_utils.py` — unit tests for `calendar_utils.py`
- Synchronized `calendar_utils.py` across `scaffold.sh`, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions

- `prime_utils.py` — prime number utilities (`prime_factors`, `nth_prime`, `primes_up_to`, `next_prime`, `previous_prime`) building on `math_utils.is_prime` with input validation
- `tests/test_prime_utils.py` — unit tests for `prime_utils.py`
- Added `prime_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `operator_utils.py` — operator utilities (`identity`, `negate`, `add`, `subtract`, `multiply`, `divide`, `power`, `modulo`, `clamp`, `between`) for common functional operations

- `sys_utils.py` — Python runtime and system information utilities (`get_python_version`, `get_python_version_string`, `get_executable`, `get_argv`, `get_platform`, `get_path`, `get_recursion_limit`, `set_recursion_limit`, `get_stdout_encoding`, `get_stderr_encoding`, `get_stdin_encoding`, `is_interactive`, `get_frame_info`, `get_refcount`) wrapping the standard library `sys` module with input validation
- `tests/test_sys_utils.py` — unit tests for `sys_utils.py`
- Added `sys_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions
- `semver_utils.py` — Semantic versioning utilities (`parse_semver`, `compare_semver`, `bump_major`, `bump_minor`, `bump_patch`, `is_valid_semver`, `SemanticVersion`) following Semantic Versioning 2.0.0
- `tests/test_semver_utils.py` — unit tests for `semver_utils.py`
- Added `semver_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- Added `semver_utils.py` with Semantic Versioning utilities and corresponding tests. Synchronized scaffold and docs.
- Bootstrap verification: all 1500 tests, ruff checks, and mypy checks pass on 2026-10-16

- `networking_utils.py` — networking utilities for TCP port and host operations (`is_valid_port`, `is_port_open`, `find_free_port`, `resolve_hostname`, `get_local_ip`, `tcp_ping`) wrapping the standard library `socket` module with input validation
- `tests/test_networking_utils.py` — unit tests for `networking_utils.py`
- Added `networking_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `itertools_utils.py` — iteration helpers (`chain_iterables`, `flatten_once`, `take_while_pred`, `chunk_iterable`, `product_of`, `combinations_of`, and more) wrapping the standard library `itertools` module with input validation
- `tests/test_itertools_utils.py` — unit tests for `itertools_utils.py`
- Added `itertools_utils.py` to README tree and module section, CHANGELOG Unreleased entry, and scaffold.sh module list

- `context_utils.py` — context manager utilities (`chdir`, `temp_environ`, `redirect_stdout`, `redirect_stderr`, `suppress`) for temporarily altering the runtime environment (working directory, environment variables, standard streams) and restoring it on exit using the standard library with input validation
- `tests/test_context_utils.py` — unit tests for `context_utils.py`
- Added `context_utils.py` to `pyproject.toml` `py_modules`, README tree and module section, `scaffold.sh` header comment and heredocs, `.kilo/command/scaffold-project.md`, and `tests/test_scaffold.py` assertions, plus this CHANGELOG Unreleased entry

- `textwrap_utils.py` — text wrapping utilities (`wrap_text`, `shorten_text`, `dedent_text`, `indent_text`, `fill_text`) using the standard library `textwrap` module with input validation
- `tests/test_textwrap_utils.py` — unit tests for `textwrap_utils.py`
- Added `textwrap_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `sys_utils.py` — Python runtime and system information utilities (`get_python_version`, `get_python_version_string`, `get_executable`, `get_argv`, `get_platform`, `get_path`, `get_recursion_limit`, `set_recursion_limit`, `get_stdout_encoding`, `get_stderr_encoding`, `get_stdin_encoding`, `is_interactive`, `get_frame_info`, `get_refcount`) for inspecting the interpreter and runtime environment using the standard library `sys` module with input validation
- `tests/test_sys_utils.py` — unit tests for `sys_utils.py`
- Added `sys_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `graphlib_utils.py` — graph and dependency resolution utilities (`topological_sort`, `has_cycle`, `dependency_order`, `is_valid_ordering`) for topological sorting and cycle detection of directed graphs using the standard library `graphlib` module with input validation
- `tests/test_graphlib_utils.py` — unit tests for `graphlib_utils.py`
- Added `graphlib_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `queue_utils.py` — FIFO queue utilities (`Queue` class backed by `collections.deque` with `enqueue`, `dequeue`, `peek`, `is_empty`, `size`, `clear`, `to_list`, `from_list`, plus module-level `create`, `enqueue`, `dequeue`, `peek`, `is_empty`, `size` helpers) with input validation
- `tests/test_queue_utils.py` — unit tests for `queue_utils.py`
- Added `queue_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `version_utils.py` — version parsing, comparison, and normalization utilities (`parse_version`, `compare_versions`, `is_greater`, `normalize_version`) for dotted version strings with input validation
- `tests/test_version_utils.py` — unit tests for `version_utils.py`
- Added `version_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `seq_utils.py` — sequence utilities (`first`, `last`, `nth`, `head`, `tail`, `split_at`, `take_while`, `drop_while`, `interleave`, `adjacent_pairs`, `is_sorted`) for common sequence operations with input validation
- `tests/test_seq_utils.py` — unit tests for `seq_utils.py`
- Added `seq_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `number_utils.py` — number utility functions (`clamp`, `round_to`, `is_integer`, `format_number`, `percentage`) for common numeric operations with input validation
- `tests/test_number_utils.py` — unit tests for `number_utils.py`
- Added `number_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions

- `sort_utils.py` — sorting utility functions (`is_sorted`, `bubble_sort`, `merge_sort`, `nth_largest`, `top_n`) for sorting and ordering operations
- `tests/test_sort_utils.py` — unit tests for `sort_utils.py`
- Added `sort_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions

- `temp_utils.py` — temporary file and directory management utilities (`create_temp_file`, `create_temp_dir`, `temp_file`, `temp_dir`, `write_temp_file`, `read_temp_file`, `cleanup_temp_path`, `is_temp_path`, `temp_path_exists`) wrapping the standard library `tempfile` module with input validation
- `tests/test_temp_utils.py` — unit tests for `temp_utils.py`
- Added `temp_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `xml_utils.py` — XML parsing and generation utilities (`parse_xml`, `parse_xml_string`, `build_xml`, `add_child`, `set_attribute`, `get_attribute`, `element_to_dict`, `dict_to_element`, `find_elements`, `find_element`, `get_element_text`, `set_element_text`, `xml_to_string`, `validate_well_formed`) wrapping the standard library `xml.etree.ElementTree` module with input validation
- `tests/test_xml_utils.py` — unit tests for `xml_utils.py`
- Added `xml_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `duration_utils.py` — time duration utilities (`parse_duration`, `format_duration`, `seconds_to_hms`, `hms_to_seconds`, `to_seconds`, `duration_between`, `add_duration`, `is_valid_duration`) for parsing, formatting, and converting time durations with input validation
- `tests/test_duration_utils.py` — unit tests for `duration_utils.py`
- Added `duration_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `http_utils.py` — HTTP status codes and response handling utilities (`status_code_category`, `status_message`, `is_informational`, `is_success`, `is_redirection`, `is_client_error`, `is_server_error`, `is_error`) using the standard library `http` module with input validation
- `tests/test_http_utils.py` — unit tests for `http_utils.py`
- Added `http_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `struct_utils.py` — Binary struct packing and unpacking utilities (`pack`, `unpack`, `pack_into`, `unpack_from`, `calcsize`, `is_valid_format`) wrapping the standard library `struct` module with input validation
- `tests/test_struct_utils.py` — unit tests for `struct_utils.py`
- Added `struct_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

### Fixed

- Completed the `struct_utils` sync that was partially done: added `struct_utils.py` and `tests/test_struct_utils.py` entries to `.kilo/command/scaffold-project.md`, added `struct_utils.py` / `tests/test_struct_utils.py` assertions to `tests/test_scaffold.py`, and added the `tests/test_struct_utils.py` entry to the scaffolded README tree in `scaffold.sh`.

- Synchronized `pyproject.toml` `py_modules` with the repository: added missing `duration_utils` and `xml_utils` modules (both exist as source files with tests and are already listed in `README.md`, `scaffold.sh`, and `.kilo/command/scaffold-project.md`) so package metadata matches the actual modules.

- `html_utils.py` — HTML escaping, unescaping, and tag-stripping utilities (`escape_html`, `unescape_html`, `strip_tags`, `escape_attribute`) using the standard library `html` module with input validation
- `tests/test_html_utils.py` — unit tests for `html_utils.py`
- Added `html_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `bytes_utils.py` — bytes and binary utilities (`to_hex`, `from_hex`, `xor`, `chunk`) for working with raw bytes and binary data with input validation
- `tests/test_bytes_utils.py` — unit tests for `bytes_utils.py`
- Fixed `scaffold.sh` syntax error introduced by a previous checkpoint commit: two bare module-list lines (missing `#   ` comment prefix) inside the script header broke bash parsing for project names containing parentheses. Replaced them with properly commented header lines and added the missing `bytes_utils.py` / `tests/test_bytes_utils.py` heredoc blocks so scaffolded projects generate the module and its tests. Added `bytes_utils` to `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions.

- `array_utils.py` — array utility functions wrapping the standard library `array` module (`array_create`, `array_fromlist`, `array_tolist`, `array_append`, `array_extend`, `array_insert`, `array_pop`, `array_remove`, `array_reverse`, `array_buffer_info`, `array_byteswap`, `array_count`, `array_index`)
- `tests/test_array_utils.py` — unit tests for `array_utils.py`
- Added `array_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `base64_utils.py` — Base64 and hexadecimal encoding/decoding utilities (`base64_encode`, `base64_decode`, `base64_encode_bytes`, `base64_decode_bytes`, `hex_encode`, `hex_decode`, `is_valid_base64`, `is_valid_hex`) using the standard library `base64` module with input validation
- `tests/test_base64_utils.py` — unit tests for `base64_utils.py`
- Added `base64_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions
- `bisect_utils.py` — bisect utility functions for binary search on sorted sequences (`bisect_left`, `bisect_right`, `insort_left`, `insort_right`, `find_leftmost`, `find_rightmost`) using the standard library `bisect` module with input validation
- `tests/test_bisect_utils.py` — unit tests for `bisect_utils.py`
- Added `bisect_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `bit_utils.py` — bitwise utility functions for working with binary representations of integers (`count_set_bits`, `is_power_of_two`, `next_power_of_two`, `prev_power_of_two`, `reverse_bits`, `rotate_left`, `rotate_right`, `get_bit`, `set_bit`, `clear_bit`, `toggle_bit`, `is_even`, `is_odd`) with input validation
- `tests/test_bit_utils.py` — unit tests for `bit_utils.py`
- `mmap_utils.py` — utilities wrapping the standard library `mmap` module with tests
- `tests/test_mmap_utils.py` — unit tests for `mmap_utils.py`
- Added `bit_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `operator_utils.py` — operator utilities (`identity`, `negate`, `add`, `subtract`, `multiply`, `divide`, `power`, `modulo`, `clamp`, `between`) for common functional operations
- `tests/test_operator_utils.py` — unit tests for `operator_utils.py`
- Added `operator_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests

### Changed

- Synchronized `pyproject.toml` `py_modules` with the repository: added missing `prompt_utils` and `uuid_utils` modules (both exist as source files with tests and are already listed in `README.md`, `scaffold.sh`, and `.kilo/command/scaffold-project.md`) so package metadata matches the actual modules.

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `ini_utils.py` — INI configuration file utilities (`load_config`, `save_config`, `get_config_value`, `set_config_value`, `merge_configs`, `list_sections`, `has_section`, `get_section`) for working with INI-style config files using `configparser`
- `tests/test_ini_utils.py` — unit tests for `ini_utils.py`
- Added `ini_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests

- `cli_utils.py` — command-line interface utilities with `create_parser` (an `argparse` parser with `--verbose` and `--version`), `parse_arguments`, and `main_wrapper` (wraps a main function returning exit codes `0`, `1`, or `130`)
- `tests/test_cli_utils.py` — unit tests for `cli_utils.py`
- Added `cli_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests

### Fixed

- Fixed inconsistent indentation in the `README.md` project structure tree: `path_utils.py`, `color_utils.py`, `pattern_utils.py`, `functools_utils.py`, `config_schema.py`, `exceptions_utils.py`, `io_utils.py`, `compression_utils.py`, `ip_utils.py`, `regex_utils.py`, `terminal_utils.py`, and the `tests/` sub-section were indented with 4 extra leading spaces instead of aligning with their siblings; also fixed `test_type_utils.py`, `test_path_utils.py`, `test_color_utils.py`, `test_pattern_utils.py`, `test_functools_utils.py`, `test_exceptions_utils.py`, `test_io_utils.py`, `test_compression_utils.py`, `test_ip_utils.py`, `test_regex_utils.py`, and `test_config_schema.py` entries in the tests sub-section. Synchronized the same fix into `scaffold.sh`'s generated `README.md` template so scaffolded projects inherit consistent indentation.

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `collections_utils.py` — collection utilities (`chunk`, `flatten`, `deep_flatten`, `windowed`, `uniq`, `uniq_by`, `frequency`, `most_common`, `least_common`, `merge_dicts`, `to_deque`, `pluck`, `compact`, `partition_by`) for working with iterables and data structures
- `tests/test_collections_utils.py` — unit tests for `collections_utils.py`
- `regex_utils.py` — regular expression utilities (`compile_pattern`, `is_valid_pattern`, `match_pattern`, `search_pattern`, `find_all`, `replace_pattern`, `split_pattern`, `escape_pattern`, `extract_groups`, `named_groups`) for safe regex compilation, matching, extraction, and manipulation
- `tests/test_regex_utils.py` — unit tests for `regex_utils.py`
- `tests/test_io_utils.py` — unit tests for `io_utils.py`
- `pattern_utils.py` — design pattern utilities (`Singleton` metaclass/base class, `Factory`, `Observer`/`Observable`, `Strategy`/`StrategyContext`) for common object-oriented patterns
- `tests/test_pattern_utils.py` — unit tests for `pattern_utils.py`
- `functools_utils.py` — functional programming utilities (`compose`, `pipe`, `curry`, `apply`) for composing, piping, and currying functions
- `tests/test_functools_utils.py` — unit tests for `functools_utils.py`
- `color_utils.py` — color manipulation utilities (`validate_hex`, `hex_to_rgb`, `rgb_to_hex`, `rgb_to_hsl`, `hsl_to_rgb`, `get_luminance`, `get_contrast_ratio`, `is_accessible`, `adjust_brightness`, `blend_colors`) supporting hex strings and RGB tuples with WCAG 2.1 luminance and contrast calculations
- `tests/test_color_utils.py` — unit tests for `color_utils.py`
- Added `color_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `path_utils.py` — path manipulation utilities (`join_path`, `normalize_path`, `get_absolute_path`, `get_relative_path`, `get_parent_dir`, `get_file_name`, `get_file_stem`, `get_file_extension`, `change_extension`, `is_absolute`, `get_path_components`, `get_common_path`, `ensure_extension`)
- `tests/test_path_utils.py` — unit tests for `path_utils.py`
- Added `path_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `string_utils.py` — advanced string manipulation utilities (`slugify`, `camel_to_snake`, `snake_to_camel`, `pluralize`, `truncate`, `wrap_text`, `indent_text`, `remove_extra_whitespace`, `title_case`)
- `tests/test_string_utils.py` — unit tests for `string_utils.py`
- Added `string_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `statistics_utils.py` — statistical utility functions (`harmonic_mean`, `geometric_mean`, `median_even`, `percentile`, `covariance`, `correlation`, `z_score`, `normalize`) beyond `stats.py`
- `tests/test_statistics_utils.py` — unit tests for `statistics_utils.py`
- Added `statistics_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- Synchronized `scaffold.sh` templates (`scaffold-project.md`, generated `README.md`, generated `CHANGELOG.md`) to include `statistics_utils.py` entries
- Updated `test_scaffold.py` to verify `statistics_utils.py` and `tests/test_statistics_utils.py` generation
- Fixed `# --- statistics_utils.py ---` and `# --- tests/test_statistics_utils.py ---` heredoc blocks in `scaffold.sh` to generate the module and its tests in scaffolded projects
- `tree_utils.py` — tree and nested structure utilities (get_nested, set_nested, delete_nested, flatten_tree, unflatten_tree, map_tree, filter_tree)
- `tests/test_tree_utils.py` — unit tests for `tree_utils.py`
- Synchronized `scaffold.sh` to include `tree_utils.py` and its tests in header, `py_modules`, and heredocs
- Updated `README.md`, `.kilo/command/scaffold-project.md`, and `CHANGELOG.md` to list `tree_utils.py` and `tests/test_tree_utils.py`
- Updated `test_scaffold.py` to expect `tree_utils.py` and `tests/test_tree_utils.py` in scaffolded outputs
- `terminal_utils.py` — terminal output utilities (`supports_color`, `colorize`, `print_colored`, `clear_screen`, `get_terminal_size`, `ProgressBar`, `progress_bar`, `prompt`) for ANSI-colored terminal output, progress bars, and user input
- `tests/test_terminal_utils.py` — unit tests for `terminal_utils.py`
- Added `terminal_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- Updated `test_scaffold.py` to verify `terminal_utils.py` and `tests/test_terminal_utils.py` generation


### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `gzip_utils.py` — gzip compression/decompression utilities (`gzip_compress`, `gzip_decompress`, `gzip_open`, `gzip_write`, `gzip_read`) wrapping the standard library `gzip` module.
- `tests/test_gzip_utils.py` — unit tests for `gzip_utils.py`.
- `config_schema.py` — typed configuration schema utilities (`SchemaField`, `ConfigSchema`, validators such as `range_validator`, `choices_validator`, `email_validator`)
- `tests/test_config_schema.py` — unit tests for `config_schema.py`
- `exceptions_utils.py` — custom exception classes and error handling utilities (`ValidationError`, `ConfigurationError`, `NotFoundError`, `PermissionError_`, `TimeoutError_`) with error details support; helper functions `catch_and_wrap()`, `get_error_details()`, and `is_instance_of_any()` for flexible exception handling
- `tests/test_exceptions_utils.py` — unit tests for `exceptions_utils.py`


### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `cache_utils.py` — caching utilities module with `memoize` decorator factory (supporting `maxsize` LRU eviction and `typed` argument distinction), `clear_cache` helper to invalidate stored results, and `cache_info` helper to inspect cache statistics
- `tests/test_cache_utils.py` — unit tests for `cache_utils.py`
- `timing_utils.py` — performance measurement helpers with `timer` context manager, `elapsed_time` function, and `benchmark` decorator
- `tests/test_timing_utils.py` — unit tests for `timing_utils.py`
- `timeit_utils.py` — wrapper for stdlib `timeit`
- `tests/test_timeit_utils.py` — unit tests for `timeit_utils.py`
- `concurrent_utils.py` — concurrent execution utilities with `ThreadPool`, `ProcessPool`, `gather`, `run_async`, and `to_async` functions
- `tests/test_concurrent_utils.py` — unit tests for `concurrent_utils.py`
- `priority_queue_utils.py` — heap-based priority queue implementation with `PriorityQueue` class and helper functions
- `tests/test_priority_queue_utils.py` — unit tests for `priority_queue_utils.py`
- `rate_limiter_utils.py` — rate limiting utilities using token bucket algorithm with `RateLimiter`, `token_bucket`, and `rate_limit` decorator
- `tests/test_rate_limiter_utils.py` — unit tests for `rate_limiter_utils.py`
- `retry_utils.py` — retry utilities with `retry`, `retry_with_backoff`, and `retry_count` decorators for exponential backoff and jitter
- `tests/test_retry_utils.py` — unit tests for `retry_utils.py`
- `dict_utils.py` — dictionary utilities (deep merge, flatten/unflatten, safe get, invert, filter)
- `tests/test_dict_utils.py` — unit tests for `dict_utils.py`
- `json_utils.py` — JSON utility functions (read/write/parse/dump/validate/pretty print)
- `tests/test_json_utils.py` — unit tests for `json_utils.py`
- `csv_utils.py` — CSV utility functions (read/write/append as dicts or lists)
- `tests/test_csv_utils.py` — unit tests for `csv_utils.py`

### Fixed

- Removed three duplicate heredoc blocks from `scaffold.sh` (`tests/test_rate_limiter_utils.py`, `tests/test_retry_utils.py`, `tests/test_dict_utils.py`) — the second copies were missing the `if __name__ == "__main__"` guard and would have overwritten the correct files during scaffolding
- Added missing `json_utils.py` and `csv_utils.py` entries to `scaffold.sh` header comment, generated README tree, generated CHANGELOG, generated `.kilo/command/scaffold-project.md` template, repo `README.md` tree and module sections, repo `CHANGELOG.md` Unreleased section, and repo `pyproject.toml` `py_modules`


### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `config_utils.py` — configuration utilities module with `load_config`, `save_config`, `get_config_value`, `set_config_value`, and `merge_configs` functions for working with JSON configuration files
- `tests/test_config_utils.py` — unit tests for `config_utils.py`

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `random_utils.py` — random number generation and sampling utilities with `random_int`, `random_choice`, `random_sample`, `random_shuffle`, `weighted_choice`, `random_uniform`, and `random_gaussian` functions, each accepting an optional `seed` for reproducible results
- `re_utils.py` — regular expression utilities wrapping `re`
- `tempfile_utils.py` — temporary file and directory utilities wrapping `tempfile`
- `tests/test_random_utils.py` — unit tests for `random_utils.py`
- `tests/test_re_utils.py` — unit tests for `re_utils.py`
- `tests/test_tempfile_utils.py` — unit tests for `tempfile_utils.py`
- `validation_utils.py` — input validation module with `is_email`, `is_numeric`, `is_integer`, `is_alphanumeric`, `is_boolean_string`, `is_none_or_empty`, `min_length`, `max_length`, `matches_regex`, and `is_valid_hostname` functions
- `tests/test_validation_utils.py` — unit tests for `validation_utils.py`
- `crypto_utils.py` — cryptographic utilities with `hash_string`, `generate_token`, `base64_encode`, and `base64_decode` functions
- `tests/test_crypto_utils.py` — unit tests for `crypto_utils.py`
- `list_utils.py` — advanced list manipulation utilities with `partition`, `group_by`, `safe_get`, `find`, `drop`, `take`, and `intersperse` functions
- `tests/test_list_utils.py` — unit tests for `list_utils.py`
- `env_utils.py` — environment variable handling utilities with `get_env`, `get_env_required`, `get_env_int`, `get_env_float`, `get_env_bool`, `set_env`, `ensure_env`, `unset_env`, and `prefix_env` functions
- `tests/test_env_utils.py` — unit tests for `env_utils.py`

### Fixed

- Synchronized `scaffold.sh` embedded `math_utils.py` template with the repository version, restoring full Args/Raises/Examples docstrings and the `n > 20` branch comment
- Synchronized `scaffold.sh` embedded `stats.py` template with the repository version: added Examples docstrings, deterministic mode tie-breaking, sample-variance element-count guard, and `float` return type on `mode`
- Synchronized `scaffold.sh` embedded `datetime_utils.py` template with the repository version: restored multiline function signatures and RST-style `` `` `` inline literals in docstrings
- Synchronized `scaffold.sh` embedded `tests/test_math_utils.py` template with the repository version, adding coprime/same GCD cases, zero LCM case, expanded prime edge cases, and `factorial(1)`/`fibonacci(6)` assertions
- Updated `scaffold.sh` embedded `.kilo/command/scaffold-project.md` template wording for the `kilo.json` scaffolder description to match the repo version
- Fixed inconsistent indentation in README.md project structure section (datetime_utils.py, file_utils.py, url_utils.py entries had extra leading spaces)
- Fixed inconsistent indentation in scaffold.sh README.md template for the same entries
- Removed duplicate `stats.py` heredoc section in `scaffold.sh` (was generated twice)
- Removed unused `import os` from `scaffold.sh`'s `file_utils.py` template (matches repo version)
- Added missing `math_utils.py` and `data_utils.py` entries to `scaffold.sh`'s generated `CHANGELOG.md` template
- Fixed `scaffold.sh` header comments to list all generated modules
- Fixed inconsistent indentation in repo's `.kilo/command/scaffold-project.md` (extra spaces on `file_utils.py`, `datetime_utils.py` entries)
- Fixed `data_utils.py` indentation in `scaffold.sh`'s generated `README.md` project structure section
- Synchronized `random_utils.py` and `validation_utils.py` modules across `scaffold.sh` embedded templates (`README.md`, `CHANGELOG.md`, `scaffold-project.md`), `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and `CHANGELOG.md`; added `validation_utils.py` and `crypto_utils.py` heredocs to `scaffold.sh`

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `url_utils.py` — URL and web utility module with `is_valid_url`, `extract_domain`, `get_query_params`, `get_query_param`, `add_query_param`, `remove_query_param`, and `build_url` functions
- `tests/test_url_utils.py` — unit tests for `url_utils.py`
- Updated scaffold template to generate `url_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include URL utilities
- Tests verifying `scaffold-project.md` and `CHANGELOG.md` list `url_utils.py` and its tests
- `LICENSE` — MIT license file (added to repo, scaffold.sh template, and scaffold-project.md)
- `PROJECT_YEARS` and `PROJECT_AUTHOR` variables in `scaffold.sh` for dynamic license generation
- Tests in `tests/test_scaffold.py` verifying all modules are listed in generated `scaffold-project.md` and `CHANGELOG.md`
- Tests verifying generated `file_utils.py` does not import unused `os` module
- Tests verifying `scaffold-project.md` list items have consistent formatting
- `LICENSE` entry added to `test_required_files_generated` in `tests/test_scaffold.py`

### Changed

- Synchronized `scaffold.sh` template with the repository: removed duplicate `stats.py` section, fixed `file_utils.py` import, added missing module entries to `scaffold-project.md` and `CHANGELOG.md` templates, fixed `README.md` project structure indentation, added `LICENSE` generation, and added `PROJECT_YEARS`/`PROJECT_AUTHOR` variables
- Added `LICENSE` file to the repository and `scaffold.sh` template, `scaffold-project.md` command doc, and README project structure
- `datetime_utils.py` — date and time utility module with `parse_datetime`, `format_datetime`, `days_between`, `is_leap_year`, `add_days`, and `get_weekday_name` functions
- `tests/test_datetime_utils.py` — unit tests for `datetime_utils.py`
- Updated scaffold template to generate `datetime_utils.py` and its tests
- Verified project foundation by running test suite, lint, and typecheck
- `strings.py` — string utility module with `reverse_string`, `is_palindrome`, and `count_vowels` functions
- `tests/test_strings.py` — unit tests for `strings.py`

### Fixed

- Removed duplicate `utils.py` and `tests/test_utils.py` entries from scaffold.sh's generated CHANGELOG.md (was listed 3 times instead of once)
- Added missing `utils.py` to the README.md project structure section
- Added missing `strings.py`, `utils.py`, `tests/test_strings.py`, and `tests/test_utils.py` to scaffold.sh's generated `scaffold-project.md` command doc and the repo's `.kilo/command/scaffold-project.md`
- Added `strings.py`, `utils.py`, `tests/test_strings.py`, and `tests/test_utils.py` to `test_required_files_generated` assertions in `tests/test_scaffold.py`
- Fixed `--no-test` argument parsing in `scaffold.sh` so the flag works regardless of argument position (previously only checked `$2`, causing `--no-test` as the third argument to be ignored and `--no-test` as the second argument to set `OUTPUT_DIR` incorrectly)
- Synchronized `scaffold.sh` embedded README.md with generated files: added `calculator.py`, `CHANGELOG.md`, `.pre-commit-config.yaml`, `.kilo/.gitignore`, and complete Makefile target table including `typecheck`, `pre-commit-install`, and `pre-commit-run`

### Tests

- Added `TestScaffoldNoTestFlag` test class verifying `--no-test` works as the third argument, without an output directory, and does not set `OUTPUT_DIR` to `--no-test`
- Added tests for README completeness (`test_readme_contains_calculator_and_new_files`, `test_readme_makefile_table_includes_all_targets`) and CHANGELOG completeness (`test_changelog_lists_new_files`)
- Added `tests/test_shapes.py` with unit tests for circle, rectangle, and triangle area/perimeter functions including input validation

### Changed

- Synchronized `scaffold.sh` with the repository: added generation of `calculator.py`, `tests/test_calculator.py`, `.pre-commit-config.yaml`, `CHANGELOG.md`, `.kilo/.gitignore`, ruff lint configuration in generated `pyproject.toml`, and `pre-commit-install`/`pre-commit-run` Makefile targets
- Updated `.kilo/command/scaffold-project.md` to document all generated files including the new calculator module, pre-commit config, and changelog
- Updated `README.md` project structure section to include all configuration files and new modules
- Added comprehensive tests in `tests/test_scaffold.py` for ruff config, Makefile targets, pre-commit hooks, and calculator operations

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `math_utils.py` — mathematical utility functions (factorial, fibonacci, gcd, lcm, is_prime, clamp)
- `tests/test_math_utils.py` — unit tests for `math_utils.py`
- Updated `scaffold.sh` to generate `math_utils.py` and its tests
- Updated scaffold tests to verify math utils generation
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include math utils
- `data_utils.py` — data utility module with `deep_copy`, `merge_dicts`, `pick`, `omit`, and `flatten_dict` functions
- `tests/test_data_utils.py` — unit tests for `data_utils.py`
- Updated scaffold template to generate `data_utils.py` and its tests
- Updated `tests/test_scaffold.py` to verify file_utils generation

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `file_utils.py` — file and path utility functions
- `tests/test_file_utils.py` — unit tests for `file_utils.py`
- Updated scaffold template to generate `file_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md` and `README.md` to include file utilities
- Updated `tests/test_scaffold.py` to verify file_utils generation
- Established project foundation by running test suite, lint, typecheck, and posted a task for next agent to scaffold a new project.

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `logging_utils.py` — logging configuration and helper utilities with `get_logger`, `configure_logging`, and a `log_calls` decorator for tracing function calls
- `tests/test_logging_utils.py` — unit tests for `logging_utils.py`
- Synchronized `scaffold.sh` templates (`scaffold-project.md`, generated `README.md`, generated `CHANGELOG.md`), repo `README.md`, repo `.kilo/command/scaffold-project.md`, and `tests/test_scaffold.py` to include the `logging_utils` module and its tests

### Fixed

- Fixed `scaffold.sh` README.md template Architecture section: added missing `config_utils.py` listing, added all missing test file entries (including `test_config_utils.py`), removed redundant `tests/` placeholder entry, and updated module descriptions to match the canonical README. Verified scaffold smoke test passes with all generated modules.
### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `json_utils.py` — JSON utility functions (read/write/parse/dump/validate/pretty print)
- `tests/test_json_utils.py` — unit tests for `json_utils.py`
- Updated `scaffold.sh` to generate `json_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include JSON utilities

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `csv_utils.py` — CSV utility functions (read/write/append as dicts or lists)
- `tests/test_csv_utils.py` — unit tests for `csv_utils.py`
- Updated `scaffold.sh`, `.kilo/command/scaffold-project.md`, and `README.md` to include CSV utilities

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `set_utils.py` — set operation utilities (`is_subset`, `is_superset`, `intersection`, `union`, `difference`, `symmetric_difference`, `cartesian_product`, `power_set`)
- `tests/test_set_utils.py` — unit tests for `set_utils.py`
- Updated `scaffold.sh` to generate `set_utils.py` and its tests
- `statistics_utils.py` — statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
- `tests/test_statistics_utils.py` — unit tests for `statistics_utils.py`
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include set and statistics utilities
- `string_utils.py` — advanced string manipulation utilities (`slugify`, `camel_to_snake`, `snake_to_camel`, `pluralize`, `truncate`, `wrap_text`, `indent_text`, `remove_extra_whitespace`, `title_case`)
- `tests/test_string_utils.py` — unit tests for `string_utils.py`
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and scaffold template to include string utilities
- `tree_utils.py` — tree and nested structure utilities (`get_nested`, `set_nested`, `delete_nested`, `flatten_tree`, `unflatten_tree`, `map_tree`, `filter_tree`)
- `tests/test_tree_utils.py` — unit tests for `tree_utils.py`
- Updated `scaffold.sh` to generate `tree_utils.py` and its tests
- `type_utils.py` — type introspection utilities (`is_optional`, `is_union`, `is_generic`, `get_type_args`, `type_name`, `is_subclass_safe`)
- `tests/test_type_utils.py` — unit tests for `type_utils.py`
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and scaffold template to include type utilities
- `uuid_utils.py` — UUID utility functions (generate_uuid, generate_uuid4, generate_uuid1, is_valid_uuid, parse_uuid)
- `tests/test_uuid_utils.py` — unit tests for `uuid_utils.py`
- `prompt_utils.py` — Prompt utility functions (truncate_prompt, format_prompt_template, clean_prompt, extract_keywords, wrap_prompt, estimate_token_count)
- `tests/test_prompt_utils.py` — unit tests for `prompt_utils.py`
- `async_utils.py` — asynchronous utility functions (`run_in_thread`, `gather_with_timeout`, `async_sleep`, `retry_async`)
- `tests/test_async_utils.py` — unit tests for `async_utils.py`
- Updated `scaffold.sh` to generate `async_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include async utilities
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and scaffold template to include uuid and prompt utilities

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `compression_utils.py` — compression and decompression utilities (gzip, bz2, zip, tar) with support for bytes/strings and archive operations
- `tests/test_compression_utils.py` — unit tests for `compression_utils.py`
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and `pyproject.toml` to include compression utilities

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `ip_utils.py` — IP address validation and manipulation utilities (IPv4/IPv6 validation, version detection, conversion between strings and integers, property checks like private/loopback/multicast/link-local/reserved, normalization, and subnet membership)
- `tests/test_ip_utils.py` — unit tests for `ip_utils.py`
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and `pyproject.toml` to include IP utilities

- `os_utils.py` — operating system utilities (`get_platform_info`, `get_cpu_count`, `get_disk_usage`, `get_user_home`, `get_username`, `find_executable`, `expand_path`, `is_executable`) for inspecting the platform and environment using the standard library
- `tests/test_os_utils.py` — unit tests for `os_utils.py`
- Added `os_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions


## Bootstrap session

- Verified test suite passes (75 test modules).

### Added

- `plistlib_utils.py` — plistlib utility functions wrapping the standard library `plistlib` module (`plist_load`, `plist_loads`, `plist_dump`, `plist_dumps`) for reading/writing binary plist data
- `tests/test_plistlib_utils.py` — unit tests for `plistlib_utils.py`
- Synchronized `plistlib_utils.py` across scaffolding (`scaffold.sh` py_modules and heredocs for module/tests/scaffold-project.md, `.kilo/command/scaffold-project.md`, `pyproject.toml`, `tests/test_scaffold.py`); added `plistlib_utils` entries where missing
- Added `reprlib_utils.py` — reprlib utilities wrapping the standard library `reprlib` module (`repr`, `get_ident`, `recursive_repr`, `Repr`) with input validation, plus `tests/test_reprlib_utils.py`.
- Synchronized `reprlib_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- `importlib_utils.py` — importlib utilities (dynamic import, reload, spec inspection, module metadata, resources)
- `tests/test_importlib_utils.py` — unit tests for `importlib_utils.py`

- `concurrent_futures_utils.py` — `concurrent.futures` wrappers with validation for executors, submission, and waiting
- `tests/test_concurrent_futures_utils.py` — unit tests for `concurrent_futures_utils.py`
- Synchronized `concurrent_futures_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.

- Added `hashlib_utils.py` — hash utilities wrapping the standard library `hashlib` module (`md5_hash`, `sha1_hash`, `sha256_hash`, `sha512_hash`, `sha3_256_hash`, `sha3_512_hash`, `blake2b_hash`, `blake2s_hash`, `file_hash`) with input validation, plus `tests/test_hashlib_utils.py`.
- Synchronized `hashlib_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, and this CHANGELOG Unreleased entry.
- Added `platform_utils.py` — platform utilities wrapping the standard library `platform` module (system/release/version/machine/processor/node, Python build/compiler/revision/implementation/version, uname, and platform identification with validation), plus `tests/test_platform_utils.py`.
- Synchronized `platform_utils.py` across `scaffold.sh` header comment and heredocs, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `tests/test_scaffold.py` assertions, CHANGELOG, and `PROJECT_STATUS.md`.



- `unittest_utils.py` — Utilities wrapping the standard library `unittest` module with tests
- `tests/test_unittest_utils.py` — unit tests for `unittest_utils.py`

- `tty_utils.py` — tty utilities wrapping stdlib tty with tests
- `tests/test_tty_utils.py` — unit tests for `tty_utils.py`
profile_utils.py
tests/test_profile_utils.py
