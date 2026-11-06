# Security policy

Report vulnerabilities privately via GitHub private vulnerability reporting if enabled, otherwise contact the repository owner through a trusted private channel. Do not open public security issues.

The MasterVisor API is a local development interface without authentication. Bind only to 127.0.0.1; do not expose to the Internet or a LAN until authentication, authorization, audit logging and CSRF/CORS policies are implemented.

ROM files, recovery images, hashes/manifests, keys and credentials must not be committed. If exposed, remove them from history and rotate affected credentials; a .gitignore rule alone does not remove committed data.

Native C/C++ emulators are untrusted integration boundaries. Review licenses, pin upstream revisions and fuzz memory callbacks.
