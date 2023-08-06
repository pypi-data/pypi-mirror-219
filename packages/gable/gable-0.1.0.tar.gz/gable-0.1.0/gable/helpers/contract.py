from typing import Any, Dict, List
import click
from gable.helpers.repo_interactions import get_git_info
from gable.openapi import ContractInput, PostContractRequest


def load_contract_from_file(file: click.File) -> Dict[str, Any]:
    if file.name.endswith(".yaml") or file.name.endswith(".yml"):
        import yaml

        try:
            return yaml.safe_load(file)  # type: ignore
        except yaml.scanner.ScannerError as exc:  # type: ignore
            # This should be a custom exception for user errors
            raise click.ClickException(f"Error parsing YAML file: {file.name}")
    elif file.name.endswith(".toml"):
        raise click.ClickException(
            "We don't currently support defining contracts with TOML, try YAML instead!"
        )
    elif file.name.endswith(".json"):
        raise click.ClickException(
            "We don't currently support defining contracts with JSON, try YAML instead!"
        )
    else:
        raise click.ClickException("Unknown filetype, try YAML instead!")


def contract_files_to_post_contract_request(
    contractFiles: List[click.File],
) -> PostContractRequest:
    contracts = []
    for contractFile in contractFiles:
        contract = load_contract_from_file(contractFile)
        if "id" not in contract:
            raise click.ClickException(f"{contractFile}:\n\tContract must have an id.")
        contractInput = ContractInput(
            id=contract["id"],
            version="0.0.1",  # This should be server calculated
            status="ACTIVE",
            **get_git_info(),  # type: ignore
            reviewers=[],  # This should be info accessible from a github PR integration
            contractSpec=contract,
        )
        contracts.append(contractInput)
    return PostContractRequest(
        __root__=contracts,
    )
