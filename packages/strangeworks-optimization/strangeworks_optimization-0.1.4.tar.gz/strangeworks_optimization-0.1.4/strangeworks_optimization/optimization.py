from ast import Dict
import strangeworks as sw
from strangeworks.core.errors.error import StrangeworksError
from strangeworks.core.client.jobs import Job
from dimod import SampleSet
import json
from typing import Optional

from dimod import BinaryQuadraticModel

import tempfile

path = "qubo"


class OptimizationJob:
    def __init__(
        self,
        model: BinaryQuadraticModel | Dict,
        var_type: str,
        lagrange_multiplier: float,
        solver: dict,
    ) -> None:
        self.var_type = var_type
        self.lagrange_multiplier = lagrange_multiplier
        self.solver = solver
        self.model = json.dumps(model.to_serializable())


class StrangeworksOptimization:
    """Strangeworks client object."""

    def __init__(self, resource_slug: Optional[str] = " ") -> None:
        if resource_slug != " " and resource_slug != "":
            self.rsc = sw.resources(slug=resource_slug)[0]
        else:
            rsc_list = sw.resources()
            for rr in range(len(rsc_list)):
                if rsc_list[rr].product.slug == "optimization":
                    self.rsc = rsc_list[rr]

        # self.backend_list = " "

    def run(self, qubo_job: OptimizationJob) -> str:
        result = sw.execute(self.rsc, payload=qubo_job.__dict__, endpoint=path)
        return Job(
            slug=result["job_slug"],
            child_jobs=None,
            external_identifier=None,
            resource=self.rsc,
            status=result["job_status"],
            is_terminal_state=None,
        )

    def get_results(self, sw_job):
        if self.get_status(sw_job) == "COMPLETED":
            if type(sw_job) is dict:
                job_slug = sw_job["slug"]
            else:
                job_slug = sw_job.slug
        else:
            raise StrangeworksError("Job not completed")

        result = sw.download_job_files(job_slug)[1]
        return SampleSet.from_serializable(result)

    def upload_model(self, bqm: BinaryQuadraticModel) -> str:
        with tempfile.NamedTemporaryFile(mode="w+") as t:
            json.dump(bqm.to_serializable(), t)
            t.flush()

            return sw.upload_file(t.name)

    def get_status(self, sw_job):
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
        else:
            job_slug = sw_job.slug

        return sw.jobs(slug=job_slug)[0].status

    def backends(self):
        """
        To-Do: Add cross check as to which backends the current user actually has
          access to.
                Currently, this just lists all backends that could work with the qaoa
                  service.
        """

        self.backends = sw.backends(backend_type_slugs=["optimization"])

        return self.backends
