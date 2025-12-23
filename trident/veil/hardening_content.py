def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()

    if args.rollback:
        rollback_all()
        return

    dry = args.dry_run

    log("🔱 Starting Veil Sentinel Hardening Pass")

    # Phase 1: Ensuring package structure (__init__.py)
    log("── Phase 1: Ensuring package structure (__init__.py)")
    ensure_init_recursive(PROJECT_ROOT / "app", dry_run=dry)
    ensure_init_recursive(PROJECT_ROOT / "infra", dry_run=dry)

    # Phase 2: Hardening core files from templates
    log("── Phase 2: Hardening core files from templates")
    for repo_rel, template_rel in FILES_FROM_TEMPLATES:
        write_hardened_from_template(repo_rel, template_rel, dry_run=dry)

    # Phase 3: Hardening docs banners
    log("── Phase 3: Hardening docs banners")
    harden_docs_folder(PROJECT_ROOT / "docs", dry_run=dry)

    # Phase 4: Hardening docs language (Updater → Hardener)
    log("── Phase 4: Hardening docs language (Updater → Hardener)")
    harden_docs_language(PROJECT_ROOT / "docs", dry_run=dry)

    # Phase 5: Drift Detection
    log("── Phase 5: Drift Detection")
    detect_drift(dry_run=dry)

    log("🔱 Hardening complete")
