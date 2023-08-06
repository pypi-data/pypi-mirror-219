from pollination_dsl.dag import Inputs, GroupedDAG, task, Outputs
from dataclasses import dataclass

from pollination.path.copy import CopyFile

from pollination.honeybee_radiance.grid import MergeFolderData
from pollination.honeybee_radiance_postprocess.post_process import GridSummaryMetrics


@dataclass
class DaylightFactorPostProcessResults(GroupedDAG):
    """Daylight factor results post-process."""

    model = Inputs.file(
        description='Input Honeybee model.',
        extensions=['json', 'hbjson', 'pkl', 'hbpkl', 'zip']
    )

    results_folder = Inputs.folder(
        description='Daylight factor results input folder.'
    )

    grids_info = Inputs.file(
        description='Grids information from the original model.'
    )

    grid_metrics = Inputs.file(
        description='A JSON file with additional custom metrics to calculate.',
        path='grid_metrics.json', optional=True
    )

    @task(template=MergeFolderData, annotations={'main_task': True})
    def restructure_results(self, input_folder=results_folder, extension='res'):
        return [
            {
                'from': MergeFolderData()._outputs.output_folder,
                'to': 'results'
            }
        ]

    @task(template=CopyFile, needs=[restructure_results])
    def copy_grid_info(self, src=grids_info):
        return [
            {
                'from': CopyFile()._outputs.dst,
                'to': 'results/grids_info.json'
            }
        ]

    @task(
        template=GridSummaryMetrics,
        needs=[restructure_results]
    )
    def grid_summary_metrics(
        self, folder=restructure_results._outputs.output_folder,
        model=model, grids_info=grids_info, grid_metrics=grid_metrics,
        folder_level='main-folder'
    ):
        return [
            {
                'from': GridSummaryMetrics()._outputs.grid_summary,
                'to': 'grid_summary.csv'
            }
        ]

    results = Outputs.folder(
        source='results',
        description='Daylight factor results.'
    )

    grid_summary = Outputs.file(
        source='grid_summary.csv', description='grid summary.'
    )
