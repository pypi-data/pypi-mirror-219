# satosacontrib.perun

Microservices for [SATOSA](https://github.com/IdentityPython/SATOSA) authentication
proxy, made by the Perun team.

## Backends

### Seznam backend

A backend for SATOSA which implements login using [Seznam OAuth](https://partner.seznam.cz/seznam-oauth/).

Use the [example config](./example/plugins/backends/seznam.yaml) and fill in your client ID and client secret.

## Microservices

### AuthSwitcher Lite

This request microservice takes ACRs (AuthnContextClassRefs in SAML, acr_values in OIDC) from a frontend
and sets them as requested ACRs for the backends. It relies on [SATOSA!419](https://github.com/IdentityPython/SATOSA/pull/419)

### Context attributes microservice

The microservice adds the target IdP data to attributes:

- display name
- logo
- target issuer

The [MetaInfoIssuer](https://github.com/SUNET/swamid-satosa/blob/main/src/swamid_plugins/metainfo/metainfo.py)
microservice needs to be run beforehand with the following [patch](https://github.com/SUNET/swamid-satosa/compare/main...kofzera:swamid-satosa:add_collector_metadata.patch).
Another [patch](https://github.com/IdentityPython/SATOSA/compare/master...kofzera:SATOSA:decorate_context_with_metadata.patch) is
also needed for the satosa package until they are incorporated into the upstream.

### Is banned microservice

The microservice connects to database storing user bans and redirects banned users to configured URL.

### Persist authorization params microservice

This request microservice retrieves configured parameters from GET or POST request (if available) and
stores the values to internal context state.

### Session started with microservice

This Satosa microservice checks, if configured attribute's value is present
in "session_started_with" values (retrieved by Persist authorization params microservice).
If so, adds attribute with configured name. The value is expected to be converted
to boolean by Attribute typing microservice.

### Compute eligibility microservice

The microservice obtains dict with format { eligiblility_type: <unix_timestamp> }
from the internal data and runs a function configured for the
given eligibility type. The config is of format `type: function_path`.

The function should have a following signature:  
`example_func(data: InternalData, *args, **kwargs) -> timestamp | bool`, and it either returns `False` or
a new timestamp, in which case the time in the dictionary is
updated in internal data. It strongly relies on the PerunAttributes microservice to fill the dict
beforehand. If you want to update eligibility in the IDM, use the UpdateUserExtSource microservice.

## Perun Microservices

Subpackage of microservices connecting to perun. These have to be allowed (or not
denied) for
a given combination of requester/target_entity in order to run.

### Additional Identifiers

Takes user attributes by config, checks values with regexes and creates hashes by
specified algorithm. Values prepared to hash are parsed into List of List of strings and
serialized with json. User ext source and user is found by mathing this hashes.
If not even one hash can be created, user will be redirected to error page.
If user is not found, he will be redirected to registration page.

This microservice does not update the user in Perun with new values. To update save freshly computed values for the
current user, you need to run `update_user_ext_source` microservice.

[RFC - eduTEAMS Identifier Generation](https://docs.google.com/document/d/1UwnEnzFG6SM9cv6gx1AsjDXw09ZkUmkyl-NqcXg0OVo/edit#heading=h.y5g6a74d5ukn) <br/>
Differences between our soulution and RFC:

- the selections are represented as list of list of attributes values serialized to JSON
- all identifiers are hashed by same hash function and with same salt
- The user’s home IdP entity-id does not need to be part of selection
- hashed values can be scoped but does not have to be
