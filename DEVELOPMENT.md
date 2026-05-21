# PNGCJE Finance: Development Setup

This document captures the specific environment requirements for the PNGCJE Financial Management Bridge (Frappe/ERPNext v15).

## 1. Environment Specifications
- **Framework**: Frappe/ERPNext v15 (Stable)
- **Base**: `frappe_docker` (Official Community Devcontainer)
- **Container Port**: 8000 mapped to **8010**
- **Default Site**: `njs.localhost`

## 2. Mandatory Setup Steps (Post-Install)
If rebuilding the environment, ensure these steps are followed to avoid broken styling or database errors:

### Frontend Dependencies
Apps like **HRMS** and **Helpdesk** require manual dependency installation before the build will succeed:
```bash
cd apps/hrms && yarn install
cd apps/helpdesk && yarn install
```

### Asset Compilation
Run a forced verbose build to ensure all bundles are generated:
```bash
bench build --apps frappe,erpnext,hrms,helpdesk,telephony,pngcje_finance --force
```

### Database Credential Sync
If you force-reinstall the site, you must manually sync the MariaDB user password with the one in `site_config.json`:
```bash
# In MariaDB container
ALTER USER '_[db_name]'@'%' IDENTIFIED BY '[db_password]';
FLUSH PRIVILEGES;
```

### Localhost Access
To access via `http://localhost:8010`:
1. Set `serve_default_site: true` in `common_site_config.json`.
2. Add `127.0.0.1 njs.localhost` to your host OS `hosts` file.
