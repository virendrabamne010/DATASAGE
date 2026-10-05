# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in DATASAGE, please report it by opening a private security advisory at:

https://github.com/virendravijaybamne/datasage/security/advisories

Please include the following information in your report:
- The version of DATASAGE affected
- A description of the vulnerability
- Steps to reproduce the issue
- Any potential impact

You should receive a response within 48 hours. If the issue is confirmed, a patch will be released as soon as possible.

## Security Best Practices

When deploying the DATASAGE Streamlit app to production:

1. **Authentication**: The Streamlit app does not include authentication by default. Deploy it behind an authentication proxy or VPN for internal use.
2. **File upload limits**: Configure the `MAX_MB` limit in `streamlit_app.py` to match your security requirements.
3. **Data privacy**: Uploaded data is stored locally in the `examples/output/` directory. Ensure this directory is properly secured and cleaned regularly.
4. **Dependencies**: Keep all dependencies updated to their latest patched versions.
5. **Deployment**: Use the provided Dockerfile which runs as a non-root user.