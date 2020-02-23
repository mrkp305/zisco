from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(r"admin", "config.dispatch.admin", name="admin"),
)
