package policy

import future.keywords.if

default allow := false

allow if {
    input.path == "/"
}

allow if {
	input.method == "POST"
	is_users_endpoint
	is_admin
}

allow if {
	is_users_endpoint
	token
    input.method == "GET"
}

is_post if {
    input.method == "POST"
}

is_users_endpoint if {
    input.path == "/api/users"
}

is_admin if {
    token.role.type == "admin"
}

token := payload if {
	# Verify the signature on the Bearer token. In this example the secret is
	# hardcoded into the policy however it could also be loaded via data or
	# an environment variable. Environment variables can be accessed using
	# the `opa.runtime()` built-in function.
	io.jwt.verify_hs256(bearer_token, "SECRET")
	[_, payload, _] := io.jwt.decode(bearer_token)
}

bearer_token := t if {
	# Bearer tokens are contained inside of the HTTP Authorization header. This rule
	# parses the header and extracts the Bearer token value. If no Bearer token is
	# provided, the `bearer_token` value is undefined.
	v := input.authorization
	startswith(v, "Bearer ")
	t := substring(v, count("Bearer "), -1)
}
