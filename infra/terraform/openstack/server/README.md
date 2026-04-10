# Template OpenStack Server Terraform

이 스택은 template repo의 backend compute를 Aspace/OpenStack 경로로 올리기 위한 generic baseline이다.

구성 범위:

- `Neutron`: app network + subnet + router
- `Nova`: backend compute instance 1대
- `Floating IP`: backend public reachability
- `Security Group`: backend ingress / SSH ingress

핵심 계약:

- `terraform apply` 한 번으로 backend compute 인스턴스가 올라간다.
- repo/source 정보(`service_name`, `phase`, `backend_repo_url`, `backend_repo_ref`)는 aspace repo onboarding auto tfvars가 채운다.
- OpenStack provider 인증값(`auth_url`, `username`, `password`, `project_name` 등)은 aspace 또는 openrc에서 주입한다.
- application environment는 `backend_env` map으로 주입하고, template는 최소 generic env만 기본값으로 제공한다.

권장 aspace 등록:

```yaml
deployments:
  - phase_pattern: dev
    engine: terraform
    path: infra/terraform/openstack/server
    stack: infra/terraform/openstack/server
    lifecycle_profile: stateful
    tf_vars:
      external_network_name: public
      backend_image_name: ubuntu-24.04-noble-amd64
      instance_flavor_name: m1.small
      backend_ingress_cidrs: ["0.0.0.0/0"]
      ssh_ingress_cidrs: ["0.0.0.0/0"]
      ssh_keypair_name: template-dev-terminal
      ssh_public_key: "ssh-ed25519 AAAA..."
    prechecks:
      - terraform fmt -check -recursive
      - terraform validate
    auto_approve: true
```

수동 검증:

```bash
terraform -chdir=infra/terraform/openstack/server init -backend=false
terraform -chdir=infra/terraform/openstack/server validate
```
