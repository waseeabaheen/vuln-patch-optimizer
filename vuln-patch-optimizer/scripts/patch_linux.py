import argparse, json, os, subprocess, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", default=False)
    p.add_argument("--targets", default="data/sample_targets_linux.json")
    args = p.parse_args()

    with open(args.targets, "r", encoding="utf-8") as f:
        targets = json.load(f)

    for t in targets:
        host = t["hostname"]
        if args.dry_run:
            print(f"[DRY-RUN] Would patch Linux host: {host}")
        else:
            # naive local example; real-world would use SSH/Ansible/etc.
            if os.path.exists("/usr/bin/apt"):
                subprocess.run(["sudo", "apt", "update"], check=False)
                subprocess.run(["sudo", "apt", "upgrade", "-y"], check=False)
            elif os.path.exists("/usr/bin/yum"):
                subprocess.run(["sudo", "yum", "update", "-y"], check=False)
            else:
                print(f"Unknown package manager on {host}")

if __name__ == "__main__":
    main()
