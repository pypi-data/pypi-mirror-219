from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class MemoryLimits(BaseResourceCheck):
    def __init__(self):
        name = "Memory Limits should be set"
        id = "CKV_K8S_12"
        supported_resources = ["kubernetes_pod", "kubernetes_pod_v1",
                               "kubernetes_deployment", "kubernetes_deployment_v1"]
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf) -> CheckResult:
        if "spec" not in conf:
            self.evaluated_keys = [""]
            return CheckResult.FAILED
        spec = conf['spec'][0]
        if not spec:
            return CheckResult.UNKNOWN

        evaluated_keys_path = "spec"

        template = spec.get("template")
        if template and isinstance(template, list):
            template = template[0]
            template_spec = template.get("spec")
            if template_spec and isinstance(template_spec, list):
                spec = template_spec[0]
                evaluated_keys_path = f'{evaluated_keys_path}/[0]/template/[0]/spec'

        containers = spec.get("container")
        if containers is None:
            return CheckResult.UNKNOWN
        for idx, container in enumerate(containers):
            if type(container) != dict:
                return CheckResult.UNKNOWN
            if container.get("resources"):
                resources = container.get("resources")[0]
                if resources.get('limits'):
                    limits = resources.get('limits')[0]
                    if isinstance(limits, dict) and limits.get('memory'):
                        return CheckResult.PASSED
                    self.evaluated_keys = [f'{evaluated_keys_path}/[0]/container/[{idx}]/resources/[0]/limits']
                    return CheckResult.FAILED
                self.evaluated_keys = [f'{evaluated_keys_path}/[0]/container/[{idx}]/resources']
                return CheckResult.FAILED
            self.evaluated_keys = [f'{evaluated_keys_path}/[0]/container/[{idx}]']
            return CheckResult.FAILED
        return CheckResult.PASSED


check = MemoryLimits()
