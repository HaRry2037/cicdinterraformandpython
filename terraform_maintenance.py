import subprocess
import sys
import yaml
import os
from rich.console import Console
from rich.prompt import Confirm
from rich.logging import RichHandler
import logging

# Initialize Rich console for better CLI output
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
log = logging.getLogger("rich")

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

TERRAFORM_DIR = config['terraform']['dir']
VARS_FILE = config['terraform']['vars_file']
ENV_VARS = config.get('environment', {})

def run_command(command, cwd=TERRAFORM_DIR, env=None):
    """Run a command in a subprocess and handle output and errors."""
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, env=env)
    if result.returncode != 0:
        log.error(result.stderr)
        sys.exit(result.returncode)
    else:
        log.info(result.stdout)

def terraform_init():
    """Initialize Terraform."""
    log.info("Initializing Terraform...")
    run_command(["terraform", "init"])

def terraform_plan():
    """Generate and show an execution plan."""
    log.info("Planning Terraform deployment...")
    run_command(["terraform", "plan", f"-var-file={VARS_FILE}"])

def terraform_apply():
    """Apply the changes required to reach the desired state of the configuration."""
    log.info("Applying Terraform deployment...")
    run_command(["terraform", "apply", f"-var-file={VARS_FILE}", "-auto-approve"])

def terraform_destroy():
    """Destroy the Terraform-managed infrastructure."""
    log.info("Destroying Terraform deployment...")
    run_command(["terraform", "destroy", f"-var-file={VARS_FILE}", "-auto-approve"])

def main():
    if len(sys.argv) < 2:
        log.error("Usage: python terraform_maintenance.py [init|plan|apply|destroy|custom]")
        sys.exit(1)

    action = sys.argv[1]
    custom_command = sys.argv[2:] if action == "custom" else None

    # Set environment variables for Terraform
    env = os.environ.copy()
    env.update(ENV_VARS)

    if action == "init":
        terraform_init()
    elif action == "plan":
        terraform_plan()
    elif action == "apply":
        if Confirm.ask("Are you sure you want to apply the Terraform changes?"):
            terraform_apply()
        else:
            log.info("Apply cancelled.")
    elif action == "destroy":
        if Confirm.ask("Are you sure you want to destroy the Terraform-managed infrastructure?"):
            terraform_destroy()
        else:
            log.info("Destroy cancelled.")
    elif action == "custom" and custom_command:
        run_command(["terraform"] + custom_command, env=env)
    else:
        log.error(f"Unsupported action: {action}")

if __name__ == "__main__":
    main()
