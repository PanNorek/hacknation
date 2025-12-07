import os
import logging
from datetime import datetime
from src.report_generator import ForecastReportGenerator
from src.models.world_model import WorldModel
from src.configuration import config
from google.adk.tools import FunctionTool
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class WorldReport(BaseModel):
    report_path: str


def get_world_report():
    """
    A tool that allows the agent to interact with the world.
    """
    # Create reports directory from configuration
    reports_dir = config.report_dir
    os.makedirs(reports_dir, exist_ok=True)

    # Initialize World Model
    logger.info("Initializing World Model...")
    model = WorldModel()

    # Run complete simulation (exploration + forecasting)
    model.run_simulation()

    # Generate PDF Report
    logger.info("Generating PDF report...")
    try:
        # Collect all forecasts from agents
        forecasts_data = model.get_forecasts()

        if forecasts_data:
            # Generate PDF report
            report_gen = ForecastReportGenerator()
            report_gen.generate_report(
                scenario=model.scenario,
                forecasts=forecasts_data,
                timestamp=datetime.now(),
            )
            logger.info(f"✅ PDF report generated: {report_gen.output_path}")
        else:
            logger.warning("No forecasts available to generate report")

    except Exception as e:
        logger.error(f"Failed to generate PDF report: {e}", exc_info=True)


world_tool = FunctionTool(func=get_world_report)
