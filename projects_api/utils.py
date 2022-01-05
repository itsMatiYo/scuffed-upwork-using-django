from rest_framework import exceptions


def is_project_owner(project, wallet):
    if project.customer.wallet != wallet:
        raise exceptions.ValidationError(
            detail="permission for project owner", code=400)


def is_project_experts_approve(project):
    if project.experts_approve == False:
        raise exceptions.ValidationError(
            detail="project must be approved by expert", code=400)


def in_time_section(all_employee, all_visitor):
    section = []
    for emp in all_employee:
        new = {
            "wallet_id": emp.wallet.id,
            "percent": "123"
        }
        section.append(new)
    for vis in all_visitor:
        new = {
            "wallet_id": vis.wallet.id,
            "percent": "123"
        }
        section.append(new)
    return section


def after_time_section(all_employee, all_visitor):
    section = []
    for emp in all_employee:
        new = {
            "wallet_id": emp.wallet.id,
            "percent": "123"
        }
        section.append(new)
    for vis in all_visitor:
        new = {
            "wallet_id": vis.wallet.id,
            "percent": "123"
        }
        section.append(new)
    return section
