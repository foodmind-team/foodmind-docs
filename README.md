# FoodMind Documentation

FoodMind Documentation is the cross-repository architecture, contract, operations, delivery-evidence, and project-governance repository for FoodMind. It is not an executable application; use the linked implementation repositories to run the product.

## Repository map

| Repository | Responsibility |
| --- | --- |
| [Backend](https://github.com/foodmind-team/foodmind-backend) | Public API, security, domain rules, and persistence |
| [Web](https://github.com/foodmind-team/foodmind-web) | Browser client |
| [Android](https://github.com/foodmind-team/foodmind-android) | Native mobile client |
| [Intelligence](https://github.com/foodmind-team/foodmind-intelligence) | Private AI and inference runtime |
| [ML](https://github.com/foodmind-team/foodmind-ml) | Offline training, evaluation, and immutable model packages |
| [Infrastructure](https://github.com/foodmind-team/foodmind-infra) | Integrated local stack, staging release inputs, and operations |

## Quick start

Clone the repository and run the documentation parity check:

~~~bash
git clone https://github.com/foodmind-team/foodmind-docs.git
cd foodmind-docs
python3 testing/check_parity_docs.py
~~~

For the strongest contract check, clone the Backend as a sibling or point the check at a specific OpenAPI file:

~~~bash
FOODMIND_BACKEND_OPENAPI=/absolute/path/to/openapi.yaml python3 testing/check_parity_docs.py
~~~

The test checks for stale client-parity claims and, when the Backend contract is available, verifies the documented operation count. It does not start services.

## Where to start

- [Project context and tutoring guide](FoodMind_AI_Project_Context_and_Tutoring_Guide.md)
- [System architecture](architecture/)
- [Public and private contract coordination](contracts/)
- [Local, staging, and production-demo runbooks](operations/)
- [Plans, delivery status, and ownership](planning/)
- [UAT, security, and traceability evidence](testing/)
- [Presentations and demo material](presentation/)

## Source of truth

The public API is owned by Backend, private runtime contracts by Intelligence, and model-package contracts by ML. A coordination copy in this repository must name its owner and revision; it is not authoritative over the source repository.

For scope conflicts, use this order: formal Proposal, formal presentation, approved project-owner clarification, accepted ADR, canonical project context guide, versioned contracts, data documentation, then historical plans. Resolve contradictory documents rather than silently choosing one.

## Documentation contribution workflow

1. Identify the owning source repository and whether the change needs an ADR.
2. Update the canonical source before a coordination copy.
3. State status, owner, last-updated date, related repositories, and open questions for substantial design material.
4. Redact credentials, tokens, personal data, and private URLs from evidence.
5. Run python3 testing/check_parity_docs.py and review links and terminology before a pull request.

## Repository layout

~~~text
architecture/  System design, ADRs, diagrams, and decisions
contracts/     Public and private contract coordination copies and examples
database/      ERD and data dictionary
evidence/      Reports and non-sensitive screenshots
operations/    Local, staging, and production-demo runbooks
planning/      Backlog, delivery plans, ownership, and status
testing/       UAT, security, traceability, and parity checks
presentation/  Slides, scripts, and demo material
~~~

## Security and privacy

This repository can contain academic and project material. Keep it private unless publication is explicitly approved, use least-privilege sharing, and obtain permission before adding screenshots, datasets, or personal information.

## License

No open-source license is currently included in this repository. Obtain permission from the maintainers before redistributing or reusing the content.
