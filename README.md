# bpftune-rpm

RPM spec for [oracle/bpftune](https://github.com/oracle/bpftune) — BPF-based auto-tuning of Linux system parameters.

Fixes over the upstream Makefile packaging:

- no openrc `init.d` script (drops the bogus `/sbin/openrc-run` dependency on Fedora)
- systemd unit `ExecStart` points at the sbin-merged binary path

A daily GitHub Action bumps the spec to the latest upstream commit; pushes trigger a Copr rebuild via webhook.
