package policy

import future.keywords.if

default allow := false

is_post if {
    input.method == "POST"
}

is_users_endpoint if {
    input.path == "/api/users"
}

is_admin if {
    token.role.type == "admin"
}

is_api_call if {
    startswith(input.path, "/api/")
}

# allow rules
allow if {
    input.method == "GET"
    not is_api_call
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
# end allow rules


token := payload if {
	# Verify the signature on the Bearer token.
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
