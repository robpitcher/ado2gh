# GitHub for ADO Developers

> **Audience:** Development teams familiar with Azure DevOps that are adopting GitHub. This guide covers GitHub's organizational model, permissions, environments, Copilot, CI/CD, and how each maps to what you already know from ADO.

---

## 1. Conceptual Foundation — "How Does GitHub Map to ADO?"

These docs directly address the mental model shift from ADO → GitHub.

| Doc | Why It Matters | Link |
|-----|---------------|------|
| **Key Differences Between Azure DevOps and GitHub** | The single best "Rosetta Stone" doc. Covers the structural mapping (ADO Org > Project > Repo → GitHub Enterprise > Org > Repo), auth differences, and workflow changes. | [docs.github.com](https://docs.github.com/en/migrations/ado/key-differences-between-azure-devops-and-github) |
| **Migrating from Azure DevOps (Overview)** | Six-part guide covering the full migration journey — preparing, configuring access, running migrations, and post-migration. | [docs.github.com](https://docs.github.com/en/migrations/ado) |
| **GitHub Well-Architected: ADO to GitHub Enterprise Migration Guide** | The most comprehensive end-to-end guide. Covers planning, feature comparisons, hybrid strategies, testing, and post-migration stabilization. Community-maintained and regularly updated. | [wellarchitected.github.com](https://wellarchitected.github.com/library/scenarios/migrations/azure-devops-migration-guide/) |

---

## 2. Organizing Your GitHub Organization — Teams, Permissions & Visibility

One of the biggest shifts from ADO is how you structure access. In ADO, Team Projects act as permission boundaries. In GitHub, you use **Teams** within an **Organization** to control who can see and do what. These docs cover the essentials:

### Teams & Structure

| Doc | What It Covers | Link |
|-----|---------------|------|
| **Best Practices for Organizations** | How to structure an org, use teams effectively, and manage at scale. | [docs.github.com](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/best-practices-for-organizations) |
| **About Teams** | How teams work — nesting (parent/child), visibility (visible vs. secret), @mentions, and how permissions cascade. | [docs.github.com](https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams) |
| **Best Practices for Organizing Work in Your Enterprise** | Guidance on when to use 1 org vs. many, how to group repos, and team-based access patterns. | [docs.github.com](https://docs.github.com/en/enterprise-cloud@latest/admin/concepts/enterprise-best-practices/organize-work) |

> **💡 Example: Nested team structure for multi-product organizations**
>
> If your org has multiple products or projects with distinct dev, QA, and operations roles, nested teams let you mirror that structure while keeping everything in a single GitHub organization:
>
> ```
> Org: contoso-engineering
> │
> ├── Team: platform              (parent — all Platform team members)
> │   ├── Team: platform-dev      (child — Write access to platform repos)
> │   ├── Team: platform-qa       (child — Read/Triage access)
> │   └── Team: platform-ops      (child — Maintain access for CI/CD and releases)
> │
> ├── Team: mobile-app            (parent — all Mobile App members)
> │   ├── Team: mobile-app-dev    (child — Write access to mobile repos)
> │   ├── Team: mobile-app-qa     (child — Read/Triage access)
> │   └── Team: mobile-app-ops    (child — Maintain access)
> │
> └── Team: shared-libraries      (cross-cutting — Read access to shared repos for all)
> ```
>
> Child teams inherit their parent's repository access but can be granted additional permissions independently. Use **private** repo visibility to restrict access between product areas, or **internal** if everyone in the org should be able to discover and read the code.

### Permissions & Roles

| Doc | What It Covers | Link |
|-----|---------------|------|
| **Repository Roles for an Organization** | The 5 built-in roles (Read, Triage, Write, Maintain, Admin) and what each can do — critical for mapping ADO permission groups. | [docs.github.com](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization) |
| **Managing Team Access to a Repository** | How to grant a team access to specific repos with specific roles. | [docs.github.com](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/managing-team-access-to-an-organization-repository) |
| **Custom Repository Roles** *(Enterprise Cloud)* | Create fine-grained roles beyond the 5 defaults — useful for DevOps teams that need specific permissions without full admin. | [docs.github.com](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/managing-custom-repository-roles-for-an-organization) |
| **Managing People's Access with Roles** | Organization-level roles (Owner, Member) and how to delegate admin tasks. | [docs.github.com](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles) |

### Repository Visibility

| Doc | What It Covers | Link |
|-----|---------------|------|
| **About Repository Visibility** | Public vs. Private vs. Internal. Internal = visible to all org/enterprise members (similar to ADO project-scoped repos). Private = invite-only (for restricting visibility between teams or product areas). | [docs.github.com](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/about-repository-visibility) |
| **Setting Repository Visibility** | How to change visibility settings. | [docs.github.com](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility) |

---

## 3. Branch Protection, Rulesets & Code Review

These map to ADO's branch policies and required reviewers.

| Doc | What It Covers | Link |
|-----|---------------|------|
| **About Protected Branches** | Require PR reviews, status checks, signed commits, linear history — equivalent to ADO branch policies. | [docs.github.com](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches) |
| **About Rulesets** | Newer, more flexible governance that can span multiple repos. Can stack and be in "evaluate" mode. Preferred over legacy branch protection for new setups. | [docs.github.com](https://docs.github.com/en/organizations/repository-configuration/repository-rulesets/about-rulesets) |
| **About Code Owners** | CODEOWNERS file auto-assigns team reviewers based on file paths — maps to ADO's "automatically included reviewers" feature. | [docs.github.com](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |

---

## 4. Environments & Deployment Protection

Maps to ADO's environments, approvals, and checks.

| Doc | What It Covers | Link |
|-----|---------------|------|
| **Deployments and Environments** | Required reviewers, wait timers, branch restrictions for deployments. | [docs.github.com](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) |
| **Managing Environments for Deployment** | Step-by-step setup of dev/staging/production environments with protection rules. | [docs.github.com](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) |
| **Creating Custom Deployment Protection Rules** | Use GitHub Apps for automated gates (observability, change management, etc.). | [docs.github.com](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/create-custom-protection-rules) |

---

## 5. CI/CD — Azure Pipelines → GitHub Actions

| Doc | What It Covers | Link |
|-----|---------------|------|
| **Migrating from Azure Pipelines to GitHub Actions (Manual)** | Side-by-side syntax comparison. Covers triggers, jobs, steps, agents → runners, variables, and more. | [docs.github.com](https://docs.github.com/en/actions/tutorials/migrate-to-github-actions/manual-migrations/migrate-from-azure-pipelines) |
| **Automating Migration with GitHub Actions Importer** | The `gh actions-importer` CLI tool — audit, dry-run, and migrate Azure Pipelines automatically. | [docs.github.com](https://docs.github.com/en/actions/tutorials/migrate-to-github-actions/automated-migrations/use-github-actions-importer) |
| **Migrating from Azure DevOps with GitHub Actions Importer** | Azure DevOps-specific instructions for the importer tool. | [docs.github.com](https://docs.github.com/en/enterprise-cloud@latest/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration) |
| **GitHub Actions Importer CLI (Repo)** | Source repo with README, installation, and troubleshooting. | [github.com/github/gh-actions-importer](https://github.com/github/gh-actions-importer) |
| **Actions Importer Labs — Azure DevOps** | Hands-on exercises for practicing pipeline migration. | [github.com/actions/importer-labs](https://github.com/actions/importer-labs/blob/main/azure_devops/readme.md) |

---

## 6. GitHub Copilot Setup & Management

| Doc | What It Covers | Link |
|-----|---------------|------|
| **Setting Up Copilot for Your Organization** | End-to-end setup — plans, enabling, network config. | [docs.github.com](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-organization) |
| **Granting Access to Members** | Assign Copilot seats to teams, individuals, or all members. | [docs.github.com](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/manage-access/grant-access) |
| **Managing Copilot Policies & Features** | Control which Copilot features/models are enabled org-wide. | [docs.github.com](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies) |

---

## 7. Training & Learning Paths (Microsoft Learn)

Structured self-paced courses — great for the whole team to work through.

| Course | What It Covers | Link |
|--------|---------------|------|
| **ADO to GitHub Enterprise Migration (4-Part Learning Path)** | Planning → Assessment → Migration → Post-Migration. The most relevant training series. | [learn.microsoft.com](https://learn.microsoft.com/en-us/training/paths/migrate-azure-devops-github-enterprise/) |
| **Migrate Your Repository Using GitHub Best Practices** | Hands-on module for repo migration. | [learn.microsoft.com](https://learn.microsoft.com/en-us/training/modules/migrate-repository-github/) |
| **Migrate CI/CD Pipelines with GitHub Actions Importer** | Hands-on lab for pipeline migration. | [learn.microsoft.com](https://learn.microsoft.com/en-us/training/modules/migrate-cicd-pipelines-to-github-with-github-actions-importer/) |
| **GitHub Foundations (Parts 1 & 2)** | General GitHub fundamentals — repos, branches, PRs, GitHub flow. Good for developers new to GitHub. | [learn.microsoft.com](https://learn.microsoft.com/en-us/training/paths/github-foundations/) |
| **GitHub Fundamentals — Administration** | Org management, security, repository admin. Good for DevOps team leads. | [learn.microsoft.com](https://learn.microsoft.com/en-us/training/paths/github-fundamentals-administration-basics/) |
| **Introduction to GitHub** | Quick-start module covering core GitHub features. | [learn.microsoft.com](https://learn.microsoft.com/en-us/training/modules/introduction-to-github/) |

---

## 8. Quick Reference — ADO ↔ GitHub Concept Map

| Azure DevOps Concept | GitHub Equivalent | Key Doc |
|---------------------|-------------------|---------|
| Organization | Enterprise Account | [Key Differences](https://docs.github.com/en/migrations/ado/key-differences-between-azure-devops-and-github) |
| Team Project | Organization (roughly) | Same as above |
| Repository | Repository | — |
| Azure Pipelines | GitHub Actions | [Migration Guide](https://docs.github.com/en/actions/tutorials/migrate-to-github-actions/manual-migrations/migrate-from-azure-pipelines) |
| Pipeline Environments | Environments (with protection rules) | [Environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) |
| Branch Policies | Branch Protection Rules / Rulesets | [Rulesets](https://docs.github.com/en/organizations/repository-configuration/repository-rulesets/about-rulesets) |
| Required Reviewers (policy) | CODEOWNERS + Branch Protection | [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |
| Project Permissions (groups) | Teams + Repository Roles | [Teams](https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams) |
| Azure Boards | GitHub Projects / Issues | [Projects Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects) |
| Service Connections | Secrets + OIDC | [Encrypted Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) |
| Variable Groups | Environment Variables / Secrets | Same as above |
| Artifacts (Packages) | GitHub Packages | [Packages Docs](https://docs.github.com/en/packages) |

---

## Notes

- Some features like custom repository roles, rulesets, and internal repository visibility require **GitHub Enterprise Cloud**. Check your plan details if those options aren't available.
- For advanced topics (SAML SSO, Enterprise Managed Users, audit log streaming, etc.), see the [GitHub Enterprise Cloud admin docs](https://docs.github.com/en/enterprise-cloud@latest/admin).
